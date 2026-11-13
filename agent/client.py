"""AIProve API client: auth (EIP-191 challenge), list, enter, submit.

HTTP goes through `curl`, not urllib: urllib POSTs hang from some sandboxes,
curl is reliable here. JSON bodies are passed to curl on stdin, never through
the shell. The session token lives in memory (and, if cached, in session.json
mode 600) and is never printed.
"""
import json
import os
import subprocess

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")


class ApiError(Exception):
    pass


def curl_json(method, url, payload=None, token=None, timeout=60):
    cmd = ["curl", "-s", "--max-time", str(timeout), "-A", UA,
           "-X", method, url, "-H", "content-type: application/json"]
    if token:
        cmd += ["-H", f"Authorization: Bearer {token}"]
    if payload is not None:
        cmd += ["-d", "@-"]  # read the JSON body from stdin
    cmd += ["-w", "\n%{http_code}"]
    data = json.dumps(payload).encode() if payload is not None else None
    out = subprocess.run(cmd, input=data, capture_output=True, timeout=timeout + 30)
    text = out.stdout.decode("utf-8", "replace")
    body, _, status = text.rpartition("\n")
    try:
        status = int(status)
    except ValueError:
        status = 0
    try:
        parsed = json.loads(body) if body.strip() else {}
    except ValueError:
        parsed = body
    return status, parsed


def curl_text(url, timeout=30):
    """GET a non-JSON resource (skill.md, market data). Returns (status, text)."""
    cmd = ["curl", "-s", "--max-time", str(timeout), "-A", UA, url,
           "-w", "\n%{http_code}"]
    out = subprocess.run(cmd, capture_output=True, timeout=timeout + 30)
    text = out.stdout.decode("utf-8", "replace")
    body, _, status = text.rpartition("\n")
    try:
        status = int(status)
    except ValueError:
        status = 0
    return status, body


class Client:
    def __init__(self, api_base):
        self.api = api_base.rstrip("/")
        self.token = None
        self.address = None

    def authenticate(self, account):
        """Challenge -> EIP-191 sign -> verify. Returns the agent address."""
        from eth_account.messages import encode_defunct
        addr = account.address
        status, ch = curl_json("GET", f"{self.api}/api/auth/challenge?address={addr}")
        challenge = ch.get("challenge") if isinstance(ch, dict) else None
        if status != 200 or not challenge:
            raise ApiError(f"challenge failed: HTTP {status} {str(ch)[:200]}")
        # Byte-exact signing: the challenge string as received, no newline.
        sig = account.sign_message(encode_defunct(text=challenge)).signature.hex()
        status, res = curl_json("POST", f"{self.api}/api/auth/verify",
                                {"address": addr, "signature": "0x" + sig})
        token = res.get("token") if isinstance(res, dict) else None
        if status != 200 or not token:
            raise ApiError(f"verify failed: HTTP {status} {str(res)[:200]}")
        self.token = token
        self.address = res.get("address", addr)
        return self.address, res.get("expiresAt")

    def _authed(self, method, path, payload=None):
        if not self.token:
            raise ApiError("not authenticated")
        return curl_json(method, f"{self.api}{path}", payload, token=self.token)

    def list_bounties(self, status_filter="open"):
        status, data = curl_json("GET", f"{self.api}/api/bounties?status={status_filter}")
        if status != 200:
            raise ApiError(f"list bounties failed: HTTP {status}")
        return data if isinstance(data, list) else data.get("bounties", [])

    def get_bounty(self, slug):
        status, data = curl_json("GET", f"{self.api}/api/bounties/{slug}")
        if status != 200:
            raise ApiError(f"get bounty {slug} failed: HTTP {status}")
        return data

    def enter(self, slug, handle):
        status, res = self._authed("POST", f"/api/bounties/{slug}/enter",
                                   {"handle": handle})
        if status not in (200, 201):
            raise ApiError(f"enter {slug} failed: HTTP {status} {str(res)[:200]}")
        return res

    def submit_prediction(self, slug, answer, confidence, handle):
        payload = {"prediction": {"answer": answer, "confidence": confidence},
                   "handle": handle}
        status, res = self._authed("POST", f"/api/bounties/{slug}/submit", payload)
        if status not in (200, 201):
            raise ApiError(f"submit {slug} failed: HTTP {status} {str(res)[:200]}")
        return res

    def submit_link(self, slug, link, note, handle):
        # Content bounties accept a link submission {link, note, handle}.
        payload = {"link": link, "note": note, "handle": handle}
        status, res = self._authed("POST", f"/api/bounties/{slug}/submit", payload)
        if status not in (200, 201):
            raise ApiError(f"submit {slug} failed: HTTP {status} {str(res)[:200]}")
        return res

    def submit_repo(self, slug, repo_url, commit, transcript, handle):
        payload = {"repoUrl": repo_url, "commit": commit,
                   "transcript": transcript, "handle": handle}
        status, res = self._authed("POST", f"/api/bounties/{slug}/submit", payload)
        if status not in (200, 201):
            raise ApiError(f"submit {slug} failed: HTTP {status} {str(res)[:200]}")
        return res

    def me(self):
        status, res = self._authed("GET", "/api/me")
        if status != 200:
            raise ApiError(f"/api/me failed: HTTP {status}")
        return res
