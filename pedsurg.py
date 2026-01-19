# =====================================
# Pediatric Surgery IQ â€“ Marketing Bot
# =====================================

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import logging
import os
import asyncio

# =====================================
# CONFIG
# =====================================

BOT_TOKEN = "8408158472:AAHbXpv2WJeubnkdlKJ6CMSV4zA4G54X-gY"
ADMIN_CHANNEL = "@clientpedsurg"  # Your admin channel
CHATBOT_USERNAME = "@PedSurgIQ"  # Your chatbot username for direct chat

# =====================================
# TEXTS
# =====================================

WELCOME_TEXT = (
    "ðŸ‘‹ *Welcome to Pediatric Surgery IQ*\n\n"
    "What would you like to study today?"
)

PAYMENT_TEXT = (
    "ðŸ’³ *Payment Required*\n\n"
    "To receive *{content_type}* about *{chapter}*, send *5,000 IQD* to:\n\n"
    "ðŸ“± *Zain Cash:* 009647833160006\n"
    "ðŸ’³ *Master Card:* 3175657935\n\n"
    "ðŸ“¸ Take a screenshot and send it to our chatbot:\n"
    f"{CHATBOT_USERNAME}\n\n"
    "You are ready âœ…\n\n"
    "ðŸ€ Good luck and enjoy the challenge ðŸ™"
)

# =====================================
# CHAPTERS
# =====================================

CHAPTERS = [
    "Chapter 1 â€“ Physiology of the Newborn",
    "Chapter 2 â€“ Nutritional Support for the Pediatric Patient",
    "Chapter 3 â€“ Anesthetic Considerations for Pediatric Surgical Conditions",
    "Chapter 4 â€“ Renal Impairment and Renovascular Hypertension",
    "Chapter 5 â€“ Coagulopathies and Sickle Cell Disease",
    "Chapter 6 â€“ Extracorporeal Membrane Oxygenation",
    "Chapter 7 â€“ Mechanical Ventilation in Pediatric Surgical Disease",    "Chapter 8 â€“ Vascular Access",
    "Chapter 9 â€“ Surgical Infectious Disease",
    "Chapter 10 â€“ Fetal Therapy",
    "Chapter 11 â€“ Ingestion of Foreign Bodies",
    "Chapter 12 â€“ Bites",
    "Chapter 13 â€“ Burns",
    "Chapter 14 â€“ Early Assessment and Management of Trauma",
    "Chapter 15 â€“ Thoracic Trauma",
    "Chapter 16 â€“ Abdominal and Renal Trauma",
    "Chapter 17 â€“ Traumatic Brain Injury",
    "Chapter 18 â€“ Pediatric Orthopedic Trauma",
    "Chapter 19 â€“ Neurosurgical Conditions",
    "Chapter 20 â€“ Chest Wall Deformities",
    "Chapter 21 â€“ Management of Laryngotracheal Obstruction in Children",
    "Chapter 22 â€“ Congenital Bronchopulmonary Malformations",
    "Chapter 23 â€“ Acquired Lesions of the Lung and Pleura",
    "Chapter 24 â€“ Congenital Diaphragmatic Hernia and Eventration",
    "Chapter 25 â€“ Mediastinal Tumors",
    "Chapter 26 â€“ The Esophagus",
    "Chapter 27 â€“ Esophageal Atresia and Tracheoesophageal Fistula",
    "Chapter 28 â€“ Gastroesophageal Reflux",
    "Chapter 29 â€“ Lesions of the Stomach",
    "Chapter 30 â€“ Duodenal and Intestinal Atresia and Stenosis",
    "Chapter 31 â€“ Malrotation",
    "Chapter 32 â€“ Meconium Disease",
    "Chapter 33 â€“ Necrotizing Enterocolitis",
    "Chapter 34 â€“ Hirschsprung Disease",
    "Chapter 35 â€“ Anorectal Atresia and Cloacal Malformations",
    "Chapter 36 â€“ Fecal Incontinence and Constipation",
    "Chapter 37 â€“ Acquired Anorectal Disorders",
    "Chapter 38 â€“ Intussusception",
    "Chapter 39 â€“ Alimentary Tract Duplications",
    "Chapter 40 â€“ Meckel Diverticulum",
    "Chapter 41 â€“ Inflammatory Bowel Disease",
    "Chapter 42 â€“ Appendicitis",
    "Chapter 43 â€“ Biliary Atresia",
    "Chapter 44 â€“ Choledochal Cyst and Gallbladder Disease",
    "Chapter 45 â€“ Solid Organ Transplantation in Children",
    "Chapter 46 â€“ Lesions of the Pancreas",
    "Chapter 47 â€“ Splenic Conditions",
    "Chapter 48 â€“ Congenital Abdominal Wall Defects",
    "Chapter 49 â€“ Umbilical and Other Abdominal Wall Hernias",
    "Chapter 50 â€“ Inguinal Hernia",
    "Chapter 51 â€“ Undescended Testes and Testicular Tumors",
    "Chapter 52 â€“ The Acute Scrotum",
    "Chapter 53 â€“ Developmental and Positional Anomalies of the Kidneys",
    "Chapter 54 â€“ Ureteral Obstruction and Malformations",
    "Chapter 55 â€“ Urinary Tract Infections and Vesicoureteral Reflux",
    "Chapter 56 â€“ Bladder and Urethra",
    "Chapter 57 â€“ Posterior Urethral Valves",    "Chapter 58 â€“ Bladder and Cloacal Exstrophy",
    "Chapter 59 â€“ Hypospadias",
    "Chapter 60 â€“ Circumcision",
    "Chapter 61 â€“ Prune Belly Syndrome",
    "Chapter 62 â€“ Differences of Sexual Development",
    "Chapter 63 â€“ Principles of Adjuvant Therapy in Childhood Cancer",
    "Chapter 64 â€“ Renal Tumors",
    "Chapter 65 â€“ Neuroblastoma",
    "Chapter 66 â€“ Lesions of the Liver",
    "Chapter 67 â€“ Teratomas, Dermoids, and Soft Tissue Tumors",
    "Chapter 68 â€“ Lymphomas",
    "Chapter 69 â€“ Rhabdomyosarcoma",
    "Chapter 70 â€“ Nevus and Melanoma",
    "Chapter 71 â€“ Vascular Anomalies",
    "Chapter 72 â€“ Head and Neck Sinuses and Masses",
    "Chapter 73 â€“ Pediatric and Adolescent Gynecology",
    "Chapter 74 â€“ Breast Diseases",
    "Chapter 75 â€“ Endocrine Disorders and Tumors",
    "Chapter 76 â€“ Bariatric Surgical Procedures in Adolescence",
]

