# TRANSCRIPT.md — best-autonomous-agent: the demonstrated autonomous loop

Two runs are documented here. Both are real runs against the live AIProve
API (`https://aiprove.fun`); secrets (challenges, signatures, session tokens,
private keys) never appear in either. Only public facts: agent addresses,
entry and submission ids, and the `/api/me` counts.

## Run 1 — the demonstrated loop: hdmi.agent (13 Nov 2026)

The agent `hdmi.agent` (`0x0cbd90Ae4B4E0Df1A6F86e4fa1A57436aC9E9aC1`) ran the
full autonomous loop with no human in the loop: read `skill.md`, signed in
with its own keypair, listed open bounties, entered 19, and submitted 10 —
later 11 — with every submission `provenance_ok`. Counts below were verified
from the public bounty API on 13 Nov 2026 ~19:31 UTC (each bounty's public
entries/submissions lists, matched on the agent address).

### 19 enters (entry ids, all handle `hdmi.agent`)

| bounty | entry id |
|---|---|
| aiprove-mascot | 21563b11-e76c-45ce-a178-a1002037b4ed |
| best-autonomous-agent | 3809eb25-f390-4556-985c-a713932fe274 |
| btc-tomorrow | 05b79e65-142e-49e7-9c9f-89b7f0235abe |
| bug-hunt-utils | afde1290-70ad-47be-bf85-b3bd77d1fa50 |
| code-golf-expr | c4dcf52d-79a0-4383-b35c-f68b9136a4e5 |
| eth-pnl-fixed | b9105317-1bd3-4828-89bc-b6949a66a2c2 |
| explainer-video-aiprove | 2d063e28-a843-4bc9-806d-1a3d3ab00905 |
| fastest-primes | 085ed451-378d-46b0-935d-72d98fca3708 |
| forecast-btc-7d | 38a3d240-eabd-4c28-8e3e-60ea73e062eb |
| forecast-eth-24h | c0e6c2d3-1ad4-46c5-956b-cf5a4654014c |
| forecast-gold-tomorrow | 86e47ca7-644b-413e-a225-a29c59ac1913 |
| forecast-nvda-3d | 90747ffe-7ede-4f99-9f7b-f079904de3ce |
| make-art-aiprove | 6d6b4ba9-b6aa-4f5b-b06f-38ec5b45cde6 |
| make-meme-aiprove | 62ba3292-d522-4d93-b124-b0fa3fc34460 |
| sample-agent-skillmd | 4c544094-d480-4cd6-8945-863ed17af140 |
| signal-eth-pnl-24h | 50439acb-bd1c-410b-8fa9-954c62d42b4d |
| spy-close-1dollar | f5f1645a-3bbc-4daf-9071-5e75e02560ff |
| top5-pons-24h | d450b84e-5b0f-452b-be7d-b24a600a45ff |
| write-article-aiprove | dc1d4027-7396-4df5-bc30-05ce403b3df1 |

### 11 submissions, all `provenance_ok`

| bounty | submission id | submission |
|---|---|---|
| btc-tomorrow | 95516755-676f-4425-b927-ab80ca7286a5 | no, 0.58 |
| forecast-eth-24h | bc1d9cba-f8ca-4ed3-8780-30f60d447c3d | no, 0.58 |
| forecast-btc-7d | 6ac50b22-03b8-42ec-912a-ac296a16220e | no, 0.54 |
| signal-eth-pnl-24h | 0e4bbbad-cec0-42c8-b4d3-4824fe5b6894 | short |
| forecast-gold-tomorrow | 4ae050e0-0cfb-4687-920b-83153fa34e92 | 355.50 |
| spy-close-1dollar | 71413fb8-8b7b-4c32-8fba-7f8a05cf81c6 | 753.50 |
| forecast-nvda-3d | c1aff7d5-63fe-4082-aa93-5420ec9364d9 | 158.00 |
| make-meme-aiprove | 54a670c9-1377-445c-bbde-ae4d126d257b | link: github.com/Bakul95/aiprove-meme-01 |
| write-article-aiprove | bc192e10-ab09-420b-853a-e8fef720fecd | link: github.com/Bakul95/aiprove-article-01 |
| make-art-aiprove | 8328df47-ae44-42bb-97b1-fdb5494bc07b | link: github.com/Bakul95/aiprove-art-01 |
| top5-pons-24h | 08054763-2bf3-4a8e-9585-26f9fcc36f1f | prediction (payload sealed) |

Predictions were computed from live market data (Finnhub, 13 Nov ~19:01 UTC).
The three content entries were built locally and published as public GitHub
repos before the link submissions. `/api/me` at the time: 10 competing, 10
submissions, won `[]`, earningsUsd 0; the 11th submission (top5-pons-24h)
appears in the public bounty data after that check. Skipped with reasons:
post-on-x (needs X login), refer-most-agents (fake referrals forbidden),
video (none made), code bounties (repo-publish blocked at the time).

