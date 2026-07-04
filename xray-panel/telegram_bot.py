import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from sqlalchemy.orm import Session
import database
import xray_manager
import uuid
import os
from dotenv import load_dotenv

load_dotenv("/opt/pho3nix-panel/.env")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

ADMIN_IDS = [int(x) for x in os.getenv("TELEGRAM_ADMIN_IDS", "").split(",") if x]

def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⛔ Yetkisiz erişim.")
        return
    
    await update.message.reply_text(
        "🦊 *Pho3nix Panel Telegram Bot*\n\n"
        "Komutlar:\n"
        "/add <kullanıcı_adı> <kota_gb> - Kullanıcı ekle\n"
        "/delete <kullanıcı_adı> - Kullanıcı sil\n"
        "/list - Tüm kullanıcıları listele\n"
        "/status - Sistem durumu\n"
        "/sub <kullanıcı_adı> - Abonelik linkini al",
        parse_mode='Markdown'
    )

async def add_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⛔ Yetkisiz erişim.")
        return
    
    if len(context.args) < 2:
        await update.message.reply_text("Kullanım: /add <kullanıcı_adı> <kota_gb>")
        return
    
    username = context.args[0]
    try:
        quota_gb = float(context.args[1])
    except ValueError:
        await update.message.reply_text("❌ Geçersiz kota değeri.")
        return
    
    db = next(database.get_db())
    try:
        existing = db.query(database.User).filter(database.User.username == username).first()
        if existing:
            await update.message.reply_text(f"❌ Kullanıcı zaten mevcut: {username}")
            return
        
        new_user = database.User(
            username=username,
            uuid=str(uuid.uuid4()),
            port=8080,
            quota_bytes=int(quota_gb * 1024 * 1024 * 1024),
            used_bytes=0,
            is_active=True
        )
        db.add(new_user)
        db.commit()
        
        xray_manager.apply_config(db)
        
        await update.message.reply_text(
            f"✅ Kullanıcı eklendi!\n\n"
            f"👤 {username}\n"
            f"💾 Kota: {quota_gb} GB\n"
            f"🔑 UUID: `{new_user.uuid}`",
            parse_mode='Markdown'
        )
    finally:
        db.close()

async def delete_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⛔ Yetkisiz erişim.")
        return
    
    if len(context.args) < 1:
        await update.message.reply_text("Kullanım: /delete <kullanıcı_adı>")
        return
    
    username = context.args[0]
    db = next(database.get_db())
    try:
        user = db.query(database.User).filter(database.User.username == username).first()
        if not user:
            await update.message.reply_text(f"❌ Kullanıcı bulunamadı: {username}")
            return
        
        db.delete(user)
        db.commit()
        xray_manager.apply_config(db)
        
        await update.message.reply_text(f"✅ Kullanıcı silindi: {username}")
    finally:
        db.close()

async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⛔ Yetkisiz erişim.")
        return
    
    db = next(database.get_db())
    try:
        users = db.query(database.User).all()
        if not users:
            await update.message.reply_text("📭 Henüz kullanıcı yok.")
            return
        
        message = "👥 *Kullanıcı Listesi*\n\n"
        for user in users:
            status = "🟢" if user.is_active else "🔴"
            quota_gb = user.quota_bytes / (1024**3) if user.quota_bytes > 0 else "Sınırsız"
            used_gb = user.used_bytes / (1024**3)
            
            message += f"{status} *{user.username}*\n"
            message += f"   💾 {used_gb:.2f} GB / {quota_gb} GB\n\n"
        
        await update.message.reply_text(message, parse_mode='Markdown')
    finally:
        db.close()

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⛔ Yetkisiz erişim.")
        return
    
    db = next(database.get_db())
    try:
        users = db.query(database.User).all()
        active_users = len([u for u in users if u.is_active])
        total_traffic = sum(u.used_bytes for u in users) / (1024**3)
        
        await update.message.reply_text(
            f"🦊 *Pho3nix Panel Durumu*\n\n"
            f"👥 Toplam Kullanıcı: {len(users)}\n"
            f"🟢 Aktif: {active_users}\n"
            f"🔴 Pasif: {len(users) - active_users}\n"
            f"📊 Toplam Trafik: {total_traffic:.2f} GB",
            parse_mode='Markdown'
        )
    finally:
        db.close()

async def get_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⛔ Yetkisiz erişim.")
        return
    
    if len(context.args) < 1:
        await update.message.reply_text("Kullanım: /sub <kullanıcı_adı>")
        return
    
    username = context.args[0]
    db = next(database.get_db())
    try:
        user = db.query(database.User).filter(database.User.username == username).first()
        if not user:
            await update.message.reply_text(f"❌ Kullanıcı bulunamadı: {username}")
            return
        
        sub_url = f"http://{os.getenv('SERVER_IP', 'localhost')}:8000/sub/{user.username}"
        await update.message.reply_text(
            f"🔗 *{username} Abonelik Linki*\n\n"
            f"`{sub_url}`\n\n"
            f"Bu linki v2rayNG, Streisand veya Hiddify'a ekleyin.",
            parse_mode='Markdown'
        )
    finally:
        db.close()

def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN bulunamadı!")
        return
    
    application = Application.builder().token(token).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add", add_user))
    application.add_handler(CommandHandler("delete", delete_user))
    application.add_handler(CommandHandler("list", list_users))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("sub", get_subscription))
    
    logger.info("Telegram bot başlatıldı...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
