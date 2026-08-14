import telebot
from telebot import types

# Жаңы токениңиз
TOKEN = '8976128121:AAG0hDOTLtbBUPdj1TQO8f5bilsXZ5sCegk'
bot = telebot.TeleBot(TOKEN)

# Унаалардын базасы
CARS = {
    "m5_f90": {
        "name": "BMW M5 F90 Competition 🚀",
        "engine": "4.4L V8 Twin-Turbo",
        "power": "625 л.с.",
        "accel": "3.3 секунд (0-100 км/ч)",
        "drive": "xDrive (Толук привод)",
        "desc": "Седан классындагы эң ылдам жана ыңгайлуу спорттук унаалардын бири."
    },
    "m4_competition": {
        "name": "BMW M4 Competition ⚡",
        "engine": "3.0L Inline-6 Twin-Turbo",
        "power": "510 л.с.",
        "accel": "3.9 секунд (0-100 км/ч)",
        "drive": "RWD / xDrive",
        "desc": "Агрессивдүү дизайн жана трек үчүн эң сонун башкарылуучу купе."
    }
}

# /start командасы
@bot.message_handler(commands=['start'])
def start_msg(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("🏎️ BMW M5 F90 Competition", callback_data="car_m5_f90")
    btn2 = types.InlineKeyboardButton("🏎️ BMW M4 Competition", callback_data="car_m4_competition")
    btn3 = types.InlineKeyboardButton("⚔️ М5 F90 vs M4 Салыштыруу", callback_data="compare_m5_m4")
    
    markup.add(btn1, btn2, btn3)
    
    text = (
        "🏎️ **Автомобиль Жардамчысы Ботуна кош келиңиз!**\n\n"
        "Бул жерден унаалардын деталдуу мүнөздөмөлөрүн көрүп, аларды өз ара салыштыра аласыз.\n\n"
        "Төмөнкү менюдан керектүү модельди тандаңыз:"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=markup)

# Инлайн баскычтарды иштетүү
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    markup = types.InlineKeyboardMarkup()
    btn_back = types.InlineKeyboardButton("🔙 Башкы менюга кайтуу", callback_data="back_to_main")
    markup.add(btn_back)

    # Башкы менюга кайтуу
    if call.data == "back_to_main":
        main_markup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton("🏎️ BMW M5 F90 Competition", callback_data="car_m5_f90")
        btn2 = types.InlineKeyboardButton("🏎️ BMW M4 Competition", callback_data="car_m4_competition")
        btn3 = types.InlineKeyboardButton("⚔️ М5 F90 vs M4 Салыштыруу", callback_data="compare_m5_m4")
        main_markup.add(btn1, btn2, btn3)
        
        text = "🏎️ **Башкы меню:**\n\nКайсы унааны же функцияны тандайсыз?"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=main_markup)

    # Унаа маалыматын көрсөтүү
    elif call.data.startswith("car_"):
        car_key = call.data.replace("car_", "")
        car = CARS[car_key]
        
        text = (
            f"🚘 **{car['name']}**\n\n"
            f"⚙️ **Кыймылдаткыч:** {car['engine']}\n"
            f"🐎 **Кубаты:** {car['power']}\n"
            f"⏱️ **0-100 км/ч:** {car['accel']}\n"
            f"🛣️ **Привод:** {car['drive']}\n\n"
            f"📝 {car['desc']}"
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    # Салыштыруу режими
    elif call.data == "compare_m5_m4":
        m5 = CARS["m5_f90"]
        m4 = CARS["m4_competition"]
        
        text = (
            "⚔️ **BMW M5 F90 vs BMW M4 Competition**\n\n"
            f"🔴 **{m5['name']}**\n"
            f"• Мотор: {m5['engine']}\n"
            f"• Кубат: {m5['power']}\n"
            f"• 0-100 км/ч: {m5['accel']}\n\n"
            f"🔵 **{m4['name']}**\n"
            f"• Мотор: {m4['engine']}\n"
            f"• Кубат: {m4['power']}\n"
            f"• 0-100 км/ч: {m4['accel']}\n\n"
            "🏆 **Ж жыйынтык:** М5 ылдамдануу жагынан эртерээк чыгат, ал эми М4 жеңилдиги жана тректеги башкарылуусу менен айырмаланат!"
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

if __name__ == "__main__":
    print("Авто Бот ишке кирди...")
    bot.infinity_polling()
