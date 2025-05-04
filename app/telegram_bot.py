import asyncio
from config import settings # Garante que as configs sejam carregadas
from config.settings import logger

# Importações das implementações concretas e use case
from infrastructure.chatbot.langchain_chatbot import LangchainChatbot
from infrastructure.memory.in_memory_user_memory import InMemoryUserMemory
from domain.use_cases.process_user_message import ProcessUserMessageUseCase
from infrastructure.telegram.bot_setup import setup_application

def main() -> None:
    """Ponto de entrada principal para iniciar o bot."""
    logger.info("Iniciando o Bot Furia Telegram...")

    # --- Criação das Dependências ---
    try:
        # 1. Criar Gateways
        chatbot_gateway = LangchainChatbot()
        memory_gateway = InMemoryUserMemory(max_history_size=10) # Limita o histórico

        # 2. Criar Use Case injetando os Gateways
        process_message_use_case = ProcessUserMessageUseCase(
            chatbot_gateway=chatbot_gateway,
            memory_gateway=memory_gateway
        )

        # 3. Configurar a Aplicação Telegram injetando o Use Case e Memory
        application = setup_application(
            process_message_use_case=process_message_use_case,
            memory_gateway=memory_gateway # Passa a memória para /start
        )

        # --- Iniciar o Bot ---
        logger.info("Iniciando polling do Telegram...")
        application.run_polling()

    except ValueError as e:
        logger.error(f"Erro de configuração: {e}")
    except Exception as e:
        logger.critical(f"Erro fatal ao iniciar o bot: {e}", exc_info=True)


if __name__ == "__main__":
    # Executa a função principal usando asyncio (necessário para funções async nos handlers)
    # Embora run_polling seja síncrono, as funções internas podem precisar do loop asyncio
    # Se usar run_async, o asyncio.run() seria mais explícito.
    # Para run_polling, chamar main() diretamente geralmente funciona.
     main()