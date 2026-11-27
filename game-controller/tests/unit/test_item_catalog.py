"""Unit tests for config-driven ItemCatalog."""

import random

import pytest
from pydantic import ValidationError

from lms_controller.engine.items import HealSpec, ItemCatalog, ItemCatalogConfig, WeaponSpec


def test_default_item_catalog_loads_all_items(item_catalog: ItemCatalog) -> None:
    assert item_catalog.default_weapon == "fists"
    assert set(item_catalog.all_ids()) == {
        "fists",
        "small_heal",
        "knife",
        "large_heal",
        "sword",
        "axe",
        "spear",
    }

    knife = item_catalog.get_weapon("knife")
    assert isinstance(knife, WeaponSpec)
    assert knife.damage == 2
    assert knife.hit_chance == 85

    heal = item_catalog.get("large_heal")
    assert isinstance(heal, HealSpec)
    assert heal.heal_amount == 4


def test_get_weapon_rejects_healing_item(item_catalog: ItemCatalog) -> None:
    with pytest.raises(TypeError, match="not a weapon"):
        item_catalog.get_weapon("small_heal")


def test_roll_random_item_is_deterministic_and_excludes_zero_weight(
    item_catalog: ItemCatalog,
) -> None:
    draws_a = [item_catalog.roll_random_item(random.Random(123 + i)).id for i in range(50)]
    draws_b = [item_catalog.roll_random_item(random.Random(123 + i)).id for i in range(50)]
    assert draws_a == draws_b
    assert "fists" not in draws_a


def test_catalog_validation_catches_bad_configs() -> None:
    # Missing default_weapon
    with pytest.raises(ValidationError, match="default_weapon"):
        ItemCatalogConfig.model_validate(
            {
                "default_weapon": "missing",
                "items": [
                    {
                        "id": "knife",
                        "type": "weapon",
                        "damage": 2,
                        "hit_chance": 85,
                        "rarity": "common",
                        "spawn_weight": 10,
                    }
                ],
            }
        )

    # hit_chance out of range
    with pytest.raises(ValidationError):
        ItemCatalogConfig.model_validate(
            {
                "default_weapon": "fists",
                "items": [
                    {
                        "id": "fists",
                        "type": "weapon",
                        "damage": 1,
                        "hit_chance": 150,
                        "rarity": "default",
                        "spawn_weight": 1,
                    }
                ],
            }
        )
