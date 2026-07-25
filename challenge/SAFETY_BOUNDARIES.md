# Safety Boundaries

Allowed:

- Local unit tests.
- Local mock tool execution.
- Synthetic email addresses under `example.com`.
- Synthetic payment amounts and currencies.
- Synthetic file paths under `/workspace/demo`.

Prohibited:

- Live external attacks.
- External scanning.
- Credential collection.
- Real payment flows.
- Real personal files.
- Exploit payload publication for undisclosed vulnerabilities.
