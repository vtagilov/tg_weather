import telebot
import geocoder
import weather

TG_TOKEN = "5674920706:AAGdbFulWZ-TI1fsh3d2-3zW2kTkqUTyssI"
bot = telebot.TeleBot(TG_TOKEN)


def write_log(m):
    log = open('log.txt', 'a')
    log.write(str(m)+"\n")
    log.close()


@bot.message_handler(commands=['start', 'help'])
def show_help_message(message):
    write_log(message)
    bot.send_message(message.chat.id, 'Бот может подсказать погоду в определенном месте.'
                                      '\nПиши свое местоположение или прикрепляй геопозицию.')


@bot.message_handler(content_types=["text"])
def handle_text(message):
    write_log(message)
    try:
        address = geocoder.get_position_api(message.text)
        info = weather.get_weather_info(latitude=address.latitude, longitude=address.longitude, address=message.text)
        bot.send_message(message.chat.id, info)
    except IndexError:
        bot.send_message(message.chat.id, "Так нельзя!")


@bot.message_handler(content_types=["location"])
def handle_text(message):
    write_log(message)
    info = weather.get_weather_info(longitude=message.location.longitude, latitude=message.location.latitude)
    bot.send_message(message.chat.id, info)


if __name__ == "__main__":
    print("bot is working...")
    bot.polling(none_stop=True, interval=0)
    print("bot stopped!")
