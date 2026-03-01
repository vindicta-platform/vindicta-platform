import json
import pathlib
from typing import Dict, TypedDict


class DomainInfo(TypedDict):
    repo_name: str
    tech_stack: str
    workflow_profile: str
    primary_language: str
    node_name: str
    package_name: str  # e.g. "vindicta_engine" or "@vindicta/ui-kit"


_CONFIG_PATH = pathlib.Path(__file__).parent / "configs" / "domains.json"


def _load_domain_registry() -> Dict[str, DomainInfo]:
    with open(_CONFIG_PATH, "r") as f:
        return json.load(f)


# Load the registry from persistence layer
DOMAIN_REGISTRY: Dict[str, DomainInfo] = _load_domain_registry()
