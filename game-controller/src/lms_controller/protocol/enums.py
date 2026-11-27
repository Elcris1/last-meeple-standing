"""Shared string enums matching docs/protocol.md."""

from enum import StrEnum

MEEPLE_IDS: tuple[str, ...] = ("m1", "m2", "m3", "m4")


class Phase(StrEnum):
    LOBBY = "lobby"
    PLAYING = "playing"
    PAUSED = "paused"
    FINISHED = "finished"


class TurnStep(StrEnum):
    START = "start"
    MOVING = "moving"
    MOVED = "moved"


class ActionType(StrEnum):
    MOVE = "move"
    CANCEL_MOVE = "cancel_move"
    ATTACK = "attack"
    PASS = "pass"
    START = "start"
    NEW_GAME = "new_game"


class LedPattern(StrEnum):
    OFF = "off"
    IDLE = "idle"
    ACTIVE = "active"
    ERROR = "error"
    DANGER = "danger"
    DEAD = "dead"
    WINNER = "winner"


class EventType(StrEnum):
    GAME_START = "game_start"
    TURN_START = "turn_start"
    MOVE_OK = "move_ok"
    MOVE_INVALID = "move_invalid"
    ACTION_REJECTED = "action_rejected"
    PICKUP = "pickup"
    ATTACK_HIT = "attack_hit"
    ATTACK_MISS = "attack_miss"
    PASS = "pass"
    LIGHTNING_WARNING = "lightning_warning"
    LIGHTNING_STRIKE = "lightning_strike"
    FIRE_DAMAGE = "fire_damage"
    ELIMINATED = "eliminated"
    PAUSED = "paused"
    RESUMED = "resumed"
    GAME_OVER = "game_over"


class MoveInvalidReason(StrEnum):
    DIAGONAL = "diagonal"
    NOT_ADJACENT = "not_adjacent"
    OCCUPIED = "occupied"
    SECOND_MOVE = "second_move"
    NOT_YOUR_TURN = "not_your_turn"
    MOVE_NOT_SELECTED = "move_not_selected"
    UNKNOWN_TAG = "unknown_tag"


class ActionRejectedReason(StrEnum):
    STALE = "stale"
    NOT_ALLOWED = "not_allowed"
    INVALID_TARGET = "invalid_target"


class EliminationCause(StrEnum):
    COMBAT = "combat"
    LIGHTNING = "lightning"
    FIRE = "fire"


class PauseReason(StrEnum):
    DEVICE_OFFLINE = "device_offline"
    ADMIN = "admin"


class GameOverReason(StrEnum):
    LAST_ALIVE = "last_alive"
    ROUND_LIMIT = "round_limit"


class AdminCmdType(StrEnum):
    START = "start"
    RESET = "reset"
    PAUSE = "pause"
    RESUME = "resume"