# =====================================
# BOT HANDLERS
# =====================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command - Single row with both options"""
    markup = InlineKeyboardMarkup(row_width=2)
    markup.row(
        InlineKeyboardButton("ðŸ“˜ MRCS", callback_data="MRCS"),
        InlineKeyboardButton("ðŸ§  Flash Cards", callback_data="Flash_Cards")
    )
    
    # Check if it's a message or callback query
    if update.message:
        await update.message.reply_text(
            WELCOME_TEXT,
            reply_markup=markup,
            parse_mode="Markdown"
        )
    elif update.callback_query:
        await update.callback_query.edit_message_text(
            WELCOME_TEXT,
            reply_markup=markup,
            parse_mode="Markdown"
        )

async def content_type_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle when user selects MRCS or Flash Cards"""
    query = update.callback_query    await query.answer()
    
    # Store selected content type
    content_type = "MRCS" if query.data == "MRCS" else "Flash Cards"
    context.user_data["content_type"] = content_type
    
    # Create chapter selection keyboard
    markup = InlineKeyboardMarkup(row_width=3)
    for i in range(0, len(CHAPTERS), 3):  # 3 buttons per row
        row = []
        for j in range(3):
            if i + j < len(CHAPTERS):
                chapter_num = i + j + 1
                chapter_text = f"Ch {chapter_num}"
                row.append(InlineKeyboardButton(chapter_text, callback_data=f"ch_{i+j}"))
        if row:
            markup.row(*row)
    
    # Add navigation buttons
    markup.row(
        InlineKeyboardButton("â¬… Back", callback_data="back_start")
    )
    
    await query.edit_message_text(
        f"ðŸ“– *Select a Chapter*\n\n"
        f"Content Type: *{content_type}*\n"
        f"Total Chapters: *{len(CHAPTERS)}*\n\n"
        f"_Click on a chapter number to select:_",
        reply_markup=markup,
        parse_mode="Markdown"
    )

async def chapter_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle when user selects a chapter"""
    query = update.callback_query
    await query.answer()
    
    # Get chapter index and info
    idx = int(query.data.split("_")[1])
    chapter = CHAPTERS[idx]
    content_type = context.user_data.get("content_type", "Content")
    
    # Store chapter info
    context.user_data["chapter"] = chapter
    context.user_data["chapter_index"] = idx
    
    # Create keyboard with chat button that opens direct chat
    markup = InlineKeyboardMarkup(row_width=1)
    markup.row(
        InlineKeyboardButton("ðŸ’¬ Chat with Admin", url=f"https://t.me/{CHATBOT_USERNAME[1:]}")    )
    markup.row(
        InlineKeyboardButton("â¬… Back to Chapters", callback_data="back_chapters")
    )
    
    # Send payment instructions
    await query.edit_message_text(
        PAYMENT_TEXT.format(content_type=content_type, chapter=chapter),
        reply_markup=markup,
        parse_mode="Markdown"
    )
    
    # Send notification to admin channel
    await notify_admin(context, query.from_user, content_type, chapter)

