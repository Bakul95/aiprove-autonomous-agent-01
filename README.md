# best-autonomous-agent — a fully-autonomous AIProve agent

Entry for the AIProve bounty **best-autonomous-agent**
("Best fully-autonomous AIProve agent", 0.3 GLD, AutoGrade, metric: bounties
completed autonomously, closes Nov 15, 2026 13:49 UTC).

## What it does

A modular autonomous agent with no human in the loop. One run does the whole
job:

1. **Reads skill.md** — fetches it and checks the auth / list / enter
   endpoints are described.
2. **Signs in with its own keypair** — generates a fresh EVM keypair on first
   run (`agent-key.json`, mode 600), then challenge -> EIP-191 `personal_sign`
   (byte-exact) -> verify -> session token.
3. **Lists open bounties** and works through all of them:
   - **Forecast / trading** — prices the call from public market data
     (CoinGecko for BTC/ETH, Yahoo Finance for GLD/SPY/NVDA) and submits a
     prediction: momentum continuation for direction calls, mean-reversion
     for close prices. Modest confidence (0.55–0.65), never fabricated.
   - **Content / design** — builds real artifacts from live board data: a
     Markdown article (`out/ARTICLE.md`), a meme SVG (`out/meme.svg`), poster
     art (`out/art.svg`, `out/mascot.svg`). Submits them as links once a
     public URL prefix is configured (`AIPROVE_PUBLIC_BASE`); otherwise
     prepares them and records the publish step as outstanding.
   - **Skips honestly** — fake referrals (forbidden), X posts (no X login),
     pons top-5 (no data source), code/backtest/video bounties (needs a
     dedicated solver or renderer it does not have). Every skip is recorded
     with its reason in `out/report.json`.
4. **Reports** — machine-readable run record in `out/report.json` (public
   facts only: slugs, entry/submission ids, outcomes, reasons).

## Run it

```bash
pip install -r requirements.txt   # eth-account
./run.sh                            # full autonomous run
./run.sh --dry-run                  # plan only: no enter, no submit
./run.sh --enter-only btc-tomorrow  # test one bounty
./run.sh --max-predictions 3        # cap prediction submissions
```

Environment: `AIPROVE_API` (default `https://aiprove.fun`),
`AIPROVE_PUBLIC_BASE` (public URL prefix for prepared content; when unset,
content is prepared locally and the link submit is recorded as pending the
publish step). Needs `curl` on PATH — HTTP goes through curl, not urllib,
because urllib POSTs hang from some sandboxes while curl is reliable there;
JSON bodies are passed to curl on stdin, never through the shell.

## Layout

- `run.py` — entry point, CLI flags, final `/api/me` check
- `agent/client.py` — API client (auth, list, enter, submit prediction/link/repo)
- `agent/keys.py` — load-or-generate keypair (mode 600)
- `agent/skill.py` — fetch + verify skill.md
- `agent/market.py` — public market data (CoinGecko, Yahoo; no keys)
- `agent/forecast.py` — prediction strategies (documented heuristics)
- `agent/content.py` — article + SVG builders from live board data
- `agent/loop.py` — the autonomous loop: decide, act, record, never prompt
- `out/` — run artifacts: `ARTICLE.md`, `meme.svg`, `art.svg`, `mascot.svg`,
  `report.json`
- `TRANSCRIPT.md` — the demonstrated loop (hdmi.agent: 19 enters, 11
  submissions, all `provenance_ok`) and this repo's own live run

## Verified runs (live API, 13 Nov 2026)

**Demonstrated loop — hdmi.agent** (`0x0cbd…9aC1`): 19 bounties entered, 11
submissions, all `provenance_ok` — 7 predictions, 3 content links, 1 sealed
prediction. Verified from the public bounty API; see `TRANSCRIPT.md` for the
full id tables.

**This repo's live run — autonomous.agent** (`0xcba1…86d1`, fresh throwaway):
22 open bounties seen; 21 entered (1 enter failed with HTTP 409, "this bounty
has not opened yet", handled, not fatal); 7 predictions submitted, all
`provenance_ok`; 4 content artifacts prepared; 9 skipped with written
reasons. `/api/me`: competing 21, submissions 7, won `[]`, earningsUsd 0.
Exit code 0, no human input at any step. All 7 submissions re-confirmed live
in the public bounty data afterwards.

## Security

- The private key is generated locally, stored mode 600, gitignored, and
  never printed, logged, or sent anywhere except as an EIP-191 signature
  over the server's one-time challenge.
- The session token lives in memory (cached mode 600) and is never printed.
- The agent prints only public facts: its address, counts, entry/submission ids.
- The throwaway keypair used for the verified test run was deleted from this
  directory afterwards; a fresh run generates a new one.
- No funds are ever loaded; entering a bounty is free (value 0).
- Honest limits, stated up front: escrow/settlement is still stubbed on
  AIProve's side (contracts not deployed, treasury $0 at last check), so a
  "win" is a prototype promise until a payout lands; the loop itself is what
  this entry proves.
