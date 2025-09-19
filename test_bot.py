import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Contact
)
import asyncio
from datetime import datetime, timedelta

# ===== SETUP =====
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize bot
bot = Bot(
    token="7600606099:AAFcOQo3GItSzpgehhEmb7d8xb7V_tktcuU",
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

# Initialize storage and dispatcher
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# ===== DATABASE MOCK =====
users_db = {}
donations_db = {}
events_db = {
    datetime.now().strftime("%Y-%m-%d"): {
        "location": "ЦК МИФИ",
        "external_link": "https://example.com/external"
    },
    (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"): {
        "location": "ЦК Городская больница №1",
        "external_link": "https://example.com/external2"
    },
}


# ===== STATES =====
class RegistrationStates(StatesGroup):
    PHONE = State()
    FIO = State()
    CATEGORY = State()
    GROUP = State()
    CONSENT = State()


class DonationRegistration(StatesGroup):
    CHOOSE_DATE = State()
    CONFIRM_EXTERNAL = State()


# ===== KEYBOARDS =====
def get_phone_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Отправить номер", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def get_category_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎓 Студент")],
            [KeyboardButton(text="👨‍💼 Сотрудник")],
            [KeyboardButton(text="👥 Внешний донор")]
        ],
        resize_keyboard=True
    )


def get_consent_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Да, согласен")],
            [KeyboardButton(text="❌ Нет, не согласен")]
        ],
        resize_keyboard=True
    )


def get_main_menu_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Мои данные")],
            [KeyboardButton(text="📅 Записаться на донацию")],
            [KeyboardButton(text="ℹ️ Информация о донорстве")],
            [KeyboardButton(text="❓ Задать вопрос")]
        ],
        resize_keyboard=True
    )


def get_dates_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for date in events_db:
        keyboard.inline_keyboard.append(
            [InlineKeyboardButton(text=date, callback_data=f"date_{date}")]
        )
    return keyboard


# ===== HANDLERS =====
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "👋 Привет! Я бот для доноров крови МИФИ.\n\n"
        "Я помогу:\n"
        "- 📅 Записаться на донацию\n"
        "- ℹ️ Узнать информацию\n"
        "- ❓ Задать вопросы\n\n"
        "Для начала пройдите регистрацию.",
        reply_markup=get_main_menu_keyboard()
    )


@dp.message(F.text == "📋 Мои данные")
async def show_profile(message: Message):
    user_id = str(message.from_user.id)
    if user_id not in users_db:
        await message.answer("Пожалуйста, авторизуйтесь", reply_markup=get_phone_keyboard())
        await dp.set_state(message.from_user.id, RegistrationStates.PHONE)
    else:
        user = users_db[user_id]
        donations = donations_db.get(user_id, [])

        text = (
            f"👤 <b>Ваши данные:</b>\n"
            f"ФИО: {user['fio']}\n"
            f"Статус: {user['category']}\n"
        )

        if user['category'] == "🎓 Студент":
            text += f"Группа: {user.get('group', 'не указана')}\n"

        text += (
            f"\n🩸 <b>Донаций:</b> {len(donations)}\n"
        )

        if donations:
            last = donations[-1]
            text += f"📅 Последняя: {last['date']} ({last['location']})\n"

        text += f"🧬 В регистре ДКМ: {'✅ Да' if user.get('in_registry', False) else '❌ Нет'}"
        await message.answer(text)


@dp.message(RegistrationStates.PHONE, F.contact)
async def process_phone(message: Message, state: FSMContext):
    phone = message.contact.phone_number
    user_id = str(message.from_user.id)

    if user_id in users_db:
        await state.clear()
        await message.answer(
            f"🔑 Вы авторизованы! Ваш номер: {phone}",
            reply_markup=get_main_menu_keyboard()
        )
    else:
        await state.update_data(phone=phone)
        await message.answer(
            "📝 Введите ваше ФИО (например, Иванов Иван Иванович):",
            reply_markup=types.ReplyKeyboardRemove()
        )
        await dp.set_state(message.from_user.id, RegistrationStates.FIO)


@dp.message(RegistrationStates.FIO)
async def process_fio(message: Message, state: FSMContext):
    fio = message.text.strip()

    if len(fio.split()) != 3 or not all(word.isalpha() for word in fio.split()):
        await message.answer("❌ Неверный формат. Введите: Фамилия Имя Отчество")
        return

    fio = " ".join(word.capitalize() for word in fio.split())
    await state.update_data(fio=fio)
    await message.answer("👥 Выберите категорию:", reply_markup=get_category_keyboard())
    await dp.set_state(message.from_user.id, RegistrationStates.CATEGORY)


@dp.message(RegistrationStates.CATEGORY)
async def process_category(message: Message, state: FSMContext):
    if message.text not in ["🎓 Студент", "👨‍💼 Сотрудник", "👥 Внешний донор"]:
        await message.answer("❌ Выберите вариант из клавиатуры")
        return

    await state.update_data(category=message.text)

    if message.text == "🎓 Студент":
        await message.answer("🎓 Введите номер группы:", reply_markup=types.ReplyKeyboardRemove())
        await dp.set_state(message.from_user.id, RegistrationStates.GROUP)
    else:
        await message.answer(
            "📄 <b>Условия использования:</b>\n\n"
            "1. Согласие на обработку данных\n"
            "2. Подписка на уведомления\n\n"
            "Вы согласны?",
            reply_markup=get_consent_keyboard()
        )
        await dp.set_state(message.from_user.id, RegistrationStates.CONSENT)


@dp.message(RegistrationStates.GROUP)
async def process_group(message: Message, state: FSMContext):
    group = message.text.strip()
    await state.update_data(group=group)
    await message.answer(
        "📄 <b>Условия использования:</b>\n\n"
        "1. Согласие на обработку данных\n"
        "2. Подписка на уведомления\n\n"
        "Вы согласны?",
        reply_markup=get_consent_keyboard()
    )
    await dp.set_state(message.from_user.id, RegistrationStates.CONSENT)


@dp.message(RegistrationStates.CONSENT)
async def process_consent(message: Message, state: FSMContext):
    if message.text != "✅ Да, согласен":
        await message.answer("❌ Регистрация отменена", reply_markup=types.ReplyKeyboardRemove())
        await state.clear()
        return

    data = await state.get_data()
    user_id = str(message.from_user.id)

    users_db[user_id] = {
        "phone": data["phone"],
        "fio": data["fio"],
        "category": data["category"],
        "group": data.get("group", ""),
        "in_registry": False,
        "consent_given": True,
        "reg_date": datetime.now().strftime("%Y-%m-%d")
    }

    await state.clear()
    await message.answer("✅ Регистрация завершена!", reply_markup=get_main_menu_keyboard())


# ===== MAIN =====
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())