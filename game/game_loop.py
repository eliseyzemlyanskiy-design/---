# -*- coding: utf-8 -*-
import sys

import pygame

from audio.sound_manager import SoundManager
from entities.weapon import WEAPON_AUTO
from game import settings as S
from game.events import handle_events
from game.game import Button
from graphics.assets import load_assets
from graphics.render import draw_instructions_screen, draw_start_screen, draw_weapon_menu


def run_game():
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

    screen = pygame.display.set_mode((S.WIDTH, S.HEIGHT))
    pygame.display.set_caption("Зомби-кликер")

    S.init_fonts()

    try:
        assets = load_assets(S.WIDTH, S.HEIGHT)
    except (pygame.error, FileNotFoundError, OSError) as e:
        print(f"Ошибка загрузки ресурсов: {e}")
        pygame.quit()
        sys.exit(1)

    sounds = SoundManager(S.SOUNDS_DIR, music_enabled=True)

    clock = pygame.time.Clock()
    state = "start"
    game = None
    running = [True]
    selected_weapon = [WEAPON_AUTO]

    inst_button = Button(S.WIDTH // 2 - 220, S.HEIGHT // 2 + 100, 200, 60, "inst", assets)
    weapon_button = Button(S.WIDTH // 2 + 20, S.HEIGHT // 2 + 100, 200, 60, "weapon", assets)
    weapon_btns = [
        Button(S.WIDTH // 2 - 150, 200, 300, 60, "auto", assets),
        Button(S.WIDTH // 2 - 150, 300, 300, 60, "shotgun", assets),
        Button(S.WIDTH // 2 - 150, 400, 300, 60, "grenade", assets),
    ]

    while running[0]:
        state, game = handle_events(
            state,
            game,
            running,
            selected_weapon,
            inst_button,
            weapon_button,
            weapon_btns,
            sounds,
            assets,
        )
        if state == "start":
            draw_start_screen(screen, inst_button, weapon_button, assets)
        elif state == "game" and game:
            game.update()
            game.draw(screen)
        elif state == "instructions":
            draw_instructions_screen(screen, assets)
        elif state == "weapon_menu":
            draw_weapon_menu(screen, weapon_btns, assets)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()
