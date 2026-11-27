"""4x4 board geometry and RFID tag UID <-> cell mapping."""

import json
from pathlib import Path

ROWS: tuple[str, ...] = ("A", "B", "C", "D")
COLS: tuple[int, ...] = (1, 2, 3, 4)

ALL_CELLS: tuple[str, ...] = tuple(f"{r}{c}" for r in ROWS for c in COLS)
ALL_CELLS_SET: frozenset[str] = frozenset(ALL_CELLS)
CORNER_CELLS: frozenset[str] = frozenset({"A1", "A4", "D1", "D4"})
NON_CORNER_CELLS: tuple[str, ...] = tuple(c for c in ALL_CELLS if c not in CORNER_CELLS)


def is_valid_cell(cell: str) -> bool:
    return cell in ALL_CELLS_SET


def is_corner(cell: str) -> bool:
    return cell in CORNER_CELLS


def cell_to_coords(cell: str) -> tuple[int, int]:
    """Convert a cell like 'B3' into zero-based (row, col) coordinates."""
    if not is_valid_cell(cell):
        raise ValueError(f"Invalid board cell: {cell!r}")
    return ROWS.index(cell[0]), int(cell[1]) - 1


def is_orthogonal_adjacent(cell_a: str, cell_b: str) -> bool:
    """Return True if cell_a and cell_b share an edge (up, down, left, right)."""
    r1, c1 = cell_to_coords(cell_a)
    r2, c2 = cell_to_coords(cell_b)
    return abs(r1 - r2) + abs(c1 - c2) == 1


def is_diagonal(cell_a: str, cell_b: str) -> bool:
    """Return True if cell_a and cell_b are diagonally adjacent."""
    r1, c1 = cell_to_coords(cell_a)
    r2, c2 = cell_to_coords(cell_b)
    return abs(r1 - r2) == 1 and abs(c1 - c2) == 1


def orthogonal_neighbors(cell: str) -> list[str]:
    """Return all valid cells orthogonally adjacent to `cell`."""
    r, c = cell_to_coords(cell)
    neighbors: list[str] = []
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(ROWS) and 0 <= nc < len(COLS):
            neighbors.append(f"{ROWS[nr]}{COLS[nc]}")
    return neighbors


class Board:
    """Bidirectional RFID tag UID <-> 4x4 cell lookup table."""

    def __init__(self, uid_to_cell: dict[str, str]) -> None:
        normalized_uid_to_cell: dict[str, str] = {}
        cell_to_uid: dict[str, str] = {}

        for raw_uid, cell in uid_to_cell.items():
            uid = raw_uid.strip().upper()
            if not uid:
                raise ValueError("RFID tag UID cannot be empty")
            if not is_valid_cell(cell):
                raise ValueError(f"Invalid cell {cell!r} for UID {uid!r}")
            if uid in normalized_uid_to_cell:
                raise ValueError(f"Duplicate RFID UID {uid!r}")
            if cell in cell_to_uid:
                raise ValueError(f"Duplicate mapping for cell {cell!r}")
            normalized_uid_to_cell[uid] = cell
            cell_to_uid[cell] = uid

        self._uid_to_cell = normalized_uid_to_cell
        self._cell_to_uid = cell_to_uid

    @classmethod
    def from_file(cls, path: Path) -> "Board":
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError(f"Expected JSON object in {path}")
        return cls(data)

    def lookup_uid(self, uid: str) -> str | None:
        """Translate a raw RFID tag UID to its board cell, or None if unknown."""
        return self._uid_to_cell.get(uid.strip().upper())

    def lookup_cell_uid(self, cell: str) -> str | None:
        """Translate a board cell to its mapped RFID tag UID (used by simulator)."""
        return self._cell_to_uid.get(cell)
