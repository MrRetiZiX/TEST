from config import TOKEN
import telebot
import random

bot = telebot.TeleBot(TOKEN)

class Car:
    def __init__(self, color, brand):
        self.color = color
        self.brand = brand
        
    def info(self):
        return f"🚗 {self.brand} ({self.color})"

jokes = ["Почему программисты не люблять природу? Там слишком много багов!"]
quotes = ["Код — как поэзия. Он должен быть красивым"]
facts = ["Кошки спят 70% жизни"]
magic_answers = ["Да", "Нет", "Возможно", "Спроси позже"]

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    text = "Доступные команды:\n/joke - Шутка\n/quote - Цитата\n/fact - Факт\n/car - Создать машину\n/dice - Бросить кубик\n/8ball - Магический шар"
    bot.reply_to(message, text)

@bot.message_handler(commands=['joke'])
def send_joke(message):
    bot.reply_to(message, random.choice(jokes))

@bot.message_handler(commands=['quote'])
def send_quote(message):
    bot.reply_to(message, random.choice(quotes))

@bot.message_handler(commands=['fact'])
def send_fact(message):
    bot.reply_to(message, random.choice(facts))

@bot.message_handler(commands=['car'])
def create_car(message):
    args = telebot.util.extract_arguments(message.text).split()
    if len(args) >= 2:
        car = Car(args[0], args[1])
        bot.reply_to(message, car.info())
    else:
        bot.reply_to(message, "Используйте: /car цвет марка")

@bot.message_handler(commands=['dice'])
def roll_dice(message):
    bot.send_dice(message.chat.id, emoji='🎲')

@bot.message_handler(commands=['8ball'])
def magic_ball(message):
    question = telebot.util.extract_arguments(message.text)
    if question:
        bot.reply_to(message, f"🎱 Ответ: {random.choice(magic_answers)}")
    else:
        bot.reply_to(message, "Задайте вопрос: /8ball ваш_вопрос")

@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for user in message.new_chat_members:
        bot.send_message(message.chat.id, f"👋 Добро пожаловать, {user.first_name}!")

@bot.message_handler(content_types=['text'])
def check_links(message):
    if 'http' in message.text.lower():
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "🚫 Ссылки запрещены!")

@bot.message_handler(content_types=['photo', 'voice', 'document'])
def handle_media(message):
    bot.reply_to(message, "✅ Контент получен")

bot.infinity_polling()
