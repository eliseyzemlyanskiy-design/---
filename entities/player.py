# -*- coding: utf-8 -*-
from game import settings as S
from entities.weapon import WEAPON_AUTO


class Player:
    def __init__(self):
        self.score = 0
        self.lives = 3
        self.weapon = WEAPON_AUTO
        self.highscore = 0
        self.zombies_destroyed = 0
        self.grenade_cooldown = 0

    def load_highscore(self):
        path = S.HIGHSCORE_FILE
        if path.is_file():
            try:
                self.highscore = int(path.read_text(encoding="utf-8").strip())
            except (ValueError, OSError):
                self.highscore = 0
        else:
            self.highscore = 0

    def save_highscore(self):
        try:
            S.HIGHSCORE_FILE.write_text(str(self.highscore), encoding="utf-8")
        except OSError:
            pass

    def reset_stats(self):
        self.score = 0
        self.lives = 3
        self.zombies_destroyed = 0
        self.grenade_cooldown = 0
        self.load_highscore()
