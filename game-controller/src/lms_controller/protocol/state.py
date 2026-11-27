"""Authoritative GameState snapshot model published on lms/game/state."""

from pydantic import BaseModel, Field

from lms_controller.protocol.enums import MEEPLE_IDS, ActionType, Phase, TurnStep

MAX_HP = 10


class PlayerState(BaseModel):
    cell: str | None = None
    hp: int = Field(default=MAX_HP, ge=0, le=MAX_HP)
    weapon: str = "fists"
    alive: bool = True
    online: bool = False
    placed: bool = False


class TurnState(BaseModel):
    player: str
    step: TurnStep = TurnStep.START
    options: list[ActionType] = Field(default_factory=list)
    targets: list[str] = Field(default_factory=list)


class GameState(BaseModel):
    """Full game snapshot serialized to lms/game/state and persisted to data/state.json."""

    rev: int = Field(default=0, ge=0)
    phase: Phase = Phase.LOBBY
    round: int = Field(default=0, ge=0)
    order: list[str] = Field(default_factory=list)
    turn: TurnState | None = None
    players: dict[str, PlayerState] = Field(
        default_factory=lambda: {mid: PlayerState() for mid in MEEPLE_IDS}
    )
    items: dict[str, str] = Field(default_factory=dict)
    fire: dict[str, int] = Field(default_factory=dict)
    lightning: list[str] = Field(default_factory=list)
    respawn: dict[str, int] = Field(default_factory=dict)
    winner: str | None = None

    def to_json_payload(self) -> str:
        return self.model_dump_json()
