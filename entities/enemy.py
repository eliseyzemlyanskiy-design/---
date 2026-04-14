# -*- coding: utf-8 -*-
import math
import random

import pygame

from game import settings as S
from graphics.assets import GameAssets


class Zombie:
    def __init__(self, assets: GameAssets):
        self._assets = assets
        self.x = random.randint(50, S.WIDTH - 50)
        self.y = random.randint(50, S.HEIGHT - 50)
        self.base_size = 80
        self.size = self.base_size
        self.growth_rate = random.uniform(0.1, 0.3)
        self.zombie_type = random.randint(0, 6)
        self.frames = assets.zombie_animations[self.zombie_type]
        self.frame = 0
        self.frame_timer = 0
        self.move_speed = random.uniform(0.5, 1.5)
        self.target_x = random.randint(50, S.WIDTH - 50)
        self.target_y = random.randint(50, S.HEIGHT - 50)
        self.target_timer = 0
        if self.zombie_type == 3:
            self.max_health = 200
        elif self.zombie_type == 5:
            self.max_health = 150
        elif self.zombie_type == 6:
            self.max_health = 80
        else:
            self.max_health = 100
        self.health = self.max_health
        self.exploding = False
        self.explosion_radius = 0
        self.invincible = False
        self.invincible_timer = 0
        if self.zombie_type == 5:
            self.invincible = True
            self.invincible_timer = 180
        self.dark_mode = False

    def update(self, time_stopped=False):
        if self.exploding:
            self.explosion_radius += 5
            if self.explosion_radius > 80:
                return "exploded"
            return "alive"
        if time_stopped:
            return "alive"
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False
        self.size += self.growth_rate
        self.frame_timer += 1
        if self.frame_timer >= 10:
            self.frame = (self.frame + 1) % len(self.frames)
            self.frame_timer = 0
        self.target_timer += 1
        if self.target_timer > 60 or (abs(self.x - self.target_x) < 5 and abs(self.y - self.target_y) < 5):
            self.target_x = random.randint(50, S.WIDTH - 50)
            self.target_y = random.randint(50, S.HEIGHT - 50)
            self.target_timer = 0
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = math.hypot(dx, dy)
        if dist > 0:
            self.x += dx / dist * self.move_speed
            self.y += dy / dist * self.move_speed
        min_size = self.size // 2
        self.x = max(min_size, min(S.WIDTH - min_size, self.x))
        self.y = max(min_size, min(S.HEIGHT - min_size, self.y))
        if self.size > 180:
            return "escaped"
        return "alive"

    def draw(self, surface):
        if self.exploding:
            pygame.draw.circle(surface, (255, 200, 0), (int(self.x), int(self.y)), int(self.explosion_radius))
            pygame.draw.circle(
                surface, (255, 100, 0), (int(self.x), int(self.y)), int(self.explosion_radius * 0.7)
            )
            for i in range(12):
                angle = i * math.pi / 6
                r = self.explosion_radius * random.uniform(0.8, 1.2)
                px = self.x + math.cos(angle) * r
                py = self.y + math.sin(angle) * r
                color = random.choice([(255, 100, 0), (255, 200, 0)])
                size = random.randint(3, 8)
                pygame.draw.circle(surface, color, (int(px), int(py)), size)
            return
        dark_animations = self._assets.dark_animations
        if self.dark_mode and dark_animations:
            current = dark_animations[self.zombie_type][self.frame]
        else:
            current = self.frames[self.frame]
        scale = self.size / self.base_size
        new_w = int(current.get_width() * scale)
        new_h = int(current.get_height() * scale)
        scaled = pygame.transform.scale(current, (new_w, new_h))
        if self.x < self.target_x:
            final = scaled
        else:
            final = pygame.transform.flip(scaled, True, False)
        rect = final.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(final, rect.topleft)
        shadow = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        shadow.blit(final, (0, 0))
        shadow.fill((0, 0, 0, 50), special_flags=pygame.BLEND_RGBA_MULT)
        surface.blit(shadow, (rect.x + 2, rect.y + 2))
        health_width = self.size * 1.2
        health_height = 6
        health_ratio = self.health / self.max_health
        bar_x = self.x - health_width / 2
        bar_y = self.y - self.size / 2 - 20
        pygame.draw.rect(surface, (50, 50, 50), (bar_x, bar_y, health_width, health_height), border_radius=3)
        if self.zombie_type == 3:
            color = (255, 165, 0)
        elif self.zombie_type == 4:
            color = S.BLUE
        elif self.zombie_type == 5:
            color = (160, 32, 240)
        elif self.zombie_type == 6:
            color = (50, 205, 50)
        else:
            color = S.GREEN if health_ratio > 0.5 else S.RED
        pygame.draw.rect(
            surface, color, (bar_x, bar_y, health_width * health_ratio, health_height), border_radius=3
        )
        if self.invincible:
            shield_radius = int(self.size * 0.3)
            pygame.draw.circle(surface, (200, 200, 255), (int(self.x), int(self.y) - shield_radius // 2), shield_radius, 3)
            pygame.draw.line(
                surface,
                (200, 200, 255),
                (int(self.x) - shield_radius, int(self.y) - shield_radius // 2),
                (int(self.x) + shield_radius, int(self.y) - shield_radius // 2),
                3,
            )

    def is_clicked(self, pos):
        scale = self.size / self.base_size
        w = self.frames[0].get_width() * scale
        h = self.frames[0].get_height() * scale
        rect = pygame.Rect(self.x - w / 2, self.y - h / 2, w, h)
        return rect.collidepoint(pos)

    def take_damage(self, damage):
        if self.invincible:
            return False
        self.health -= damage
        if self.health <= 0:
            self.exploding = True
            return True
        return False
