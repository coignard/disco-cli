from rich.console import Console
from rich.text import Text
from rich.style import Style
from blessed import Terminal
from typing import Optional
from models.skill_check import SkillCheck
from config.constants import SKILL_COLORS
from localization.locale_manager import LocaleManager
from config.config_manager import ConfigManager

class DialogRenderer:
    def __init__(self, config_manager: Optional[ConfigManager] = None):
        self.console = Console(width=72)
        self.term = Terminal()
        self.locale = LocaleManager(config_manager=config_manager)
        self.last_lines = 0
        self.max_width = 72
        self.continue_shown = False

    def get_skill_color(self, skill_check: SkillCheck) -> str:
        if skill_check.category:
            return SKILL_COLORS.get(skill_check.category, '#FFFFFF')
        return '#FFFFFF'

    def render_skill_check(self, skill_check: SkillCheck, show_continue: bool = False, continue_active: bool = False) -> None:
        total_lines = self.last_lines + (1 if self.continue_shown else 0)
        if total_lines > 0:
            print(self.term.move_up(total_lines) + self.term.clear_eos, end='')

        text = Text()
        text.append("\n")

        skill_color = self.get_skill_color(skill_check)
        skill_name = self.locale.translate('skills', skill_check.skill)
        text.append(skill_name.upper(), style=f"bold {skill_color}")

        difficulty = self.locale.translate('difficulties', skill_check.difficulty)
        result = self.locale.translate('results', 'Success' if skill_check.success else 'Failure')
        text.append(f" [{difficulty}: {result}]")

        text.append(" - ", style="white")

        text.append(skill_check.content, style="white")

        self.console.print(text)
        self.console.print()

        self.last_lines = 2

        if show_continue:
            self.show_continue(active=continue_active)
        else:
            self.continue_shown = False

    def render_user_input(self, text: str) -> None:
        total_lines = self.last_lines + (1 if self.continue_shown else 0)
        if total_lines > 0:
            print(self.term.move_up(total_lines) + self.term.clear_eos, end='')

        self.console.print()
        formatted_text = Text()
        formatted_text.append(
            self.locale.translate('ui', 'you'),
            style="bold white"
        )
        formatted_text.append(" - ", style="white")
        formatted_text.append(f"{text}", style="white")
        self.console.print(formatted_text)

        self.last_lines = 0
        self.continue_shown = False

    def show_continue(self, active: bool = False) -> None:
        continue_text = "  " + self.locale.translate('ui', 'continue_prompt') + " ▶" + "  "
        style = "white on #8F2510" if active else "white on #808080"
        self.console.print(continue_text, style=style)
        self.continue_shown = True

    def update_continue(self, active: bool = False) -> None:
        if self.continue_shown:
            print(self.term.move_up() + self.term.clear_eos, end='')
        self.show_continue(active=active)

    def clear_continue(self) -> None:
        if self.continue_shown:
            print(self.term.move_up() + self.term.clear_eos, end='')
            self.continue_shown = False
