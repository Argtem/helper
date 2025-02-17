import random
from lexicon.lexicon_ru import LEXICON_RU
from keyboards.keyboards import tasks_kb, weather_kb, happy_kb
import requests


# Функция, возвращающая ключ из словаря, по которому
# хранится значение, передаваемое как аргумент - выбор пользователя
def normalize_user_answer(user_answer: str) -> str:
    for key in LEXICON_RU:
        if LEXICON_RU[key] == user_answer:
            break
    return key


def select_point(user_answer: str) -> str:
    for key in LEXICON_RU:
        if user_answer == 'weather':
            return weather_kb
        elif user_answer == 'tasks':
            return tasks_kb
        elif user_answer == 'happy':
            return happy_kb
        else:
            return LEXICON_RU['other_answer']


# Прогноз погоды по API
def get_weather(city: str) -> str:
    # Координаты города: Saint Petersburg, Russia
    longitude = 30.3141
    latitude = 59.9386

    # Получаем данные по Open-Meteo API
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    weather_response = requests.get(weather_url)
    weather_data = weather_response.json()

    if weather_response.status_code == 200 and "current_weather" in weather_data:
        # Обработка полученной информации
        temperature = weather_data['current_weather']['temperature']
        wind_speed = weather_data['current_weather']['windspeed']
        weather_code = weather_data['current_weather']['weathercode']

        # Добавление описания
        weather_descriptions = {
            0: "Ясно. Понятно?",
            1: "Преимущественно ясно, но не очень",
            2: "Переменная облачность. Тучи. Но немного",
            3: "Пасмурно. Тучи, много туч",
            45: "Туман. Как обычно в Петербурге и в Лондоне",
            48: "Гололедный туман. Мало того, что туман, так и гололед",
            51: "Легкая морось. Капает, но мало",
            53: "Умеренная морось. Капает. Уже не мало",
            55: "Сильная морось. Сильно капает",
            56: "Легкая ледяная морось. Замерзло и капает",
            57: "Сильная ледяная морось. Замерзло и сильно капает",
            61: "Небольшой дождь. Норм, без зонта",
            63: "Умеренный дождь. Нужен зонт",
            65: "Сильный дождь. Сиди дома",
            66: "Легкий ледяной дождь",
            67: "Сильный ледяной дождь. Не просто дождь, а ледяной!",
            71: "Небольшой снегопад. Чуть-чуть",
            73: "Умеренный снегопад. Снег, но не прямо много",
            75: "Сильный снегопад. Очень много снега",
            77: "Снежные зерна",
            80: "Небольшие ливни. Когда льёт как из ведра, но маленького",
            81: "Умеренные ливни. Когда льёт как из ведра, среднего",
            82: "Сильные ливни. Когда льёт как из ведра, большого",
            85: "Снегопад и ливень",
            86: "Сильный снегопад и ливень. Ужас какой-то",
            95: "Гроза. Очень шумно",
            96: "Гроза с легким градом. Как будто одной грозы мало",
            99: "Гроза с сильным градом. Шумно и больно",
        }
        weather_description = weather_descriptions.get(weather_code, "Непонятная погода")

        weather_report = (
            f"Погода в нашем городе сейчас такая:\n"
            f"Чего ждать: {weather_description}\n"
            f"Температура по цельсию: {temperature:.1f}°C\n"
            f"Скорость ветра: {wind_speed:.1f} м/с, так что не улетишь"
        )
    else:
        weather_report = "Не могу понять, что за погода"

    return weather_report


words1 = ['человек', 'столб', 'дом', 'птица', 'чебурек']
words2 = ['шёл', 'летел', 'плыл']
words3 = ['под водой', 'по лесу', 'высоко над облаками', 'чебурек']
words4 = ['и упал', 'и споткнулся', 'и стал рыбой', 'чебурек']


def get_joke():
    selected_1 = ' '.join(random.sample(words1, 1))
    selected_2 = ' '.join(random.sample(words2, 1))
    selected_3 = ' '.join(random.sample(words3, 1))
    selected_4 = ' '.join(random.sample(words4, 1))
    joke = f"{selected_1} {selected_2} {selected_3} {selected_4}"
    return joke
