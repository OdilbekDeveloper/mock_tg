import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from bot_init import bot

# 🔥 LOAD OLD BOT LOGIC
import bot as old_bot

print("Bot running...")
bot.infinity_polling()
