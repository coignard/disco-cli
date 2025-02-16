from typing import Optional, Generator
import xml.etree.ElementTree as ET
from models.skill_check import SkillCheck
from config.constants import SKILL_CATEGORIES
from utils.exceptions import XMLProcessingError
import logging

class XMLStreamProcessor:
    def __init__(self):
        self.buffer = ""
        self._logger = logging.getLogger(__name__)
        self._partial_tag = ""

    def _normalize_text(self, text: str) -> str:
        dashes = ['—', '–', '‐', '‑', '⁃', '−']
        for dash in dashes:
            text = text.replace(dash, '-')
        return ' '.join(text.split())

    def clear_buffer(self) -> None:
        self.buffer = ""

    def process_stream(self, chunk: str) -> Generator[Optional[SkillCheck], None, None]:
        if hasattr(chunk, 'text'):
            chunk = chunk.text
        elif isinstance(chunk, list) and len(chunk) > 0 and hasattr(chunk[0], 'text'):
            chunk = chunk[0].text

        chunk = str(chunk)
        self.buffer += chunk

        while True:
            start = self.buffer.find("<skill")
            if start == -1:
                break

            end = self.buffer.find("</skill>", start)
            if end == -1:
                break

            end += len("</skill>")
            complete_tag = self.buffer[start:end]

            try:
                skill_check = self._parse_skill_check(complete_tag)
                if skill_check:
                    yield skill_check
                self.buffer = self.buffer[end:]
            except ET.ParseError as e:
                self._logger.debug(f"Partial XML chunk received: {complete_tag}")
                break
            except Exception as e:
                self._logger.error(f"Check failure: Error processing XML chunk: {e}")
                self.buffer = self.buffer[end:]

    def _normalize_skill_name(self, skill_name: str) -> str:
        skill_name = skill_name.strip()
        for category, skills in SKILL_CATEGORIES.items():
            for skill in skills:
                if skill_name.lower() == skill.lower():
                    return skill
        return skill_name

    def _normalize_difficulty(self, difficulty: str) -> str:
        from config.constants import DIFFICULTY_LEVELS
        difficulty = difficulty.strip()
        for level in DIFFICULTY_LEVELS.keys():
            if difficulty.lower() == level.lower():
                return level
        return difficulty

    def _parse_skill_check(self, xml_chunk: str) -> Optional[SkillCheck]:
        try:
            root = ET.fromstring(xml_chunk)

            raw_skill_name = root.attrib.get('name', 'Unknown')
            skill_name = self._normalize_skill_name(raw_skill_name)

            raw_difficulty = root.attrib.get('difficulty', 'medium')
            difficulty = self._normalize_difficulty(raw_difficulty)

            success = root.attrib.get('success', 'false').lower() == 'true'
            content = self._normalize_text(root.text or "")

            category = next(
                (cat for cat, skills in SKILL_CATEGORIES.items()
                 if skill_name in skills),
                None
            )

            return SkillCheck(
                skill=skill_name,
                difficulty=difficulty,
                success=success,
                content=content,
                category=category
            )
        except ET.ParseError as e:
            raise
        except Exception as e:
            self._logger.error(f"Check failure: Error parsing skill check: {e}")
            return None

    def get_remaining_buffer(self) -> str:
        return self.buffer
