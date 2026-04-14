# -*- coding: utf-8 -*-
"""Константы игры и пути к ресурсам."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"
SOUNDS_DIR = ASSETS_DIR / "sounds"
IMAGES_DIR = ASSETS_DIR / "images"
IMAGE_BG_DIR = IMAGES_DIR / "background"
IMAGE_ENEMIES_DIR = IMAGES_DIR / "enemies"
IMAGE_UI_DIR = IMAGES_DIR / "ui"
HIGHSCORE_FILE = BASE_DIR / "highscore.txt"

WIDTH = 1000
HEIGHT = 700

TEXT_COLOR = (220, 220, 220)
RED = (220, 50, 50)
GREEN = (50, 220, 50)
BLUE = (50, 150, 255)
YELLOW = (255, 255, 100)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

DARK_MODE_INTERVAL = 7200
DARK_MODE_DURATION = 1800

font = None
big_font = None
small_font = None
inst_font = None


def init_fonts():
    import pygame

    global font, big_font, small_font, inst_font
    font = pygame.font.SysFont("arial", 28)
    big_font = pygame.font.SysFont("arial", 48, bold=True)
    small_font = pygame.font.SysFont("arial", 20)
    inst_font = pygame.font.SysFont("arial", 24)
