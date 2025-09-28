from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
import logging
import hashlib
import hmac
import time
import urllib.parse
from config import (
    BOT_TOKEN, 
    GAME_SHORT_NAME, 
    GAME_URL, 
    LOG_CONFIG, 
    BOT_MESSAGES
)

# 开启日志  （方便调试）
logging.basicConfig(
    format=LOG_CONFIG['format'], 
    level=getattr(logging, LOG_CONFIG['level'])
)

# ====== initData 验证函数 ======
def validate_init_data(init_data: str, bot_token: str) -> bool:
    """
    验证 Telegram WebApp initData 的有效性
    
    Args:
        init_data: 从 Telegram WebApp 传递的 initData 字符串
        bot_token: 机器人的 Token
    
    Returns:
        bool: 验证是否通过
    """
    try:
        # 解析 initData
        parsed_data = urllib.parse.parse_qs(init_data)
        
        # 提取 hash 和 auth_date
        hash_value = parsed_data.get('hash', [None])[0]
        auth_date = parsed_data.get('auth_date', [None])[0]
        
        if not hash_value or not auth_date:
            return False
        
        # 检查时间戳是否在有效期内（24小时）
        current_time = int(time.time())
        auth_timestamp = int(auth_date)
        if current_time - auth_timestamp > 86400:  # 24小时 = 86400秒
            return False
        
        # 移除 hash 参数，准备验证
        data_check_string = init_data.replace(f'&hash={hash_value}', '').replace(f'hash={hash_value}&', '').replace(f'hash={hash_value}', '')
        
        # 创建验证密钥
        secret_key = hmac.new(
            "WebAppData".encode(),
            bot_token.encode(),
            hashlib.sha256
        ).digest()
        
        # 计算期望的 hash
        expected_hash = hmac.new(
            secret_key,
            data_check_string.encode(),
            hashlib.sha256
        ).hexdigest()
        
        # 比较 hash
        return hmac.compare_digest(hash_value, expected_hash)
        
    except Exception as e:
        logging.getLogger(__name__).error(f"initData 验证失败: {e}")
        return False

def parse_init_data(init_data: str) -> dict:
    """
    解析 initData 中的用户信息
    
    Args:
        init_data: 从 Telegram WebApp 传递的 initData 字符串
    
    Returns:
        dict: 解析后的用户信息
    """
    try:
        parsed_data = urllib.parse.parse_qs(init_data)
        user_data = {}
        
        # 提取用户信息
        if 'user' in parsed_data:
            import json
            user_json = parsed_data['user'][0]
            user_data = json.loads(user_json)
        
        return user_data
    except Exception as e:
        logging.getLogger(__name__).error(f"解析 initData 失败: {e}")
        return {}

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
    
    # 记录用户信息到日志（用于调试）
    logger.info("📝 用户信息已记录到日志")
    
    # 使用 initData 模式：不直接传递用户信息，而是让 Telegram 处理
    # Telegram 会自动将用户信息通过 initData 传递给游戏
    logger.info("🔐 使用 initData 模式传递用户信息")
    logger.info(f"🔗 游戏URL: {GAME_URL}")
    
    # 玩家点击游戏入口时，返回游戏URL（不包含用户信息参数）
    # Telegram 会自动通过 initData 将用户信息传递给游戏
    await context.bot.answer_callback_query(
        callback_query_id=query.id,
        url=GAME_URL
    )
    
    logger.info("✅ 游戏URL已发送给玩家（使用 initData 模式）")
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