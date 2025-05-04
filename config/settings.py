import os
from dotenv import load_dotenv
import logging

# Configuração básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Carrega variáveis do arquivo .env
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Validação básica das chaves
if not GROQ_API_KEY:
    logger.error("Erro: Chave da API da Groq (GROQ_API_KEY) não encontrada no .env")
    raise ValueError("GROQ_API_KEY não definida")

if not TELEGRAM_BOT_TOKEN:
    logger.error("Erro: Token do Bot do Telegram (TELEGRAM_BOT_TOKEN) não encontrado no .env")
    raise ValueError("TELEGRAM_BOT_TOKEN não definido")

# --- Configurações Adicionais do Bot (pode adicionar mais aqui) ---
MODEL_NAME = "llama3-8b-8192"
SYSTEM_PROMPT = """
Você é um assistente chatbot amigável e MUITO entusiasmado, um grande fã do time de Counter-Strike (CS) da FURIA.
Seu objetivo é ajudar outros fãs com informações sobre o time.
Use um tom animado, inclua emojis relevantes como 🐾 (pantera), 🔥 (fogo), 🏆 (troféu) quando apropriado.
Responda sempre em português brasileiro.
Mantenha as respostas relativamente curtas e diretas, a menos que peçam detalhes.
Se não souber a resposta, diga que vai procurar ou que não tem essa informação no momento, mas sempre com entusiasmo pela FURIA!
Forneça a resposta diretamente, sem frases como "Claro!" ou "Com certeza!".
Não inclua cumprimentos genéricos como "Olá!" no início de cada resposta, vá direto ao ponto.
"""

# Comandos predefinidos e respostas diretas (ou prompts para LLM)
PREDEFINED_COMMANDS = {
    "próximos jogos": """
O próximo confronto da equipe FURIA acontecerá contra a equipe Coming soon.
De acordo com o horário do torneio Coming soon, o confronto será em Coming soon.\n
Vamos com tudo, FURIA! 🐾🔥
""",
    "jogadores": "Atualmente, os jogadores da FURIA de CS:GO são:\n FalleN 👑 (Gabriel Toledo)\n yuurih 💥 (Yuri Boian)\n KSCERATO 💪 (Kaike Cerato)\n YEKINDAR 🐅 (Mareks Gaļinskis)\n molodoy 🛡️ (Danil Golubenko)\n\n O treinador da equipe é sidde (Sidnei Macedo).", # Prompt para LLM
    "curiosidades": "Melhor Organização🏆: A FURIA foi eleita a Melhor Organização de eSports no Prêmio eSports Brasil por dois anos consecutivos, em 2020 e 2021, um reconhecimento do seu impacto e profissionalismo no cenário🐾🔥.", # Prompt para LLM
    "frases": '"A FURIA VEIO PRA VENCEEEEEEER🐾🔥", grito de torcida muito utilizado para expressar a alegria dos torcedores!', # Prompt para LLM
}

ALLOWED_USER_IDS = [] # Opcional: Lista de IDs de usuário permitidos (se vazio, permite todos)

logger.info("Configurações carregadas com sucesso.")