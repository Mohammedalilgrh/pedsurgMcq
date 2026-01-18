from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
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
# CONFIG
# =====================================
BOT_TOKEN = "8408158472:AAHbXpv2WJeubnkdlKJ6CMSV4zA4G54X-gY"
ADMIN_CHANNEL = "@clientpedsurg"
CHATBOT_USERNAME = "PedSurgIQ"

# =====================================
# TEXTS
# =====================================
WELCOME_TEXT = "👋 *Welcome to Pediatric Surgery IQ*\n\nWhat would you like to study today?"

# =====================================
# ALL 76 CHAPTERS
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

# =====================================
# BOT HANDLERS
# =====================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton("📘 MRCS", callback_data="MRCS"),
        InlineKeyboardButton("🧩 Flash Cards", callback_data="Flash_Cards")
    ]]
    await update.message.reply_text(
        WELCOME_TEXT,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def content_type_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    content_type = "MRCS" if query.data == "MRCS" else "Flash Cards"
    context.user_data["content_type"] = content_type

    # Build chapter buttons (2 per row)
    keyboard = []
    for i in range(0, len(CHAPTERS), 2):
        row = []
        row.append(InlineKeyboardButton(f"Ch {i+1}", callback_data=f"ch_{i}"))
        if i + 1 < len(CHAPTERS):
            row.append(InlineKeyboardButton(f"Ch {i+2}", callback_data=f"ch_{i+1}"))
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="back_start")])
    await query.message.reply_text(
        f"📚 *Select a Chapter*\n\nContent Type: *{content_type}*",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )
    # Do NOT edit — send new message

async def chapter_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    idx = int(query.data.split("_")[1])
    chapter = CHAPTERS[idx]
    content_type = context.user_data.get("content_type", "Content")

    payment_text = f"""💰 *Payment Required*

To receive *{content_type}* about *{chapter}*, send *5,000 IQD* to:

📱 *Zain Cash:* 009647833160006  
💳 *Master Card:* 3175657935

📸 Take a screenshot and send it to:
@{CHATBOT_USERNAME}

You are ready ✅

🍀 Good luck and enjoy the challenge 🙏"""

    keyboard = [
        [InlineKeyboardButton("💬 Chat with Admin", url=f"https://t.me/{CHATBOT_USERNAME}")],
        [InlineKeyboardButton("🔙 Back to Chapters", callback_data="back_chapters")]
    ]

    await query.message.reply_text(
        payment_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

    # Notify admin
    await notify_admin(context, query.from_user, content_type, chapter)

async def notify_admin(context: ContextTypes.DEFAULT_TYPE, user, content_type: str, chapter: str):
    try:
        user_id = user.id
        username = f"@{user.username}" if user.username else "No username"
        name = user.first_name or "No name"

        admin_message = f"""🆕 New Client Inquiry
👤 Name: {name}
📱 Username: {username}
🆔 User ID: {user_id}
📚 Type: {content_type}
📖 Chapter: {chapter}

💬 [Chat with Client](tg://user?id={user_id})"""

        await context.bot.send_message(
            chat_id=ADMIN_CHANNEL,
            text=admin_message,
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"Admin notification error: {e}")

async def back_to_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [[
        InlineKeyboardButton("📘 MRCS", callback_data="MRCS"),
        InlineKeyboardButton("🧩 Flash Cards", callback_data="Flash_Cards")
    ]]
    await query.message.reply_text(
        WELCOME_TEXT,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def back_to_chapters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    # Reuse the same logic as content_type_selected but without changing content type
    content_type = context.user_data.get("content_type", "MRCS")
    keyboard = []
    for i in range(0, len(CHAPTERS), 2):
        row = []
        row.append(InlineKeyboardButton(f"Ch {i+1}", callback_data=f"ch_{i}"))
        if i + 1 < len(CHAPTERS):
            row.append(InlineKeyboardButton(f"Ch {i+2}", callback_data=f"ch_{i+1}"))
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="back_start")])

    await query.message.reply_text(
        f"📚 *Select a Chapter*\n\nContent Type: *{content_type}*",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )
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
    application.add_handler(CallbackQueryHandler(content_type_selected, pattern="^(MRCS|Flash_Cards)$"))
    application.add_handler(CallbackQueryHandler(chapter_selected, pattern=r"^ch_\d+$"))
    application.add_handler(CallbackQueryHandler(back_to_start, pattern="^back_start$"))
    application.add_handler(CallbackQueryHandler(back_to_chapters, pattern="^back_chapters$"))

    return application

# =====================================
# MAIN
# =====================================
def main():
    print("🚀 Starting Pediatric Surgery IQ Bot...")

    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    time.sleep(3)

    application = setup_bot()
    print("🤖 Bot is running...")
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
