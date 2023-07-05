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


def main():
    pygame.init()

    role_images = graphics.read_role_images()
    window = pygame.display.set_mode((config.WINDOW_SIZE, config.WINDOW_SIZE))

    board = chess.new_board()
    selected_piece_position = None
    moves = None

    while True:
        events = graphics.get_events()

        if graphics.should_close(events):
            break

        if graphics.did_select_piece(events):
            position = graphics.get_selected_piece_position()

            if moves is not None and position in moves:
                chess.move_piece(board, selected_piece_position, position)
                selected_piece_position = None
                moves = None
            else:
                selected_piece_position = position
                moves = chess.get_available_piece_moves(board, position)

        window.fill(config.BACKGROUND_COLOR)

        graphics.draw_tiles(window)
        graphics.draw_pieces(window, role_images, board)

        if moves is not None:
            graphics.draw_moves(window, moves)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
