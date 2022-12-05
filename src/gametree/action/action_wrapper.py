from abc import ABC
from gametree.action.search_bot_action import SearchBotAction
from __future__ import annotations

class ActionWrapper(ABC):
    action: SearchBotAction
