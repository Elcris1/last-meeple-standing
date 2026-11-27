"""Shared pytest fixtures for unit and integration tests."""

import random
from pathlib import Path

import pytest

from lms_controller.engine.board import Board
from lms_controller.engine.items import ItemCatalog

CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"


@pytest.fixture
def rng() -> random.Random:
    """Deterministic RNG for reproducible unit tests."""
    return random.Random(42)


@pytest.fixture
def board() -> Board:
    """Default 4x4 board loaded from config/board.json."""
    return Board.from_file(CONFIG_DIR / "board.json")


@pytest.fixture
def item_catalog() -> ItemCatalog:
    """Default item catalog loaded from config/items.json."""
    return ItemCatalog.from_file(CONFIG_DIR / "items.json")
