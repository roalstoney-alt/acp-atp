# PATL Integrations

This directory contains isolated integration experiments.

Current status:

- `selected_framework/`: a LangChain-style tool invocation adapter.
- Evidence maturity: EML-2.
- Limitation: common agent framework packages were not installed locally, so this is boundary compatibility work, not independent framework integration.

Run:

```bash
python3 -B -m integrations.selected_framework.demo
```
