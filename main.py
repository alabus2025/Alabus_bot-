import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")  # Токен будет передан через настройки на Render

bot = telebot.TeleBot(TOKEN)

CHANNEL_USERNAME = "@Alabuszakaz"  # Сюда отправляются заказы

# Приветствие
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = telebot.types.KeyboardButton('Билет заказ кылуу / Забронировать билет')
    item2 = telebot.types.KeyboardButton('Байланышуу / Связаться с нами')
    markup.add(item1, item2)
    
    welcome_text = ("Добро пожаловать в Alabus!\n"
                    "Alabus'ка кош келиңиз!\n\n"
                    "Выберите действие:\n"
                    "Кызматты тандаңыз:")
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

# Ответ на кнопки
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == 'Билет заказ кылуу / Забронировать билет':
        bot.send_message(message.chat.id, "Напишите ваше имя:")
        bot.register_next_step_handler(message, get_name)
    elif message.text == 'Байланышуу / Связаться с нами':
        contact_text = ("Контакты Alabus:\n"
                        "Телефон: +996501150504\n"
                        "WhatsApp: +996501150504\n"
                        "Instagram: @Alabus_Fan")
        bot.send_message(message.chat.id, contact_text)

# Заполняем форму бронирования
def get_name(message):
    name = message.text
    bot.send_message(message.chat.id, "Напишите ваш номер телефона:")
    bot.register_next_step_handler(message, get_phone, name)

def get_phone(message, name):
    phone = message.text
    bot.send_message(message.chat.id, "Откуда выезжаете?")
    bot.register_next_step_handler(message, get_from, name, phone)

def get_from(message, name, phone):
    from_city = message.text
    bot.send_message(message.chat.id, "Куда едете?")
    bot.register_next_step_handler(message, get_to, name, phone, from_city)

def get_to(message, name, phone, from_city):
    to_city = message.text
    bot.send_message(message.chat.id, "Дата поездки:")
    bot.register_next_step_handler(message, get_date, name, phone, from_city, to_city)

def get_date(message, name, phone, from_city, to_city):
    date = message.text
    bot.send_message(message.chat.id, "Количество пассажиров:")
    bot.register_next_step_handler(message, confirm_booking, name, phone, from_city, to_city, date)

def confirm_booking(message, name, phone, from_city, to_city, date):
    passengers = message.text
    booking_text = (f"Новая бронь:\n\n"
                    f"Имя: {name}\n"
                    f"Телефон: {phone}\n"
                    f"Откуда: {from_city}\n"
                    f"Куда: {to_city}\n"
                    f"Дата поездки: {date}\n"
                    f"Пассажиров: {passengers}")
    
    bot.send_message(CHANNEL_USERNAME, booking_text)
    bot.send_message(message.chat.id, "Ваша заявка принята! Мы скоро свяжемся с вами.")

# Запуск бота
bot.polling(non_stop=True)
