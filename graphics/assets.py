# -*- coding: utf-8 -*-
"""Загрузка изображений из assets/images."""
import pygame

from game import settings as S


class GameAssets:
    def __init__(self):
        self.background_image = None
        self.zombie_animations = []
        self.dark_animations = []
        self.bonus_images = {}
        self.button_images = {}


def load_assets(width: int, height: int) -> GameAssets:
    assets = GameAssets()
    bg_path = S.IMAGE_BG_DIR / "background.png"
    try:
        if bg_path.is_file():
            img = pygame.image.load(str(bg_path)).convert()
            assets.background_image = pygame.transform.scale(img, (width, height))
    except pygame.error:
        pass

    assets.zombie_animations = []
    for zt in range(1, 8):
        frames = []
        for f in range(1, 4):
            path = S.IMAGE_ENEMIES_DIR / f"zombie{zt}_frame{f}.png"
            img = pygame.image.load(str(path)).convert_alpha()
            img = pygame.transform.scale(img, (80, 80))
            frames.append(img)
        assets.zombie_animations.append(frames)

    assets.dark_animations = []
    for zt in range(1, 8):
        frames = []
        for f in range(1, 4):
            dark_path = S.IMAGE_ENEMIES_DIR / f"zombie{zt}_frame{f}_dark.png"
            try:
                img = pygame.image.load(str(dark_path)).convert_alpha()
            except pygame.error:
                img = assets.zombie_animations[zt - 1][f - 1].copy()
                dark_surface = pygame.Surface(img.get_size(), pygame.SRCALPHA)
                dark_surface.fill((0, 0, 0, 100))
                img.blit(dark_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            img = pygame.transform.scale(img, (80, 80))
            frames.append(img)
        assets.dark_animations.append(frames)

    for name, file in [
        ("clock", "bonus_clock.png"),
        ("medkit", "bonus_medkit.png"),
        ("bomb", "bonus_bomb.png"),
    ]:
        path = S.IMAGE_UI_DIR / file
        try:
            img = pygame.image.load(str(path)).convert_alpha()
            img = pygame.transform.scale(img, (50, 50))
            assets.bonus_images[name] = img
        except pygame.error:
            assets.bonus_images[name] = None

    button_files = {
        "restart": "button_restart.png",
        "exit": "button_exit.png",
        "resume": "button_resume.png",
        "inst": "button_inst.png",
        "weapon": "button_weapon.png",
        "auto": "button_auto.png",
        "shotgun": "button_shotgun.png",
        "grenade": "button_grenade.png",
    }
    for key, filename in button_files.items():
        path = S.IMAGE_UI_DIR / filename
        try:
            img = pygame.image.load(str(path)).convert_alpha()
            img = pygame.transform.scale(img, (200, 60))
            assets.button_images[key] = img
        except pygame.error:
            assets.button_images[key] = None

    return assets
