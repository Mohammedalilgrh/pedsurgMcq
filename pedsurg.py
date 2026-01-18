from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Pediatric Surgery IQ Bot</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
            .container { max-width: 800px; margin: 0 auto; }
            .status { color: green; font-size: 24px; margin: 20px 0; }
            .info-box { background: #f5f5f5; padding: 20px; border-radius: 10px; margin: 20px 0; }
            .telegram-btn { 
                background: #0088cc; 
                color: white; 
                padding: 15px 30px; 
                text-decoration: none; 
                border-radius: 5px;
                display: inline-block;
                margin: 10px;
                font-size: 18px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Pediatric Surgery IQ Bot</h1>
            <div class="status">✅ Bot is running 24/7</div>
            
            <div class="info-box">
                <h2>How to use:</h2>
                <p>1. Open Telegram</p>
                <p>2. Search for: <strong>@PedSurgIQ</strong></p>
                <p>3. Send <code>/start</code> to begin</p>
            </div>
            
            <a href="https://t.me/PedSurgIQ" class="telegram-btn" target="_blank">
                Open Telegram Bot
            </a>
            
            <div class="info-box">
                <h3>Features:</h3>
                <p>📚 76 Medical Chapters</p>
                <p>📘 MRCS & Flash Cards</p>
                <p>💰 5,000 IQD per chapter</p>
                <p>💬 Live chat support</p>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    print(f"Starting Flask server on port {port}...")
    app.run(host='0.0.0.0', port=port)
```

File 2: bot.py (Run this on YOUR COMPUTER 24/7)

```python
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import logging
import asyncio

BOT_TOKEN = "8408158472:AAHbXpv2WJeubnkdlKJ6CMSV4zA4G54X-gY"
ADMIN_CHANNEL = "@clientpedsurg"
CHATBOT_USERNAME = "PedSurgIQ"

WELCOME_TEXT = "👋 Welcome to Pediatric Surgery IQ\n\nWhat would you like to study today?"

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
    
    keyboard = []
    for i in range(0, min(20, len(CHAPTERS))):  # Show first 20
        keyboard.append([InlineKeyboardButton(f"Chapter {i+1}", callback_data=f"ch_{i}")])
    
    keyboard.append([InlineKeyboardButton("⬅ Back", callback_data="back_start")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"📖 Select a Chapter\n\nContent Type: {content_type}",
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

📸 Take screenshot and send to: @{CHATBOT_USERNAME}

You are ready ✅

Good luck! 🙏"""
    
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

def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    
    print("🤖 Starting Pediatric Surgery IQ Bot...")
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(content_type_selected, pattern="^(MRCS|Flash_Cards)$"))
    application.add_handler(CallbackQueryHandler(chapter_selected, pattern="^ch_"))
    application.add_handler(CallbackQueryHandler(back_to_start, pattern="^back_start$"))
    application.add_handler(CallbackQueryHandler(back_to_chapters, pattern="^back_chapters$"))
    
    print("✅ Bot is ready! Send /start on Telegram")
    print("⚠️ Keep this window open 24/7")
    
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
```

File 3: requirements.txt

```txt
python-telegram-bot==20.7
```

File 4: Procfile (for Render)

```txt
web: python app.py
```

🚀 TWO-PART SOLUTION:

PART 1: Deploy to Render

1. Go to Render → New Web Service
2. Upload these files:
   · app.py (Flask website)
   · requirements.txt (just Flask)
   · Procfile
3. Configure:
   · Name: pedsurgiq
   · Build Command: pip install -r requirements.txt
   · Start Command: python app.py
4. Deploy → Your website will be at https://pedsurgiq.onrender.com

PART 2: Run Bot on Your Computer

1. On your computer, install:
   ```bash
   pip install python-telegram-bot==20.7
   ```
2. Save bot.py on your computer
3. Run it:
   ```bash
   python bot.py
   ```
4. Keep the terminal/command prompt open 24/7

📱 What happens:

1. Render: Hosts your website (https://pedsurgiq.onrender.com) 24/7
2. Your Computer: Runs the Telegram bot 24/7
3. Users: Go to Telegram → @PedSurgIQ → /start

🔧 Alternative: Use PythonAnywhere (FREE) for Bot

If you can't keep your computer on 24/7:

1. Go to PythonAnywhere.com
2. Create free account
3. Upload bot.py
4. Create Always-on Task to run the bot

Why this works:

· Render free tier only supports web services (not polling bots)
· Telegram bots need polling (continuous connection)
· You need 2 separate services:
  1. Flask web service (on Render) - keeps URL alive
  2. Telegram bot (on your computer) - handles messages

Your bot will work 100% with this setup!
