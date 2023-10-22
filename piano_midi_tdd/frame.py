import math

import numpy as np

from piano_midi_tdd.key import color_table
from piano_midi_tdd.key import Hand
from piano_midi_tdd.key import Key
from piano_midi_tdd.key import WHITE_KEY_NUM


def find_adjacent_pixels(numbers: list[int], threshold: int) -> list[tuple[int, int]]:
    if threshold < 0:
        raise ValueError("Threshold must be non-negative")

    if any(num < 0 for num in numbers):
        raise ValueError("Numbers in the array must be non-negative")

    groups = []
    current_group_start = None
    last_number = None
    for number in numbers:
        if last_number is None:
            current_group_start = number  # initial case
        elif number == last_number + 1:
            pass  # same group
        elif number > last_number + 1:  # detect a gap
            if last_number - current_group_start >= threshold - 1:
                groups.append((current_group_start, last_number))  # add group to groups
            current_group_start = number
        last_number = number
    if (
        current_group_start is not None and last_number is not None
    ):  # make sure both exist
        if last_number - current_group_start >= threshold - 1:
            groups.append((current_group_start, last_number))  # add last group
    return groups


def find_white_keys_in_groups(
    groups: list[tuple[int, int]], white_key_width_px: float
) -> list[int]:
    keys = []
    for start_px, end_px in groups:
        key_start = math.ceil(start_px / white_key_width_px)
        group_size_px = end_px - start_px
        num_keys = round(group_size_px / white_key_width_px)
        keys += list(range(key_start, key_start + num_keys))
    return keys


def find_pixel_indices(
    pixel_row: np.ndarray[np.uint8],
    color: tuple[np.uint8, np.uint8, np.uint8],
    threshold: int,
) -> list[int]:
    pixel_indices = []
    for idx, px in enumerate(pixel_row):
        # Calculate the absolute difference between the row and the background color
        color_difference = np.abs(px - color)

        # Check if any channel difference exceeds the threshold
        if np.any(color_difference < threshold):
            pixel_indices.append(idx)
    return pixel_indices


def detect_white_keys(
    frame: np.ndarray[np.uint8],
    hand: Hand,
    scan_line: int = 0,
) -> list[Key]:
    # Initialize a list to store non-background rows
    key_width_px = len(frame[0]) / WHITE_KEY_NUM
    threshold = 10
    pixel_indices = find_pixel_indices(frame[scan_line], hand.value, threshold)
    pixel_groups = find_adjacent_pixels(pixel_indices, 5)
    keys = find_white_keys_in_groups(pixel_groups, white_key_width_px=key_width_px)
    white_keys = [Key(num=k, hand=hand) for k in keys]
    return white_keys


def detect_keys(
    frame: np.ndarray[np.uint8], scan_line_white: int, scan_line_black: int
) -> list[Key]:
    threshold = 10
    keys: list[Key] = []
    for (hand, is_black), color in color_table.items():
        scan_line = scan_line_black if is_black else scan_line_white
        pixel_indices = find_pixel_indices(frame[scan_line], color, threshold)
        pixel_groups = find_adjacent_pixels(pixel_indices, 5)
        # TODO: find keys in groups
    return keys
