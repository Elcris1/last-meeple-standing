"""Unit tests for 4x4 board geometry and RFID UID mapping."""

import pytest

from lms_controller.engine.board import (
    ALL_CELLS,
    CORNER_CELLS,
    NON_CORNER_CELLS,
    Board,
    cell_to_coords,
    is_corner,
    is_diagonal,
    is_orthogonal_adjacent,
    is_valid_cell,
    orthogonal_neighbors,
)


def test_board_constants() -> None:
    assert len(ALL_CELLS) == 16
    assert set(CORNER_CELLS) == {"A1", "A4", "D1", "D4"}
    assert len(NON_CORNER_CELLS) == 12
    assert is_valid_cell("B3") is True
    assert is_valid_cell("E1") is False
    assert is_corner("A1") is True
    assert is_corner("B2") is False


def test_coordinates_and_adjacency() -> None:
    assert cell_to_coords("A1") == (0, 0)
    assert cell_to_coords("D4") == (3, 3)

    assert is_orthogonal_adjacent("B2", "B3") is True
    assert is_orthogonal_adjacent("B2", "A2") is True
    assert is_orthogonal_adjacent("B2", "C3") is False
    assert is_orthogonal_adjacent("B2", "B4") is False
    assert is_orthogonal_adjacent("B2", "B2") is False

    assert is_diagonal("B2", "C3") is True
    assert is_diagonal("B2", "A1") is True
    assert is_diagonal("B2", "B3") is False
    assert is_diagonal("A1", "C3") is False


def test_orthogonal_neighbors() -> None:
    assert set(orthogonal_neighbors("A1")) == {"A2", "B1"}
    assert set(orthogonal_neighbors("B2")) == {"A2", "C2", "B1", "B3"}


def test_board_uid_lookup_from_config(board: Board) -> None:
    assert board.lookup_uid("04000001") == "A1"
    assert board.lookup_uid("04000016") == "D4"
    assert board.lookup_uid("  04000001  ") == "A1"
    assert board.lookup_uid("UNKNOWN") is None
    assert board.lookup_cell_uid("A1") == "04000001"


def test_board_rejects_invalid_or_duplicate_mappings() -> None:
    with pytest.raises(ValueError, match="Invalid cell"):
        Board({"04AA": "Z9"})

    with pytest.raises(ValueError, match="Duplicate mapping"):
        Board({"04AA": "A1", "04BB": "A1"})
