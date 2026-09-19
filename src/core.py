"""Хайлтын алгоритмуудын дундын цөм.

Энд Grid World орчин, хайлтын мод дахь Node, үр дүнгийн бүтэц болон бүх
алгоритм (BFS, DFS, GBFS, A*) хуваалцах `Search` хийсвэр класс байрлана.
Дэд класс бүр зөвхөн frontier-ээ хэрхэн зохион байгуулахаа тодорхойлно.
"""

from __future__ import annotations

import sys
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from math import sqrt
from typing import Iterable, Iterator, Optional

State = tuple[int, int]

WALL, FREE, START, GOAL = "#", ".", "S", "G"

# (мөрийн шилжилт, баганын шилжилт, үйлдлийн нэр)
ORTHOGONAL: tuple[tuple[int, int, str], ...] = (
    (-1, 0, "U"),
    (0, 1, "R"),
    (1, 0, "D"),
    (0, -1, "L"),
)
DIAGONAL: tuple[tuple[int, int, str], ...] = (
    (-1, 1, "UR"),
    (1, 1, "DR"),
    (1, -1, "DL"),
    (-1, -1, "UL"),
)


def use_utf8_output() -> None:
    """Гаралтыг UTF-8 болгоно.

    Windows-ийн консол анхдагчаар cp1252 кодчилол ашигладаг тул кирилл үсэг
    хэвлэхэд `UnicodeEncodeError` өгдөг (ялангуяа гаралтыг файл эсвэл өөр
    програм руу дамжуулахад). Скрипт бүрийн `main()` үүнийг эхэнд дуудна.
    """
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        encoding = (getattr(stream, "encoding", "") or "").lower()
        if reconfigure is not None and encoding.replace("-", "") != "utf8":
            reconfigure(encoding="utf-8", errors="replace")


@dataclass(slots=True)
class Node:
    """Хайлтын мод дахь нэг зангилаа."""

    state: State
    parent: Optional["Node"] = None
    action: str = ""
    g: float = 0.0          # эхлэлээс энэ зангилаа хүртэлх бодит зардал
    depth: int = 0

    def path(self) -> list[State]:
        """Эхлэлээс энэ зангилаа хүртэлх замыг эцэг рүү ухрааж сэргээнэ."""
        node: Optional[Node] = self
        states: list[State] = []
        while node is not None:
            states.append(node.state)
            node = node.parent
        states.reverse()
        return states


@dataclass(slots=True)
class SearchResult:
    """Нэг хайлтын гүйцэтгэлийн хэмжигдэхүүнүүд (benchmark-д ашиглана)."""

    algorithm: str
    found: bool
    path: list[State] = field(default_factory=list)
    cost: float = 0.0
    expanded: int = 0          # frontier-ээс гарган дэлгэсэн зангилааны тоо
    generated: int = 0         # үүсгэсэн хүүхэд зангилааны тоо
    max_frontier: int = 0      # frontier-ийн хамгийн их хэмжээ (санах ой)
    elapsed: float = 0.0       # секунд

    @property
    def path_length(self) -> int:
        """Замын нүдний тоо (эхлэл ба зорилгыг оруулаад)."""
        return len(self.path)

    def as_row(self) -> dict[str, object]:
        """pandas.DataFrame-д шууд хийхэд тохиромжтой мөр."""
        return {
            "algorithm": self.algorithm,
            "found": self.found,
            "cost": round(self.cost, 4),
            "path_length": self.path_length,
            "expanded": self.expanded,
            "generated": self.generated,
            "max_frontier": self.max_frontier,
            "time_ms": round(self.elapsed * 1000, 3),
        }

    def summary(self) -> str:
        if not self.found:
            return f"{self.algorithm}: зам олдсонгүй ({self.expanded} зангилаа дэлгэв)"
        return (
            f"{self.algorithm}: зардал={self.cost:.2f} "
            f"урт={self.path_length} дэлгэсэн={self.expanded} "
            f"үүсгэсэн={self.generated} max_frontier={self.max_frontier} "
            f"хугацаа={self.elapsed * 1000:.2f}ms"
        )


