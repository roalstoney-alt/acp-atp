# Reuse / Archive / Gap Matrix

| Asset | Decision | Rationale | PATL Action |
| --- | --- | --- | --- |
| `ACP-ATP Personal Agent Trust Layer.docx` | Reuse | Authoritative seed plan and mission | Converted into PATL docs/spec direction |
| MDL evidence standards | Reuse | Strong append-only evidence and negative-result discipline | Adapted into evidence event and validation report language |
| MOS/PGA permission/risk language | Reuse selectively | Contains useful deterministic gating patterns | Used as inspiration only; no trading logic imported |
| MOS/PGA generated data/logs | Archive in place | Domain-specific and unrelated to personal-agent trust | Left untouched |
| `reality-quest` nested repo | Archive in place | Separate git project unrelated to PATL | Not modified |
| Workspace root git state | Gap | No root git repository | Documented as audit limitation |
| PAAC machine schema | Gap closed | No schema existed | Added `schemas/paac-v0.1.schema.json` |
| Evidence format | Gap closed | No PATL evidence format existed | Added evidence schema and generator |
| Agent credit format | Gap closed | No PATL credit event format existed | Added schema and generator |
| Enforcement layer | Gap closed for alpha | No local ATP gateway existed | Added deterministic Python implementation |
| Email/travel/file demos | Gap closed for alpha | Required MVP scenarios absent | Added synthetic demo runner and docs |
| Hardware-backed root authority | Unresolved | Requires platform security work | Marked proposed, not implemented |
| Third-party audit network | Unresolved | Requires protocol/network design | Marked proposed, not implemented |
| Real account connectors | Intentionally excluded | User required synthetic data/mock services | Not implemented |
