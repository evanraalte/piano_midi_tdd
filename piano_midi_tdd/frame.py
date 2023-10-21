import math

import numpy as np

WHITE_KEY_NUM = 52


def find_adjacent_groups(numbers: list[int], threshold: int) -> list[tuple[int, int]]:
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


def detect_white_keys(
    frame: np.ndarray[np.uint8],
    scan_line: int = 0,
    bg_color: tuple[np.uint8, np.uint8, np.uint8] = (0, 0, 0),
) -> list[int]:
    # Initialize a list to store non-background rows
    key_width_px = len(frame[0]) / WHITE_KEY_NUM
    non_background_rows = []
    threshold = 10
    # Iterate through the rows of the image
    for idx, row in enumerate(frame[scan_line]):
        # Calculate the absolute difference between the row and the background color
        color_difference = np.abs(row - bg_color)

        # Check if any channel difference exceeds the threshold
        if np.any(color_difference > threshold):
            non_background_rows.append(idx)

    groups = find_adjacent_groups(non_background_rows, 5)
    keys = []
    for start_px, end_px in groups:
        key_start = math.ceil(start_px / key_width_px)
        group_size_px = end_px - start_px
        num_keys = round(group_size_px / key_width_px)
        keys += list(range(key_start, key_start + num_keys))
    return keys
