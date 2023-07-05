import dataclasses
import enum
import itertools

import config
import iterables


class Role(enum.StrEnum):
    PAWN = "pawn"
    KNIGHT = "knight"
    BISHOP = "bishop"
    ROOK = "rook"
    QUEEN = "queen"
    KING = "king"


def all_roles():
    return Role.__members__.values()


class Color(enum.StrEnum):
    WHITE = "white"
    BLACK = "black"


@dataclasses.dataclass
class Piece:
    color: Color
    role: Role
    moved: bool = False


def _rank(color, roles):
    return [Piece(color, role) for role in roles]


def new_board():
    back_rank = [Role.ROOK, Role.KNIGHT, Role.BISHOP, Role.QUEEN, Role.KING, Role.BISHOP, Role.KNIGHT, Role.ROOK]
    front_rank = [Role.PAWN for _ in range(config.BOARD_SIZE)]
    empty_rank = lambda: [None for _ in range(config.BOARD_SIZE)]

    return [
        _rank(Color.WHITE, back_rank),
        _rank(Color.WHITE, front_rank),
        *(empty_rank() for _ in range(config.BOARD_SIZE - 4)),
        _rank(Color.BLACK, front_rank),
        _rank(Color.BLACK, back_rank),
    ]


def _get_pawn_moves(color, moved):
    direction = 1 if color == Color.WHITE else -1
    moves = [(0, direction)]

    if not moved:
        moves.append((0, direction * 2))

    return [moves]


def _get_knight_moves():
    yield ((-1, 2),)
    yield ((1, 2),)
    yield ((2, 1),)
    yield ((2, -1),)
    yield ((1, -2),)
    yield ((-1, -2),)
    yield ((-2, -1),)
    yield ((-2, 1),)


def _get_moves_in_line(dx, dy):
    for i in range(1, config.BOARD_SIZE, 1):
        yield i * dx, i * dy


def _get_bishop_moves():
    yield _get_moves_in_line(1, 1)
    yield _get_moves_in_line(1, -1)
    yield _get_moves_in_line(-1, -1)
    yield _get_moves_in_line(-1, 1)


def _get_rook_moves():
    yield _get_moves_in_line(0, 1)
    yield _get_moves_in_line(0, -1)
    yield _get_moves_in_line(1, 0)
    yield _get_moves_in_line(-1, 0)


def _get_queen_moves():
    yield from _get_bishop_moves()
    yield from _get_rook_moves()


def _get_king_moves(king_moved, right_rook_castlable, left_rool_casstlable):
    yield ((1, 0),)
    yield ((1, 1),)
    yield ((0, 1),)
    yield ((-1, 1),)
    yield ((-1, 0),)
    yield ((-1, -1),)
    yield ((0, -1),)
    yield ((1, -1),)


def _get_piece_moves(piece):
    match piece.role:
        case Role.PAWN:
            return _get_pawn_moves(piece.color, piece.moved)
        case Role.KNIGHT:
            return _get_knight_moves()
        case Role.BISHOP:
            return _get_bishop_moves()
        case Role.ROOK:
            return _get_rook_moves()
        case Role.QUEEN:
            return _get_queen_moves()
        case Role.KING:
            return _get_king_moves(piece.moved, False, False)


def _is_within_bounds(position):
    i, j = position
    return 0 <= i < config.BOARD_SIZE and 0 <= j < config.BOARD_SIZE


def _is_tile_empty(board):
    def inner(position):
        i, j = position
        return board[j][i] is None

    return inner


def _is_empty_or_different_color(board, color):
    def inner(position):
        i, j = position
        piece = board[j][i]
        return piece is None or piece.color != color

    return inner


def get_available_piece_moves(board, position):
    i, j = position
    piece = board[j][i]

    if piece is None:
        return ()

    moves = _get_piece_moves(piece)
    moves = (((i + mi, j + mj) for mi, mj in path) for path in moves)
    moves = (itertools.takewhile(_is_within_bounds, path) for path in moves)
    moves = (iterables.take_while_inclusive(_is_tile_empty(board), path) for path in moves)
    moves = (itertools.takewhile(_is_empty_or_different_color(board, piece.color), path) for path in moves)

    return {move for path in moves for move in path}


def move_piece(board, position, move):
    i, j = position
    piece = board[j][i]
    piece.moved = True
    ni, nj = move
    board[j][i] = None
    board[nj][ni] = piece
