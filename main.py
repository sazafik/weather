import requests
import datetime
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

load_dotenv()
TOKEN = os.getenv('TOKEN')
USER = os.getenv("USER")
API_KEY = os.getenv("API_KEY")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Вітання! Напиши мені назву міста латиницею і я надішлю тобі прогноз погоди!\nНаприклад kyiv")


@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Хмарно \U00002601",
        "Rain": "Дощ \U00002614",
        "Drizzle": "Дощ \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Cніг \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={API_KEY}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Подивися у вікно, не зрозумію, що там за погода!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                            f"Погода у місті:: {city}\nТемпература: {cur_weather}C° {wd}\n"
                            f"Вологість: {humidity}%\nТиск: {pressure} мм.рт.ст\nВітер: {wind} м/с\n"
                            f"Схід сонця: {sunrise_timestamp}\nЗахід сонця: {sunset_timestamp}\nТривалість дня: {length_of_the_day}\n"
                            f"***Гарного дня!***"
                            )

    except:
        await message.reply("\U00002620 Перевірте назву міста \U00002620")


async def set_default_commands(dp):
    await bot.set_my_commands(
        [
            types.BotCommand('start', 'Запустити бота')
        ]
    )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=set_default_commands)
