from abc import ABC, abstractmethod
from typing import List, Tuple

# Define a estrutura esperada para o histórico (tupla de string input/output)
ChatHistoryType = List[Tuple[str, str]]

class ChatbotGateway(ABC):
    """Interface para interagir com o modelo de linguagem."""

    @abstractmethod
    async def generate_response(self, user_id: int, user_input: str, history: ChatHistoryType) -> str:
        """
        Gera uma resposta do chatbot com base na entrada e histórico do usuário.

        Args:
            user_id: Identificador único do usuário.
            user_input: A mensagem mais recente do usuário.
            history: O histórico da conversa [(input_user1, output_bot1), ...].

        Returns:
            A resposta gerada pelo chatbot.
        """
        pass