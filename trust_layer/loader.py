from __future__ import annotations

from pathlib import Path
from typing import Any

import jsonschema

from .fixtures import dt
from .models import PAACContract


def load_schema(schema_path: str | Path = "schemas/paac-v0.1.schema.json") -> dict[str, Any]:
    return _load_json(schema_path)


def load_contracts_from_json(
    documents: list[dict[str, Any]],
    schema_path: str | Path = "schemas/paac-v0.1.schema.json",
) -> dict[str, PAACContract]:
    schema = _load_json(schema_path)
    validator_cls = jsonschema.validators.validator_for(schema)
    validator_cls.check_schema(schema)
    validator = validator_cls(schema)
    contracts: dict[str, PAACContract] = {}
    for document in documents:
        errors = sorted(validator.iter_errors(document), key=lambda error: list(error.path))
        if errors:
            detail = "; ".join(error.message for error in errors)
            raise ValueError(f"Invalid PAAC contract {document.get('contract_id', '<missing>')}: {detail}")
        contract = _to_contract(document)
        contracts[contract.contract_id] = contract
    return contracts


def _to_contract(document: dict[str, Any]) -> PAACContract:
    agent_stack = document["agent_stack"]
    validity = document["validity"]
    principal = document["principal"]
    return PAACContract(
        paac_version=document["paac_version"],
        contract_id=document["contract_id"],
        principal_id=principal["pseudonymous_id"],
        agent_id=agent_stack["agent_id"],
        agent_version=agent_stack["agent_version"],
        model_id=agent_stack["model_id"],
        tool_ids=list(agent_stack.get("tool_ids", [])),
        purpose=document["purpose"],
        permitted_actions=list(document["permitted_actions"]),
        prohibited_actions=list(document["prohibited_actions"]),
        resources=dict(document["resources"]),
        constraints=dict(document["constraints"]),
        valid_from=dt(validity["valid_from"]),
        valid_until=dt(validity["valid_until"]),
        confirmation_required_actions=list(document.get("confirmation_required_actions", [])),
        log_required_actions=list(document.get("log_required_actions", [])),
    )


def _load_json(path: str | Path) -> dict[str, Any]:
    import json

    return json.loads(Path(path).read_text(encoding="utf-8"))
