import os
import logging
import json
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
API_TOKEN = os.getenv('API_KEY')

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
ASK_AGE, ASK_HISTORY, ASK_COMPLAINT, ASK_ACTIONS, FOLLOW_UP = range(5)


def ask_openrouter(question: str) -> str:
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_TOKEN}",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": "google/gemini-2.0-pro-exp-02-05:free",
                "messages": [
                    {"role": "system", "content": "Anda adalah seorang dokter yang memberikan informasi medis yang akurat kepada pasien. Jawablah setiap pertanyaan dengan penjelasan yang singkat, padat, jelas, akurat, dan sesuai dengan praktik kedokteran yang valid. Anda boleh memberikan rekomendasi obat. Jika gejala yang dialami pasien memerlukan pemeriksaan lebih lanjut, sarankan untuk berkonsultasi langsung dengan tenaga medis. Jangan pernah memberikan rekomendasi yang bertentangan dengan standar medis yang berlaku. Jika pertanyaan yang dimaksud tidak berkaitan dengan keluhan medis, jawablah dengan 'Maaf, saya tidak dapat membantu dengan pertanyaan ini.' Semua jawaban harus dalam format teks biasa tanpa tambahan format atau gaya apapun."},
                    {"role": "user", "content": question}
                ]
            })
        )
        response_json = response.json()
        return response_json.get("choices", [{}])[0].get("message", {}).get("content", "Maaf, saya tidak bisa memahami pertanyaan Anda. Silakan ajukan pertanyaan yang lebih jelas.").strip()
    except Exception as e:
        logger.error(f"Error saat menghubungi OpenRouter: {e}")
        return "Terjadi kesalahan saat menghubungi sistem. Silakan coba lagi nanti."


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Halo! Saya adalah Dokter AI yang siap mendengar keluhan kesehatan Anda. Sebelum saya memberikan informasi, saya perlu mengumpulkan beberapa data.")
    await update.message.reply_text("Berapa usia Anda?")
    return ASK_AGE


async def ask_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["age"] = update.message.text
    await update.message.reply_text("Apakah Anda memiliki riwayat penyakit tertentu? Jika tidak, ketik 'Tidak ada'.")
    return ASK_HISTORY


async def ask_history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["history"] = update.message.text
    await update.message.reply_text("Apa keluhan kesehatan yang Anda rasakan saat ini?")
    return ASK_COMPLAINT


async def ask_complaint(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["complaint"] = update.message.text
    await update.message.reply_text("Apa saja yang sudah Anda lakukan untuk mengatasi keluhan ini?")
    return ASK_ACTIONS


async def ask_actions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["actions"] = update.message.text

    user_info = (
        f"Sekarang saya berusia {context.user_data['age']} tahun.\n"
        f"Riwayat penyakit saya sebelumnya {context.user_data['history']}\n"
        f"Keluhan saya saat ini adalah {context.user_data['complaint']}\n"
        f"Tindakan yang sudah saya lakukan adalah {context.user_data['actions']}\n\n"
        f"Tolong berikan informasi medis yang jelas dan akurat berdasarkan keluhan saya."
    )

    response = ask_openrouter(user_info)
    await update.message.reply_text(response)
    await update.message.reply_text("Semoga informasi ini bermanfaat. Apakah ada hal lain yang ingin Anda tanyakan?")
    return FOLLOW_UP


async def follow_up(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_question = update.message.text
    response = ask_openrouter(user_question)
    await update.message.reply_text(response)
    await update.message.reply_text("Apakah masih ada yang ingin Anda tanyakan?")
    return FOLLOW_UP


def main() -> None:
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_age)],
            ASK_HISTORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_history)],
            ASK_COMPLAINT: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_complaint)],
            ASK_ACTIONS: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_actions)],
            FOLLOW_UP: [MessageHandler(filters.TEXT & ~filters.COMMAND, follow_up)],
        },
        fallbacks=[],
    )

    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
