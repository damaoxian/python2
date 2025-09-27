from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
import logging
from config import (
    BOT_TOKEN, 
    GAME_SHORT_NAME, 
    GAME_URL, 
    LOG_CONFIG, 
    BOT_MESSAGES
)
from database_simple import db_manager

# 开启日志（方便调试）
logging.basicConfig(
    format=LOG_CONFIG['format'], 
    level=getattr(logging, LOG_CONFIG['level'])
)

# ====== 2. 命令处理函数 ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 获取用户信息
    user = update.effective_user
    chat = update.effective_chat
    
    # 记录启动日志
    logger = logging.getLogger(__name__)
    logger.info("🚀 用户启动机器人")
    logger.info(f"   - 用户: {user.first_name} (@{user.username})" if user.username else f"   - 用户: {user.first_name}")
    logger.info(f"   - 用户ID: {user.id}")
    logger.info(f"   - 聊天类型: {chat.type}")
    
    await update.message.reply_text(BOT_MESSAGES['start_message'])
    
    logger.info("✅ 欢迎消息已发送")

async def game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 获取用户信息
    user = update.effective_user
    chat = update.effective_chat
    
    # 记录游戏请求日志
    logger = logging.getLogger(__name__)
    logger.info("🎮 用户请求游戏")
    logger.info(f"   - 用户: {user.first_name} (@{user.username})" if user.username else f"   - 用户: {user.first_name}")
    logger.info(f"   - 用户ID: {user.id}")
    logger.info(f"   - 聊天类型: {chat.type}")
    
    # 发送小游戏入口（short_name）
    await update.message.reply_game(GAME_SHORT_NAME)
    
    logger.info("✅ 游戏入口已发送")

async def game_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    
    # 获取玩家信息
    user = query.from_user
    chat = query.message.chat if query.message else None
    
    # 打印玩家信息日志
    logger = logging.getLogger(__name__)
    logger.info("=" * 50)
    logger.info("🎮 玩家点击游戏入口")
    logger.info("=" * 50)
    
    # 玩家基本信息
    logger.info(f"👤 玩家信息:")
    logger.info(f"   - 用户ID: {user.id}")
    logger.info(f"   - 用户名: @{user.username}" if user.username else f"   - 用户名: 未设置")
    logger.info(f"   - 姓名: {user.first_name} {user.last_name or ''}".strip())
    logger.info(f"   - 语言: {user.language_code}")
    logger.info(f"   - 是否为机器人: {user.is_bot}")
    
    # 聊天信息
    if chat:
        logger.info(f"💬 聊天信息:")
        logger.info(f"   - 聊天ID: {chat.id}")
        logger.info(f"   - 聊天类型: {chat.type}")
        if chat.title:
            logger.info(f"   - 群组名称: {chat.title}")
    
    # 查询信息
    logger.info(f"🔍 查询信息:")
    logger.info(f"   - 查询ID: {query.id}")
    logger.info(f"   - 游戏短名称: {query.game_short_name}")
    logger.info(f"   - 游戏URL: {GAME_URL}")
    
    # 时间信息
    logger.info(f"⏰ 时间信息:")
    logger.info(f"   - 查询时间: {query.message.date if query.message else '未知'}")
    
    logger.info("=" * 50)
    
    # 准备用户信息（简化版，只保存用户ID）
    user_info = {
        'id': user.id
    }
    
    # 保存用户信息到数据库
    logger.info("💾 正在保存用户信息到数据库...")
    save_success = db_manager.save_user(user_info)
    
    if save_success:
        logger.info("✅ 用户信息已保存到数据库")
    else:
        logger.warning("⚠️ 用户信息保存失败，但继续执行")
    
    # 构建包含用户信息的游戏URL
    import urllib.parse
    
    # 将用户信息编码为URL参数
    user_info_json = urllib.parse.quote(str(user_info).replace("'", '"'))
    game_url_with_user = f"{GAME_URL}?user={user_info_json}"
    
    logger.info(f"🔗 游戏URL (含用户信息): {game_url_with_user}")
    
    # 玩家点击游戏入口时，返回包含用户信息的URL
    await context.bot.answer_callback_query(
        callback_query_id=query.id,
        url=game_url_with_user
    )
    
    logger.info("✅ 游戏URL已发送给玩家")
    logger.info("=" * 50)

# ====== 3. 主函数 ======
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # 绑定命令
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("game", game))
    app.add_handler(CallbackQueryHandler(game_callback))  # 移除了 pattern 限制

    # 运行
    app.run_polling()

if __name__ == "__main__":
    main()