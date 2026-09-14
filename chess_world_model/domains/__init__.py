"""
Domains registry for Dialectical Chess World Model.
"""

from typing import Dict
from chess_world_model.ontology import Domain
from chess_world_model.domains.ai_moratorium import build_ai_moratorium_domain
from chess_world_model.domains.higher_power import build_higher_power_domain
from chess_world_model.domains.capitalism import build_capitalism_domain


def get_domain(domain_id: str) -> Domain:
    if domain_id in ("ai_moratorium", "ai", "1"):
        return build_ai_moratorium_domain()
    elif domain_id in ("higher_power", "theism", "religion", "2"):
        return build_higher_power_domain()
    elif domain_id in ("capitalism", "economy", "market", "3"):
        return build_capitalism_domain()
    else:
        raise ValueError(f"Unknown domain ID: {domain_id}")


def get_all_domains() -> Dict[str, Domain]:
    return {
        "ai_moratorium": build_ai_moratorium_domain(),
        "higher_power": build_higher_power_domain(),
        "capitalism": build_capitalism_domain(),
    }
