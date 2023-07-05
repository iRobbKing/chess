import pygame

import chess
import config
import connection
import graphics


def ask_mode():
    while True:
        mode = input("1. Создать\n2. Подключиться\n")

        if mode == "1" or mode == "2":
            return connection.start_server if mode == "1" else connection.connect_to_server


def new_game():
    pygame.init()

    role_images = graphics.read_role_images()
    window = pygame.display.set_mode((config.WINDOW_SIZE, config.WINDOW_SIZE))

    board = chess.new_board()
    selected_piece_position = None
    moves = None

    moved = None

    events = set()

    def read_events():
        nonlocal events
        events = graphics.get_events()

    def update_graphics():
        window.fill(config.BACKGROUND_COLOR)

        graphics.draw_tiles(window)
        graphics.draw_pieces(window, role_images, board)

        if moves is not None:
            graphics.draw_moves(window, moves)

        pygame.display.update()

    def update_game(opponent_move=None):
        nonlocal moves, selected_piece_position, moved

        if opponent_move is not None:
            chess.move_piece(board, *opponent_move)

        moved = None

        if graphics.should_close(events):
            return

        if graphics.did_select_piece(events):
            position = graphics.get_selected_piece_position()

            if moves is not None and position in moves:
                chess.move_piece(board, selected_piece_position, position)
                moved = selected_piece_position, position
                selected_piece_position = None
                moves = None
            else:
                selected_piece_position = position
                moves = chess.get_available_piece_moves(board, position)

        return moved

    return read_events, update_graphics, update_game


def main():
    read_events, update_graphics, update_game = new_game()


if __name__ == "__main__":
    main()
