# =====================================
# Pediatric Surgery IQ – Marketing Bot
# =====================================

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from flask import Flask, request
import logging
import os

# =====================================
# CONFIG
# =====================================

BOT_TOKEN = "8408158472:AAHbXpv2WJeubnkdlKJ6CMSV4zA4G54X-gY"
ADMIN_CHANNEL = "@clientpedsurg"
WEBHOOK_URL = "https://pedsurgmcq.onrender.com"  # Your Render URL
PORT = int(os.environ.get('PORT', 8080))  # Render provides PORT

# =====================================
# TEXTS
# =====================================

WELCOME_TEXT = (
    "👋 *Welcome to Pediatric Surgery IQ*\n\n"
    "Choose what you want to study:"
)

PAYMENT_TEXT = (
    "💳 *Payment Required*\n\n"
    "To receive content for this chapter, send *5,000 IQD* to:\n\n"
    "📱 *Zain Cash:* 009647833160006\n\n"
    "💳 *Master Card:* 3175657935\n\n"
    "📸 Take a screenshot and send it to:\n"
    "@PedSurgIQ\n\n"
    "You are ready ✅\n\n"
    "🍀 Good luck and enjoy the challenge 🙏"
)

# =====================================
# CHAPTERS (CLEAN & UNIQUE)
# =====================================

CHAPTERS = [
    "Chapter 1 – Physiology of the Newborn",
    "Chapter 2 – Nutritional Support for the Pediatric Patient",
    "Chapter 3 – Anesthetic Considerations for Pediatric Surgical Conditions",
    "Chapter 4 – Renal Impairment and Renovascular Hypertension",
    "Chapter 5 – Coagulopathies and Sickle Cell Disease",
    "Chapter 6 – Extracorporeal Membrane Oxygenation",
    "Chapter 7 – Mechanical Ventilation in Pediatric Surgical Disease",
    "Chapter 8 – Vascular Access",
    "Chapter 9 – Surgical Infectious Disease",
    "Chapter 10 – Fetal Therapy",
    "Chapter 11 – Ingestion of Foreign Bodies",
    "Chapter 12 – Bites",
    "Chapter 13 – Burns",
    "Chapter 14 – Early Assessment and Management of Trauma",
    "Chapter 15 – Thoracic Trauma",
    "Chapter 16 – Abdominal and Renal Trauma",
    "Chapter 17 – Traumatic Brain Injury",
    "Chapter 18 – Pediatric Orthopedic Trauma",
    "Chapter 19 – Neurosurgical Conditions",
    "Chapter 20 – Chest Wall Deformities",
    "Chapter 21 – Management of Laryngotracheal Obstruction in Children",
    "Chapter 22 – Congenital Bronchopulmonary Malformations",
    "Chapter 23 – Acquired Lesions of the Lung and Pleura",
    "Chapter 24 – Congenital Diaphragmatic Hernia and Eventration",
    "Chapter 25 – Mediastinal Tumors",
    "Chapter 26 – The Esophagus",
    "Chapter 27 – Esophageal Atresia and Tracheoesophageal Fistula",
    "Chapter 28 – Gastroesophageal Reflux",
    "Chapter 29 – Lesions of the Stomach",
    "Chapter 30 – Duodenal and Intestinal Atresia and Stenosis",
    "Chapter 31 – Malrotation",
    "Chapter 32 – Meconium Disease",
    "Chapter 33 – Necrotizing Enterocolitis",
    "Chapter 34 – Hirschsprung Disease",
    "Chapter 35 – Anorectal Atresia and Cloacal Malformations",
    "Chapter 36 – Fecal Incontinence and Constipation",
    "Chapter 37 – Acquired Anorectal Disorders",
    "Chapter 38 – Intussusception",
    "Chapter 39 – Alimentary Tract Duplications",
    "Chapter 40 – Meckel Diverticulum",
    "Chapter 41 – Inflammatory Bowel Disease",
    "Chapter 42 – Appendicitis",
    "Chapter 43 – Biliary Atresia",
    "Chapter 44 – Choledochal Cyst and Gallbladder Disease",
    "Chapter 45 – Solid Organ Transplantation in Children",
    "Chapter 46 – Lesions of the Pancreas",
    "Chapter 47 – Splenic Conditions",
    "Chapter 48 – Congenital Abdominal Wall Defects",
    "Chapter 49 – Umbilical and Other Abdominal Wall Hernias",
    "Chapter 50 – Inguinal Hernia",
    "Chapter 51 – Undescended Testes and Testicular Tumors",
    "Chapter 52 – The Acute Scrotum",
    "Chapter 53 – Developmental and Positional Anomalies of the Kidneys",
    "Chapter 54 – Ureteral Obstruction and Malformations",
    "Chapter 55 – Urinary Tract Infections and Vesicoureteral Reflux",
    "Chapter 56 – Bladder and Urethra",
    "Chapter 57 – Posterior Urethral Valves",
    "Chapter 58 – Bladder and Cloacal Exstrophy",
    "Chapter 59 – Hypospadias",
    "Chapter 60 – Circumcision",
    "Chapter 61 – Prune Belly Syndrome",
    "Chapter 62 – Differences of Sexual Development",
    "Chapter 63 – Principles of Adjuvant Therapy in Childhood Cancer",
    "Chapter 64 – Renal Tumors",
    "Chapter 65 – Neuroblastoma",
    "Chapter 66 – Lesions of the Liver",
    "Chapter 67 – Teratomas, Dermoids, and Soft Tissue Tumors",
    "Chapter 68 – Lymphomas",
    "Chapter 69 – Rhabdomyosarcoma",
    "Chapter 70 – Nevus and Melanoma",
    "Chapter 71 – Vascular Anomalies",
    "Chapter 72 – Head and Neck Sinuses and Masses",
    "Chapter 73 – Pediatric and Adolescent Gynecology",
    "Chapter 74 – Breast Diseases",
    "Chapter 75 – Endocrine Disorders and Tumors",
    "Chapter 76 – Bariatric Surgical Procedures in Adolescence",
]

