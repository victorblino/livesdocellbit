from core.stream_state import StreamState


def test_default_state_values():
    state = StreamState()

    assert state.online is False
    assert state.current_game == ''
    assert state.stream_title == ''


def test_update_from_update_changes_state():
    state = StreamState()
    update = {
        'online': True,
        'current_game': 'Umineko When They Cry',
        'stream_title': 'The Golden Witch is Real'
    }

    state.update_from_update(update)

    assert state.online is True
    assert state.current_game == 'Umineko When They Cry'
    assert state.stream_title == 'The Golden Witch is Real'


def test_reset_for_offline_sets_online_false():
    state = StreamState(online=True, current_game='Umineko When They Cry', stream_title='The Golden Witch is Real')

    state.reset_for_offline()

    assert state.online is False
    assert state.current_game == 'Umineko When They Cry'
    assert state.stream_title == 'The Golden Witch is Real'
