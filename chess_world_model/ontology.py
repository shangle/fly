"""
Ontology definitions for Dialectical Chess.
Defines premises, roles, logical representations, and Lojban structures.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class PieceRole(str, Enum):
    KING = "King"        # Teleological Thesis / Core Conclusion
    QUEEN = "Queen"      # Grand Synthesis / Meta-Framework
    ROOK = "Rook"        # Institutional / Empirical / Axiomatic Pillar
    BISHOP = "Bishop"    # Epistemological / Methodological Paradigm Axis
    KNIGHT = "Knight"    # Non-linear Counterexample / Reductio Leap / Paradox
    PAWN = "Pawn"        # Granular Empirical Lemma / Factual Claim


class Side(str, Enum):
    WHITE = "White"
    BLACK = "Black"


@dataclass
class Premise:
    id: str  # e.g. "wK", "wQ", "wR1", "wR2", "wB1", "wB2", "wN1", "wN2", "wP1".."wP8"
    name: str
    role: PieceRole
    side: Side
    file: str  # 'a' through 'h'
    natural_claim: str
    predicate_logic: str
    lojban: str
    lojban_gloss: str
    base_weight: float  # Prior epistemic soundness (0.1 - 1.0)
    vulnerabilities: List[str] = field(default_factory=list)
    targets: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role.value,
            "side": self.side.value,
            "file": self.file,
            "natural_claim": self.natural_claim,
            "predicate_logic": self.predicate_logic,
            "lojban": self.lojban,
            "lojban_gloss": self.lojban_gloss,
            "base_weight": self.base_weight,
            "vulnerabilities": self.vulnerabilities,
            "targets": self.targets,
        }


@dataclass
class Domain:
    domain_id: str
    title: str
    core_question: str
    white_thesis: str
    black_thesis: str
    premises: Dict[str, Premise] = field(default_factory=dict)

    def get_premise(self, piece_id: str) -> Optional[Premise]:
        return self.premises.get(piece_id)

    def to_dict(self) -> dict:
        return {
            "domain_id": self.domain_id,
            "title": self.title,
            "core_question": self.core_question,
            "white_thesis": self.white_thesis,
            "black_thesis": self.black_thesis,
            "premises": {k: p.to_dict() for k, p in self.premises.items()},
        }
