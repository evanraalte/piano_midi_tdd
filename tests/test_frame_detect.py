import cv2
import numpy as np
import pytest
from hypothesis import given

from piano_midi_tdd.frame import detect_white_keys
from piano_midi_tdd.frame import find_adjacent_pixels
from piano_midi_tdd.key import Hand
from piano_midi_tdd.key import Key
from tests.custom_strategies import piano_key_list_strategy
from tests.custom_strategies import white_key_list_strategy
from tests.utils import generate_piano_keys_in_frame
from tests.utils import generate_white_keys_in_frame


@pytest.mark.skip()
@given(piano_key_list_strategy())
def test_can_detect_multiple_key_presses_in_frame(
    keys: list[Key],
) -> None:
    BG_COLOR = (43, 42, 43)
    frame = generate_piano_keys_in_frame(pressed_keys=keys, bg_color=BG_COLOR)
    cv2.imshow("", frame)
    cv2.wait
    pass


@given(white_key_list_strategy())
def test_can_detect_multiple_white_key_press_in_frame(
    white_keys: list[Key],
) -> None:
    BG_COLOR = (43, 42, 43)
    frame = generate_white_keys_in_frame(pressed_keys=white_keys, bg_color=BG_COLOR)
    detected_keys = detect_white_keys(frame=frame, hand=Hand.LEFT)
    detected_keys += detect_white_keys(frame=frame, hand=Hand.RIGHT)
    assert set(detected_keys) == set(white_keys)


def test_adjacent_groups() -> None:
    # Test when there are multiple adjacent groups
    numbers = [1, 2, 3, 5, 6, 7, 8, 10, 11]
    assert find_adjacent_pixels(numbers, threshold=2) == [(1, 3), (5, 8), (10, 11)]

    # Test with a threshold of 2
    numbers = [1, 2, 4, 5, 9, 10]
    assert find_adjacent_pixels(numbers, threshold=2) == [(1, 2), (4, 5), (9, 10)]

    # Test with a threshold of 3
    numbers = [1, 2, 5, 6, 10, 11, 12]
    assert find_adjacent_pixels(numbers, threshold=3) == [(10, 12)]

    # Test when the list contains a single number
    numbers = [1]
    assert find_adjacent_pixels(numbers, threshold=1) == [(1, 1)]

    # Test with negative numbers (should raise a ValueError)
    with pytest.raises(ValueError):
        numbers = [-2, -1, 0, 1, 3, 4]
        find_adjacent_pixels(numbers, threshold=1)

    # Test with negative threshold (should raise a ValueError)
    with pytest.raises(ValueError):
        numbers = [1, 3, 5, 9, 10, 11, 15, 20]
        find_adjacent_pixels(numbers, threshold=-2)

    numbers = [0, 1, 2]
    assert find_adjacent_pixels(numbers, 2) == [(0, 2)]
