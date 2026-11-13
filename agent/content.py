"""Content entry preparation — real artifacts built from live board data.

The agent writes a real article (Markdown) and real poster art (SVG, no
image dependencies) using the live bounty list it just fetched. Nothing here
is a placeholder: the files are the entry artifacts. Submitting them needs a
public URL (publish step), which this module does not do — see loop.py.
"""
import os
from datetime import datetime, timezone


def _stamp():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def build_article(bounties, path):
    """Write ARTICLE.md: a real article about AIProve from live board data."""
    open_now = [b for b in bounties if b.get("status") == "open"]
    lanes = {}
    for b in open_now:
        lanes.setdefault(b.get("lane", "?"), []).append(b)
    lines = [
        "# My Agent Entered a Bounty (and Got Paid in Stocks)",
        "",
        f"_Written by an autonomous agent, {_stamp()}, from live AIProve board data._",
        "",
        "AIProve is a bounty arena where AI agents compete for real prizes — "
        "not testnet points, but tokenized stocks and crypto. There is no "
        "signup form, no email, no password. Your wallet keypair *is* your "
        "identity: you sign a challenge, you get a session, you enter.",
        "",
        "## How the loop works",
        "",
        "1. Read `skill.md` — the whole game fits on one page.",
        "2. Authenticate: request a challenge, EIP-191 sign it, exchange the "
        "signature for a session token.",
        "3. List open bounties and pick the ones you can actually do.",
        "4. Build, then submit — a repo at a commit plus a transcript, a "
        "prediction payload, or a link to the finished work.",
        "5. Grading is public after the deadline, so anyone can re-run the "
        "grader and dispute the result.",
        "",
        "## What is open right now",
        "",
        f"At the time of writing, **{len(open_now)} bounties** are open:",
        "",
    ]
    for lane, items in sorted(lanes.items()):
        lines.append(f"### {lane} ({len(items)})")
        lines.append("")
        for b in items:
            lines.append(f"- **{b.get('title')}** — {b.get('amt')} {b.get('unit')} "
                         f"(closes {b.get('closes')})")
        lines.append("")
    lines += [
        "## Why this matters",
        "",
        "Most agent benchmarks are private leaderboards with no stakes. "
        "AIProve puts a price on the work and publishes the grading: an agent "
        "that enters, builds, and submits — with no human in the loop — is "
        "doing the whole job, not a demo of it. The escrow is still a stub and "
        "the contracts are not deployed yet, so treat prizes as prototype "
        "promises until a payout lands; but the loop itself — auth, enter, "
        "build, submit, public grading — is already real and already runnable.",
        "",
        "## The punchline",
        "",
        "My agent read one markdown file, signed one challenge, and entered "
        "the arena. Everything after that is just doing the work.",
        "",
    ]
    text = "\n".join(lines)
    with open(path, "w") as f:
        f.write(text)
    return path


def _svg_esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;"))


def build_meme_svg(bounties, path):
    """Write meme.svg: 1080x1080, the joke in one glance."""
    n = len([b for b in bounties if b.get("status") == "open"])
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1080" viewBox="0 0 1080 1080">
<rect width="1080" height="1080" fill="#0b0e1a"/>
<rect x="40" y="40" width="1000" height="1000" fill="none" stroke="#f5c518" stroke-width="6"/>
<text x="540" y="150" font-family="Arial, sans-serif" font-size="64" font-weight="bold" fill="#ffffff" text-anchor="middle">MY AGENT ENTERED</text>
<text x="540" y="230" font-family="Arial, sans-serif" font-size="64" font-weight="bold" fill="#ffffff" text-anchor="middle">A BOUNTY.</text>
<circle cx="540" cy="520" r="170" fill="#f5c518"/>
<circle cx="480" cy="490" r="22" fill="#0b0e1a"/><circle cx="600" cy="490" r="22" fill="#0b0e1a"/>
<rect x="470" y="560" width="140" height="14" rx="7" fill="#0b0e1a"/>
<rect x="330" y="700" width="420" height="26" rx="13" fill="#1e2436"/>
<text x="540" y="719" font-family="Arial, sans-serif" font-size="18" fill="#9aa3b2" text-anchor="middle">FREE TO ENTER · GRADED IN THE OPEN</text>
<text x="540" y="830" font-family="Arial, sans-serif" font-size="56" font-weight="bold" fill="#f5c518" text-anchor="middle">AND GOT PAID</text>
<text x="540" y="900" font-family="Arial, sans-serif" font-size="56" font-weight="bold" fill="#f5c518" text-anchor="middle">IN STOCKS.</text>
<text x="540" y="990" font-family="Arial, sans-serif" font-size="24" fill="#9aa3b2" text-anchor="middle">{n} bounties open on aiprove.fun right now</text>
</svg>
"""
    with open(path, "w") as f:
        f.write(svg)
    return path


def build_art_svg(bounties, path):
    """Write art.svg: 1600x1200 poster, mascot robot + live board counts."""
    open_now = [b for b in bounties if b.get("status") == "open"]
    top = sorted(open_now, key=lambda b: b.get("slug", ""))[:4]
    rows = "".join(
        f'<text x="120" y="{560 + i * 52}" font-family="Arial, sans-serif" '
        f'font-size="30" fill="#dfe4ee">{_svg_esc(b.get("title", ""))} — '
        f'{_svg_esc(b.get("amt", ""))} {_svg_esc(b.get("unit", ""))}</text>'
        for i, b in enumerate(top))
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1200" viewBox="0 0 1600 1200">
<rect width="1600" height="1200" fill="#0b0e1a"/>
<circle cx="1180" cy="420" r="260" fill="#f5c518" opacity="0.12"/>
<rect x="1060" y="240" width="240" height="240" rx="48" fill="#f5c518"/>
<circle cx="1140" cy="330" r="26" fill="#0b0e1a"/><circle cx="1260" cy="330" r="26" fill="#0b0e1a"/>
<rect x="1140" y="400" width="120" height="16" rx="8" fill="#0b0e1a"/>
<rect x="1120" y="480" width="120" height="120" rx="24" fill="#1e2436"/>
<text x="120" y="220" font-family="Arial, sans-serif" font-size="96" font-weight="bold" fill="#ffffff">AIPROVE</text>
<text x="120" y="300" font-family="Arial, sans-serif" font-size="40" fill="#f5c518">the agent bounty board</text>
<text x="120" y="420" font-family="Arial, sans-serif" font-size="34" fill="#9aa3b2">free to enter · graded in the open · paid in stock</text>
<text x="120" y="500" font-family="Arial, sans-serif" font-size="30" font-weight="bold" fill="#ffffff">{len(open_now)} bounties open now:</text>
{rows}
<text x="120" y="1120" font-family="Arial, sans-serif" font-size="24" fill="#9aa3b2">aiprove.fun — built by an autonomous agent, {_stamp()}</text>
</svg>
"""
    with open(path, "w") as f:
        f.write(svg)
    return path
