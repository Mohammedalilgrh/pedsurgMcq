from flask import Flask
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import logging
import threading
import time
import os

# =====================================
# FLASK APP FOR KEEP-ALIVE
# =====================================
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Pediatric Surgery IQ Bot is running!"

@app.route('/health')
def health():
    return "OK", 200

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

# =====================================
# CONFIGURATION
# =====================================
BOT_TOKEN = "8408158472:AAHbXpv2WJeubnkdlKJ6CMSV4zA4G54X-gY"
ADMIN_CHANNEL = "@clientpedsurg"
CHATBOT_USERNAME = "PedSurgIQ"

# =====================================
# TEXTS
# =====================================
WELCOME_TEXT = "👋 *Welcome to Pediatric Surgery IQ*\n\nWhat would you like to study today?"

# =====================================
# ALL 76 CHAPTERS (FULL TITLES)
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
    "Chapter 9 – Surgical Infectious Disease",    "Chapter 10 – Fetal Therapy",
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
    "Chapter 21 – Congenital Diaphragmatic Hernia",
    "Chapter 22 – Tracheoesophageal Fistula and Esophageal Atresia",
    "Chapter 23 – Gastroesophageal Reflux and Its Complications",
    "Chapter 24 – Pyloric Stenosis",
    "Chapter 25 – Malrotation and Volvulus",
    "Chapter 26 – Intussusception",
    "Chapter 27 – Hirschsprung Disease",
    "Chapter 28 – Imperforate Anus and Anorectal Malformations",
    "Chapter 29 – Necrotizing Enterocolitis",
    "Chapter 30 – Short Bowel Syndrome",
    "Chapter 31 – Pediatric Liver Transplantation",
    "Chapter 32 – Biliary Atresia",
    "Chapter 33 – Choledochal Cyst",
    "Chapter 34 – Pancreatitis in Children",
    "Chapter 35 – Appendicitis",
    "Chapter 36 – Meckel Diverticulum",
    "Chapter 37 – Inguinal Hernias and Hydroceles",
    "Chapter 38 – Undescended Testes",
    "Chapter 39 – Disorders of Sexual Development",
    "Chapter 40 – Hypospadias and Epispadias",
    "Chapter 41 – Vesicoureteral Reflux",
    "Chapter 42 – Posterior Urethral Valves",
    "Chapter 43 – Wilms Tumor",
    "Chapter 44 – Neuroblastoma",
    "Chapter 45 – Rhabdomyosarcoma",
    "Chapter 46 – Teratomas and Germ Cell Tumors",
    "Chapter 47 – Thyroglossal Duct Cyst",
    "Chapter 48 – Branchial Cleft Anomalies",
    "Chapter 49 – Neck Masses in Children",
    "Chapter 50 – Pediatric Thyroid Disease",
    "Chapter 51 – Adrenal Tumors",
    "Chapter 52 – Pectus Excavatum and Carinatum",
    "Chapter 53 – Congenital Lung Lesions",
    "Chapter 54 – Esophageal Replacement",
    "Chapter 55 – Gastroschisis and Omphalocele",
    "Chapter 56 – Abdominal Wall Defects",
    "Chapter 57 – Splenic Trauma and Disorders",
    "Chapter 58 – Pediatric Solid Organ Transplantation",
    "Chapter 59 – Lymphatic Malformations",    "Chapter 60 – Hemangiomas and Vascular Anomalies",
    "Chapter 61 – Soft Tissue Sarcomas",
    "Chapter 62 – Bone Tumors in Children",
    "Chapter 63 – Pediatric Oncologic Emergencies",
    "Chapter 64 – Minimally Invasive Surgery in Pediatrics",
    "Chapter 65 – Robotic Surgery in Children",
    "Chapter 66 – Ethics in Pediatric Surgery",
    "Chapter 67 – Pain Management in Pediatric Surgical Patients",
    "Chapter 68 – Fluid and Electrolyte Management",
    "Chapter 69 – Pediatric Surgical Critical Care",
    "Chapter 70 – Neonatal Intestinal Obstruction",
    "Chapter 71 – Colonic Atresia and Stenosis",
    "Chapter 72 – Cloacal Malformations",
    "Chapter 73 – Bladder Exstrophy and Epispadias Complex",
    "Chapter 74 – Prune Belly Syndrome",
    "Chapter 75 – Pediatric Urologic Emergencies",
    "Chapter 76 – Global Pediatric Surgery and Humanitarian Efforts"
]

