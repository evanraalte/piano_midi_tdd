from piano_midi_tdd.key import Hand, WhiteKey


def test_key_equals():
    assert 1 != WhiteKey(num=1,hand=Hand.LEFT)
    assert WhiteKey(num=1,hand=Hand.LEFT) != WhiteKey(num=1,hand=Hand.RIGHT)
    assert WhiteKey(num=2,hand=Hand.LEFT) != WhiteKey(num=1,hand=Hand.LEFT)
