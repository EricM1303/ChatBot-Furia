from typing import Dict, List, Tuple
from collections import deque # Fila para limitar o tamanho da memória

from domain.gateways.memory_gateway import MemoryGateway, ChatHistoryType
from config.settings import logger

class InMemoryUserMemory(MemoryGateway):
    """Implementação da memória que guarda o histórico em um dicionário na RAM."""

    def __init__(self, max_history_size: int = 15):
        # Dicionário para guardar a memória de cada usuário
        # A chave é user_id, o valor é um deque (fila) de tuplas (input, output)
        self._user_memory: Dict[int, deque[Tuple[str, str]]] = {}
        self._max_history_size = max_history_size
        logger.info(f"Memória em RAM inicializada (máx. {max_history_size} interações por usuário).")

    async def get_history(self, user_id: int) -> ChatHistoryType:
        """Recupera o histórico como uma lista de tuplas."""
        if user_id in self._user_memory:
            # Converte o deque para lista antes de retornar
            return list(self._user_memory[user_id])
        return []

    async def add_interaction(self, user_id: int, user_input: str, bot_output: str) -> None:
        """Adiciona interação, garantindo que o usuário exista e respeitando o limite."""
        if user_id not in self._user_memory:
            # Cria um deque com tamanho máximo para o novo usuário
            self._user_memory[user_id] = deque(maxlen=self._max_history_size)

        self._user_memory[user_id].append((user_input, bot_output))
        # logger.debug(f"Interação adicionada para user_id {user_id}. Histórico atual: {list(self._user_memory[user_id])}")

    async def clear_history(self, user_id: int) -> None:
        """Limpa o histórico do usuário, se existir."""
        if user_id in self._user_memory:
            self._user_memory[user_id].clear()
            logger.info(f"Histórico limpo para user_id {user_id}.")
        else:
            logger.warning(f"Tentativa de limpar histórico para user_id {user_id} inexistente.")