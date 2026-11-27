"""MQTT topic constants, builders, and parser for the lms/ topic tree."""

import re
from dataclasses import dataclass

ROOT = "lms"
QOS_GAME = 2
QOS_LOG = 0

TOPIC_GAME_STATE = f"{ROOT}/game/state"
TOPIC_GAME_EVENT = f"{ROOT}/game/event"
TOPIC_GAME_CMD = f"{ROOT}/game/cmd"
TOPIC_BASE_ACTION = f"{ROOT}/base/action"
TOPIC_BASE_STATUS = f"{ROOT}/base/status"
TOPIC_CONTROLLER_STATUS = f"{ROOT}/controller/status"

_MEEPLE_TAG_RE = re.compile(rf"^{ROOT}/meeple/(m[1-4])/tag$")
_MEEPLE_STATUS_RE = re.compile(rf"^{ROOT}/meeple/(m[1-4])/status$")


def meeple_tag_topic(meeple_id: str) -> str:
    return f"{ROOT}/meeple/{meeple_id}/tag"


def meeple_led_topic(meeple_id: str) -> str:
    return f"{ROOT}/meeple/{meeple_id}/led"


def meeple_status_topic(meeple_id: str) -> str:
    return f"{ROOT}/meeple/{meeple_id}/status"


def meeple_log_topic(meeple_id: str) -> str:
    return f"{ROOT}/meeple/{meeple_id}/log"


def game_state_topic() -> str:
    return TOPIC_GAME_STATE


def game_event_topic() -> str:
    return TOPIC_GAME_EVENT


def controller_status_topic() -> str:
    return TOPIC_CONTROLLER_STATUS


def input_subscription_topics() -> list[tuple[str, int]]:
    """Topics the controller subscribes to (all with QoS 2)."""
    return [
        (f"{ROOT}/meeple/+/tag", QOS_GAME),
        (f"{ROOT}/meeple/+/status", QOS_GAME),
        (TOPIC_BASE_ACTION, QOS_GAME),
        (TOPIC_BASE_STATUS, QOS_GAME),
        (TOPIC_GAME_CMD, QOS_GAME),
    ]


@dataclass(frozen=True)
class MeepleTagRoute:
    meeple_id: str


@dataclass(frozen=True)
class BaseActionRoute:
    pass


@dataclass(frozen=True)
class DeviceStatusRoute:
    device_id: str  # "m1".."m4" or "base"


@dataclass(frozen=True)
class AdminCmdRoute:
    pass


TopicRoute = MeepleTagRoute | BaseActionRoute | DeviceStatusRoute | AdminCmdRoute


def parse_topic(topic: str) -> TopicRoute | None:
    """Parse an incoming MQTT topic into a typed route, or None if unrecognized."""
    if match := _MEEPLE_TAG_RE.match(topic):
        return MeepleTagRoute(meeple_id=match.group(1))
    if match := _MEEPLE_STATUS_RE.match(topic):
        return DeviceStatusRoute(device_id=match.group(1))
    if topic == TOPIC_BASE_ACTION:
        return BaseActionRoute()
    if topic == TOPIC_BASE_STATUS:
        return DeviceStatusRoute(device_id="base")
    if topic == TOPIC_GAME_CMD:
        return AdminCmdRoute()
    return None