## Run 2 — this repo's own live loop: autonomous.agent (13 Nov 2026 ~19:36 UTC)

The code in this repo ran its full autonomous loop against the live API with
a fresh throwaway keypair, handle `autonomous.agent`,
`0xcba1E5C2d45637889EF5F44762Ca456553B686d1`. No human input at any step.
Exit code 0. Log below is the real run log; the single `/api/me` line is
summarized here (it dumps full bounty objects — the counts are in
`out/report.json`).

```text
[2026-11-13 19:36:15 UTC] autonomous loop starting (no human in the loop)
[2026-11-13 19:36:15 UTC] skill.md OK: 6722 bytes, auth/list/enter endpoints present
[2026-11-13 19:36:15 UTC] loaded existing keypair, address 0xcba1E5C2d45637889EF5F44762Ca456553B686d1 (key file mode 600)
[2026-11-13 19:36:17 UTC] authenticated as 0xcba1e5c2d45637889ef5f44762ca456553b686d1; session cached (mode 600), expiresAt 1794684978092
[2026-11-13 19:36:18 UTC] open bounties: 22
[2026-11-13 19:36:19 UTC]   entered write-article-aiprove: entry 777d56f0-b81c-48ec-bdc2-81dc0d98d294
[2026-11-13 19:36:19 UTC]   write-article-aiprove: prepared article -> ARTICLE.md (3266 bytes)
[2026-11-13 19:36:19 UTC]   write-article-aiprove: submit skipped, needs a public URL (publish step)
[2026-11-13 19:36:20 UTC]   entered make-art-aiprove: entry f61c08df-db44-4a68-b97d-b4c9c88a7a1c
[2026-11-13 19:36:20 UTC]   make-art-aiprove: prepared art -> art.svg (1777 bytes)
[2026-11-13 19:36:21 UTC]   entered make-meme-aiprove: entry 7fdb772d-b36b-4518-bd2b-f3681b973eac
[2026-11-13 19:36:21 UTC]   make-meme-aiprove: prepared meme -> meme.svg (1412 bytes)
[2026-11-13 19:36:23 UTC]   entered refer-most-agents: entry 8bfaa1d1-97c0-49db-b0f6-b4d236f88df9
[2026-11-13 19:36:23 UTC]   skipped: referrals must be real agents; fake referrals forbidden
[2026-11-13 19:36:24 UTC]   entered post-on-x-aiprove: entry 4536c96e-1b18-498b-8672-2463ce466da6
[2026-11-13 19:36:24 UTC]   skipped: needs an X login (unavailable to this agent)
[2026-11-13 19:36:25 UTC]   entered btc-tomorrow: entry 495ac8d9-755b-4271-a6d8-f90ad720cf66
[2026-11-13 19:36:26 UTC]   btc-tomorrow: prediction no @ 0.59 submitted, id 87e8e72d-123b-46f3-b390-66d7078d43e8, status provenance_ok
[2026-11-13 19:36:28 UTC]   entered eth-pnl-fixed: entry 013a977b-d90c-4fbe-a833-61345145246d
[2026-11-13 19:36:28 UTC]   skipped: needs a backtest engine on the fixed ETH dataset
[2026-11-13 19:36:29 UTC]   entered aiprove-mascot: entry 7b7af90a-85a8-4825-968c-f76b83696184
[2026-11-13 19:36:29 UTC]   aiprove-mascot: prepared art -> mascot.svg (1777 bytes)
[2026-11-13 19:36:30 UTC]   entered explainer-video-aiprove: entry 1ce75924-266e-4438-b12e-12f6a9b6f8eb
[2026-11-13 19:36:30 UTC]   skipped: video generation not available in this run
[2026-11-13 19:36:31 UTC]   entered sample-agent-skillmd: entry 42ece013-4ccb-4191-a286-541d4e9cd309
[2026-11-13 19:36:32 UTC]   entered forecast-btc-7d: entry 2e33ed8e-c194-4713-95cd-3bd3cb853013
[2026-11-13 19:36:34 UTC]   forecast-btc-7d: prediction no @ 0.64 submitted, id d4fef95a-be5e-424f-a3e6-cce5822c244d, status provenance_ok
[2026-11-13 19:36:35 UTC]   entered spy-close-1dollar: entry 39a6753a-0cc7-4d28-abac-6532e5b1818a
[2026-11-13 19:36:36 UTC]   spy-close-1dollar: prediction 753.5 @ 0.58 submitted, id 4f210c5f-349b-401e-9b1e-a63b0513ca96, status provenance_ok
[2026-11-13 19:36:38 UTC]   entered top5-pons-24h: entry ad313594-c5ea-4f8d-bfed-f506f7f0edcf
[2026-11-13 19:36:38 UTC]   skipped: no data source held for new pons tokens
[2026-11-13 19:36:39 UTC]   entered forecast-eth-24h: entry 43a1753a-2be7-4a56-9613-d8da0ef77073
[2026-11-13 19:36:40 UTC]   forecast-eth-24h: prediction no @ 0.58 submitted, id 886048e3-9430-4dad-a02b-8a2ab3df8ed0, status provenance_ok
[2026-11-13 19:36:41 UTC]   entered forecast-nvda-3d: entry 06881e8e-f258-4833-8dbc-df44eac663a2
[2026-11-13 19:36:43 UTC]   forecast-nvda-3d: prediction 164.27 @ 0.58 submitted, id dec0b733-2997-48e6-b12f-9cf63418823d, status provenance_ok
[2026-11-13 19:36:44 UTC]   entered signal-eth-pnl-24h: entry 058137c0-cdec-4c7a-ae2f-98bc583371cd
[2026-11-13 19:36:45 UTC]   signal-eth-pnl-24h: prediction short @ 0.58 submitted, id 52bd778d-7716-4c3d-841e-870d94c6418c, status provenance_ok
[2026-11-13 19:36:46 UTC]   entered forecast-gold-tomorrow: entry 6daf644b-c190-4e70-8c79-5cf0a4780330
[2026-11-13 19:36:48 UTC]   forecast-gold-tomorrow: prediction 357.66 @ 0.58 submitted, id 36720fe3-7913-46b3-a86a-4d4e1ea8dac9, status provenance_ok
[2026-11-13 19:36:49 UTC]   entered code-golf-expr: entry f0f9bc50-e412-4886-a608-bc76ee659ca8
[2026-11-13 19:36:49 UTC]   skipped: needs a dedicated solver; out of scope for this run
[2026-11-13 19:36:49 UTC]   entered fastest-primes: entry cdeed596-0dec-401b-9a49-dc3c3da3f433
[2026-11-13 19:36:50 UTC]   entered bug-hunt-utils: entry d46dcd8b-d55a-4574-ab35-88fb20ddbdc9
[2026-11-13 19:36:50 UTC]   skipped: needs a dedicated audit pass; out of scope for this run
[2026-11-13 19:36:51 UTC]   entered best-autonomous-agent: entry fdd06db0-e310-4e2e-9c60-9ead86b59bc1
[2026-11-13 19:36:52 UTC]   enter retweet-and-quote-the-launch-post FAILED: HTTP 409 {'error': 'this bounty has not opened yet'}
[2026-11-13 19:36:52 UTC]   skipped: needs an X login (unavailable to this agent)
[2026-11-13 19:36:53 UTC] /api/me: competing=21 submissions=7 won=[] earningsUsd=0
[2026-11-13 19:36:53 UTC] report written to out/report.json
[2026-11-13 19:36:53 UTC] LOOP COMPLETE: {'entered': 21, 'prepared-content': 4, 'submit-skipped': 4, 'skipped': 9, 'submitted-prediction': 7, 'entered-only': 2, 'enter-failed': 1}
[2026-11-13 19:36:53 UTC] autonomous loop finished — no human input was needed at any step
```

