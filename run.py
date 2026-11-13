#!/usr/bin/env python3
"""Best fully-autonomous AIProve agent — no human in the loop.

Reads skill.md, signs in with its own keypair, lists open bounties, and
enters and completes as many as it can on its own: predictions from public
market data, content artifacts built from live board data, and an honest
written reason for everything it skips.

Usage:
    python3 run.py [--handle HANDLE] [--max-predictions N]
                   [--enter-only SLUG] [--dry-run]

Flags:
  --handle           public handle (default: autonomous.agent)
  --max-predictions  cap on prediction submissions (default: unlimited)
  --enter-only SLUG  process only one bounty (test mode)
  --dry-run          plan only: no enter, no submit, no files written

Environment:
  AIPROVE_API         API base (default https://aiprove.fun)
  AIPROVE_PUBLIC_BASE public URL prefix for prepared content files; when set,
                      content entries are submitted as links, otherwise they
                      are prepared locally and the submit is recorded as
                      needing the publish step.

The agent prints only public facts. Challenge, signature and session token
are never printed; the keypair (agent-key.json, mode 600) is never printed
and never leaves this machine.
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone

from agent import skill as skill_mod
from agent.client import ApiError, Client
from agent.keys import load_or_create_key
from agent.loop import Loop

API = os.environ.get("AIPROVE_API", "https://aiprove.fun")
HERE = os.path.dirname(os.path.abspath(__file__))
KEY_PATH = os.path.join(HERE, "agent-key.json")
SESS_PATH = os.path.join(HERE, "session.json")
OUT_DIR = os.path.join(HERE, "out")


def log(msg):
    print(f"[{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC] {msg}",
          flush=True)


def main():
    ap = argparse.ArgumentParser(description="Fully-autonomous AIProve agent.")
    ap.add_argument("--handle", default="autonomous.agent")
    ap.add_argument("--max-predictions", type=int, default=None)
    ap.add_argument("--enter-only", default=None)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    os.makedirs(OUT_DIR, exist_ok=True)
    log("autonomous loop starting (no human in the loop)")

    # 1. Read skill.md
    text = skill_mod.read_skill(API)
    log(f"skill.md OK: {len(text)} bytes, auth/list/enter endpoints present")

    # 2. Own keypair
    account, created = load_or_create_key(KEY_PATH)
    log(f"{'generated fresh' if created else 'loaded existing'} keypair, "
        f"address {account.address} (key file mode 600)")

    # 3. Authenticate
    client = Client(API)
    try:
        address, expires = client.authenticate(account)
    except ApiError as e:
        sys.exit(f"auth failed: {e}")
    if not args.dry_run:
        fd = os.open(SESS_PATH, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w") as f:
            json.dump({"address": address, "expiresAt": expires}, f)
        os.chmod(SESS_PATH, 0o600)
    log(f"authenticated as {address}; session cached (mode 600), expiresAt {expires}")

    # 4. List open bounties
    try:
        bounties = client.list_bounties()
    except ApiError as e:
        sys.exit(f"list failed: {e}")
    log(f"open bounties: {len(bounties)}")

    # 5. Autonomous loop
    loop = Loop(client, args.handle, OUT_DIR, log)
    loop.report.update({
        "agent": address,
        "handle": args.handle,
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "dry_run": args.dry_run,
    })
    try:
        loop.run(bounties, dry_run=args.dry_run,
                 enter_only=args.enter_only,
                 max_predictions=args.max_predictions)
    except ApiError as e:
        sys.exit(f"loop failed: {e}")

    # 6. Final state + report
    counts = {}
    for s in loop.report["steps"]:
        counts[s["action"]] = counts.get(s["action"], 0) + 1
    if not args.dry_run:
        try:
            me = client.me()
            loop.report["me"] = {
                "competing_count": len(me.get("competing") or []),
                "submissions_count": len(me.get("submissions") or []),
                "won": me.get("won"),
                "earningsUsd": me.get("earningsUsd"),
            }
            log(f"/api/me: competing={len(me.get('competing') or [])} "
                f"submissions={len(me.get('submissions') or [])} "
                f"won={me.get('won')} earningsUsd={me.get('earningsUsd')}")
        except ApiError as e:
            log(f"/api/me check failed (non-fatal): {e}")
        report_path = os.path.join(OUT_DIR, "report.json")
        with open(report_path, "w") as f:
            json.dump(loop.report, f, indent=2)
        log(f"report written to {report_path}")
    log(f"LOOP COMPLETE: {counts}")
    log("autonomous loop finished — no human input was needed at any step")


if __name__ == "__main__":
    main()
