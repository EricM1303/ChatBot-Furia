# Documentação do Bot Furia Telegram 🐾🤖

## 1. Introdução

Bem-vindo à documentação do **Bot Furia Telegram**! 🎮📱  
Este bot foi criado para interagir com fãs do time de CS da **FURIA**, fornecendo informações como próximos jogos, curiosidades, etc. Ele usa a inteligência artificial do **Groq** (através da biblioteca **LangChain**) para gerar respostas e a biblioteca `python-telegram-bot` para se conectar e interagir no Telegram. 💬🧠

O projeto utiliza uma abordagem chamada **Clean Architecture**. A ideia principal é separar o código em camadas bem definidas, tornando-o:

* ✅ **Mais fácil de entender:** Cada parte tem sua responsabilidade clara.
* ✅ **Mais fácil de testar:** Podemos testar a lógica principal sem depender do Telegram ou do Groq.
* ✅ **Mais fácil de manter e modificar:** Mudar a biblioteca do Telegram ou o serviço de IA afeta menos o resto do código.
* ✅ **Independente de frameworks:** As regras de negócio centrais não dependem de detalhes externos.

---

## 2. Estrutura de Pastas 📁

A organização das pastas segue os princípios da Clean Architecture:

```
furia_telegram_bot/
├── config/         # Configurações (chaves API, textos fixos)
├── domain/         # Lógica central, regras de negócio (independente)
│   ├── use_cases/  # Ações/Casos de uso (o que o bot faz)
│   └── gateways/   # Interfaces para serviços externos
├── infrastructure/ # Implementações concretas (dependente de libs externas)
│   ├── chatbot/    # Implementação do acesso à IA (Langchain/Groq)
│   ├── memory/     # Implementação da memória da conversa
│   └── telegram/   # Código específico do Telegram (conexão, handlers)
├── app/            # Camada que conecta tudo e inicia o bot
├── .env
└── requirements.txt # Lista de bibliotecas Python necessárias
```

* **`config`**: Guarda configurações que podem mudar, como chaves de API (lidas do `.env`) e textos fixos (como o prompt do sistema).
* **`domain`**: O coração do sistema. Contém a lógica pura, sem saber se é um bot de Telegram ou um site.
  * `gateways`: Define *o que* precisamos de serviços externos (como "preciso gerar uma resposta" ou "preciso salvar o histórico"), mas não *como* isso é feito. São como contratos.
  * `use_cases`: Orquestram as ações. Ex: o "Processar Mensagem do Usuário" pega a mensagem, usa o gateway de memória, usa o gateway do chatbot e retorna a resposta.
* **`infrastructure`**: Implementa os "contratos" definidos nos gateways e lida com as bibliotecas externas.
  * `memory`: Implementa *como* salvar e buscar o histórico (aqui, usamos a memória RAM do computador).
  * `chatbot`: Implementa *como* falar com a IA (aqui, usamos LangChain e Groq).
  * `telegram`: Implementa *como* receber mensagens do Telegram e enviar respostas, usando a biblioteca `python-telegram-bot`.
* **`app`**: O ponto de entrada. Cria as instâncias das classes das outras camadas e as conecta (injeção de dependência), iniciando o bot.

---

## 3. Fluxo de uma Mensagem 💬➡️🧠➡️📲

Para entender como tudo se conecta, veja o caminho que uma mensagem de texto comum faz:

1. **Usuário (Telegram):** Envia uma mensagem (ex: "quais as curiosidades?").
2. **`python-telegram-bot` (Infra/Telegram):** Recebe a mensagem e aciona o `MessageHandler`.
3. **`handlers.handle_message` (Infra/Telegram):**
    * Pega o ID do usuário e o texto da mensagem.
    * Mostra "digitando...".
    * Pega a instância do `ProcessUserMessageUseCase`.
    * Chama `process_message_use_case.execute(user_id, message_text)`.
4. **`ProcessUserMessageUseCase.execute` (Domain/UseCases):**
    * Normaliza o input.
    * Verifica se é um comando predefinido.
    * Chama `self.memory_gateway.get_history(user_id)`.
5. **`InMemoryUserMemory.get_history` (Infra/Memory):**
    * Busca o histórico no `_user_memory`.
6. **De volta ao `UseCase`:**
    * Chama `self.chatbot_gateway.generate_response(...)`.
7. **`LangchainChatbot.generate_response` (Infra/Chatbot):**
    * Formata histórico.
    * Preenche o `prompt_template`.
    * Envia para o Groq e recebe a resposta.
8. **De volta ao `UseCase`:**
    * Chama `self.memory_gateway.add_interaction(...)`.
9. **`InMemoryUserMemory.add_interaction`:**
    * Salva a interação.
10. **`UseCase` retorna `bot_response` para o handler.**
11. **`handlers.handle_message`:**
    * Envia a resposta para o usuário.
12. **Usuário (Telegram):** Recebe a resposta. 🎉

---

## 4. Como Rodar Localmente 🖥️⚙️

1. **Instalar Dependências:**  
   No terminal, dentro da pasta raiz do projeto (`furia_telegram_bot/`), execute:
   ```bash
   pip install -r requirements.txt
   ```

2. **Criar e Configurar `.env`:**  
   Crie um arquivo `.env` com as seguintes chaves:
   ```env
   GROQ_API_KEY=sua_chave_groq_aqui
   TELEGRAM_BOT_TOKEN=seu_token_do_botfather_aqui
   ```

3. **Executar o Bot:**  
   No terminal:
   ```bash
   python -m app.telegram_bot
   ```

---

## 5. Acessar o Bot Diretamente no Telegram 📲

Você pode testar o bot sem precisar rodar nada localmente!  
Basta clicar no link abaixo para abrir o chat diretamente no Telegram:

👉 [Acesse o bot Furia no Telegram](https://t.me/FuriaChat_FuriosoBot)

Envie uma mensagem como `curiosidades` ou `qual o próximo jogo?` e veja a mágica acontecer. 🧠✨

---

Divirta-se explorando o mundo da FURIA com inteligência artificial! 💬🎯👾
