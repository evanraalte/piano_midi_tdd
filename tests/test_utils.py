import pytest
from hypothesis import given
from hypothesis import strategies as st

from piano_midi_tdd.key import Hand
from piano_midi_tdd.key import Key
from piano_midi_tdd.key import key_is_black
from piano_midi_tdd.key import PIANO_KEY_NUM
from piano_midi_tdd.key import WHITE_KEY_NUM
from tests.utils import black_keys_seen
from tests.utils import get_points
from tests.utils import get_white_key_idx


@given(key_num=st.integers(min_value=0, max_value=PIANO_KEY_NUM - 1))
def test_key_location_not_outside_frame(key_num: int) -> None:
    frame_width_px = 1920
    start, end = get_points(
        Key(hand=Hand.LEFT, num=key_num), frame_width_px=frame_width_px
    )
    assert start < frame_width_px
    assert end < frame_width_px


def test_nth_white_key_range() -> None:
    last_white_key_idx = -1
    for key_num in range(PIANO_KEY_NUM):
        white_key_idx = get_white_key_idx(key_num)
        if white_key_idx is not None:
            print(f"{key_num=} {white_key_idx=}")
            assert white_key_idx == last_white_key_idx + 1
            assert white_key_idx < WHITE_KEY_NUM
            last_white_key_idx = white_key_idx
        else:
            assert key_is_black(key_num)


def test_black_seen_increment_by_one() -> None:
    black_seen_prev = 0
    for key_num in range(PIANO_KEY_NUM):
        if key_is_black(key_num=key_num):
            black_seen = black_keys_seen(key_num)
            print(f"{key_num=} {black_seen=}")
            assert black_seen == black_seen_prev + 1
            black_seen_prev = black_seen


def test_nth_white_key() -> None:
    truth_table = [
        (0, 0),
        (1, None),
        (2, 1),
        (3, 2),
        (4, None),
        (5, 3),
        (6, None),
        (7, 4),
        (8, 5),
        (9, None),
        (10, 6),
        (11, None),
        (12, 7),
        (13, None),
        (14, 8),
        (15, 9),
    ]
    for key_num, value in truth_table:
        assert get_white_key_idx(key_num) == value


def test_blacks_seen() -> None:
    truth_table = {0: 0, 1: 1, 4: 2, 6: 3, 9: 4, 11: 5, 13: 6}
    for key_num, expected_black_keys in truth_table.items():
        assert black_keys_seen(key_num) == expected_black_keys
