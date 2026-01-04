import os

import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, MessageHandler, filters

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000/api")
BOT_TOKEN = os.getenv("BOT_TOKEN")

SUBJECT, QUESTION, TOPIC, PAGES, SLIDES = range(5)


def build_api_headers(token):
    return {"Authorization": f"Bearer {token}"}


async def start(update: Update, context):
    await update.message.reply_text(
        "Добро пожаловать! Отправьте /login email пароль для входа или /register для регистрации."
    )


async def register(update: Update, context):
    await update.message.reply_text("Регистрация доступна на сайте: https://example.com/register")


async def login(update: Update, context):
    try:
        _, email, password = update.message.text.split()
    except ValueError:
        await update.message.reply_text("Используйте: /login email пароль")
        return
    response = requests.post(f"{API_URL}/auth/login", json={"email": email, "password": password}, timeout=10)
    if response.status_code != 200:
        await update.message.reply_text("Не удалось войти")
        return
    token = response.json()["access"]
    context.user_data["token"] = token
    await update.message.reply_text("Вход выполнен")


async def solve_start(update: Update, context):
    await update.message.reply_text("Введите предмет")
    return SUBJECT


async def solve_subject(update: Update, context):
    context.user_data["subject"] = update.message.text
    await update.message.reply_text("Введите задачу")
    return QUESTION


async def solve_question(update: Update, context):
    token = context.user_data.get("token")
    payload = {
        "subject": context.user_data.get("subject"),
        "question": update.message.text,
    }
    response = requests.post(
        f"{API_URL}/task/solve",
        json=payload,
        headers=build_api_headers(token),
        timeout=20,
    )
    if response.status_code == 200:
        await update.message.reply_text(response.json().get("answer"))
    else:
        await update.message.reply_text("Ошибка решения задачи")
    return ConversationHandler.END


async def write_start(update: Update, context):
    await update.message.reply_text("Введите тему работы")
    return TOPIC


async def write_topic(update: Update, context):
    context.user_data["topic"] = update.message.text
    await update.message.reply_text("Введите количество страниц")
    return PAGES


async def write_pages(update: Update, context):
    token = context.user_data.get("token")
    response = requests.post(
        f"{API_URL}/work/create",
        json={"topic": context.user_data.get("topic"), "pages": int(update.message.text)},
        headers=build_api_headers(token),
        timeout=20,
    )
    if response.status_code == 200:
        await update.message.reply_text(f"Файл: {response.json().get('file_url')}")
    else:
        await update.message.reply_text("Ошибка генерации работы")
    return ConversationHandler.END


async def ppt_start(update: Update, context):
    await update.message.reply_text("Введите тему презентации")
    return TOPIC


async def ppt_topic(update: Update, context):
    context.user_data["topic"] = update.message.text
    await update.message.reply_text("Введите количество слайдов")
    return SLIDES


async def ppt_slides(update: Update, context):
    token = context.user_data.get("token")
    response = requests.post(
        f"{API_URL}/presentation/create",
        json={"topic": context.user_data.get("topic"), "slides": int(update.message.text)},
        headers=build_api_headers(token),
        timeout=20,
    )
    if response.status_code == 200:
        await update.message.reply_text(f"Файл: {response.json().get('file_url')}")
    else:
        await update.message.reply_text("Ошибка генерации презентации")
    return ConversationHandler.END


async def exam(update: Update, context):
    token = context.user_data.get("token")
    subjects = update.message.text.replace("/exam", "").strip().split(",")
    response = requests.post(
        f"{API_URL}/exam/prepare",
        json={"subjects": subjects},
        headers=build_api_headers(token),
        timeout=20,
    )
    if response.status_code == 200:
        await update.message.reply_text("Материалы подготовлены")
    else:
        await update.message.reply_text("Ошибка подготовки")


async def subscribe(update: Update, context):
    await update.message.reply_text("Выберите тариф: https://example.com/plans")


def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is required")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("register", register))
    app.add_handler(CommandHandler("login", login))
    app.add_handler(CommandHandler("exam", exam))
    app.add_handler(CommandHandler("subscribe", subscribe))

    solve_conv = ConversationHandler(
        entry_points=[CommandHandler("solve", solve_start)],
        states={
            SUBJECT: [MessageHandler(filters.TEXT & ~filters.COMMAND, solve_subject)],
            QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, solve_question)],
        },
        fallbacks=[],
    )

    write_conv = ConversationHandler(
        entry_points=[CommandHandler("write", write_start)],
        states={
            TOPIC: [MessageHandler(filters.TEXT & ~filters.COMMAND, write_topic)],
            PAGES: [MessageHandler(filters.TEXT & ~filters.COMMAND, write_pages)],
        },
        fallbacks=[],
    )

    ppt_conv = ConversationHandler(
        entry_points=[CommandHandler("ppt", ppt_start)],
        states={
            TOPIC: [MessageHandler(filters.TEXT & ~filters.COMMAND, ppt_topic)],
            SLIDES: [MessageHandler(filters.TEXT & ~filters.COMMAND, ppt_slides)],
        },
        fallbacks=[],
    )

    app.add_handler(solve_conv)
    app.add_handler(write_conv)
    app.add_handler(ppt_conv)
    app.run_polling()


if __name__ == "__main__":
    main()
