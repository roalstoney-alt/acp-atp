# Selected Framework Adapter

Selected boundary: LangChain-style tool invocation wrapper.

Selection rationale:

- Open agent frameworks commonly expose a tool-call boundary.
- A pre-execution authorization wrapper can be demonstrated without real credentials.
- The adapter does not fork or redesign framework core behavior.
- The local environment did not include installed framework packages, so this remains a dependency-light compatibility adapter.

Demonstrated:

- Allowed operation completes.
- Confirmation-required operation pauses.
- Exact confirmation permits execution.
- Revocation blocks subsequent action.
- Undeclared tool is blocked.
- Evidence chain records decisions.

Run:

```bash
python3 -B -m integrations.selected_framework.demo
```

Limitation: This is not external independent integration and not framework endorsement.
