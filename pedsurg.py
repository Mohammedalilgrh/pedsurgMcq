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
# FULL CHAPTERS LIST (All 76)
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
    "Chapter 76 – Bariatric Surgical Procedures in Adolescence"
]

# =====================================
# BOT HANDLERS
# =====================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start with TWO buttons"""
    keyboard = [
        [InlineKeyboardButton("📘 MCQs", callback_data="type_MCQs_0")],
        [InlineKeyboardButton("🧠 Flash Cards", callback_data="type_Flash_0")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = "👋 *Welcome to Pediatric Surgery IQ*\n\nWhat would you like to study today?"
    
    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def paginate_chapters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show chapters with full names (10 per page)"""
    query = update.callback_query
    await query.answer()
    
    # Data format: type_[CONTENT]_[PAGE]
    parts = query.data.split("_")
    content_type = parts[1]
    page = int(parts[2])
    
    context.user_data["content_type"] = content_type
    
    per_page = 10
    start_idx = page * per_page
    end_idx = start_idx + per_page
    subset = CHAPTERS[start_idx:end_idx]
    
    keyboard = []
    for i, name in enumerate(subset):
        actual_index = start_idx + i
        keyboard.append([InlineKeyboardButton(name, callback_data=f"ch_{actual_index}")])
    
    # Navigation
    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton("⬅️ Prev", callback_data=f"type_{content_type}_{page-1}"))
    if end_idx < len(CHAPTERS):
        nav_row.append(InlineKeyboardButton("Next ➡️", callback_data=f"type_{content_type}_{page+1}"))
    
    if nav_row:
        keyboard.append(nav_row)
        
    keyboard.append([InlineKeyboardButton("🏠 Back to Main Menu", callback_data="back_start")])

    await query.edit_message_text(
        f"📚 *Select a Chapter* ({content_type})\nPage: {page+1}\n\nChoose a topic below:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def chapter_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Payment screen with directed emoji logic"""
    query = update.callback_query
    await query.answer()
    
    idx = int(query.data.split("_")[1])
    chapter = CHAPTERS[idx]
    content_type = context.user_data.get("content_type", "Content")
    
    payment_text = (
        f"💳 *Payment Required*\n\n"
        f"To receive *{content_type}* materials for:\n*{chapter}*\n\n"
        f"Send *5,000 IQD* to:\n\n"
        f"📲 *Zain Cash:* 009647833160006\n"
        f"💳 *Master Card:* 2058473725\n\n"
        f"📸 Take a screenshot and send it to our chatbot:\n👇🏽"
    )
    
    keyboard = [
        [InlineKeyboardButton("💬 Chat with Admin / Send Screenshot", url=f"https://t.me/{CHATBOT_USERNAME[1:]}")],
        [InlineKeyboardButton("⬅️ Back to Chapters", callback_data=f"type_{content_type}_0")]
    ]
    
    await query.edit_message_text(payment_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    
    # Notify Admin Channel
    user = query.from_user
    admin_msg = (
        "🚀 *NEW SALE INQUIRY*\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"👤 *Client:* {user.full_name}\n"
        f"🆔 *ID:* `{user.id}`\n"
        f"🏷 *Username:* @{user.username if user.username else 'None'}\n"
        f"🎯 *Choice:* {content_type}\n"
        f"📖 *Topic:* {chapter}\n"
        "━━━━━━━━━━━━━━━━━━"
    )
    
    # Direct link to chat with client
    admin_kb = [[InlineKeyboardButton("📩 Contact Client Now", url=f"tg://user?id={user.id}")]]
    
    try:
        await context.bot.send_message(
            chat_id=ADMIN_CHANNEL, 
            text=admin_msg, 
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(admin_kb)
        )
    except:
        pass

# =====================================
# KEEP ALIVE (FOR RENDER)
# =====================================
async def handle(request):
    return web.Response(text="Bot is running")

def run_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(runner.setup())
    port = int(os.environ.get('PORT', 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    loop.run_until_complete(site.start())
    loop.run_forever()

# =====================================
# RUN BOT
# =====================================
if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(start, pattern="back_start"))
    app.add_handler(CallbackQueryHandler(paginate_chapters, pattern="^type_"))
    app.add_handler(CallbackQueryHandler(chapter_selected, pattern="^ch_"))
    
    print("Bot is started. Chapters ready.")
    app.run_polling()
