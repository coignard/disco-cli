from typing import List, Dict
from dataclasses import dataclass, field

@dataclass
class DialogueHistory:
    messages: List[Dict[str, str]] = field(default_factory=list)

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

    def get_messages(self) -> List[Dict[str, str]]:
        return self.messages

    def clear(self):
        self.messages = []
