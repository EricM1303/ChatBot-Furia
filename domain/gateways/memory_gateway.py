from abc import ABC, abstractmethod
from typing import List, Tuple

# Reusa o tipo definido no chatbot_gateway
from .chatbot_gateway import ChatHistoryType

class MemoryGateway(ABC):
    """Interface para gerenciar a memória da conversa por usuário."""

    @abstractmethod
    async def get_history(self, user_id: int) -> ChatHistoryType:
        """Recupera o histórico de conversa para um usuário específico."""
        pass

    @abstractmethod
    async def add_interaction(self, user_id: int, user_input: str, bot_output: str) -> None:
        """Adiciona uma nova interação (usuário/bot) ao histórico do usuário."""
        pass

    @abstractmethod
    async def clear_history(self, user_id: int) -> None:
        """Limpa o histórico de conversa para um usuário específico."""
        pass