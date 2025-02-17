from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from keyboards.keyboards import helper_kb, tasks_kb, weather_kb, happy_kb
from lexicon.lexicon_ru import LEXICON_RU
from services.services import get_weather, get_joke

router = Router()
bot = Bot


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'],
                         reply_markup=helper_kb)


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'],
                         reply_markup=helper_kb)


# Эти хэндлеры срабатывают на любую из кнопок
@router.message(F.text.in_([LEXICON_RU['weather']]))
async def process_weather_button(message: Message):
    await message.answer(text=LEXICON_RU['weather_answer'],
                         reply_markup=weather_kb)


@router.message(F.text.in_([LEXICON_RU['tasks']]))
async def process_tasks_button(message: Message):
    await message.answer(text=LEXICON_RU['tasks_answer'],
                         reply_markup=tasks_kb)


@router.message(F.text.in_([LEXICON_RU['happy']]))
async def process_happy_button(message: Message):
    await message.answer(text=LEXICON_RU['happy_answer'],
                         reply_markup=happy_kb)


@router.message(F.text.in_([LEXICON_RU['back']]))
async def process_back_button(message: Message):
    await message.answer(text=LEXICON_RU['ready'],
                         reply_markup=helper_kb)


# Этот хэндлер будет срабатывать на команду "/placeholder"
@router.message(Command(commands='placeholder'))
async def process_placeholder_command(message: Message):
    await message.answer(
        text='Выберите что делать с задачами',
    )


@router.message(F.text.in_([LEXICON_RU['ask_weather']]))
async def send_weather(message: Message):
    city = 'Saint-Petersburg'  # По умолчанию - Петербург
    weather_report = get_weather(city)
    await message.reply(weather_report)

# locations = {}

# @router.message(F.text.in_([LEXICON_RU['ask_weather']]))
# async def send_weather(message: Message):
#     weather_report = get_weather(latitude, longitude)
#     await message.reply(weather_report)


@router.message(F.text.in_([LEXICON_RU['gen_joke']]))
async def send_joke(message: Message):
    joke = get_joke()
    await message.reply(joke)


# @router.message(F.text.in_([LEXICON_RU['get_cat']]))
# async def send_joke(message: Message):
#     joke = get_joke()
#     await message.reply(joke)

user_tasks = {}


@router.message(Command(commands='add_task'))
async def add_task(message: Message):
    task = message.text.replace('/add_task', '')
    if task:
        user_id = message.from_user.id
        if user_id not in user_tasks:
            user_tasks[user_id] = []
        user_tasks[user_id].append(task)
        await message.reply(f"Задача '{task}' добавлена.")
    else:
        await message.reply("Кажется, задача пустая. Введите задачу после команды /add_task")


@router.message(Command(commands='list'))
async def list_tasks(message: Message):
    user_id = message.from_user.id
    if user_id in user_tasks and user_tasks[user_id]:
        tasks = "\n".join(f"{idx + 1}. {task}" for idx, task in enumerate(user_tasks[user_id]))
        await message.reply(f"Ваши задачи на день:\n{tasks}")
    else:
        await message.reply("У вас нет задач.")


@router.message(Command(commands='clear'))
async def clear_tasks(message: Message):
    user_id = message.from_user.id
    user_tasks[user_id] = []
    await message.reply("Все задачи удалены.")


@router.message(lambda message: message.text and not message.text.startswith('/'))
async def catch_all(message: Message):
    await message.reply("Пока без кнопок. Используйте /add_task для добавления задачи, /list для просмотра задач и /clear для удаления всех задач.")