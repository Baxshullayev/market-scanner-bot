import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    CallbackContext,
    filters,
)

# Scrapers
from scrapers.asaxiy import search_asaxiy
from scrapers.olcha import search_olcha
from scrapers.uzum import search_uzum
from scrapers.mediapark import search_mediapark
from scrapers.yandex import search_yandex

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# User database
USERS_FILE = "users.txt"

def save_user(user_id: int):
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            pass
    with open(USERS_FILE, "r+") as f:
        users = f.read().splitlines()
        if str(user_id) not in users:
            f.write(f"{user_id}\n")

async def start(update: Update, context: CallbackContext):
    user = update.effective_user
    save_user(user.id)
    await update.message.reply_text(
        "📦 Salom! Mahsulot nomini yuboring va men sizga Asaxiy, Olcha, Uzum, Mediapark va Yandex Market’dagi narxlarni topib beraman.\n\nMisol: `Redmi Note 12`",
        parse_mode="Markdown"
    )

async def handle_message(update: Update, context: CallbackContext):
    user = update.effective_user
    save_user(user.id)
    query = update.message.text.strip()

    await update.message.reply_text("🔍 Qidirilmoqda...")

    sites = {
        "Asaxiy": search_asaxiy(query),
        "Olcha": search_olcha(query),
        "Uzum": search_uzum(query),
        "Mediapark": search_mediapark(query),
        "Yandex": search_yandex(query),
    }

    messages = []
    for site, data in sites.items():
        if "error" in data:
            messages.append(f"❌ {site}: {data['error']}")
        else:
            messages.append(f"✅ {site}:\n📌 {data['title']}\n💰 {data['price']}\n🔗 [Havola]({data['link']})")

    await update.message.reply_text(
        "\n\n".join(messages),
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

async def broadcast(update: Update, context: CallbackContext):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ Sizda ruxsat yo‘q.")
        return

    text = update.message.text.replace("/broadcast", "").strip()
    if not text:
        await update.message.reply_text("✏️ Xabar yuborish: `/broadcast Xabar matni`", parse_mode="Markdown")
        return

    if not os.path.exists(USERS_FILE):
        await update.message.reply_text("👤 Hech qanday foydalanuvchi yo‘q.")
        return

    with open(USERS_FILE, "r") as f:
        users = f.read().splitlines()

    sent = 0
    for uid in users:
        try:
            await context.bot.send_message(chat_id=int(uid), text=f"📢 {text}")
            sent += 1
        except Exception as e:
            logger.warning(f"Yuborilmadi: {uid} — {e}")

    await update.message.reply_text(f"✅ Xabar {sent} foydalanuvchiga yuborildi.")

async def admin_panel(update: Update, context: CallbackContext):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ Sizda ruxsat yo‘q.")
        return

    keyboard = [
        [InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast")],
        [InlineKeyboardButton("👥 Foydalanuvchilar", callback_data="admin_users")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🛠 Admin paneliga xush kelibsiz:", reply_markup=reply_markup)

async def handle_admin_buttons(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
# This code is a Telegram bot that allows users to search for product prices across multiple online stores in Uzbekistan.
    if query.from_user.id != ADMIN_ID:
        await query.edit_message_text("⛔ Sizda ruxsat yo‘q.")
        return

    if query.data == "admin_broadcast":
        await query.edit_message_text("📨 Iltimos, xabarni `/broadcast XABAR` tarzida yuboring.")
    elif query.data == "admin_users":
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, "r") as f:
                user_count = len(f.read().splitlines())
        else:
            user_count = 0
        await query.edit_message_text(f"👥 Umumiy foydalanuvchilar soni: {user_count} ta")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(CallbackQueryHandler(handle_admin_buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("🤖 Bot ishga tushdi.")
    app.run_polling()

if __name__ == "__main__":
    main()
# This code is a Telegram bot that allows users to search for product prices across multiple online stores in Uzbekistan.