class GridWorld:
    """Хана бүхий хоёр хэмжээст тор. `#` хана, `.` чөлөөт, `S` эхлэл, `G` зорилго."""

    def __init__(self, rows: Iterable[str], diagonal: bool = False) -> None:
        self.grid: list[str] = [row.rstrip("\n") for row in rows if row.strip()]
        if not self.grid:
            raise ValueError("Тор хоосон байна")

        self.height = len(self.grid)
        self.width = max(len(row) for row in self.grid)
        self.grid = [row.ljust(self.width, FREE) for row in self.grid]
        self.diagonal = diagonal

        self.start = self._locate(START)
        self.goal = self._locate(GOAL)

    @classmethod
    def from_text(cls, text: str, diagonal: bool = False) -> "GridWorld":
        """Олон мөрт тэмдэгт мөрөөс тор үүсгэнэ."""
        return cls(text.strip("\n").splitlines(), diagonal=diagonal)

    def _locate(self, symbol: str) -> State:
        for r, row in enumerate(self.grid):
            c = row.find(symbol)
            if c != -1:
                return (r, c)
        raise ValueError(f"Торон дээр {symbol!r} тэмдэг олдсонгүй")

    def in_bounds(self, state: State) -> bool:
        r, c = state
        return 0 <= r < self.height and 0 <= c < self.width

    def is_wall(self, state: State) -> bool:
        r, c = state
        return self.grid[r][c] == WALL

    def is_goal(self, state: State) -> bool:
        return state == self.goal

    def moves(self) -> tuple[tuple[int, int, str], ...]:
        return ORTHOGONAL + DIAGONAL if self.diagonal else ORTHOGONAL

    def neighbors(self, state: State) -> Iterator[tuple[State, str, float]]:
        """(дараагийн төлөв, үйлдэл, алхмын зардал) гурвалуудыг гаргана."""
        r, c = state
        for dr, dc, action in self.moves():
            nxt = (r + dr, c + dc)
            if not self.in_bounds(nxt) or self.is_wall(nxt):
                continue
            cost = sqrt(2) if dr and dc else 1.0
            yield nxt, action, cost

    def render(self, path: Iterable[State] = ()) -> str:
        """Торыг ASCII хэлбэрээр, замыг `*`-аар тэмдэглэн буцаана."""
        canvas = [list(row) for row in self.grid]
        for r, c in path:
            if canvas[r][c] not in (START, GOAL):
                canvas[r][c] = "*"
        return "\n".join("".join(row) for row in canvas)

    def __repr__(self) -> str:
        return f"GridWorld({self.height}x{self.width}, start={self.start}, goal={self.goal})"


class Search(ABC):
    """Бүх хайлтын алгоритмын дундын суурь (graph search).

    Дэд класс дөрвөн frontier үйлдлийг л хэрэгжүүлнэ; давталтын логик,
    хэмжигдэхүүн тоолох, зам сэргээх хэсэг нь энд нэг удаа бичигдсэн.
    """

    name: str = "Search"

    def __init__(self, problem: GridWorld) -> None:
        self.problem = problem

    # ── Дэд класс дарж бичих хэсэг ──────────────────────────────────
    @abstractmethod
    def _reset_frontier(self) -> None:
        """Frontier-ийг хоосон байдалд оруулна."""

    @abstractmethod
    def _push(self, node: Node) -> None:
        """Зангилааг frontier-т нэмнэ."""

    @abstractmethod
    def _pop(self) -> Node:
        """Дараагийн дэлгэх зангилааг frontier-ээс авна."""

    @abstractmethod
    def _frontier_size(self) -> int:
        """Frontier дэх зангилааны тоо."""

    # ── Заавал биш дэгээ ────────────────────────────────────────────
    def _child_order(self, children: list[Node]) -> Iterable[Node]:
        """Хүүхдүүдийг frontier-т ямар дарааллаар хийхийг тохируулна."""
        return children

    def _accept_child(self, child: Node) -> bool:
        """Хүүхдийг frontier-т оруулах эсэх (жишээ нь гүний хязгаар)."""
        return True

    # ── Дундын хайлтын давталт ──────────────────────────────────────
    def solve(self) -> SearchResult:
        problem = self.problem
        self._reset_frontier()
        self._push(Node(problem.start))

        explored: set[State] = set()
        expanded = generated = 0
        max_frontier = 1
        started = time.perf_counter()

        while self._frontier_size() > 0:
            node = self._pop()
            if node.state in explored:
                continue

            if problem.is_goal(node.state):
                return SearchResult(
                    algorithm=self.name,
                    found=True,
                    path=node.path(),
                    cost=node.g,
                    expanded=expanded,
                    generated=generated,
                    max_frontier=max_frontier,
                    elapsed=time.perf_counter() - started,
                )

            explored.add(node.state)
            expanded += 1

            children: list[Node] = []
            for nxt, action, cost in problem.neighbors(node.state):
                if nxt in explored:
                    continue
                child = Node(nxt, node, action, node.g + cost, node.depth + 1)
                if self._accept_child(child):
                    children.append(child)

            for child in self._child_order(children):
                self._push(child)
                generated += 1

            max_frontier = max(max_frontier, self._frontier_size())

        return SearchResult(
            algorithm=self.name,
            found=False,
            expanded=expanded,
            generated=generated,
            max_frontier=max_frontier,
            elapsed=time.perf_counter() - started,
        )