async def notify_admin(context: ContextTypes.DEFAULT_TYPE, user, content_type: str, chapter: str):
    """Send notification to admin channel"""
    try:
        user_id = user.id
        username = f"@{user.username}" if user.username else "No username"
        first_name = user.first_name or ""
        last_name = user.last_name or ""
        full_name = f"{first_name} {last_name}".strip() or "No name"
        
        admin_message = (
            "ðŸ†• *New Client Inquiry*\n\n"
            f"ðŸ‘¤ *Name:* {full_name}\n"
            f"ðŸ“± *Username:* {username}\n"
            f"ðŸ†” *User ID:* `{user_id}`\n"
            f"ðŸ“š *Content Type:* {content_type}\n"
            f"ðŸ“– *Chapter:* {chapter}\n\n"
            f"ðŸ’¬ [Click to Chat with Client](tg://user?id={user_id})\n"
            f"ðŸ¤– [Go to Chatbot](https://t.me/{CHATBOT_USERNAME[1:]})"
        )
        
        await context.bot.send_message(
            chat_id=ADMIN_CHANNEL,
            text=admin_message,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
        
    except Exception as e:
        logging.error(f"Failed to send admin notification: {e}")

async def back_to_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle back to start button"""
    query = update.callback_query
    await query.answer()
    await start(update, context)
async def back_to_chapters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle back to chapters button"""
    query = update.callback_query
    await query.answer()
    await content_type_selected(update, context)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = (
        "ðŸ¤– *Pediatric Surgery IQ Bot Help*\n\n"
        "*/start* - Start the bot and choose content type\n"
        "*/help* - Show this help message\n\n"
        "*How to use:*\n"
        "1. Click /start\n"
        "2. Choose MRCS or Flash Cards\n"
        "3. Select a chapter\n"
        "4. Follow payment instructions\n"
        "5. Chat with admin for assistance\n\n"
        f"*Need help?* Contact: {CHATBOT_USERNAME}"
    )
    
    await update.message.reply_text(
        help_text,
        parse_mode="Markdown"
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors gracefully"""
    logging.error(f"Update {update} caused error {context.error}")
    
    try:
        if update and update.callback_query:
            await update.callback_query.message.reply_text(
                "âš ï¸ An error occurred. Please try again with /start",
                parse_mode="Markdown"
            )
    except:
        pass

# =====================================
# KEEP ALIVE FUNCTION
# =====================================

async def keep_alive():
    """Simple keep-alive function for Render"""
    # This function doesn't do anything but keeps the bot running
    while True:
        await asyncio.sleep(300)  # Sleep for 5 minutes
# =====================================
# MAIN FUNCTION
# =====================================

def main():
    """Start the bot"""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    try:
        # Create application
        application = ApplicationBuilder().token(BOT_TOKEN).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CallbackQueryHandler(content_type_selected, pattern="^(MRCS|Flash_Cards)$"))
        application.add_handler(CallbackQueryHandler(chapter_selected, pattern="^ch_"))
        application.add_handler(CallbackQueryHandler(back_to_start, pattern="^back_start$"))
        application.add_handler(CallbackQueryHandler(back_to_chapters, pattern="^back_chapters$"))
        
        # Add error handler
        application.add_error_handler(error_handler)
        
        logger.info("Starting Pediatric Surgery IQ Bot...")
        logger.info("Bot is running in polling mode...")
        
        # Start polling
        application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True,
            poll_interval=0.5,
            timeout=30
        )
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise

# =====================================
# SIMPLE WEB SERVER FOR KEEP-ALIVE
# =====================================

from aiohttp import web
import threading
async def handle_health_check(request):
    """Handle health check requests"""
    return web.Response(text="Pediatric Surgery IQ Bot is running!")

def run_web_server():
    """Run a simple web server for keep-alive"""
    app = web.Application()
    app.router.add_get('/', handle_health_check)
    app.router.add_get('/health', handle_health_check)
    
    port = int(os.environ.get('PORT', 8080))
    web.run_app(app, host='0.0.0.0', port=port)

if __name__ == "__main__":
    # Start web server in a separate thread
    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()
    
    # Start the bot
    main()
