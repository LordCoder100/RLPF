from dataclasses import dataclass, field 
from typing import Optional, Dict, Any
from enum import Enum 

class PredicateType(Enum):
    ASSERTION: str = "assertion"
    PERMISSION: str = "permission"
    OBLIGATION: str = "obligation"
    RESTRICTION: str = "restriction"
    RELATION: str = "relation"

@dataclass 
class Predicate:
    subj: str 
    pred: str
    obj: Any 
    confidence: float = 1.0
    source: Optional[str] = None 
    predicate_type: Optional[PredicateType] = None 
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.subj = self.subj.strip() if isinstance(self.subj, str) else self.subj 
        self.pred = self.pred.strip() if isinstance(self.pred, str) else self.pred 
        if isinstance(self.obj, str):
            self.obj = self.obj.strip()
        
        if not self.subj or not self.pred or self.obj is None:
            raise ValueError("Subject, Predicate and Object must be non-empty")
        
        if not 0 <= self.confidence <= 1:
            raise ValueError(f"Confidence score must be in range [0, 1], got {self.confidence}")
    
    def to_triple(self) -> tuple:
        return (self.subj, self.pred, self.obj)
    
    def to_dict(self) -> dict:
        return {
            "subject": self.subj, 
            "predicate": self.pred, 
            "object": self.obj, 
            "confidence": self.confidence, 
            "source": self.source, 
            "type": self.predicate_type if self.predicate_type else None, 
            "metadata": self.metadata 
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Predicate':
        pred_type = PredicateType(data["type"] if data.get("type") else None)
        return cls(
            subj=data["subject"], 
            pred=data["predicate"], 
            obj=data['obj'], 
            confidence=data.get("confidence", 1.0),
            source=data.get("source"),
            predicate_type=pred_type,
            metadata=data.get("metadata", {})
        )
    
    def is_negation(self) -> bool:
        negation_predicates: set = {"cannot", "shall_not", "should_not", "must_not", "is_not", "are_not", "does_not", "do_not", "forbids", "restricts", "was_not", "were_not", "ought_not", "might_not"}
        return self.pred in negation_predicates or self.pred.startswith("not_")
    
    def matches(self, other: 'Predicate', fuzzy: bool = False) -> bool:
        if fuzzy:
            return (
                self._fuzzy_match(self.subj, other.subj) and self.pred == other.pred and self._fuzzy_match(str(self.obj), str(other.obj))
            )
        else:
            return self.to_triple() == other.to_triple()
    
    @staticmethod
    def _fuzzy_match(s1: str, s2: str, threshold: float = 0.5) -> bool:
        s1, s2 = s1.lower().strip(), s2.lower().strip()
        
        # Normalize: remove underscores, extra spaces
        s1 = ' '.join(s1.replace('_', ' ').split())
        s2 = ' '.join(s2.replace('_', ' ').split())
        
        # Exact match after normalization
        if s1 == s2:
            return True
        
        # Check if one is substring of another (e.g., "MIT" in "MIT License")
        if s1 in s2 or s2 in s1:
            return True
        
        # Word-based similarity (Jaccard)
        words1, words2 = set(s1.split()), set(s2.split())
        if not words1 or not words2:
            return False
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        if union == 0:
            return False
            
        similarity = intersection / union
        return similarity >= threshold
    
    def __hash__(self):
        return hash(self.subj, self.pred, str(self.obj))
    
    def __eq__(self, other):
        if not isinstance(other, Predicate):
            return False 
        return self.to_triple() == other.to_triple()
    
    def __repr__(self):
        conf_str: str = f", conf={self.confidence:.2f}" if self.confidence < 1.0 else ""
        return f"Predicate({self.subj}, {self.pred}, {self.obj}{conf_str})"


if __name__ == "__main__":
    # Basic predicate
    p1 = Predicate(
        subj="MIT License",
        pred="allows",
        obj="commercial_use"
    )
    print(p1)  # Predicate(MIT License, allows, commercial_use)
    
    # With metadata
    p2 = Predicate(
        subj="Python",
        pred="created_by",
        obj="Guido van Rossum",
        confidence=0.99,
        source="wikipedia",
        predicate_type=PredicateType.ASSERTION,
        metadata={"year": 1991}
    )
    print(p2.to_dict())
    
    # Negation
    p3 = Predicate("GPL", "cannot", "close_source")
    print(f"Is negation: {p3.is_negation()}")  # True
    
    # Fuzzy matching
    p4 = Predicate("MIT License", "allows", "commercial use")
    p5 = Predicate("MIT", "allows", "commercial_use")
    print(f"Fuzzy match: {p4.matches(p5, fuzzy=True)}")  # True
    print(f"Exact match: {p4.matches(p5, fuzzy=False)}")







