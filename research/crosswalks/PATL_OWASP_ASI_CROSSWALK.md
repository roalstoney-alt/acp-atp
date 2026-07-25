# PATL x OWASP Agentic Security Initiative Crosswalk

Sources:

- OWASP Agentic AI Threats and Mitigations: https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/
- OWASP ASI insecure agent samples page: https://owasp.org/www-project-top-10-for-large-language-model-applications/initiatives/agent_security_initiative/

No endorsement or compliance is claimed.

| Topic | Status | PATL alignment | Gap |
|---|---|---|---|
| Tool misuse and excessive agency | PARTIAL_ALIGNMENT | PAAC permits or blocks declared action types and tools. | PATL does not analyze prompt content or tool output semantics. |
| Agent misconfiguration | DIRECT_ALIGNMENT | Runtime blocks missing or undeclared tool, model, version, and delegation metadata. | Identity is declared, not cryptographically attested. |
| Multi-step workflows | PATL_EXTENSION | Evidence Chain records each gateway decision. | No distributed trace format yet. |
| Sandbox escape | NOT_ADDRESSED | PATL can block unauthorized method requests before execution. | PATL is not a sandbox and cannot contain a compromised host. |
| Insecure framework samples | REQUIRES_REVIEW | Boundary Challenge scenarios can become safe local test cases. | Needs OWASP maintainer review before contribution. |

Concrete contribution PATL could offer: a compact method-authorization challenge suite focused on goal-versus-method boundaries.
