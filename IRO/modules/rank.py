import IRO
from collections import defaultdict
from datetime import datetime, timedelta

# Replace 'YOUR_BOT_TOKEN' with your actual bot token obtained from BotFather
bot = telebot.TeleBot('YOUR_BOT_TOKEN')

# Dictionary to store message counts for each user
message_counts = defaultdict(int)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Update message count for the user
    message_counts[message.from_user.id] += 1

@bot.message_handler(commands=['rank'])
def rank_users(message):
    today = datetime.now().date()
    start_of_day = datetime.combine(today, datetime.min.time())
    end_of_day = datetime.combine(today, datetime.max.time())

    # Filter message counts for today
    todays_message_counts = {user_id: count for user_id, count in message_counts.items() 
                             if start_of_day <= message.date <= end_of_day}

    # Sort users by message count
    sorted_users = sorted(todays_message_counts.items(), key=lambda x: x[1], reverse=True)

    # Prepare and send the ranking message
    rank_message = "Today's Message Ranking:\n"
    for i, (user_id, count) in enumerate(sorted_users, start=1):
        user = bot.get_chat_member(message.chat.id, user_id).user
        username = user.username if user.username else user.first_name
        rank_message += f"{i}. @{username}: {count} messages\n"

    bot.reply_to(message, rank_message)

bot.polling()
