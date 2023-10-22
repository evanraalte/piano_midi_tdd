from piano_midi_tdd.key import Hand
from piano_midi_tdd.key import Key
from piano_midi_tdd.key import key_is_black


def test_key_equals() -> None:
    assert 1 != Key(num=1, hand=Hand.LEFT)
    assert Key(num=1, hand=Hand.LEFT) != Key(num=1, hand=Hand.RIGHT)
    assert Key(num=2, hand=Hand.LEFT) != Key(num=1, hand=Hand.LEFT)


def test_key_is_black() -> None:
    truth_table = [
        (0, False),  # A
        (1, True),  # A#
        (2, False),  # B
        (3, False),  # C
        (4, True),  # C#
        (5, False),  # D
        (6, True),  # D#
        (7, False),  # E
        (8, False),  # F
        (9, True),  # F#
        (10, False),  # G
        (11, True),  # G#
        (12, False),  #  A
        (13, True),  # A#
        (14, False),  # B
        (15, False),  # C
        (16, True),  # C#
    ]
    for key_num, is_black in truth_table:
        assert key_is_black(key_num) == is_black
