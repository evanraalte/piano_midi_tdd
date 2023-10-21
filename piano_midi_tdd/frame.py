import math

import numpy as np

from piano_midi_tdd.key import WHITE_KEY_NUM
from piano_midi_tdd.key import WhiteKey


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


def find_keys_in_groups(
    groups: list[tuple[int, int]], key_width_px: float
) -> list[int]:
    keys = []
    for start_px, end_px in groups:
        key_start = math.ceil(start_px / key_width_px)
        group_size_px = end_px - start_px
        num_keys = round(group_size_px / key_width_px)
        keys += list(range(key_start, key_start + num_keys))
    return keys


def find_non_background_pixel_indices(
    pixel_row: np.ndarray[np.uint8],
    bg_color: tuple[np.uint8, np.uint8, np.uint8],
    threshold: int,
) -> list[int]:
    non_background_pixel_indices = []
    for idx, px in enumerate(pixel_row):
        # Calculate the absolute difference between the row and the background color
        color_difference = np.abs(px - bg_color)

        # Check if any channel difference exceeds the threshold
        if np.any(color_difference > threshold):
            non_background_pixel_indices.append(idx)
    return non_background_pixel_indices


def detect_white_keys(
    frame: np.ndarray[np.uint8],
    scan_line: int = 0,
    bg_color: tuple[np.uint8, np.uint8, np.uint8] = (0, 0, 0),
) -> list[int]:
    # Initialize a list to store non-background rows
    key_width_px = len(frame[0]) / WHITE_KEY_NUM
    threshold = 10
    non_background_pixel_indices = find_non_background_pixel_indices(
        frame[scan_line], bg_color, threshold
    )
    pixel_groups = find_adjacent_pixels(non_background_pixel_indices, 5)
    keys = find_keys_in_groups(pixel_groups, key_width_px=key_width_px)
    return keys
