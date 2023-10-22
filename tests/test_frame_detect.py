import cv2
import numpy as np
import pytest
from hypothesis import given
from hypothesis import strategies as st

from piano_midi_tdd.frame import detect_white_keys
from piano_midi_tdd.frame import find_adjacent_pixels
from piano_midi_tdd.key import Hand
from piano_midi_tdd.key import Key
from piano_midi_tdd.key import WHITE_KEY_NUM


def whitekey_strategy():  # type: ignore
    # Define a strategy for the 'hand' field using sampled values from the Enum
    hand_strategy = st.sampled_from(Hand)

    # Define a strategy for the 'num' field (assuming it's an integer)
    num_strategy = st.integers(min_value=1, max_value=WHITE_KEY_NUM - 1)

    # Use st.builds to create instances of WhiteKey using the generated values
    return st.builds(Key, hand=hand_strategy, num=num_strategy)


@st.composite
def white_key_list_strategy(draw):  # type: ignore
    # Determine the length of the list
    list_length = draw(st.integers(min_value=0, max_value=WHITE_KEY_NUM - 1))

    unique_nums = draw(
        st.lists(
            st.integers(min_value=1, max_value=WHITE_KEY_NUM - 1),
            unique=True,
            min_size=list_length,
            max_size=list_length,
        )
    )

    white_key_list = [
        Key(draw(st.sampled_from([Hand.LEFT, Hand.RIGHT])), num) for num in unique_nums
    ]

    return white_key_list


def generate_white_keys_in_frame(
    pressed_keys: list[Key],
    bg_color: tuple[np.uint8, np.uint8, np.uint8] = (0, 0, 0),
    frame_width: int = 1920,
    frame_height: int = 50,
) -> np.ndarray[np.uint8]:
    white_key_width = frame_width / WHITE_KEY_NUM
    image = np.zeros((frame_height, frame_width, 3), np.uint8)

    # Add background color
    b, g, r = bg_color
    image[:, :, 0] = b
    image[:, :, 1] = g
    image[:, :, 2] = r

    # Add keys
    for pressed_key in pressed_keys:
        if pressed_key.num > WHITE_KEY_NUM:
            raise ValueError
        x_start = int(pressed_key.num * white_key_width)
        x_end = x_start + int(white_key_width)
        y_start = 0
        y_end = frame_height
        b, g, r = pressed_key.hand.value
        image[y_start:y_end, x_start:x_end, 0] = b
        image[y_start:y_end, x_start:x_end, 1] = g
        image[y_start:y_end, x_start:x_end, 2] = r
    return image


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
