from itertools import cycle
from typing import Optional

import numpy as np

from piano_midi_tdd.key import get_piano_key_width_px
from piano_midi_tdd.key import Key
from piano_midi_tdd.key import key_is_black
from piano_midi_tdd.key import PIANO_KEY_NUM
from piano_midi_tdd.key import WHITE_KEY_NUM


def black_keys_seen(key_num: int) -> int:
    jumps = cycle([3, 2, 3, 2, 2])
    if key_num == 0:
        return 0
    cnt = 1
    next_jump = next(jumps)
    last_seen = 1
    for k in range(2, key_num + 1):
        if k == last_seen + next_jump:
            cnt += 1
            next_jump = next(jumps)
            last_seen = k
    return cnt


def get_white_key_idx(key_num: int) -> Optional[int]:
    if key_is_black(key_num=key_num):
        return None
    return key_num - black_keys_seen(key_num)


def get_points(key: Key, frame_width_px: int) -> tuple[int, int]:
    white_key_width_px, black_key_width_px = get_piano_key_width_px(frame_width_px)
    if key_is_black(key.num):
        # look up x_start of next key (which is white by def)
        next_white_key_idx = get_white_key_idx(key.num + 1)
        if next_white_key_idx is None:
            raise ValueError
        x_start = int(next_white_key_idx * white_key_width_px)
        # and half a black key to get the  start of black
        x_start -= int(black_key_width_px / 2)
        x_end = x_start + int(black_key_width_px)
    else:
        white_key_idx = get_white_key_idx(key.num)
        if white_key_idx is None:
            raise ValueError
        x_start = int(white_key_idx * white_key_width_px)
        x_end = x_start + int(white_key_width_px)
    return (x_start, x_end)


def generate_piano_keys_in_frame(
    pressed_keys: list[Key],
    bg_color: tuple[np.uint8, np.uint8, np.uint8] = (0, 0, 0),
    frame_width: int = 1920,
    frame_height: int = 50,
) -> np.ndarray[np.uint8]:
    image = np.zeros((frame_height, frame_width, 3), np.uint8)

    # Add background color
    b, g, r = bg_color
    image[:, :, 0] = b
    image[:, :, 1] = g
    image[:, :, 2] = r

    # Add white keys
    for pressed_key in pressed_keys:
        if key_is_black(pressed_key.num):
            continue
        if pressed_key.num >= PIANO_KEY_NUM:
            raise ValueError
        x_start, x_end = get_points(pressed_key, frame_width)
        y_start = frame_height // 2
        y_end = frame_height
        b, g, r = pressed_key.color
        image[y_start:y_end, x_start:x_end, 0] = b
        image[y_start:y_end, x_start:x_end, 1] = g
        image[y_start:y_end, x_start:x_end, 2] = r

    # Add black keys
    for pressed_key in pressed_keys:
        if not key_is_black(pressed_key.num):
            continue
        if pressed_key.num >= PIANO_KEY_NUM:
            raise ValueError
        x_start, x_end = get_points(pressed_key, frame_width)
        y_start = 0
        y_end = frame_height // 2
        b, g, r = pressed_key.color
        image[y_start:y_end, x_start:x_end, 0] = b
        image[y_start:y_end, x_start:x_end, 1] = g
        image[y_start:y_end, x_start:x_end, 2] = r
    return image


def generate_white_keys_in_frame(
    pressed_keys: list[Key],
    bg_color: tuple[np.uint8, np.uint8, np.uint8] = (0, 0, 0),
    frame_width: int = 1920,
    frame_height: int = 1,
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
