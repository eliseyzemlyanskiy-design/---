# -*- coding: utf-8 -*-
import pygame

from game import settings as S
from game.game import Button
from graphics.assets import GameAssets


def draw_instructions_screen(surface, assets: GameAssets):
    if assets.background_image:
        surface.blit(assets.background_image, (0, 0))
    else:
        surface.fill((20, 20, 30))
    overlay = pygame.Surface((S.WIDTH, S.HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    surface.blit(overlay, (0, 0))
    title = S.big_font.render("Инструкция", True, S.YELLOW)
    surface.blit(title, (S.WIDTH // 2 - title.get_width() // 2, 50))
    lines = [
        "Кликай по зомби, чтобы уничтожить их.",
        "Автомат: 2 клика (100 HP), бронированный - 4 клика (200 HP).",
        "Дробовик: 6 снарядов в радиусе 40, каждый наносит 20 урона.",
        "Гранатомёт: взрыв радиусом 110, урон 100, перезарядка 1 сек.",
        "Если зомби вырастает слишком большим, ты теряешь жизнь.",
        "Бонусы: Аптечка +1 жизнь, Бомба – всех убить, Часы – стоп 5 сек.",
        "Медик (синяя полоска) при убийстве даёт +1 жизнь.",
        "НЕУЯЗВИМЫЙ (фиолетовая полоска): 150 HP, первые 3 сек не получает урон.",
        "ЯДОВИТЫЙ (светло-зелёный): при побеге снимает 3 жизни.",
        "Каждые 2 минуты – ТЁМНЫЙ РЕЖИМ: 30 сек, удвоенный урон, тёмные зомби, частицы.",
        "Управление:",
        "  ESC - пауза / продолжить",
        "  R - перезапуск игры",
        "  M - включить/выключить музыку",
        "  1,2,3 - смена оружия (Автомат, Дробовик, Гранатомёт)",
        "Кликни в любом месте, чтобы вернуться в главное меню.",
    ]
    y_offset = 150
    for line in lines:
        text = S.inst_font.render(line, True, S.WHITE)
        surface.blit(text, (S.WIDTH // 2 - text.get_width() // 2, y_offset))
        y_offset += 35
    prompt = S.font.render("Кликните для возврата", True, (200, 200, 200))
    surface.blit(prompt, (S.WIDTH // 2 - prompt.get_width() // 2, S.HEIGHT - 80))


def draw_start_screen(surface, inst_btn: Button, weapon_btn: Button, assets: GameAssets):
    if assets.background_image:
        surface.blit(assets.background_image, (0, 0))
    else:
        surface.fill((20, 20, 30))
    overlay = pygame.Surface((S.WIDTH, S.HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 100))
    surface.blit(overlay, (0, 0))
    title = S.big_font.render("Зомби-кликер", True, (255, 255, 100))
    surface.blit(title, (S.WIDTH // 2 - title.get_width() // 2, S.HEIGHT // 2 - 150))
    prompt = S.font.render("Кликните в любом месте, чтобы начать", True, S.WHITE)
    surface.blit(prompt, (S.WIDTH // 2 - prompt.get_width() // 2, S.HEIGHT // 2 - 30))
    esc_hint = S.font.render("Нажмите ESC для выхода", True, (200, 200, 200))
    surface.blit(esc_hint, (S.WIDTH // 2 - esc_hint.get_width() // 2, S.HEIGHT // 2 + 20))
    inst_btn.draw(surface)
    weapon_btn.draw(surface)


def draw_weapon_menu(surface, buttons, assets: GameAssets):
    if assets.background_image:
        surface.blit(assets.background_image, (0, 0))
    else:
        surface.fill((20, 20, 30))
    overlay = pygame.Surface((S.WIDTH, S.HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    surface.blit(overlay, (0, 0))
    title = S.big_font.render("Выберите оружие", True, S.YELLOW)
    surface.blit(title, (S.WIDTH // 2 - title.get_width() // 2, 80))
    for btn in buttons:
        btn.draw(surface)
    back = S.font.render("Нажмите ESC для возврата", True, (200, 200, 200))
    surface.blit(back, (S.WIDTH // 2 - back.get_width() // 2, S.HEIGHT - 50))
