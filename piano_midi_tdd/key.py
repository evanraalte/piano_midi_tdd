from dataclasses import dataclass
from enum import Enum, auto
from typing import Any

WHITE_KEY_NUM = 52

class Hand(Enum):
    LEFT = auto()
    RIGHT = auto()

@dataclass
class WhiteKey:
    hand: Hand
    num: int
    
    def __eq__(self, other : Any) -> bool:
        if not isinstance(other, WhiteKey):
            if isinstance(other, int) and self.num == other:
                return True
            return False
        return self.hand == other.hand and self.num == other.num

    def __hash__(self) -> int:
        return hash(self.num)
