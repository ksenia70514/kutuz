import telebot  # библиотека telebot
from config import token  # импорт токена

bot = telebot.TeleBot(token) 

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот для управления чатом.")

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message:  # проверка, что команда вызвана в ответ на сообщение
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно забанить администратора.")
        else:
            bot.ban_chat_member(chat_id, user_id)
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите забанить.")

# Новый обработчик для проверки ссылок в сообщениях
@bot.message_handler(func=lambda message: True)
def check_links_and_ban(message):
    text = message.text
    user = message.from_user
    chat_id = message.chat.id

    if text and "https://" in text:
        # Сохраняем информацию о пользователе в файл
        with open("banned_users.txt", "a", encoding="utf-8") as f:
            f.write(f"{user.id}, @{user.username}, {user.first_name}, {user.last_name}\n")

        try:
            bot.ban_chat_member(chat_id, user.id)
            bot.reply_to(message, "Пользователь забанен за отправку ссылки.")
        except Exception as e:
            bot.reply_to(message, f"Не удалось забанить пользователя: {e}")
    else:
        # Если ссылки нет — просто отвечаем тем же текстом
        bot.reply_to(message, text)

bot.infinity_polling(none_stop=True)