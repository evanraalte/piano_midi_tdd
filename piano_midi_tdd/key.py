from dataclasses import dataclass
from enum import Enum
from typing import Any

import numpy as np

WHITE_KEY_NUM = 52
PIANO_KEY_NUM = 88


class Hand(Enum):
    LEFT = (202, 159, 123)
    RIGHT = (84, 224, 150)


def key_is_black(key_num: int) -> bool:
    black = [1, 3, 6, 8, 10]
    key_num += 9
    return (key_num % 12) in black


color_table = {
    (Hand.LEFT, False): (202, 159, 123),
    (Hand.LEFT, True): (164, 96, 49),
    (Hand.RIGHT, False): (84, 224, 150),
    (Hand.RIGHT, True): (19, 144, 78),
}


def get_piano_key_width_px(frame_width: int) -> tuple[float, float]:
    white_key_width = frame_width / 52
    black_key_width = white_key_width * (7 / 12)
    return white_key_width, black_key_width


@dataclass
class Key:
    hand: Hand
    num: int

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Key):
            return False
        return self.hand == other.hand and self.num == other.num

    def __hash__(self) -> int:
        return hash((self.num, self.hand))

    @property
    def color(self) -> tuple[np.uint8, np.uint8, np.uint8]:
        return color_table[self.hand, key_is_black(self.num)]
