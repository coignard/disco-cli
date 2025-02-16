from prompt_toolkit import PromptSession
from typing import Optional, List
from processors.xml_processor import XMLStreamProcessor
from ui.renderer import DialogRenderer
from audio.sound_manager import SoundManager
import logging
from blessed import Terminal
from models.skill_check import SkillCheck
import asyncio

class DialogStateManager:
    def __init__(self, config_manager=None):
        self.session = PromptSession()
        self.processor = XMLStreamProcessor()
        self.renderer = DialogRenderer(config_manager)
        self.sound_manager = SoundManager()
        self.term = Terminal()
        self._logger = logging.getLogger(__name__)
        self._current_check: Optional[SkillCheck] = None
        self._next_check: Optional[SkillCheck] = None
        self._waiting_for_continue = False

    async def handle_user_input(self) -> Optional[str]:
        try:
            user_input = await self.session.prompt_async(">>> ")

            if user_input.lower() in ('exit', 'quit'):
                raise EOFError("Check failure: User requested exit")

            if not user_input or user_input.isspace():
                return None

            self.renderer.render_user_input(user_input)
            self.sound_manager.play_click()
            return user_input

        except (EOFError, KeyboardInterrupt):
            print(self.term.show_cursor, end='', flush=True)
            raise

    async def process_response_chunk(self, chunk: str) -> None:
        try:
            for skill_check in self.processor.process_stream(chunk):
                if not skill_check:
                    continue

                if self._current_check is None:
                    self._current_check = skill_check
                    self.renderer.render_skill_check(skill_check, show_continue=True, continue_active=False)
                    if skill_check.category:
                        self.sound_manager.play_skill_sound(skill_check.category)
                elif self._next_check is None:
                    self._next_check = skill_check
                    self.renderer.update_continue(active=True)
                    self._waiting_for_continue = True
                    await self._wait_for_continue()
                else:
                    while self._waiting_for_continue:
                        await asyncio.sleep(0.1)
                    self._current_check = skill_check
                    self._next_check = None
                    self.renderer.render_skill_check(skill_check, show_continue=True, continue_active=False)
                    if skill_check.category:
                        self.sound_manager.play_skill_sound(skill_check.category)

        except Exception as e:
            self._logger.error(f"Check failure: Error processing chunk: {e}")

    async def _wait_for_continue(self) -> None:
        if not self._waiting_for_continue:
            return

        try:
            await self.session.prompt_async("", refresh_interval=None)
            self.renderer.clear_continue()
            self.sound_manager.play_click()

            if self._next_check:
                self._current_check = self._next_check
                self._next_check = None
                self.renderer.render_skill_check(self._current_check, show_continue=True, continue_active=False)
                if self._current_check.category:
                    self.sound_manager.play_skill_sound(self._current_check.category)

            self._waiting_for_continue = False

        except Exception as e:
            self._logger.error(f"Check failure: Error waiting for continue: {e}")

    async def finish_response(self) -> None:
        try:
            remaining_checks = list(self.processor.process_stream(self.processor.get_remaining_buffer()))

            for skill_check in remaining_checks:
                if skill_check:
                    if self._current_check is None:
                        self._current_check = skill_check
                        self.renderer.render_skill_check(skill_check, show_continue=False)
                        if skill_check.category:
                            self.sound_manager.play_skill_sound(skill_check.category)
                    else:
                        self._next_check = skill_check
                        self.renderer.update_continue(active=True)
                        self._waiting_for_continue = True
                        await self._wait_for_continue()

            self.processor.clear_buffer()
            self._current_check = None
            self._next_check = None
            self._waiting_for_continue = False
            self.renderer.clear_continue()

        except Exception as e:
            self._logger.error(f"Check failure: Error processing final chunk: {e}")
