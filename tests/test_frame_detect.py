import cv2
import numpy as np
from hypothesis import given
from hypothesis import strategies as st

from piano_midi_tdd.frame import detect_white_keys
from piano_midi_tdd.frame import WHITE_KEY_NUM


def generate_white_keys_in_frame(
    pressed_keys: list[int],
    bg_color: tuple[np.uint8, np.uint8, np.uint8] = (0, 0, 0),
    pressed_key_color: tuple[np.uint8, np.uint8, np.uint8] = (83, 224, 150),
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
        if pressed_key > WHITE_KEY_NUM:
            raise ValueError
        x_start = int(pressed_key * white_key_width)
        x_end = x_start + int(white_key_width)
        y_start = 0
        y_end = frame_height
        b, g, r = pressed_key_color
        image[y_start:y_end, x_start:x_end, 0] = b
        image[y_start:y_end, x_start:x_end, 1] = g
        image[y_start:y_end, x_start:x_end, 2] = r
    return image


@given(st.integers(min_value=0, max_value=WHITE_KEY_NUM - 1))
def test_can_detect_a_white_key_press_in_frame(key_num: int) -> None:
    bg_color = (43, 42, 43)
    frame = generate_white_keys_in_frame(pressed_keys=[key_num], bg_color=bg_color)
    assert detect_white_keys(frame, bg_color=bg_color) == [key_num]
