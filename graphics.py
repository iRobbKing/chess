import itertools
import pygame
import os

import chess
import config


def get_events():
    return set(event.type for event in pygame.event.get())


def should_close(events):
    return pygame.QUIT in events


def did_select_piece(events):
    return pygame.MOUSEBUTTONUP in events


def get_selected_piece_position():
    x, y = pygame.mouse.get_pos()
    i = x // config.TILE_SIZE
    j = y // config.TILE_SIZE
    return i, config.BOARD_SIZE - j - 1


def read_role_images():
    roles = lambda: {role: None for role in chess.all_roles()}
    result = {chess.Color.WHITE: roles(), chess.Color.BLACK: roles()}

    for image_name in os.listdir(config.ROLE_IMAGES_PATH):
        color, role = image_name.split(".")[0].split("_")
        image_path = os.path.join(config.ROLE_IMAGES_PATH, image_name)
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (config.ROLE_IMAGE_SIZE, config.ROLE_IMAGE_SIZE))
        result[color][role] = image

    return result


def _get_tile_rect(i, j, offset=0):
    x = config.TILE_SIZE * i + offset
    y = config.TILE_SIZE * j + offset
    return x, y, config.TILE_SIZE, config.TILE_SIZE


def _get_rect_center(rect):
    x, y, w, h = rect
    return x + w // 2, y + h // 2


def draw_tiles(surface):
    for i, j in itertools.product(range(config.BOARD_SIZE), range(config.BOARD_SIZE)):
        if ((i % 2) + j) % 2 == 1:
            pygame.draw.rect(surface, config.TILE_COLOR, _get_tile_rect(i, j))


def draw_pieces(surface, role_images, board):
    for j, row in enumerate(board):
        for i, piece in enumerate(row):
            if piece is not None:
                rect = _get_tile_rect(i, config.BOARD_SIZE - j - 1, config.ROLE_IMAGE_OFFSET)
                surface.blit(role_images[piece.color][piece.role], rect)


def draw_moves(surface, moves):
    for i, j in moves:
        j = config.BOARD_SIZE - j - 1
        center = _get_rect_center(_get_tile_rect(i, j))
        pygame.draw.circle(surface, config.MOVE_COLOR, center, config.MOVE_CIRCLE_RADIUS)
