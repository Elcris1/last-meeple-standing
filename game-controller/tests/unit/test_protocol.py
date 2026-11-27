"""Unit tests for protocol models, serialization, and topic routing."""

import json

import pytest
from pydantic import ValidationError

from lms_controller.protocol import (
    MEEPLE_IDS,
    ActionType,
    AdminCmdMessage,
    AdminCmdRoute,
    AdminCmdType,
    BaseActionMessage,
    BaseActionRoute,
    DeviceStatusRoute,
    EventType,
    GameEvent,
    GameState,
    LedCommandMessage,
    LedPattern,
    MeepleTagRoute,
    Phase,
    RequestRef,
    StatusMessage,
    TagMessage,
    TransitionResult,
    input_subscription_topics,
    meeple_led_topic,
    parse_topic,
)


def test_default_game_state_initializes_four_players() -> None:
    state = GameState()
    assert state.phase == Phase.LOBBY
    assert state.rev == 0
    assert tuple(state.players.keys()) == MEEPLE_IDS
    for player in state.players.values():
        assert player.hp == 10
        assert player.weapon == "fists"
        assert player.alive is True
        assert player.online is False
        assert player.placed is False


def test_tag_message_placed_and_removed() -> None:
    placed = TagMessage.model_validate_json('{"seq": 17, "uid": "04A1B2C3", "ts": 51234}')
    assert placed.seq == 17
    assert placed.uid == "04A1B2C3"

    removed = TagMessage.model_validate_json('{"seq": 18, "uid": null, "ts": 53010}')
    assert removed.seq == 18
    assert removed.uid is None


def test_base_action_rejects_invalid_action() -> None:
    with pytest.raises(ValidationError):
        BaseActionMessage.model_validate_json('{"seq": 1, "action": "fly", "seen_rev": 0}')


def test_base_action_valid_attack() -> None:
    msg = BaseActionMessage.model_validate_json(
        '{"seq": 5, "action": "attack", "target": "m1", "seen_rev": 42, "ts": 120400}'
    )
    assert msg.action == ActionType.ATTACK
    assert msg.target == "m1"
    assert msg.seen_rev == 42


def test_status_and_admin_messages() -> None:
    status = StatusMessage.model_validate_json('{"online": false}')
    assert status.online is False
    cmd = AdminCmdMessage.model_validate_json('{"cmd": "reset"}')
    assert cmd.cmd == AdminCmdType.RESET


def test_game_event_flat_serialization_with_request_ref() -> None:
    event = GameEvent(
        rev=43,
        type=EventType.ATTACK_HIT,
        req=RequestRef(from_device="base", seq=5),
        by="m2",
        on="m1",
        weapon="knife",
        dmg=2,
        hp=5,
    )
    raw = json.loads(event.to_json_payload())
    assert raw == {
        "rev": 43,
        "type": "attack_hit",
        "req": {"from": "base", "seq": 5},
        "by": "m2",
        "on": "m1",
        "weapon": "knife",
        "dmg": 2,
        "hp": 5,
    }


def test_led_command_and_transition_result() -> None:
    led = LedCommandMessage(rev=42, pattern=LedPattern.ACTIVE)
    assert json.loads(led.model_dump_json()) == {"rev": 42, "pattern": "active"}

    res = TransitionResult(state_changed=True, led_updates={"m2": LedPattern.ACTIVE})
    assert res.state_changed is True
    assert res.events == []
    assert res.led_updates == {"m2": LedPattern.ACTIVE}


@pytest.mark.parametrize(
    ("topic", "expected"),
    [
        ("lms/meeple/m1/tag", MeepleTagRoute(meeple_id="m1")),
        ("lms/meeple/m4/tag", MeepleTagRoute(meeple_id="m4")),
        ("lms/meeple/m2/status", DeviceStatusRoute(device_id="m2")),
        ("lms/base/action", BaseActionRoute()),
        ("lms/base/status", DeviceStatusRoute(device_id="base")),
        ("lms/game/cmd", AdminCmdRoute()),
        ("lms/meeple/m5/tag", None),
        ("lms/game/state", None),
        ("other/topic", None),
    ],
)
def test_parse_topic(topic: str, expected: object) -> None:
    assert parse_topic(topic) == expected


def test_topic_helpers_and_qos2_subscriptions() -> None:
    assert meeple_led_topic("m3") == "lms/meeple/m3/led"
    subs = input_subscription_topics()
    assert all(qos == 2 for _, qos in subs)
    assert len(subs) == 5
