# -*- coding: utf-8 -*-
import pygame

from game import settings as S


class Particle:
    def __init__(self, x, y, vx, vy, color, lifetime):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        return self.lifetime > 0

    def draw(self, surface):
        radius = max(1, int(3 * (self.lifetime / self.max_lifetime)))
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), radius)


class Bonus:
    def __init__(self, x, y, bonus_type, bonus_images, small_font):
        self.x = x
        self.y = y
        self.type = bonus_type
        self.lifetime = 300
        self.max_lifetime = 300
        self.radius = 25
        self._bonus_images = bonus_images
        self._small_font = small_font

    def update(self):
        self.lifetime -= 1
        return self.lifetime > 0

    def draw(self, surface):
        img = self._bonus_images.get(self.type)
        if img:
            rect = img.get_rect(center=(int(self.x), int(self.y)))
            surface.blit(img, rect.topleft)
        else:
            color_map = {"clock": S.YELLOW, "medkit": S.GREEN, "bomb": S.RED}
            color = color_map.get(self.type, S.WHITE)
            pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.radius)
            letter = self.type[0].upper()
            surf = self._small_font.render(letter, True, S.BLACK)
            text_rect = surf.get_rect(center=(int(self.x), int(self.y)))
            surface.blit(surf, text_rect)
        progress = self.lifetime / self.max_lifetime
        bar_width = 50
        bar_height = 6
        bar_x = self.x - bar_width // 2
        bar_y = self.y - self.radius - 10
        pygame.draw.rect(surface, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height), border_radius=2)
        pygame.draw.rect(
            surface, (255, 255, 100), (bar_x, bar_y, bar_width * progress, bar_height), border_radius=2
        )

    def is_clicked(self, pos):
        dx = pos[0] - self.x
        dy = pos[1] - self.y
        return dx * dx + dy * dy <= self.radius * self.radius
