"""The autonomous loop — no human in the loop.

Reads skill.md, signs in with its own keypair, lists open bounties, and for
each one either completes it or records exactly why it cannot. It enters
every open bounty (entering is free), submits predictions it can price from
public market data, prepares content artifacts locally, and skips — with a
written reason — anything that needs a login, a fake referral, a solver it
does not have, or data it cannot fetch. It never prompts, never guesses
blind, and never submits what it cannot price or build.

Decisions are written to out/report.json (public facts only: slugs, entry
and submission ids, outcomes, reasons — never keys, tokens or signatures).
"""
import json
import os
from datetime import datetime, timezone

from . import content, forecast
from .client import ApiError

# slug -> (builder, filename) for content/design bounties (PosterJudge, link).
CONTENT_MAP = {
    "write-article-aiprove": ("article", "ARTICLE.md"),
    "make-meme-aiprove": ("meme", "meme.svg"),
    "make-art-aiprove": ("art", "art.svg"),
    "aiprove-mascot": ("art", "mascot.svg"),
}

# Bounties the loop will not attempt, and the honest reason why.
SKIP_REASONS = {
    "refer-most-agents": "referrals must be real agents; fake referrals forbidden",
    "post-on-x-aiprove": "needs an X login (unavailable to this agent)",
    "retweet-and-quote-the-launch-post": "needs an X login (unavailable to this agent)",
    "top5-pons-24h": "no data source held for new pons tokens",
    "code-golf-expr": "needs a dedicated solver; out of scope for this run",
    "fastest-primes": "needs a dedicated solver; out of scope for this run",
    "bug-hunt-utils": "needs a dedicated audit pass; out of scope for this run",
    "eth-pnl-fixed": "needs a backtest engine on the fixed ETH dataset",
    "explainer-video-aiprove": "video generation not available in this run",
}

# Bounties whose completion IS this agent's repo (enter only).
SELF_BOUNTIES = ("sample-agent-skillmd", "best-autonomous-agent")

FORECAST_SLUGS = (
    "btc-tomorrow", "forecast-eth-24h", "forecast-btc-7d",
    "signal-eth-pnl-24h", "forecast-gold-tomorrow", "spy-close-1dollar",
    "forecast-nvda-3d",
)


def _utcnow():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


class Loop:
    def __init__(self, client, handle, out_dir, log):
        self.client = client
        self.handle = handle
        self.out_dir = out_dir
        self.log = log
        self.report = {"steps": []}
        self.predictions_left = None  # None = unlimited

    def _record(self, slug, action, detail):
        self.report["steps"].append(
            {"time": _utcnow(), "bounty": slug, "action": action, "detail": detail})

    def _enter(self, slug, dry_run):
        if dry_run:
            self._record(slug, "would-enter", "dry run, no write made")
            return None
        try:
            res = self.client.enter(slug, self.handle)
            entry_id = res.get("id") or res.get("entry", {}).get("id")
            self._record(slug, "entered", f"entry {entry_id}")
            self.log(f"  entered {slug}: entry {entry_id}")
            return entry_id
        except ApiError as e:
            self._record(slug, "enter-failed", str(e))
            self.log(f"  enter {slug} FAILED: {e}")
            return None

    def _forecast(self, slug, dry_run):
        pred = forecast.predict(slug)
        if pred is None:
            self._record(slug, "skipped", "market data unavailable, will not guess")
            self.log(f"  {slug}: skipped, market data unavailable")
            return
        answer, confidence = pred
        if dry_run:
            self._record(slug, "would-submit-prediction",
                         f"answer={answer} confidence={confidence}")
            self.log(f"  {slug}: would submit prediction {answer} @ {confidence}")
            return
        if self.predictions_left is not None:
            if self.predictions_left <= 0:
                self._record(slug, "skipped", "prediction budget reached")
                return
            self.predictions_left -= 1
        try:
            res = self.client.submit_prediction(slug, answer, confidence, self.handle)
            sub_id = res.get("id") or res.get("submission", {}).get("id")
            self._record(slug, "submitted-prediction",
                         f"answer={answer} confidence={confidence} id={sub_id} "
                         f"status={res.get('status')}")
            self.log(f"  {slug}: prediction {answer} @ {confidence} submitted, "
                     f"id {sub_id}, status {res.get('status')}")
        except ApiError as e:
            self._record(slug, "submit-failed", str(e))
            self.log(f"  {slug}: submit FAILED: {e}")

    def _content(self, slug, bounties, dry_run):
        kind, filename = CONTENT_MAP[slug]
        path = os.path.join(self.out_dir, filename)
        if dry_run:
            self._record(slug, "would-prepare-content", f"{kind} -> {filename}")
            self.log(f"  {slug}: would prepare {kind} -> {filename}")
            return
        builder = {"article": content.build_article,
                   "meme": content.build_meme_svg,
                   "art": content.build_art_svg}[kind]
        builder(bounties, path)
        size = os.path.getsize(path)
        self._record(slug, "prepared-content", f"{kind} -> {filename} ({size} bytes)")
        self.log(f"  {slug}: prepared {kind} -> {filename} ({size} bytes)")
        public_base = os.environ.get("AIPROVE_PUBLIC_BASE", "").rstrip("/")
        if not public_base:
            self._record(slug, "submit-skipped",
                         "content prepared; submit needs a public URL (publish step)")
            self.log(f"  {slug}: submit skipped, needs a public URL (publish step)")
            return
        try:
            res = self.client.submit_link(
                slug, f"{public_base}/{filename}",
                f"{kind} for AIProve, built autonomously from live board data",
                self.handle)
            sub_id = res.get("id") or res.get("submission", {}).get("id")
            self._record(slug, "submitted-link",
                         f"link {public_base}/{filename} id={sub_id} "
                         f"status={res.get('status')}")
            self.log(f"  {slug}: link submitted, id {sub_id}")
        except ApiError as e:
            self._record(slug, "submit-failed", str(e))
            self.log(f"  {slug}: submit FAILED: {e}")

    def run(self, bounties, dry_run=False, enter_only=None, max_predictions=None):
        self.predictions_left = max_predictions
        for b in bounties:
            slug = b.get("slug")
            if enter_only and slug != enter_only:
                continue
            self.log(f"[{slug}] {b.get('title')} "
                     f"({b.get('amt')} {b.get('unit')}, {b.get('lane')})")
            if slug in SKIP_REASONS:
                self._enter(slug, dry_run)
                self._record(slug, "skipped", SKIP_REASONS[slug])
                self.log(f"  skipped: {SKIP_REASONS[slug]}")
                continue
            if slug in SELF_BOUNTIES:
                self._enter(slug, dry_run)
                self._record(slug, "entered-only",
                             "completion of this bounty is this agent's repo")
                continue
            self._enter(slug, dry_run)
            if slug in FORECAST_SLUGS:
                self._forecast(slug, dry_run)
            elif slug in CONTENT_MAP:
                self._content(slug, bounties, dry_run)
            else:
                self._record(slug, "skipped", "no handler for this bounty type")
                self.log(f"  skipped: no handler for this bounty type")
        return self.report
