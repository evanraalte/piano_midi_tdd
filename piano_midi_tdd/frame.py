import math

import numpy as np

WHITE_KEY_NUM = 52


def detect_white_keys(
    frame: np.ndarray[np.uint8],
    scan_line: int = 0,
    bg_color: tuple[np.uint8, np.uint8, np.uint8] = (0, 0, 0),
) -> list[int]:
    # Initialize a list to store non-background rows
    key_width = len(frame[0]) / WHITE_KEY_NUM
    non_background_rows = []
    threshold = 10
    # Iterate through the rows of the image
    for idx, row in enumerate(frame[scan_line]):
        # Calculate the absolute difference between the row and the background color
        color_difference = np.abs(row - bg_color)

        # Check if any channel difference exceeds the threshold
        if np.any(color_difference > threshold):
            non_background_rows.append(idx)
    idx_min = min(non_background_rows)
    idx_max = max(non_background_rows)
    key = math.ceil(idx_min / key_width)
    return [key]
