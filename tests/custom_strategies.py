from hypothesis import strategies as st

from piano_midi_tdd.key import Hand
from piano_midi_tdd.key import Key
from piano_midi_tdd.key import PIANO_KEY_NUM
from piano_midi_tdd.key import WHITE_KEY_NUM


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


@st.composite
def piano_key_list_strategy(draw):  # type: ignore
    # Determine the length of the list
    list_length = draw(st.integers(min_value=0, max_value=PIANO_KEY_NUM - 1))

    unique_nums = draw(
        st.lists(
            st.integers(min_value=1, max_value=PIANO_KEY_NUM - 1),
            unique=True,
            min_size=list_length,
            max_size=list_length,
        )
    )

    key_list = [
        Key(draw(st.sampled_from([Hand.LEFT, Hand.RIGHT])), num) for num in unique_nums
    ]

    return key_list
