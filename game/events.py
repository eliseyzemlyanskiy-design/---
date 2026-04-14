# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import List, Optional, Tuple

import pygame

from audio.sound_manager import SoundManager
from entities.weapon import WEAPON_AUTO, WEAPON_GRENADE, WEAPON_SHOTGUN
from game.game import Button, Game
from graphics.assets import GameAssets


def handle_events(
    state: str,
    game: Optional[Game],
    running: List[bool],
    selected_weapon: List[int],
    inst_button: Button,
    weapon_button: Button,
    weapon_btns: list,
    sounds: SoundManager,
    assets: GameAssets,
) -> Tuple[str, Optional[Game]]:
    """Обрабатывает очередь событий pygame. Возвращает (state, game)."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running[0] = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if state == "start":
                if inst_button.is_clicked(event.pos):
                    state = "instructions"
                elif weapon_button.is_clicked(event.pos):
                    state = "weapon_menu"
                else:
                    state = "game"
                    game = Game(assets, sounds)
                    game.weapon = selected_weapon[0]
            elif state == "game" and game:
                game.handle_click(event.pos)
            elif state == "instructions":
                state = "start"
            elif state == "weapon_menu":
                for btn in weapon_btns:
                    if btn.is_clicked(event.pos):
                        if btn.action == "auto":
                            selected_weapon[0] = WEAPON_AUTO
                        elif btn.action == "shotgun":
                            selected_weapon[0] = WEAPON_SHOTGUN
                        elif btn.action == "grenade":
                            selected_weapon[0] = WEAPON_GRENADE
                        state = "start"
        elif event.type == pygame.KEYDOWN:
            if state == "start":
                if event.key == pygame.K_ESCAPE:
                    running[0] = False
            elif state == "game" and game:
                if event.key == pygame.K_ESCAPE:
                    if game.game_over:
                        running[0] = False
                    else:
                        game.paused = not game.paused
                elif event.key == pygame.K_r:
                    game.reset()
                elif event.key == pygame.K_m:
                    sounds.set_music_enabled(not sounds.music_enabled)
                elif event.key == pygame.K_1:
                    game.weapon = WEAPON_AUTO
                elif event.key == pygame.K_2:
                    game.weapon = WEAPON_SHOTGUN
                elif event.key == pygame.K_3:
                    game.weapon = WEAPON_GRENADE
            elif state == "instructions":
                if event.key == pygame.K_ESCAPE:
                    state = "start"
            elif state == "weapon_menu":
                if event.key == pygame.K_ESCAPE:
                    state = "start"
    return state, game
