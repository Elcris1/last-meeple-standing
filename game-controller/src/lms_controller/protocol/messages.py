"""Pydantic v2 models for all MQTT input and output payloads."""

from pydantic import BaseModel, ConfigDict, Field

from lms_controller.protocol.enums import ActionType, AdminCmdType, EventType, LedPattern

# --- Inputs (devices / frontend -> controller) ---


class TagMessage(BaseModel):
    """Payload for lms/meeple/{id}/tag."""

    seq: int = Field(ge=0)
    uid: str | None = None
    ts: int | None = None


class BaseActionMessage(BaseModel):
    """Payload for lms/base/action."""

    seq: int = Field(ge=0)
    action: ActionType
    target: str | None = None
    seen_rev: int = Field(ge=0)
    ts: int | None = None


class StatusMessage(BaseModel):
    """Payload for lms/meeple/{id}/status and lms/base/status (including LWT)."""

    online: bool
    fw: str | None = None
    ip: str | None = None
    rssi: int | None = None


class AdminCmdMessage(BaseModel):
    """Payload for lms/game/cmd."""

    cmd: AdminCmdType


# --- Outputs (controller -> devices / frontend) ---


class LedCommandMessage(BaseModel):
    """Payload for lms/meeple/{id}/led."""

    rev: int = Field(ge=0)
    pattern: LedPattern


class ControllerStatusMessage(BaseModel):
    """Payload for lms/controller/status (including LWT)."""

    online: bool


class RequestRef(BaseModel):
    """Echoes the originating device message for logical request->reaction matching."""

    model_config = ConfigDict(populate_by_name=True)

    from_device: str = Field(alias="from")
    seq: int = Field(ge=0)


class GameEvent(BaseModel):
    """Transient event published on lms/game/event.

    Event-specific fields (e.g. `by`, `on`, `dmg`, `reason`) are stored as flat JSON keys
    matching docs/protocol.md.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    rev: int = Field(ge=0)
    type: EventType
    req: RequestRef | None = None

    def to_json_payload(self) -> str:
        return self.model_dump_json(exclude_none=True, by_alias=True)
