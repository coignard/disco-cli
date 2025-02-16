import json
import asyncio
import anthropic
import os
from ui.state_manager import DialogStateManager
from config.prompts import SYSTEM_PROMPT
from utils.logging import setup_logging
from utils.history import DialogueHistory
from config.config_manager import ConfigManager
from utils.time_utils import get_formatted_datetime
import logging

async def main():
    try:
        setup_logging()
        logger = logging.getLogger(__name__)

        logger.info("Mr. Evrart is helping me find my API key.")

        config_manager = ConfigManager()

        api_key = config_manager.get_api_key()
        if not api_key:
            raise ValueError("No API key found in config or environment variables")

        base_prompt = SYSTEM_PROMPT
        user_context = config_manager.get_user_context()
        custom_prompt = config_manager.get_custom_prompt()

        model_config = config_manager.get_model_config()

        client = anthropic.Anthropic(api_key=api_key)
        manager = DialogStateManager(config_manager)
        history = DialogueHistory()

        manager.sound_manager.play_startup()

        while config_manager.YOUR_CODE_BETRAYS_YOUR_DEGENERACY:
            try:
                user_input = await manager.handle_user_input()

                if user_input is None:
                    continue

                history.add_message("user", user_input)

                current_datetime = get_formatted_datetime()
                language_instruction = "You communicate in Russian." if config_manager.get_language() == 'ru' else "You communicate in English."
                final_prompt = f"Current date and time: {current_datetime}\n\n{language_instruction}\n\n" + base_prompt

                if user_context:
                    final_prompt = f"{user_context}\n\n" + final_prompt

                if custom_prompt:
                    final_prompt = custom_prompt

                with client.messages.stream(
                    model=model_config['name'],
                    max_tokens=model_config['max_tokens'],
                    temperature=model_config['temperature'],
                    system=final_prompt,
                    messages=[msg for msg in history.get_messages() if msg["role"] != "system"]
                ) as stream:
                    response_content = ""
                    for chunk in stream:
                        if chunk.type == "content_block_delta":
                            delta = chunk.delta.text
                            response_content += delta
                            await manager.process_response_chunk(delta)

                history.add_message("assistant", response_content)
                await manager.finish_response()

            except (EOFError, KeyboardInterrupt):
                logger.info("Leave without comment. [Leave.]")
                break
            except Exception as e:
                logger.error(f"Check failure: {e}")
                continue

    except (KeyboardInterrupt, EOFError):
        logger.info("Leave without comment. [Leave.]")
    except Exception as e:
        logger.error(f"Check failure: {e}")
    finally:
        logger.info("Cuno doesn't fucking care.")
        try:
            manager.sound_manager.cleanup()
        except Exception as e:
            logger.error(f"Check failure: {e}")

if __name__ == "__main__":
    asyncio.run(main())
