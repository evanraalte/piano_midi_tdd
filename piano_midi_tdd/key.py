from dataclasses import dataclass
from enum import Enum
from typing import Any

WHITE_KEY_NUM = 52


class Hand(Enum):
    LEFT = (202, 159, 123)
    RIGHT = (84, 224, 150)


@dataclass
class WhiteKey:
    hand: Hand
    num: int

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, WhiteKey):
            return False
        return self.hand == other.hand and self.num == other.num

    def __hash__(self) -> int:
        return hash((self.num, self.hand))
