from typing import Optional
from .translations import TRANSLATIONS
from config.config_manager import ConfigManager

class LocaleManager:
    def __init__(self, language: str = 'en', config_manager: Optional[ConfigManager] = None):
        if config_manager:
            self.language = config_manager.get_language()
        else:
            self.language = language
        self._translations = TRANSLATIONS

    def set_language(self, language: str) -> None:
        if language in self._translations:
            self.language = language

    def translate(self, category: str, key: str) -> str:
        try:
            return self._translations[self.language][category][key]
        except KeyError:
            return key