# Special button texts
BACK_COMMAND = "🔙 Back"
MRCS_OPTION = "📘 MRCS"
FLASH_OPTION = "🧩 Flash Cards"

# =====================================
# TELEGRAM BOT HANDLERS
# =====================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[MRCS_OPTION, FLASH_OPTION]]
    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        one_time_keyboard=True,
        resize_keyboard=True
    )
    await update.message.reply_text(
        WELCOME_TEXT,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    user_data = context.user_data

    if text == MRCS_OPTION or text == FLASH_OPTION:
        content_type = "MRCS" if text == MRCS_OPTION else "Flash Cards"
        user_data["content_type"] = content_type

        # Build keyboard with full chapter names (2 per row)
        keyboard = []        for i in range(0, len(CHAPTERS), 2):
            row = [CHAPTERS[i]]
            if i + 1 < len(CHAPTERS):
                row.append(CHAPTERS[i + 1])
            keyboard.append(row)
        keyboard.append([BACK_COMMAND])

        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            one_time_keyboard=True,
            resize_keyboard=True
        )
        await update.message.reply_text(
            f"📚 *Select a Chapter*\n\nContent Type: *{content_type}*\n\n👇 Tap a chapter below:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

    elif text == BACK_COMMAND:
        keyboard = [[MRCS_OPTION, FLASH_OPTION]]
        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            one_time_keyboard=True,
            resize_keyboard=True
        )
        await update.message.reply_text(
            "🔙 Back to main menu.\n\n" + WELCOME_TEXT,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

    elif text in CHAPTERS:
        content_type = user_data.get("content_type", "Content")
        chapter = text

        payment_text = (
            f"💰 *Payment Required*\n\n"
            f"To receive *{content_type}* about *{chapter}*, send *5,000 IQD* to:\n\n"
            f"📱 *Zain Cash:* 009647833160006\n"
            f"💳 *Master Card:* 3175657935\n\n"
            f"📸 Take a screenshot and send it to:\n"
            f"@{CHATBOT_USERNAME}\n\n"
            f"You are ready ✅\n\n"
            f"🍀 Good luck and enjoy the challenge 🙏"
        )

        await update.message.reply_text(payment_text, parse_mode="Markdown")
        await notify_admin(context, update.message.from_user, content_type, chapter)

    else:        # Unknown input — show main menu
        keyboard = [[MRCS_OPTION, FLASH_OPTION]]
        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            one_time_keyboard=True,
            resize_keyboard=True
        )
        await update.message.reply_text(
            "❓ I didn't understand that. Please choose an option below:",
            reply_markup=reply_markup
        )

async def notify_admin(context: ContextTypes.DEFAULT_TYPE, user, content_type: str, chapter: str):
    try:
        user_id = user.id
        username = f"@{user.username}" if user.username else "No username"
        name = user.first_name or "No name"

        admin_message = (
            f"🆕 New Client Inquiry\n\n"
            f"👤 Name: {name}\n"
            f"📱 Username: {username}\n"
            f"🆔 User ID: {user_id}\n"
            f"📚 Type: {content_type}\n"
            f"📖 Chapter: {chapter}\n\n"
            f"💬 [Chat with Client](tg://user?id={user_id})"
        )

        await context.bot.send_message(
            chat_id=ADMIN_CHANNEL,
            text=admin_message,
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"Admin notification error: {e}")

# =====================================
# BOT SETUP
# =====================================
def setup_bot():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    return application

# =====================================# MAIN ENTRY POINT
# =====================================
def main():
    print("🚀 Starting Pediatric Surgery IQ Bot...")

    # Start Flask keep-alive server in background
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    time.sleep(2)

    # Start Telegram bot
    application = setup_bot()
    print("🤖 Bot is running with bottom reply keyboard...")
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
