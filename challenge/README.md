# PATL Boundary Challenge 001

Question: Can an agent exceed its authorized methods?

This challenge uses only synthetic requests, mock tools, and local fixtures. It does not scan, attack, or contact external systems.

Web entry:

```text
challenge/portal.html
```

The portal creates a browser-local synthetic tester profile and prepares a structured report draft. It does not create a real user account, send data to a server, or authorize testing outside this repository.

Run:

```bash
python3 -B -m challenge.run_boundary_challenge
```

Expected summary:

```text
"passed": 15
"failed": 0
```

The command writes `challenge/BASELINE_RESULTS.json`.

Status: internal reproduction only until an external reviewer reports results.

Public release status:

- Local technical validation: PASS.
- Boundary Challenge: 15/15.
- Independent reproduction: PENDING.
- Real framework integration: PENDING.
- Production readiness: NO.

Use GitHub Issues to report reproduction results, bounded authorization bypasses, integration reports or specification feedback. See `SECURITY.md` and `challenge/RESPONSIBLE_DISCLOSURE.md` before reporting anything that could create real-world risk.
