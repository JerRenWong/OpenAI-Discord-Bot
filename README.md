# OpenAI Discord Bot

A Discord bot that uses OpenAI's GPT models for conversation within Discord threads.

## Features

- Context memory within threads (up to 20 messages)
- Automatic message splitting for long responses from OpenAI
- !clear command to clear the conversation history

## Setup

1. Clone the repository:
```bash
git clone https://github.com/JerRenWong/OpenAI-Discord-Bot.git
cd OpenAI-Discord-Bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your API keys:
```env
DISCORD_BOT_TOKEN=your_discord_bot_token
OPENAI_API_KEY=your_openai_api_key
```

4. Run the bot:
```bash
python main.py
```

## Discord Instructions

1. Start a thread in any channel where the bot has access
2. The bot will automatically respond to messages in the thread
3. Use `!clear` command to clear the conversation history in the current thread

## Note

The bot uses GPT-4o by default, but you can modify the model in the code if needed.
