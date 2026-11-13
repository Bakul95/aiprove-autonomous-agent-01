"""Read aiprove.fun/skill.md and confirm the loop it describes."""
from .client import curl_text

REQUIRED_MARKERS = ("/api/auth/challenge", "/api/bounties", "/enter",
                    "/api/auth/verify")


def read_skill(api_base):
    """Fetch skill.md. Returns its text; raises ValueError if incomplete."""
    status, text = curl_text(f"{api_base.rstrip('/')}/skill.md")
    if status != 200 or not text:
        raise ValueError(f"skill.md fetch failed: HTTP {status}")
    missing = [m for m in REQUIRED_MARKERS if m not in text]
    if missing:
        raise ValueError(f"skill.md missing endpoint markers: {missing}")
    return text
