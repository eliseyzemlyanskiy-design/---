# -*- coding: utf-8 -*-
"""Загрузка и воспроизведение звуков через pygame.mixer."""
from pathlib import Path

import pygame


class SoundManager:
    def __init__(self, sounds_dir: Path, music_enabled: bool = True):
        self._sounds_dir = Path(sounds_dir)
        self._sounds = {}
        self.music_enabled = music_enabled
        self._music_loaded = False
        self._ensure_mixer()
        self._load_sounds()
        self._load_music()

    def _ensure_mixer(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

    def _path(self, name: str) -> Path:
        return self._sounds_dir / name

    def _load_sounds(self):
        mapping = {
            "click": "click.wav",
            "explosion": "explosion.wav",
            "bonus": "bonus.wav",
            "lose_life": "lose.wav",
        }
        for key, filename in mapping.items():
            path = self._path(filename)
            if not path.is_file():
                print(f"Звук не найден: {path}")
                self._sounds[key] = None
                continue
            try:
                self._sounds[key] = pygame.mixer.Sound(str(path))
                print(f"Загружен звук: {path.name}")
            except pygame.error as e:
                print(f"Не удалось загрузить {path}: {e}")
                self._sounds[key] = None

    def _load_music(self):
        for candidate in ("music.ogg", "music.mp3", "music.wav"):
            path = self._path(candidate)
            if not path.is_file():
                continue
            try:
                pygame.mixer.music.load(str(path))
                pygame.mixer.music.set_volume(0.3)
                self._music_loaded = True
                print(f"Загружена музыка: {path.name}")
                if self.music_enabled:
                    pygame.mixer.music.play(-1)
                return
            except pygame.error as e:
                print(f"Музыка {path.name} не воспроизводится: {e}")
        print("Фоновая музыка не загружена (нет music.ogg / .mp3 / .wav).")

    def play_sound(self, name: str, volume: float = 0.5):
        snd = self._sounds.get(name)
        if snd is None:
            return
        v = max(0.0, min(1.0, float(volume)))
        try:
            snd.set_volume(v)
            snd.play()
        except pygame.error:
            pass

    def set_music_enabled(self, enabled: bool):
        self.music_enabled = enabled
        if not self._music_loaded:
            return
        if enabled:
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.stop()
