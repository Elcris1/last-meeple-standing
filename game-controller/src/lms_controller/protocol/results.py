"""Shared result contract returned by GameEngine transitions."""

from dataclasses import dataclass, field

from lms_controller.protocol.enums import LedPattern
from lms_controller.protocol.messages import GameEvent


@dataclass(frozen=True)
class TransitionResult:
    """Side effects produced by a single GameEngine input handler call."""

    state_changed: bool = False
    events: list[GameEvent] = field(default_factory=list)
    led_updates: dict[str, LedPattern] = field(default_factory=dict)
