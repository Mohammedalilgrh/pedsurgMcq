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
WELCOME_TEXT = "👋 Welcome to Pediatric Surgery IQ\n\nWhat would you like to study today?"

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
# BOT HANDLERS
# =====================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton("📘 MRCS", callback_data="MRCS"),
        InlineKeyboardButton("🧠 Flash Cards", callback_data="Flash_Cards")
    ]]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        WELCOME_TEXT,
        reply_markup=reply_markup
    )

async def content_type_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    content_type = "MRCS" if query.data == "MRCS" else "Flash Cards"
    context.user_data["content_type"] = content_type
    
    # Create chapter buttons (3 per row)
    keyboard = []
    for i in range(0, len(CHAPTERS), 3):
        row = []
        for j in range(3):
            if i + j < len(CHAPTERS):
                chapter_num = i + j + 1
                row.append(InlineKeyboardButton(str(chapter_num), callback_data=f"ch_{i+j}"))
        if row:
            keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton("⬅ Back", callback_data="back_start")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"📖 Select a Chapter\n\nContent Type: {content_type}\nTotal: {len(CHAPTERS)} chapters",
        reply_markup=reply_markup
    )

async def chapter_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    idx = int(query.data.split("_")[1])
    chapter = CHAPTERS[idx]
    content_type = context.user_data.get("content_type", "Content")
    
    payment_text = f"""💳 Payment Required

To receive {content_type} about {chapter}, send 5,000 IQD to:

📱 Zain Cash: 009647833160006
💳 Master Card: 3175657935

📸 Take a screenshot and send it to:
@{CHATBOT_USERNAME}

You are ready ✅

🍀 Good luck and enjoy the challenge 🙏"""
    
    keyboard = [[
        InlineKeyboardButton("💬 Chat with Admin", url=f"https://t.me/{CHATBOT_USERNAME}")
    ], [
        InlineKeyboardButton("⬅ Back to Chapters", callback_data="back_chapters")
    ]]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        payment_text,
        reply_markup=reply_markup
    )
    
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

💬 Chat with Client: tg://user?id={user_id}"""
        
        await context.bot.send_message(
            chat_id=ADMIN_CHANNEL,
            text=admin_message
        )
    except Exception as e:
        print(f"Admin error: {e}")

async def back_to_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [[
        InlineKeyboardButton("📘 MRCS", callback_data="MRCS"),
        InlineKeyboardButton("🧠 Flash Cards", callback_data="Flash_Cards")
    ]]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        WELCOME_TEXT,
        reply_markup=reply_markup
    )

async def back_to_chapters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await content_type_selected(update, context)

# =====================================
# BOT SETUP FUNCTION
# =====================================
def setup_bot():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(content_type_selected, pattern="^(MRCS|Flash_Cards)$"))
    application.add_handler(CallbackQueryHandler(chapter_selected, pattern="^ch_"))
    application.add_handler(CallbackQueryHandler(back_to_start, pattern="^back_start$"))
    application.add_handler(CallbackQueryHandler(back_to_chapters, pattern="^back_chapters$"))
    
    return application

# =====================================
# MAIN FUNCTION
# =====================================
def main():
    print("Starting Pediatric Surgery IQ Bot...")
    
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    time.sleep(3)
    
    application = setup_bot()
    print("Bot is running...")
    
    application.run_polling(
        drop_pending_updates=True,
        poll_interval=0.5,
        timeout=30
    )

if __name__ == "__main__":
    main()
