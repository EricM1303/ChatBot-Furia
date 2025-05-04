from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import HumanMessage, AIMessage
from typing import List, Tuple

from domain.gateways.chatbot_gateway import ChatbotGateway, ChatHistoryType
from config import settings # Importa configurações
from config.settings import logger

class LangchainChatbot(ChatbotGateway):
    """Implementação do ChatbotGateway usando Langchain e Groq."""

    def __init__(self):
        try:
            self.llm = ChatGroq(
                model_name=settings.MODEL_NAME,
                groq_api_key=settings.GROQ_API_KEY,
                temperature=0.7
            )
            logger.info(f"LLM Langchain/Groq ({settings.MODEL_NAME}) inicializado.")
        except Exception as e:
            logger.error(f"Falha ao inicializar o LLM Langchain/Groq: {e}", exc_info=True)
            raise

        # Cria o template do prompt uma vez
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", settings.SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])

    async def generate_response(self, user_id: int, user_input: str, history: ChatHistoryType) -> str:
        """Gera resposta usando o LLM com histórico formatado."""
        try:
            # Converte o histórico [(str, str)] para o formato [HumanMessage, AIMessage]
            formatted_history = []
            for human_msg, ai_msg in history:
                formatted_history.append(HumanMessage(content=human_msg))
                formatted_history.append(AIMessage(content=ai_msg))

            # Prepara o input para o template
            input_data = {
                "input": user_input,
                "chat_history": formatted_history
            }

            # Cria a cadeia (chain) ou invoca diretamente formatando
            # Para simplicidade, vamos formatar e invocar
            formatted_prompt = self.prompt_template.format_messages(**input_data)

            logger.info(f"Enviando prompt para LLM (user_id: {user_id})...")
            ai_response = await self.llm.ainvoke(formatted_prompt) # Usa ainvoke para async
            response_content = ai_response.content
            logger.info(f"Resposta recebida do LLM (user_id: {user_id}).")

            return response_content

        except Exception as e:
            logger.error(f"Erro ao gerar resposta do LLM para user_id {user_id}: {e}", exc_info=True)
            return "Desculpe, tive um problema interno ao processar sua mensagem. Tente novamente mais tarde. 😥"