# =====================================
# FLASK APP
# =====================================

app = Flask(__name__)

# Create bot application
bot_application = ApplicationBuilder().token(BOT_TOKEN).build()

# =====================================
# BOT HANDLERS
# =====================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📝 MCQs", callback_data="MCQs")],
        [InlineKeyboardButton("📚 Flash Cards", callback_data="Flash Cards")]
    ]
    
    if update.message:
        await update.message.reply_text(
            WELCOME_TEXT,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
    elif update.callback_query:
        await update.callback_query.message.reply_text(
            WELCOME_TEXT,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

async def show_chapters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    context.user_data["type"] = query.data

    keyboard = [[InlineKeyboardButton(ch, callback_data=f"ch_{i}")]
                for i, ch in enumerate(CHAPTERS)]
    keyboard.append([InlineKeyboardButton("⬅ Back", callback_data="back_home")])

    await query.edit_message_text(
        "📖 *Select a Chapter*",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def chapter_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    idx = int(query.data.split("_")[1])
    chapter = CHAPTERS[idx]
    context.user_data["chapter"] = chapter

    keyboard = [
        [InlineKeyboardButton("💬 Contact Us", callback_data="contact")],
        [InlineKeyboardButton("⬅ Back", callback_data="back_chapters")]
    ]

    await query.edit_message_text(
        f"📌 *{chapter}*\n\n{PAYMENT_TEXT}",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = query.from_user
    username = f"@{user.username}" if user.username else "No username"

    msg = (
        "📩 *New Interested Client*\n\n"
        f"👤 User: {username}\n"
        f"📘 Type: {context.user_data.get('type')}\n"
        f"📖 Chapter: {context.user_data.get('chapter')}"
    )

    await context.bot.send_message(ADMIN_CHANNEL, msg, parse_mode="Markdown")

    await query.edit_message_text(
        "✅ Your request has been sent.\nWe will contact you shortly."
    )

async def back_home(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await start(update, context)

async def back_chapters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await show_chapters(update, context)

async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle unknown commands"""
    if update.message:
        await update.message.reply_text(
            "Sorry, I didn't understand that command. Use /start to begin."
        )

# Setup bot handlers
bot_application.add_handler(CommandHandler("start", start))
bot_application.add_handler(CallbackQueryHandler(show_chapters, pattern="^(MCQs|Flash Cards)$"))
bot_application.add_handler(CallbackQueryHandler(chapter_selected, pattern="^ch_"))
bot_application.add_handler(CallbackQueryHandler(contact, pattern="^contact$"))
bot_application.add_handler(CallbackQueryHandler(back_home, pattern="^back_home$"))
bot_application.add_handler(CallbackQueryHandler(back_chapters, pattern="^back_chapters$"))
bot_application.add_handler(MessageHandler(filters.COMMAND, unknown_command))

# =====================================
# FLASK ROUTES
# =====================================

@app.route("/")
def home():
    return "✅ Pediatric Surgery IQ Bot is running! Send /start on Telegram."

@app.route("/set_webhook", methods=["GET"])
def set_webhook():
    """Set webhook for Telegram bot"""
    webhook_url = f"{WEBHOOK_URL}/webhook"
    success = bot_application.bot.set_webhook(webhook_url)
    if success:
        return f"✅ Webhook set successfully to: {webhook_url}"
    else:
        return "❌ Failed to set webhook"

@app.route("/remove_webhook", methods=["GET"])
def remove_webhook():
    """Remove webhook (use polling for testing)"""
    success = bot_application.bot.delete_webhook()
    if success:
        return "✅ Webhook removed successfully"
    else:
        return "❌ Failed to remove webhook"

@app.route("/webhook", methods=["POST"])
def webhook():
    """Handle incoming updates from Telegram"""
    update = Update.de_json(request.get_json(), bot_application.bot)
    bot_application.update_queue.put_nowait(update)
    return "OK"

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for Render"""
    return "OK", 200

# =====================================
# START BOT
# =====================================

def start_bot():
    """Initialize and start the bot"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Starting Pediatric Surgery IQ Bot...")
    
    # Initialize bot (this starts the update queue)
    bot_application.initialize()
    
    # Set webhook automatically
    webhook_url = f"{WEBHOOK_URL}/webhook"
    bot_application.bot.set_webhook(webhook_url)
    logger.info(f"Webhook set to: {webhook_url}")
    
    logger.info("Bot is ready and waiting for updates...")

# =====================================
# MAIN ENTRY POINT
# =====================================

if __name__ == "__main__":
    # Start the bot
    start_bot()
    
    # Start Flask server
    app.run(host="0.0.0.0", port=PORT, debug=False, use_reloader=False)
