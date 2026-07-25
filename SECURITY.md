# Security And Responsible Disclosure

PATL v0.1.1 Challenge welcomes defensive reports about the local synthetic challenge, PAAC specifications, evidence-chain logic, tests, and documentation.

Authorized testing is limited to this repository's local fixtures, mock tools, synthetic data, and documented commands.

Do not test against ACP-ATP infrastructure, GitHub, third-party systems, real accounts, production services, payment systems, personal files, live credentials, or external networks.

## Report A Finding

Use the Authorization Bypass issue template for local synthetic bypasses. If public disclosure could create real-world risk, start with a private note to the maintainer before public amplification.

Include:

- exact local reproduction steps;
- scenario id or a proposed synthetic scenario;
- observed versus expected decision;
- whether the finding requires breaking the trusted local enforcement boundary;
- logs without secrets, credentials, personal data, or live target details.

See also: `challenge/RESPONSIBLE_DISCLOSURE.md`.

