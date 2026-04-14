# -*- coding: utf-8 -*-
import math
import random
import sys

import pygame

from audio.sound_manager import SoundManager
from entities.bonus import Bonus, Particle
from entities.enemy import Zombie
from entities.player import Player
from entities.weapon import WEAPON_AUTO, WEAPON_GRENADE, WEAPON_SHOTGUN, damage_for
from game import settings as S
from graphics.assets import GameAssets


class Button:
    def __init__(self, x, y, width, height, action, assets: GameAssets):
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action
        self.visible = True
        self._assets = assets

    def draw(self, surface):
        if not self.visible:
            return
        img = self._assets.button_images.get(self.action)
        if img:
            surface.blit(img, self.rect.topleft)
        else:
            pygame.draw.rect(surface, (100, 100, 200), self.rect, border_radius=10)
            pygame.draw.rect(surface, S.WHITE, self.rect, 3, border_radius=10)
            text = S.font.render(self.action.capitalize(), True, S.WHITE)
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos) if self.visible else False


class Game:
    def __init__(self, assets: GameAssets, sounds: SoundManager):
        self.assets = assets
        self.sounds = sounds
        self.player = Player()
        self.pause_buttons = []
        self.game_over_buttons = []
        self.reset()

    def reset(self):
        self.zombies = []
        self.bonuses = []
        self.player.reset_stats()
        self.wave = 1
        self.spawn_timer = 0
        self.spawn_delay = 60
        self.click_effects = []
        self.game_over = False
        self.paused = False
        self.time_stopped = False
        self.time_stop_duration = 0
        self.game_start_time = pygame.time.get_ticks()
        self.dark_mode_timer = 0
        self.dark_mode_active = False
        self.dark_mode_remaining = 0
        self.particles = []
        btn_w = 180
        btn_h = 60
        spacing = 20
        total_w = btn_w * 3 + spacing * 2
        start_x = (S.WIDTH - total_w) // 2
        button_y = S.HEIGHT // 2
        self.pause_buttons = [
            Button(start_x, button_y, btn_w, btn_h, "resume", self.assets),
            Button(start_x + btn_w + spacing, button_y, btn_w, btn_h, "restart", self.assets),
            Button(start_x + (btn_w + spacing) * 2, button_y, btn_w, btn_h, "exit", self.assets),
        ]
        btn_w2 = 200
        btn_h2 = 60
        spacing2 = 30
        total_w2 = btn_w2 * 2 + spacing2
        start_x2 = (S.WIDTH - total_w2) // 2
        button_y2 = S.HEIGHT // 2 + 50
        self.game_over_buttons = [
            Button(start_x2, button_y2, btn_w2, btn_h2, "restart", self.assets),
            Button(start_x2 + btn_w2 + spacing2, button_y2, btn_w2, btn_h2, "exit", self.assets),
        ]
        for _ in range(3):
            self.spawn_zombie()

    @property
    def weapon(self):
        return self.player.weapon

    @weapon.setter
    def weapon(self, value):
        self.player.weapon = value

    def spawn_zombie(self):
        z = Zombie(self.assets)
        if self.dark_mode_active:
            z.dark_mode = True
        self.zombies.append(z)

    def spawn_bonus(self):
        typ = random.choice(["clock", "medkit", "bomb"])
        x = random.randint(50, S.WIDTH - 50)
        y = random.randint(50, S.HEIGHT - 50)
        self.bonuses.append(Bonus(x, y, typ, self.assets.bonus_images, S.small_font))

    def update(self):
        if self.game_over or self.paused:
            return
        if self.player.grenade_cooldown > 0:
            self.player.grenade_cooldown -= 1
        if self.time_stopped:
            self.time_stop_duration -= 1
            if self.time_stop_duration <= 0:
                self.time_stopped = False
        current_time = (pygame.time.get_ticks() - self.game_start_time) / 1000
        new_wave = 1 + int(current_time // 30)
        if new_wave > self.wave:
            self.wave = new_wave
            self.spawn_delay = max(30, self.spawn_delay - 2)
        self.spawn_timer += 1
        rate = max(10, self.spawn_delay - (self.wave - 1) * 2)
        if self.spawn_timer >= rate and len(self.zombies) < 10 + self.wave:
            self.spawn_zombie()
            self.spawn_timer = 0
        if random.random() < 0.005:
            self.spawn_bonus()
        to_remove = []
        for i, z in enumerate(self.zombies):
            res = z.update(self.time_stopped)
            if res == "escaped":
                self.sounds.play_sound("lose_life", volume=0.55)
                if z.zombie_type == 6:
                    self.player.lives -= 3
                else:
                    self.player.lives -= 1
                to_remove.append(i)
                if self.player.lives <= 0:
                    self.game_over = True
            elif res == "exploded":
                to_remove.append(i)
        for i in sorted(to_remove, reverse=True):
            self.zombies.pop(i)
        self.bonuses = [b for b in self.bonuses if b.update()]
        self.click_effects = [eff for eff in self.click_effects if eff[2] < 30]
        for i in range(len(self.click_effects)):
            x, y, r = self.click_effects[i]
            self.click_effects[i] = (x, y, r + 1)

        if not self.game_over and not self.paused:
            self.dark_mode_timer += 1
            if not self.dark_mode_active:
                if self.dark_mode_timer >= S.DARK_MODE_INTERVAL:
                    self.dark_mode_active = True
                    self.dark_mode_remaining = S.DARK_MODE_DURATION
                    self.dark_mode_timer = 0
                    for z in self.zombies:
                        z.dark_mode = True
            else:
                self.dark_mode_remaining -= 1
                if self.dark_mode_remaining <= 0:
                    self.dark_mode_active = False
                    for z in self.zombies:
                        z.dark_mode = False
        if self.dark_mode_active:
            for z in self.zombies:
                if random.random() < 0.15:
                    angle = random.uniform(0, 2 * math.pi)
                    speed = random.uniform(0.5, 2.5)
                    vx = math.cos(angle) * speed
                    vy = math.sin(angle) * speed
                    color = random.choice(
                        [(255, 0, 0), (200, 0, 0), (150, 0, 0), (255, 50, 50), (180, 0, 80)]
                    )
                    self.particles.append(Particle(z.x, z.y, vx, vy, color, 40))
        self.particles = [p for p in self.particles if p.update()]

    def _on_zombie_killed(self, z: Zombie):
        self.sounds.play_sound("explosion", volume=0.65)
        self.player.score += 10 * self.wave
        self.player.zombies_destroyed += 1
        if self.player.score > self.player.highscore:
            self.player.highscore = self.player.score
            self.player.save_highscore()
        if z.zombie_type == 4:
            self.player.lives += 1

    def handle_click(self, pos):
        if self.game_over:
            for btn in self.game_over_buttons:
                if btn.is_clicked(pos):
                    if btn.action == "restart":
                        self.reset()
                    elif btn.action == "exit":
                        pygame.quit()
                        sys.exit()
            return
        if self.paused:
            for btn in self.pause_buttons:
                if btn.is_clicked(pos):
                    if btn.action == "resume":
                        self.paused = False
                    elif btn.action == "restart":
                        self.reset()
                    elif btn.action == "exit":
                        pygame.quit()
                        sys.exit()
            return
        for i in range(len(self.bonuses) - 1, -1, -1):
            b = self.bonuses[i]
            if b.is_clicked(pos):
                self.sounds.play_sound("bonus", volume=0.5)
                if b.type == "medkit":
                    self.player.lives += 1
                elif b.type == "bomb":
                    for _z in self.zombies[:]:
                        self.player.score += 10 * self.wave
                        self.player.zombies_destroyed += 1
                    self.zombies.clear()
                elif b.type == "clock":
                    self.time_stopped = True
                    self.time_stop_duration = 300
                self.bonuses.pop(i)
                self.click_effects.append((pos[0], pos[1], 5))
                return

        w = self.player.weapon
        dark = self.dark_mode_active
        if w == WEAPON_AUTO:
            damage = damage_for(WEAPON_AUTO, dark)
            self.click_effects.append((pos[0], pos[1], 5))
            for i in range(len(self.zombies) - 1, -1, -1):
                z = self.zombies[i]
                if z.is_clicked(pos):
                    self.sounds.play_sound("click", volume=0.45)
                    if z.take_damage(damage):
                        self._on_zombie_killed(z)
                    return
        elif w == WEAPON_SHOTGUN:
            damage = damage_for(WEAPON_SHOTGUN, dark)
            for _ in range(6):
                angle = random.uniform(0, 2 * math.pi)
                dist = random.uniform(0, 40)
                shot_x = pos[0] + math.cos(angle) * dist
                shot_y = pos[1] + math.sin(angle) * dist
                self.click_effects.append((shot_x, shot_y, 8))
                for z in self.zombies:
                    dx = z.x - shot_x
                    dy = z.y - shot_y
                    if math.hypot(dx, dy) < 25:
                        if z.take_damage(damage):
                            self._on_zombie_killed(z)
            self.sounds.play_sound("click", volume=0.4)
        elif w == WEAPON_GRENADE:
            if self.player.grenade_cooldown > 0:
                return
            damage = damage_for(WEAPON_GRENADE, dark)
            self.click_effects.append((pos[0], pos[1], 40))
            for _ in range(20):
                angle = random.uniform(0, 2 * math.pi)
                dist = random.uniform(0, 110)
                fx = pos[0] + math.cos(angle) * dist
                fy = pos[1] + math.sin(angle) * dist
                self.click_effects.append((fx, fy, 5))
            for z in self.zombies[:]:
                dx = z.x - pos[0]
                dy = z.y - pos[1]
                if math.hypot(dx, dy) < 110:
                    if z.take_damage(damage):
                        self._on_zombie_killed(z)
            self.sounds.play_sound("click", volume=0.5)
            self.player.grenade_cooldown = 60

    def draw(self, surface):
        if self.assets.background_image:
            surface.blit(self.assets.background_image, (0, 0))
        else:
            surface.fill((20, 20, 30))
            for x in range(0, S.WIDTH, 50):
                pygame.draw.line(surface, (40, 40, 50), (x, 0), (x, S.HEIGHT), 1)
            for y in range(0, S.HEIGHT, 50):
                pygame.draw.line(surface, (40, 40, 50), (0, y), (S.WIDTH, y), 1)
        for x, y, r in self.click_effects:
            pygame.draw.circle(surface, (255, 255, 100, 150), (x, y), r, 3)
        for z in self.zombies:
            z.draw(surface)
        for b in self.bonuses:
            b.draw(surface)
        if self.dark_mode_active:
            dark_overlay = pygame.Surface((S.WIDTH, S.HEIGHT), pygame.SRCALPHA)
            dark_overlay.fill((0, 0, 0, 140))
            surface.blit(dark_overlay, (0, 0))
            remaining_seconds = self.dark_mode_remaining // 60
            timer_text = S.small_font.render(f"DARK MODE: {remaining_seconds}s", True, (255, 100, 100))
            surface.blit(timer_text, (S.WIDTH - 180, 60))
            mode_text = S.small_font.render("DARK MODE ACTIVE", True, (255, 0, 0))
            surface.blit(mode_text, (20, 60))
        for p in self.particles:
            p.draw(surface)
        panel = pygame.Surface((S.WIDTH, 50), pygame.SRCALPHA)
        panel.fill((40, 40, 55, 200))
        surface.blit(panel, (0, 0))
        pygame.draw.line(surface, (80, 80, 100), (0, 50), (S.WIDTH, 50), 2)
        surface.blit(S.font.render(f"Очки: {self.player.score}", True, S.TEXT_COLOR), (20, 10))
        surface.blit(
            S.font.render(f"Жизни: {self.player.lives}", True, S.GREEN if self.player.lives > 1 else S.RED),
            (200, 10),
        )
        surface.blit(S.font.render(f"Волна: {self.wave}", True, S.TEXT_COLOR), (350, 10))
        surface.blit(S.font.render(f"Убито: {self.player.zombies_destroyed}", True, S.TEXT_COLOR), (500, 10))
        surface.blit(S.font.render(f"На экране: {len(self.zombies)}", True, S.TEXT_COLOR), (650, 10))
        if self.time_stopped:
            surface.blit(S.small_font.render("Время остановлено!", True, S.YELLOW), (850, 35))
        highscore_surf = S.font.render(f"Рекорд: {self.player.highscore}", True, S.YELLOW)
        surface.blit(highscore_surf, (S.WIDTH - highscore_surf.get_width() - 20, S.HEIGHT - 40))
        weapon_names = ["Автомат", "Дробовик", "Гранатомёт"]
        weapon_text = S.small_font.render(
            f"Оружие: {weapon_names[self.player.weapon]} (1-2-3)", True, S.YELLOW
        )
        surface.blit(weapon_text, (20, S.HEIGHT - 30))
        if self.player.weapon == WEAPON_GRENADE and self.player.grenade_cooldown > 0:
            cx, cy = 220, S.HEIGHT - 18
            radius = 12
            pygame.draw.circle(surface, (100, 100, 100), (cx, cy), radius, 2)
            cd = self.player.grenade_cooldown
            cd_text = S.small_font.render(f"{cd // 10}.{cd % 10}", True, S.RED)
            surface.blit(cd_text, (cx - 15, cy - 10))
        if self.game_over:
            overlay = pygame.Surface((S.WIDTH, S.HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            surface.blit(overlay, (0, 0))
            go = S.big_font.render("GAME OVER", True, S.RED)
            surface.blit(go, (S.WIDTH // 2 - go.get_width() // 2, S.HEIGHT // 2 - 150))
            fs = S.font.render(f"Финальный счёт: {self.player.score}", True, S.TEXT_COLOR)
            surface.blit(fs, (S.WIDTH // 2 - fs.get_width() // 2, S.HEIGHT // 2 - 50))
            fz = S.font.render(f"Зомби уничтожено: {self.player.zombies_destroyed}", True, S.TEXT_COLOR)
            surface.blit(fz, (S.WIDTH // 2 - fz.get_width() // 2, S.HEIGHT // 2 - 10))
            for btn in self.game_over_buttons:
                btn.draw(surface)
        elif self.paused:
            overlay = pygame.Surface((S.WIDTH, S.HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            surface.blit(overlay, (0, 0))
            pause = S.big_font.render("ПАУЗА", True, S.WHITE)
            surface.blit(pause, (S.WIDTH // 2 - pause.get_width() // 2, S.HEIGHT // 2 - 150))
            for btn in self.pause_buttons:
                btn.draw(surface)
