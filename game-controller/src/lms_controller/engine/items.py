"""Config-driven item specifications and weighted loot catalog."""

import random
from pathlib import Path
from typing import Annotated, Literal

from pydantic import BaseModel, Field, model_validator


class WeaponSpec(BaseModel, frozen=True):
    id: str = Field(min_length=1)
    type: Literal["weapon"] = "weapon"
    damage: int = Field(ge=1)
    hit_chance: int = Field(ge=1, le=100)
    rarity: str = Field(min_length=1)
    spawn_weight: int = Field(ge=0)


class HealSpec(BaseModel, frozen=True):
    id: str = Field(min_length=1)
    type: Literal["healing"] = "healing"
    heal_amount: int = Field(ge=1)
    rarity: str = Field(min_length=1)
    spawn_weight: int = Field(ge=0)


ItemSpec = Annotated[WeaponSpec | HealSpec, Field(discriminator="type")]


class ItemCatalogConfig(BaseModel):
    """Schema for config/items.json."""

    default_weapon: str = Field(min_length=1)
    items: list[ItemSpec] = Field(min_length=1)

    @model_validator(mode="after")
    def _validate_catalog(self) -> "ItemCatalogConfig":
        by_id: dict[str, ItemSpec] = {}
        for item in self.items:
            if item.id in by_id:
                raise ValueError(f"Duplicate item id: {item.id!r}")
            by_id[item.id] = item

        default = by_id.get(self.default_weapon)
        if default is None:
            raise ValueError(f"default_weapon {self.default_weapon!r} not found in items")
        if not isinstance(default, WeaponSpec):
            raise ValueError(f"default_weapon {self.default_weapon!r} must be a weapon")

        if not any(item.spawn_weight > 0 for item in self.items):
            raise ValueError("At least one item must have spawn_weight > 0")

        return self


class ItemCatalog:
    """Immutable item lookup and weighted random draw registry."""

    def __init__(self, config: ItemCatalogConfig) -> None:
        self._default_weapon = config.default_weapon
        self._items: dict[str, ItemSpec] = {item.id: item for item in config.items}
        self._spawnable: list[ItemSpec] = [item for item in config.items if item.spawn_weight > 0]
        self._weights: list[int] = [item.spawn_weight for item in self._spawnable]

    @classmethod
    def from_file(cls, path: Path) -> "ItemCatalog":
        config = ItemCatalogConfig.model_validate_json(path.read_text(encoding="utf-8"))
        return cls(config)

    @property
    def default_weapon(self) -> str:
        return self._default_weapon

    def all_ids(self) -> tuple[str, ...]:
        return tuple(self._items.keys())

    def get(self, item_id: str) -> ItemSpec:
        return self._items[item_id]

    def get_weapon(self, weapon_id: str) -> WeaponSpec:
        item = self._items[weapon_id]
        if not isinstance(item, WeaponSpec):
            raise TypeError(f"Item {weapon_id!r} is not a weapon")
        return item

    def roll_random_item(self, rng: random.Random) -> ItemSpec:
        """Draw a random spawnable item using configured spawn weights."""
        return rng.choices(self._spawnable, weights=self._weights, k=1)[0]
