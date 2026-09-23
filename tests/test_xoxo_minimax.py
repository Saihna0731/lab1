import os
import sys
from pathlib import Path

import numpy as np
import pytest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import XOXO as game


def set_board(rows):
    game.board[:] = np.array(rows, dtype=float)


def test_ai_takes_immediate_win():
    set_board([[2, 2, 0],
               [1, 1, 0],
               [0, 0, 0]])
    game.best_move()
    assert game.board[0][2] == game.AI


def test_ai_blocks_human_win():
    set_board([[1, 1, 0],
               [2, 0, 0],
               [0, 0, 0]])
    game.best_move()
    assert game.board[0][2] == game.AI


def test_ai_prefers_faster_win():
    set_board([[2, 2, 0],
               [1, 1, 0],
               [2, 0, 1]])
    game.best_move()
    assert game.board[0][2] == game.AI


def test_node_counter_is_reported():
    set_board([[1, 0, 0],
               [0, 0, 0],
               [0, 0, 0]])
    game.best_move()
    assert game.nodes_evaluated > 0


@pytest.mark.parametrize("opening", [(0, 0), (0, 1), (1, 1)])
def test_ai_never_loses(opening):
    """Exhaustively expand every human reply against the minimax AI."""

    def play(board, human_turn):
        if game.check_win(game.HUMAN, board):
            pytest.fail(f"AI lost after human opening {opening}")
        if game.check_win(game.AI, board) or game.is_board_full(board):
            return
        if human_turn:
            for row in range(3):
                for col in range(3):
                    if board[row][col] == 0:
                        board[row][col] = game.HUMAN
                        play(board, False)
                        board[row][col] = 0
        else:
            game.board[:] = board
            game.best_move()
            play(game.board.copy(), True)

    start = np.zeros((3, 3))
    start[opening] = game.HUMAN
    play(start, False)
