from domain.gateways.chatbot_gateway import ChatbotGateway
from domain.gateways.memory_gateway import MemoryGateway
from config import settings # Importa comandos predefinidos
from config.settings import logger

class ProcessUserMessageUseCase:
    """Caso de uso para processar uma mensagem recebida do usuário."""

    def __init__(self, chatbot_gateway: ChatbotGateway, memory_gateway: MemoryGateway):
        self.chatbot_gateway = chatbot_gateway
        self.memory_gateway = memory_gateway
        self.predefined_commands = settings.PREDEFINED_COMMANDS
        logger.info("Use Case 'ProcessUserMessage' inicializado.")

    async def execute(self, user_id: int, user_input: str) -> str:
        """
        Processa a mensagem do usuário, verifica comandos predefinidos,
        consulta o LLM se necessário e atualiza a memória.
        """
        logger.info(f"Executando Use Case para user_id {user_id} com input: '{user_input}'")
        normalized_input = user_input.strip().lower()
        bot_response = ""

        # 1. Verificar Comandos Predefinidos
        if normalized_input in self.predefined_commands:
            response_or_prompt = self.predefined_commands[normalized_input]
            # Se for um prompt para o LLM (começa com "Fale", "Conte", "Quais são")
            if response_or_prompt.startswith(("fale", "conte", "quais são")):
                logger.info(f"Comando '{normalized_input}' mapeado para prompt do LLM.")
                # Usaremos o prompt como input para o LLM, mas com o histórico ATUAL
                history = await self.memory_gateway.get_history(user_id)
                bot_response = await self.chatbot_gateway.generate_response(user_id, response_or_prompt, history)
            else:
                # É uma resposta direta
                logger.info(f"Comando '{normalized_input}' mapeado para resposta direta.")
                bot_response = response_or_prompt
        else:
            # 2. Não é comando predefinido, consultar LLM
            logger.info(f"Input não é comando predefinido, consultando LLM.")
            history = await self.memory_gateway.get_history(user_id)
            bot_response = await self.chatbot_gateway.generate_response(user_id, user_input, history)

        # 3. Adicionar interação à memória (mesmo se for resposta predefinida)
        await self.memory_gateway.add_interaction(user_id, user_input, bot_response)
        logger.info(f"Interação salva na memória para user_id {user_id}.")

        return bot_response