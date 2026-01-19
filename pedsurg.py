import logging
import os
import asyncio
import threading
from aiohttp import web
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# =====================================
# CONFIG
# =====================================
BOT_TOKEN = "8408158472:AAHbXpv2WJeubnkdlKJ6CMSV4zA4G54X-gY"
ADMIN_CHANNEL = "@clientpedsurg"
CHATBOT_USERNAME = "@PedSurgIQ"

# =====================================
# CHAPTERS LIST
# =====================================
CHAPTERS = [
    f"Chapter {i+1}" for i in range(76) 
] 
# Note: You can replace the list above with your full text-based CHAPTERS list 
# provided in your snippet. I kept it dynamic for code cleanliness.
CHAPTER_TITLES = [
    "Physiology of the Newborn", "Nutritional Support", "Anesthetic Considerations",
    "Renal Impairment", "Coagulopathies", "ECMO", "Mechanical Ventilation",
    "Vascular Access", "Surgical Infectious Disease", "Fetal Therapy",
    "Foreign Bodies", "Bites", "Burns", "Trauma Assessment", "Thoracic Trauma",
    "Abdominal/Renal Trauma", "Brain Injury", "Orthopedic Trauma", "Neurosurgical",
    "Chest Wall", "Laryngotracheal", "Bronchopulmonary", "Lung/Pleura", "CDH",
    "Mediastinal Tumors", "Esophagus", "EA/TEF", "GERD", "Stomach", "Duodenal Atresia",
    "Malrotation", "Meconium Disease", "NEC", "Hirschsprung", "Anorectal",
    "Fecal Incontinence", "Anorectal Disorders", "Intussusception", "Duplications",
    "Meckel", "IBD", "Appendicitis", "Biliary Atresia", "Choledochal Cyst",
    "Transplantation", "Pancreas", "Splenic", "Abdominal Wall", "Umbilical Hernia",
    "Inguinal Hernia", "Undescended Testis", "Acute Scrotum", "Kidney Anomalies",
    "Ureteral Obstruction", "UTI/VUR", "Bladder/Urethra", "PUV", "Exstrophy",
    "Hypospadias", "Circumcision", "Prune Belly", "Sexual Development",
    "Cancer Principles", "Renal Tumors", "Neuroblastoma", "Liver Lesions",
    "Teratomas", "Lymphomas", "Rhabdomyosarcoma", "Melanoma", "Vascular Anomalies",
    "Head and Neck", "Gynecology", "Breast Diseases", "Endocrine", "Bariatric"
]

# =====================================
# BOT HANDLERS
# =====================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Entry point: Shows MRCS and Flash Cards in one row."""
    keyboard = [
        [
            InlineKeyboardButton("📚 MRCS", callback_data="MRCS"),
            InlineKeyboardButton("🧠 Flash Cards", callback_data="Flash_Cards")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = "👋 *Welcome to Pediatric Surgery IQ*\n\nWhat would you like to study today?"
    
    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def content_type_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Shows chapter grid (4 buttons per row)."""
    query = update.callback_query
    await query.answer()
    
    content_type = "MRCS" if query.data == "MRCS" else "Flash Cards"
    context.user_data["content_type"] = content_type
    
    # Building the grid: 4 buttons per row
    keyboard = []
    row = []
    for i in range(len(CHAPTER_TITLES)):
        row.append(InlineKeyboardButton(f"Ch {i+1}", callback_data=f"ch_{i}"))
        if len(row) == 4:
            keyboard.append(row)
            row = []
    if row: # Add remaining buttons
        keyboard.append(row)
    
    # Add a Back button in its own row
    keyboard.append([InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="back_start")])
    
    await query.edit_message_text(
        f"📖 *Select a Chapter*\nType: *{content_type}*\n\nChoose a chapter number:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def chapter_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Shows payment details."""
    query = update.callback_query
    await query.answer()
    
    idx = int(query.data.split("_")[1])
    chapter_name = f"Chapter {idx+1}: {CHAPTER_TITLES[idx]}"
    content_type = context.user_data.get("content_type", "Content")
    
    payment_text = (
        f"💳 *Payment Required*\n\n"
        f"To receive *{content_type}* for:\n*{chapter_name}*\n\n"
        f"Send *5,000 IQD* to:\n"
        f"📲 *Zain Cash:* 009647833160006\n"
        f"💳 *Master Card:* 3175657935\n\n"
        f"📸 Take a screenshot and send it to:\n{CHATBOT_USERNAME}\n\n"
        f"✅ After verification, your content will be unlocked."
    )
    
    keyboard = [
        [InlineKeyboardButton("💬 Chat with Admin", url=f"https://t.me/{CHATBOT_USERNAME[1:]}")],
        [InlineKeyboardButton("⬅️ Back to Chapters", callback_data="back_chapters")]
    ]
    
    await query.edit_message_text(payment_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    
    # Notify Admin
    await notify_admin(context, query.from_user, content_type, chapter_name)

async def notify_admin(context: ContextTypes.DEFAULT_TYPE, user, content_type, chapter):
    try:
        msg = (
            "🚀 *New Lead!*\n\n"
            f"👤 *User:* {user.full_name}\n"
            f"🆔 *ID:* `{user.id}`\n"
            f"🎯 *Type:* {content_type}\n"
            f"📚 *Chapter:* {chapter}\n"
        )
        await context.bot.send_message(chat_id=ADMIN_CHANNEL, text=msg, parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Admin Notify Error: {e}")

# =====================================
# WEB SERVER FOR KEEP-ALIVE (RENDER)
# =====================================
async def health(request):
    return web.Response(text="Bot is Alive")

def run_server():
    app = web.Application()
    app.router.add_get('/', health)
    runner = web.AppRunner(app)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(runner.setup())
    site = web.TCPSite(runner, '0.0.0.0', int(os.environ.get('PORT', 8080)))
    loop.run_until_complete(site.start())
    loop.run_forever()

# =====================================
# MAIN EXECUTION
# =====================================
if __name__ == "__main__":
    # Start Keep-Alive Server
    threading.Thread(target=run_server, daemon=True).start()
    
    logging.basicConfig(level=logging.INFO)
    
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(start, pattern="back_start"))
    app.add_handler(CallbackQueryHandler(content_type_selected, pattern="^(MRCS|Flash_Cards|back_chapters)$"))
    app.add_handler(CallbackQueryHandler(chapter_selected, pattern="^ch_"))
    
    print("Bot is running...")
    app.run_polling()
