import logging
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand, MenuButtonCommands
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, filters, ContextTypes,
)

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8434025433:AAHctHSmBMpmhQbqFOBCjlU22Bf5HWDZkYs"
CHANNEL = "https://t.me/ZeroShellHQ"
GROUP = "https://t.me/ZeroShellGroup"
ADMIN = "https://t.me/ZeroSheII"

user_lang = {}

TEXTS = {
    'en': {
        'welcome': "👋 Hello {name}!\n\n🤖 Welcome to ZeroShell Bot!\n\n📢 Channel: {channel}\n👥 Group: {group}\n\nSelect an option below:",
        'services': "🛠 Our Services:\n\n☁️ Private Cloud\n📧 Hotmail Checker\n🔀 Mix Checker\n🎯 Custom Target\n🎯 Private Hits\n\n💬 To buy, contact Admin: @ZeroSheII 👇",
        'help': "📚 Commands:\n\n/start - Start Bot\n/help - Help\n/about - About\n/services - Our Services\n\nJoin our community! 👇",
        'about': "🤖 ZeroShell Bot\n\n⚙️ Made with Python\n❤️ Built with love\n\nJoin our community! 👇",
        'join_channel': "📢 Channel",
        'join_group': "👥 Group",
        'contact_admin': "💬 To Buy - Contact Admin",
        'services_btn': "🛠 Services",
        'lang_btn': "🌍 Change Language",
        'hi_reply': "👋 Hello! How are you?\n\nJoin our community! 👇",
        'thanks_reply': "🙏 You're welcome!",
        'bye_reply': "👋 Goodbye! See you soon!",
        'default_reply': "You said: '{msg}' 😊\n\nJoin our group to chat! 👇",
    },
    'ru': {
        'welcome': "👋 Привет {name}!\n\n🤖 Добро пожаловать в ZeroShell Bot!\n\n📢 Канал: {channel}\n👥 Группа: {group}\n\nВыберите вариант ниже:",
        'services': "🛠 Наши услуги:\n\n☁️ Private Cloud\n📧 Hotmail Checker\n🔀 Mix Checker\n🎯 Custom Target\n🎯 Private Hits\n\n💬 Для покупки, напишите Админу: @ZeroSheII 👇",
        'help': "📚 Команды:\n\n/start - Старт\n/help - Помощь\n/about - О боте\n/services - Услуги\n\nПрисоединяйтесь! 👇",
        'about': "🤖 ZeroShell Bot\n\n⚙️ Создан на Python\n❤️ Сделан с любовью\n\nПрисоединяйтесь! 👇",
        'join_channel': "📢 Канал",
        'join_group': "👥 Группа",
        'contact_admin': "💬 Купить - Написать Админу",
        'services_btn': "🛠 Услуги",
        'lang_btn': "🌍 Сменить язык",
        'hi_reply': "👋 Привет! Как дела?\n\nПрисоединяйтесь! 👇",
        'thanks_reply': "🙏 Пожалуйста!",
        'bye_reply': "👋 До свидания!",
        'default_reply': "Вы сказали: '{msg}' 😊\n\nПрисоединяйтесь к группе! 👇",
    }
}

def get_lang(user_id):
    return user_lang.get(user_id, 'en')

def get_main_keyboard(lang):
    t = TEXTS[lang]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t['join_channel'], url=CHANNEL),
         InlineKeyboardButton(t['join_group'], url=GROUP)],
        [InlineKeyboardButton(t['services_btn'], callback_data='services')],
        [InlineKeyboardButton(t['lang_btn'], callback_data='change_lang')],
    ])

def get_link_keyboard(lang):
    t = TEXTS[lang]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t['join_channel'], url=CHANNEL),
         InlineKeyboardButton(t['join_group'], url=GROUP)],
    ])

def get_services_keyboard(lang):
    t = TEXTS[lang]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t['contact_admin'], url=ADMIN)],
        [InlineKeyboardButton(t['join_channel'], url=CHANNEL),
         InlineKeyboardButton(t['join_group'], url=GROUP)],
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🇬🇧 English", callback_data='lang_en')],
        [InlineKeyboardButton("🇷🇺 Русский", callback_data='lang_ru')],
    ])
    await update.message.reply_text(
        "🌍 Please select your language:\n🌍 Пожалуйста, выберите язык:",
        reply_markup=keyboard
    )

async def services_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update.effective_user.id)
    await update.message.reply_text(TEXTS[lang]['services'], reply_markup=get_services_keyboard(lang))

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update.effective_user.id)
    await update.message.reply_text(TEXTS[lang]['help'], reply_markup=get_link_keyboard(lang))

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update.effective_user.id)
    await update.message.reply_text(TEXTS[lang]['about'], reply_markup=get_link_keyboard(lang))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update.effective_user.id)
    t = TEXTS[lang]
    msg = update.message.text.lower()
    if any(w in msg for w in ['hi', 'hello', 'привет', 'здравствуй']):
        await update.message.reply_text(t['hi_reply'], reply_markup=get_link_keyboard(lang))
    elif any(w in msg for w in ['thanks', 'thank you', 'спасибо']):
        await update.message.reply_text(t['thanks_reply'])
    elif any(w in msg for w in ['bye', 'goodbye', 'пока', 'до свидания']):
        await update.message.reply_text(t['bye_reply'])
    else:
        await update.message.reply_text(
            t['default_reply'].format(msg=update.message.text),
            reply_markup=get_link_keyboard(lang)
        )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    if query.data == 'lang_en':
        user_lang[user_id] = 'en'
        lang = 'en'
        await query.edit_message_text(
            TEXTS[lang]['welcome'].format(name=query.from_user.first_name, channel=CHANNEL, group=GROUP),
            reply_markup=get_main_keyboard(lang)
        )
    elif query.data == 'lang_ru':
        user_lang[user_id] = 'ru'
        lang = 'ru'
        await query.edit_message_text(
            TEXTS[lang]['welcome'].format(name=query.from_user.first_name, channel=CHANNEL, group=GROUP),
            reply_markup=get_main_keyboard(lang)
        )
    elif query.data == 'change_lang':
        await query.edit_message_text(
            "🌍 Select language | Выберите язык:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🇬🇧 English", callback_data='lang_en')],
                [InlineKeyboardButton("🇷🇺 Русский", callback_data='lang_ru')],
            ])
        )
    elif query.data == 'services':
        lang = get_lang(user_id)
        await query.edit_message_text(TEXTS[lang]['services'], reply_markup=get_services_keyboard(lang))

async def post_init(application):
    await application.bot.set_my_commands([
        BotCommand("start", "▶️ Start Bot"),
        BotCommand("services", "🛠 Services"),
        BotCommand("help", "ℹ️ Help"),
        BotCommand("about", "🤖 About"),
    ])
    await application.bot.set_chat_menu_button(menu_button=MenuButtonCommands())

# Simple HTTP server to keep Render free tier alive
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ZeroShell Bot is running!")
    def log_message(self, format, *args):
        pass

def run_http_server():
    server = HTTPServer(('0.0.0.0', 8080), HealthHandler)
    server.serve_forever()

def main():
    # Start HTTP server in background thread
    thread = threading.Thread(target=run_http_server, daemon=True)
    thread.start()
    logger.info("✅ Health check server started on port 8080")

    app = Application.builder().token(TOKEN).post_init(post_init).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(CommandHandler("services", services_command))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("✅ ZeroShell Bot Started!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
