# Contributor Guide

## Principles

- Preserve user authority.
- Add tests for every security claim.
- Clearly mark implemented, simulated, proposed and unresolved controls.
- Do not add real account connectors to alpha without a separate security design.
- Preserve negative results.

## Development

```bash
python3 -B -m unittest discover -s tests
```

## Pull Request Checklist

- Docs updated.
- Tests added for security changes.
- No real credentials or personal data.
- No LLM-only gate for critical permissions.
- Design decisions recorded when material.
