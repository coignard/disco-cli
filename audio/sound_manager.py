from pathlib import Path
import pygame
import logging
from typing import Dict

class SoundManager:
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        pygame.mixer.init()

        self.sfx_path = Path('sfx')
        self.sounds: Dict[str, pygame.mixer.Sound] = {}

        try:
            self.sounds['startup'] = pygame.mixer.Sound(self.sfx_path / 'switch-04.wav')
            self.sounds['click'] = pygame.mixer.Sound(self.sfx_path / 'dialogue-click.wav')
            self.sounds['FYS'] = pygame.mixer.Sound(self.sfx_path / 'interface-skill-passiveFYS-03-01.wav')
            self.sounds['INT'] = pygame.mixer.Sound(self.sfx_path / 'interface-skill-passiveINT-04-01.wav')
            self.sounds['MOT'] = pygame.mixer.Sound(self.sfx_path / 'interface-skill-passiveMOT-04-01.wav')
            self.sounds['PSY'] = pygame.mixer.Sound(self.sfx_path / 'interface-skill-passivePSY-04-02.wav')
            self._logger.info("Sound effects loaded successfully")
        except Exception as e:
            self._logger.error(f"Check failure: Failed to load sound effects: {e}")

    def play_startup(self) -> None:
        try:
            if 'startup' in self.sounds:
                self.sounds['startup'].play()
                self._logger.debug("Playing startup sound")
        except Exception as e:
            self._logger.error(f"Check failure: Failed to play startup sound: {e}")

    def play_skill_sound(self, category: str) -> None:
        try:
            category_to_sound = {
                'INTELLECT': 'INT',
                'PSYCHE': 'PSY',
                'PHYSIQUE': 'FYS',
                'MOTORICS': 'MOT'
            }

            sound_key = category_to_sound.get(category)
            if sound_key and sound_key in self.sounds:
                self.sounds[sound_key].play()
                self._logger.debug(f"Playing sound for category: {category}")
        except Exception as e:
            self._logger.error(f"Check failure: Failed to play skill sound: {e}")

    def play_click(self) -> None:
        try:
            if 'click' in self.sounds:
                self.sounds['click'].play()
                self._logger.debug("Playing click sound")
        except Exception as e:
            self._logger.error(f"Check failure: Failed to play click sound: {e}")

    def cleanup(self) -> None:
        try:
            pygame.mixer.quit()
            self._logger.info("Sound system cleaned up")
        except Exception as e:
            self._logger.error(f"Check failure: Error cleaning up sound system: {e}")
