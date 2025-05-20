
import telebot

TOKEN = '7219760925:AAHPrhcYyOEufmfvFCgpcaa6i0CnQ24WjIo'
bot = telebot.TeleBot(TOKEN)

device_power = {
    "یخچال": 150,
    "لامپ": 20,
    "تلویزیون": 100,
    "کولر": 1000,
    "لب‌تاپ": 65
}

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_data[message.chat.id] = {"devices": []}
    bot.send_message(message.chat.id, "به ماشین حساب هوشیار صنعت ماد خوش آمدید!\nنام وسیله‌ای که می‌خوای وارد کنی رو بنویس (مثلاً لامپ):")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    chat_id = message.chat.id
    text = message.text.strip()

    if text == "پایان":
        total = sum(device_power[d] * c for d, c in user_data[chat_id]["devices"])
        bot.send_message(chat_id, f"توان کلی مورد نیاز شما: {total} وات")
        return

    if "current_device" not in user_data[chat_id]:
        if text in device_power:
            user_data[chat_id]["current_device"] = text
            bot.send_message(chat_id, f"چند عدد {text} داری؟")
        else:
            bot.send_message(chat_id, "این وسیله تو لیست نیست. وسایل مجاز: " + ", ".join(device_power.keys()))
    else:
        try:
            count = int(text)
            device = user_data[chat_id]["current_device"]
            user_data[chat_id]["devices"].append((device, count))
            del user_data[chat_id]["current_device"]

            total = sum(device_power[d] * c for d, c in user_data[chat_id]["devices"])
            bot.send_message(chat_id, f"تا الان {total} وات نیاز داری. برای افزودن وسیله دیگر اسمش را بنویس یا بنویس 'پایان'")
        except ValueError:
            bot.send_message(chat_id, "لطفاً فقط عدد وارد کن.")

bot.infinity_polling()
