from telegram.ext import Application, CommandHandler, MessageHandler, filters, ApplicationBuilder

from config import settings
from config.settings import logger
from . import handlers # Importa os handlers definidos

# Importa as dependências que os handlers precisam
from domain.use_cases.process_user_message import ProcessUserMessageUseCase
from domain.gateways.chatbot_gateway import ChatbotGateway
from domain.gateways.memory_gateway import MemoryGateway

def setup_application(
    process_message_use_case: ProcessUserMessageUseCase,
    memory_gateway: MemoryGateway # Passa a memory gateway tbm, para o /start
) -> Application:
    """Configura e retorna a aplicação do bot Telegram com handlers."""
    logger.info("Configurando a aplicação do bot Telegram...")

    application = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()

    # --- Injeção de Dependência ---
    # Armazena as instâncias necessárias no contexto da aplicação
    # para que os handlers possam acessá-las via context.application.bot_data
    application.bot_data['process_message_use_case'] = process_message_use_case
    application.bot_data['memory_gateway'] = memory_gateway
    logger.info("Instâncias de UseCase e Gateway injetadas no contexto do bot.")

    # --- Registro de Handlers ---
    # Comando /start
    application.add_handler(CommandHandler("start", handlers.start_command))

    # Comando /help
    application.add_handler(CommandHandler("help", handlers.help_command))

    # Mensagens de texto (não comandos)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.handle_message))

    # Handler de erros
    application.add_error_handler(handlers.error_handler)

    logger.info("Handlers registrados. Aplicação pronta.")
    return application