# =====================================
# Pediatric Surgery IQ – Marketing Bot
# =====================================

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import logging
import os

# =====================================
# CONFIG
# =====================================

BOT_TOKEN = "8408158472:AAHbXpv2WJeubnkdlKJ6CMSV4zA4G54X-gY"
ADMIN_CHANNEL = "@clientpedsurg"  # Your admin channel

# =====================================
# TEXTS
# =====================================

WELCOME_TEXT = (
    "👋 *Welcome to Pediatric Surgery IQ*\n\n"
    "What would you like to study today?"
)

PAYMENT_TEXT = (
    "💳 *Payment Required*\n\n"
    "To receive *{content_type}* about *{chapter}*, send *5,000 IQD* to:\n\n"
    "📱 *Zain Cash:* 009647833160006\n"
    "💳 *Master Card:* 3175657935\n\n"
    "📸 Take a screenshot and send it here:\n"
    "@PedSurgIQ\n\n"
    "You are ready ✅\n\n"
    "🍀 Good luck and enjoy the challenge 🙏"
)

# =====================================
# CHAPTERS
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
    """Handle /start command - Single button for both options"""
    # Single inline keyboard with one row
    keyboard = [[
        InlineKeyboardButton("📘 MRCS", callback_data="MRCS"),
        InlineKeyboardButton("🧠 Flash Cards", callback_data="Flash Cards")
    ]]
    
    await update.message.reply_text(
        WELCOME_TEXT,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def content_type_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle when user selects MRCS or Flash Cards"""
    query = update.callback_query
    await query.answer()
    
    # Store selected content type
    context.user_data["content_type"] = query.data
    
    # Create chapter selection keyboard with pagination
    keyboard = []
    
    # Add chapters in rows of 2 for better display
    for i in range(0, len(CHAPTERS), 2):
        row = []
        row.append(InlineKeyboardButton(CHAPTERS[i], callback_data=f"ch_{i}"))
        if i + 1 < len(CHAPTERS):
            row.append(InlineKeyboardButton(CHAPTERS[i + 1], callback_data=f"ch_{i + 1}"))
        keyboard.append(row)
    
    # Add back button at the end
    keyboard.append([InlineKeyboardButton("⬅ Back", callback_data="back_start")])
    
    await query.edit_message_text(
        "📖 *Select a Chapter*\n\n"
        f"Selected: *{query.data}*",
        reply_markup=InlineKeyboardMarkup(keyboard),
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
    
    # Create keyboard with chat button
    keyboard = [[
        InlineKeyboardButton("💬 Chat with Admin", callback_data="chat_admin")
    ]]
    
    # Send payment instructions
    await query.edit_message_text(
        PAYMENT_TEXT.format(content_type=content_type, chapter=chapter),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def chat_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle chat with admin request"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    user_id = user.id
    username = f"@{user.username}" if user.username else f"User ID: {user_id}"
    first_name = user.first_name or ""
    last_name = user.last_name or ""
    full_name = f"{first_name} {last_name}".strip()
    
    # Get stored data
    content_type = context.user_data.get("content_type", "Unknown")
    chapter = context.user_data.get("chapter", "Unknown")
    
    # Create admin notification message
    admin_message = (
        "🆕 *New Client Request*\n\n"
        f"👤 *Client:* {full_name}\n"
        f"📱 *Username:* {username}\n"
        f"🆔 *User ID:* `{user_id}`\n"
        f"📚 *Requested:* {content_type}\n"
        f"📖 *Chapter:* {chapter}\n\n"
        f"💬 [Click to Chat with Client](tg://user?id={user_id})"
    )
    
    try:
        # Send to admin channel
        await context.bot.send_message(
            chat_id=ADMIN_CHANNEL,
            text=admin_message,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
        
        # Confirm to user
        await query.edit_message_text(
            "✅ *Request Sent Successfully!*\n\n"
            "Our admin will contact you shortly to assist with payment.\n"
            "You can also send payment screenshot to @PedSurgIQ\n\n"
            "Thank you for your interest! 🙏",
            parse_mode="Markdown"
        )
        
    except Exception as e:
        logging.error(f"Failed to send admin notification: {e}")
        await query.edit_message_text(
            "⚠️ *Something went wrong!*\n\n"
            "Please contact @PedSurgIQ directly with:\n"
            f"- Your selected chapter: {chapter}\n"
            f"- Content type: {content_type}\n\n"
            "We apologize for the inconvenience.",
            parse_mode="Markdown"
        )

async def back_to_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle back to start button"""
    query = update.callback_query
    await query.answer()
    
    # Reset user data
    context.user_data.clear()
    
    # Show start menu again
    keyboard = [[
        InlineKeyboardButton("📘 MRCS", callback_data="MRCS"),
        InlineKeyboardButton("🧠 Flash Cards", callback_data="Flash Cards")
    ]]
    
    await query.edit_message_text(
        WELCOME_TEXT,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors gracefully"""
    logging.error(f"Update {update} caused error {context.error}")
    
    if update and update.callback_query:
        try:
            await update.callback_query.message.reply_text(
                "⚠️ An error occurred. Please try again with /start",
                parse_mode="Markdown"
            )
        except:
            pass

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
        application.add_handler(CallbackQueryHandler(content_type_selected, pattern="^(MRCS|Flash Cards)$"))
        application.add_handler(CallbackQueryHandler(chapter_selected, pattern="^ch_"))
        application.add_handler(CallbackQueryHandler(chat_admin, pattern="^chat_admin$"))
        application.add_handler(CallbackQueryHandler(back_to_start, pattern="^back_start$"))
        
        # Add error handler
        application.add_error_handler(error_handler)
        
        logger.info("Starting Pediatric Surgery IQ Bot...")
        logger.info("Bot is running in polling mode...")
        
        # Start polling
        application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True,
            poll_interval=0.5  # Faster response time
        )
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise

# =====================================
# KEEP-ALIVE FOR RENDER
# =====================================
# Render requires a web server to keep the app alive
# We'll use a simple HTTP server in a separate thread

from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

class KeepAliveHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Pediatric Surgery IQ Bot is running!')
    
    def log_message(self, format, *args):
        pass  # Disable logging

def run_keep_alive():
    """Run a simple HTTP server to keep Render alive"""
    port = int(os.environ.get('PORT', 8080))
    server = HTTPServer(('0.0.0.0', port), KeepAliveHandler)
    print(f"Keep-alive server running on port {port}")
    server.serve_forever()

if __name__ == "__main__":
    # Start keep-alive server in a separate thread
    keep_alive_thread = threading.Thread(target=run_keep_alive, daemon=True)
    keep_alive_thread.start()
    
    # Start the bot
    main()