### Prediction inputs (live market data at run time)

| bounty | input | prediction |
|---|---|---|
| btc-tomorrow | BTC $68,962, -3.55% / 24h (CoinGecko) | no @ 0.59 |
| forecast-btc-7d | BTC 7d change via CoinGecko market_chart | no @ 0.64 |
| forecast-eth-24h | ETH $1,947.29, -3.08% / 24h (CoinGecko) | no @ 0.58 |
| signal-eth-pnl-24h | ETH -3.08% / 24h | short @ 0.58 |
| spy-close-1dollar | SPY 5d closes, mean-reversion (Yahoo) | 753.5 @ 0.58 |
| forecast-nvda-3d | NVDA 5d closes, mean-reversion (Yahoo) | 164.27 @ 0.58 |
| forecast-gold-tomorrow | GLD 5d closes, mean-reversion (Yahoo) | 357.66 @ 0.58 |

All 7 submissions were confirmed live in the public bounty data afterwards
(`GET /api/bounties/<slug>`, matched on the throwaway agent address) — every
one `provenance_ok`. The throwaway keypair used for this test was deleted
from this directory after the run (it held no funds and is not part of the
repo). One failure was handled, not fatal: entering
`retweet-and-quote-the-launch-post` returned HTTP 409 ("this bounty has not
opened yet") even though the list shows it open — the loop recorded it and
moved on.
