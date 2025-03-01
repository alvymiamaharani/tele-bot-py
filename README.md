# Telegram Medical Bot

## Getting Started

### 1. Clone the Repository

```
git clone https://github.com/alvymiamaharani/tele-bot-py
cd tele-bot-py
```

### 2. Create a Virtual Environment

```
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate    # On Windows
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file following `.env.example` and add your credentials:

```shell
BOT_TOKEN=your_telegram_bot_token
API_KEY=your_openrouter_api_key
```

### 5. Run the Bot

```shell
python bot.py
```

## Features

- Conversational AI-powered medical bot
- Asks for user details (age, medical history, complaints, actions taken)
- Provides medical information based on user input
- Allows follow-up questions after initial diagnosis

## Dependencies

- `python-telegram-bot`
- `requests`
- `python-dotenv`
- `logging`

## Deployment

For deployment, you can use a cloud server (e.g., AWS, Heroku) or run the bot on your local machine with a process manager like `systemd` or `pm2`.
