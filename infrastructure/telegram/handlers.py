from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from domain.use_cases.process_user_message import ProcessUserMessageUseCase
from domain.gateways.memory_gateway import MemoryGateway # Para limpar histórico
from config import settings
from config.settings import logger

# --- Variáveis Globais (ou passadas via context.application.bot_data) ---
# É crucial instanciar essas dependências uma vez e passá-las para os handlers.
# Faremos isso no bot_setup.py e acessaremos via context.
# process_message_use_case: ProcessUserMessageUseCase = None -> Será injetado
# memory_gateway: MemoryGateway = None -> Será injetado

# --- Teclado de Sugestões ---
SUGGESTION_KEYBOARD = [
    [KeyboardButton("Próximos jogos"), KeyboardButton("Jogadores")],
    [KeyboardButton("Curiosidades"), KeyboardButton("Frases")],
]
SUGGESTION_MARKUP = ReplyKeyboardMarkup(SUGGESTION_KEYBOARD, resize_keyboard=True, one_time_keyboard=False)


# --- Filtro de Usuários Permitidos (Opcional) ---
async def is_user_allowed(update: Update) -> bool:
    if not settings.ALLOWED_USER_IDS: # Se a lista está vazia, permite todos
        return True
    return update.effective_user.id in settings.ALLOWED_USER_IDS


# --- Handlers ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler para o comando /start."""
    user = update.effective_user
    user_id = user.id
    logger.info(f"Comando /start recebido de user_id {user_id} ({user.username})")

    if not await is_user_allowed(update):
        logger.warning(f"Usuário {user_id} não autorizado tentou usar /start.")
        await update.message.reply_text("Desculpe, você não tem permissão para usar este bot.")
        return

    # Limpa o histórico do usuário ao iniciar (opcional, mas bom para recomeçar)
    memory_gateway: MemoryGateway = context.application.bot_data['memory_gateway']
    await memory_gateway.clear_history(user_id)

    # Mensagem inicial
    initial_greeting = f"Olá, {user.first_name}! Sou o assistente dos fãs de CS da FURIA 🐾"
    initial_help = "Como posso te ajudar? Você pode digitar sua pergunta ou usar os botões abaixo!"

    await update.message.reply_text(initial_greeting)
    await update.message.reply_text(initial_help, reply_markup=SUGGESTION_MARKUP)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler para o comando /help."""
    user_id = update.effective_user.id
    logger.info(f"Comando /help recebido de user_id {user_id}")

    if not await is_user_allowed(update):
        logger.warning(f"Usuário {user_id} não autorizado tentou usar /help.")
        await update.message.reply_text("Desculpe, você não tem permissão para usar este bot.")
        return

    help_text = (
        "Eu sou o assistente de fãs da FURIA! 🐾\n\n"
        "Você pode me perguntar sobre:\n"
        "📅 Próximos jogos\n"
        "👥 Jogadores\n"
        "💡 Curiosidades\n"
        "🗣️ Frases marcantes\n\n"
        "Ou simplesmente converse comigo sobre a FURIA! Use os botões ou digite sua pergunta.\n\n"
        "Use /start para reiniciar nossa conversa (limpa o histórico)."
    )
    await update.message.reply_text(help_text, reply_markup=SUGGESTION_MARKUP)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler para mensagens de texto normais."""
    user_id = update.effective_user.id
    message_text = update.message.text
    logger.info(f"Mensagem recebida de user_id {user_id}: '{message_text}'")

    if not await is_user_allowed(update):
        logger.warning(f"Usuário {user_id} não autorizado enviou mensagem.")
        # Pode optar por não responder ou enviar uma mensagem padrão
        # await update.message.reply_text("Acesso não autorizado.")
        return

    # Recupera o use case injetado durante a configuração
    process_message_use_case: ProcessUserMessageUseCase = context.application.bot_data['process_message_use_case']

    try:
        # Envia ação "digitando..." para o usuário
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')

        # Executa o caso de uso para obter a resposta
        bot_response = await process_message_use_case.execute(user_id, message_text)

        # Envia a resposta de volta ao usuário
        # Usamos parse_mode=ParseMode.HTML ou MARKDOWN se quisermos formatar
        await update.message.reply_text(bot_response, reply_markup=SUGGESTION_MARKUP)
        logger.info(f"Resposta enviada para user_id {user_id}.")

    except Exception as e:
        logger.error(f"Erro ao processar mensagem de user_id {user_id}: {e}", exc_info=True)
        await update.message.reply_text("Ocorreu um erro inesperado ao processar sua solicitação. Por favor, tente novamente.")


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Loga os erros causados por Updates."""
    logger.error(f"Exceção ao processar um update: {context.error}", exc_info=context.error)
    # Opcional: Informar o usuário que algo deu errado
    if isinstance(update, Update):
        await update.message.reply_text("Desculpe, ocorreu um erro interno. A equipe foi notificada.")