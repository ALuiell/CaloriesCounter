from __future__ import annotations

from aiogram import Dispatcher, F, Router
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from app.db.database import Database
from app.services.nutrition import NutritionService
from app.services.profile import DailyNutritionTargets, ProfileService, UserProfile, activity_label


class ProfileCreateStates(StatesGroup):
    waiting_for_sex = State()
    waiting_for_age = State()
    waiting_for_height = State()
    waiting_for_weight = State()
    waiting_for_activity_level = State()


class ProfileEditStates(StatesGroup):
    choosing_field = State()
    waiting_for_sex = State()
    waiting_for_age = State()
    waiting_for_height = State()
    waiting_for_weight = State()
    waiting_for_activity_level = State()


class ActivityTodayStates(StatesGroup):
    waiting_for_activity_level = State()


class SearchStates(StatesGroup):
    waiting_for_query = State()


class AddFoodStates(StatesGroup):
    waiting_for_product = State()


BUTTON_ADD_FOOD = "Добавить еду"
BUTTON_CREATE_PROFILE = "Профиль+"
BUTTON_PROFILE = "Профиль"
BUTTON_TODAY = "Сегодня"
BUTTON_ACTIVITY = "Активность"
BUTTON_SEARCH = "Поиск"
BUTTON_HELP = "Помощь"
BUTTON_ASSISTANT_ON = "Вкл. assistant"
BUTTON_ASSISTANT_OFF = "Выкл. assistant"

CANCEL_TEXT = "Отмена"
CANCEL_EDIT_PROFILE_TEXT = CANCEL_TEXT
CANCEL_SEARCH_TEXT = CANCEL_TEXT
CANCEL_ADD_FOOD_TEXT = CANCEL_TEXT

BUTTON_ACTIVITY_TODAY = "Активность на сегодня"
BUTTON_ACTIVITY_RESET = "Сбросить активность"
BUTTON_PROFILE_EDIT = "Изменить профиль"
BUTTON_TERMS = "Что такое BMR и TDEE"
BUTTON_BACK = "Назад"

CALLBACK_PROFILE_EDIT = "profile:edit"
CALLBACK_PROFILE_ACTIVITY_TODAY = "profile:activity_today"
CALLBACK_PROFILE_ACTIVITY_RESET = "profile:activity_reset"
CALLBACK_PROFILE_ASSISTANT = "profile:assistant"
CALLBACK_PROFILE_TERMS = "profile:terms"
CALLBACK_ACTIVITY_CHANGE = "activity:change"
CALLBACK_ACTIVITY_RESET = "activity:reset"
CALLBACK_ACTIVITY_BACK = "activity:back"
CALLBACK_SEARCH_CATEGORY_PREFIX = "search:cat:"
CALLBACK_SEARCH_BACK = "search:back"
CALLBACK_ADD_FOOD_NEW = "add_food:new"
CALLBACK_ADD_FOOD_LIST = "add_food:list"
CALLBACK_ADD_FOOD_DELETE_PREFIX = "add_food:delete:"
CALLBACK_ADD_FOOD_BACK = "add_food:back"

SEX_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="male"), KeyboardButton(text="female")]],
    resize_keyboard=True,
    one_time_keyboard=True,
)

ACTIVITY_VALUE_BY_BUTTON = {
    "Спокойный день": "sedentary",
    "Легкая активность": "light",
    "Умеренная активность": "moderate",
    "Высокая активность": "active",
    "Очень высокая активность": "very_active",
}

ACTIVITY_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Спокойный день"), KeyboardButton(text="Легкая активность")],
        [KeyboardButton(text="Умеренная активность"), KeyboardButton(text="Высокая активность")],
        [KeyboardButton(text="Очень высокая активность")],
        [KeyboardButton(text=CANCEL_TEXT)],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

EDIT_PROFILE_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Пол"), KeyboardButton(text="Возраст")],
        [KeyboardButton(text="Рост"), KeyboardButton(text="Вес")],
        [KeyboardButton(text="Активность по умолчанию")],
        [KeyboardButton(text=CANCEL_EDIT_PROFILE_TEXT)],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

SEARCH_CANCEL_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=CANCEL_SEARCH_TEXT)]],
    resize_keyboard=True,
    one_time_keyboard=True,
)

ADD_FOOD_CANCEL_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=CANCEL_ADD_FOOD_TEXT)]],
    resize_keyboard=True,
    one_time_keyboard=True,
)

EDIT_FIELD_CONFIG = {
    "Пол": {
        "field": "sex",
        "state": ProfileEditStates.waiting_for_sex,
        "prompt": "Укажи новый пол: male или female.",
        "reply_markup": SEX_KEYBOARD,
    },
    "Возраст": {
        "field": "age",
        "state": ProfileEditStates.waiting_for_age,
        "prompt": "Отправь новый возраст в годах.",
        "reply_markup": ReplyKeyboardRemove(),
    },
    "Рост": {
        "field": "height_cm",
        "state": ProfileEditStates.waiting_for_height,
        "prompt": "Отправь новый рост в см.",
        "reply_markup": ReplyKeyboardRemove(),
    },
    "Вес": {
        "field": "weight_kg",
        "state": ProfileEditStates.waiting_for_weight,
        "prompt": "Отправь новый вес в кг.",
        "reply_markup": ReplyKeyboardRemove(),
    },
    "Активность по умолчанию": {
        "field": "activity_level",
        "state": ProfileEditStates.waiting_for_activity_level,
        "prompt": "Выбери новую активность по умолчанию.",
        "reply_markup": ACTIVITY_KEYBOARD,
    },
}


def build_main_menu(profile: UserProfile | None, assistant_enabled: bool) -> ReplyKeyboardMarkup:
    if profile is None or not profile.is_complete:
        keyboard = [
            [KeyboardButton(text=BUTTON_ADD_FOOD), KeyboardButton(text=BUTTON_CREATE_PROFILE)],
            [KeyboardButton(text=BUTTON_SEARCH), KeyboardButton(text=BUTTON_HELP)],
        ]
    elif assistant_enabled:
        keyboard = [
            [KeyboardButton(text=BUTTON_ADD_FOOD), KeyboardButton(text=BUTTON_TODAY)],
            [KeyboardButton(text=BUTTON_PROFILE), KeyboardButton(text=BUTTON_ACTIVITY)],
            [KeyboardButton(text=BUTTON_SEARCH), KeyboardButton(text=BUTTON_ASSISTANT_OFF)],
        ]
    else:
        keyboard = [
            [KeyboardButton(text=BUTTON_ADD_FOOD), KeyboardButton(text=BUTTON_PROFILE)],
            [KeyboardButton(text=BUTTON_SEARCH), KeyboardButton(text=BUTTON_HELP)],
            [KeyboardButton(text=BUTTON_ASSISTANT_ON)],
        ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def build_profile_actions(profile: UserProfile) -> InlineKeyboardMarkup:
    assistant_text = BUTTON_ASSISTANT_OFF if profile.assistant_enabled else BUTTON_ASSISTANT_ON
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=BUTTON_PROFILE_EDIT, callback_data=CALLBACK_PROFILE_EDIT)],
            [
                InlineKeyboardButton(text=BUTTON_ACTIVITY_TODAY, callback_data=CALLBACK_PROFILE_ACTIVITY_TODAY),
                InlineKeyboardButton(text=BUTTON_ACTIVITY_RESET, callback_data=CALLBACK_PROFILE_ACTIVITY_RESET),
            ],
            [
                InlineKeyboardButton(text=assistant_text, callback_data=CALLBACK_PROFILE_ASSISTANT),
                InlineKeyboardButton(text=BUTTON_TERMS, callback_data=CALLBACK_PROFILE_TERMS),
            ],
        ]
    )


def build_activity_actions() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=BUTTON_ACTIVITY_TODAY, callback_data=CALLBACK_ACTIVITY_CHANGE)],
            [InlineKeyboardButton(text=BUTTON_ACTIVITY_RESET, callback_data=CALLBACK_ACTIVITY_RESET)],
            [InlineKeyboardButton(text=BUTTON_BACK, callback_data=CALLBACK_ACTIVITY_BACK)],
        ]
    )


def build_search_categories(categories) -> InlineKeyboardMarkup:
    rows = [
        [
            InlineKeyboardButton(
                text=f"{category.name} ({category.count})",
                callback_data=f"{CALLBACK_SEARCH_CATEGORY_PREFIX}{category.slug}",
            )
        ]
        for category in categories
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def build_add_food_actions() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Добавить продукт", callback_data=CALLBACK_ADD_FOOD_NEW)],
            [InlineKeyboardButton(text="Мои продукты", callback_data=CALLBACK_ADD_FOOD_LIST)],
        ]
    )


def build_user_product_actions(products) -> InlineKeyboardMarkup:
    rows = [
        [
            InlineKeyboardButton(
                text=f"Удалить: {product.name}",
                callback_data=f"{CALLBACK_ADD_FOOD_DELETE_PREFIX}{product.id}",
            )
        ]
        for product in products
    ]
    rows.append([InlineKeyboardButton(text=BUTTON_BACK, callback_data=CALLBACK_ADD_FOOD_BACK)])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def register_handlers(dispatcher: Dispatcher, database: Database) -> None:
    router = Router()
    nutrition_service = NutritionService(database)
    profile_service = ProfileService(database)

    @router.message(Command("start"))
    async def start_handler(message: Message, state: FSMContext) -> None:
        await state.clear()
        await _show_welcome(message, profile_service, message.from_user.id, message.from_user.username)

    @router.message(Command("help"))
    @router.message(Command("calc"))
    async def help_handler(message: Message) -> None:
        await _show_help(message, profile_service, message.from_user.id, message.from_user.username)

    @router.message(Command("terms"))
    async def terms_handler(message: Message) -> None:
        await _send_with_main_menu(
            message,
            profile_service,
            message.from_user.id,
            message.from_user.username,
            _terms_text(),
        )

    @router.message(Command("profile"))
    async def profile_handler(message: Message, state: FSMContext) -> None:
        await _show_profile(message, state, profile_service, message.from_user.id, message.from_user.username)

    @router.message(Command("edit_profile"))
    async def edit_profile_handler(message: Message, state: FSMContext) -> None:
        await _show_edit_profile(message, state, profile_service, message.from_user.id, message.from_user.username)

    @router.message(Command("activity_today"))
    async def activity_today_handler(message: Message, state: FSMContext) -> None:
        await _prompt_activity_today(message, state, profile_service, message.from_user.id, message.from_user.username)

    @router.message(Command("activity_reset"))
    async def activity_reset_handler(message: Message) -> None:
        await _reset_activity_today(message, profile_service, message.from_user.id, message.from_user.username)

    @router.message(Command("assistant_on"))
    async def assistant_on_handler(message: Message) -> None:
        await _set_assistant_mode(message, profile_service, message.from_user.id, message.from_user.username, enabled=True)

    @router.message(Command("assistant_off"))
    async def assistant_off_handler(message: Message) -> None:
        await _set_assistant_mode(message, profile_service, message.from_user.id, message.from_user.username, enabled=False)

    @router.message(Command("today"))
    async def today_handler(message: Message) -> None:
        await _show_today(
            message,
            nutrition_service,
            profile_service,
            message.from_user.id,
            message.from_user.username,
        )

    @router.message(Command("search"))
    async def search_handler(message: Message, state: FSMContext, command: CommandObject) -> None:
        query = (command.args or "").strip()
        if query:
            await _perform_search(
                message,
                nutrition_service,
                profile_service,
                message.from_user.id,
                message.from_user.username,
                query,
            )
            return
        await _prompt_search(message, state, profile_service, message.from_user.id, message.from_user.username)

    @router.callback_query(F.data == CALLBACK_PROFILE_EDIT)
    async def profile_edit_callback(callback: CallbackQuery, state: FSMContext) -> None:
        await callback.answer()
        if callback.message is not None:
            await _show_edit_profile(
                callback.message,
                state,
                profile_service,
                callback.from_user.id,
                callback.from_user.username,
            )

    @router.callback_query(F.data == CALLBACK_PROFILE_ACTIVITY_TODAY)
    async def profile_activity_today_callback(callback: CallbackQuery, state: FSMContext) -> None:
        await callback.answer()
        if callback.message is not None:
            await _prompt_activity_today(
                callback.message,
                state,
                profile_service,
                callback.from_user.id,
                callback.from_user.username,
            )

    @router.callback_query(F.data == CALLBACK_PROFILE_ACTIVITY_RESET)
    async def profile_activity_reset_callback(callback: CallbackQuery) -> None:
        await callback.answer()
        if callback.message is not None:
            await _reset_activity_today(
                callback.message,
                profile_service,
                callback.from_user.id,
                callback.from_user.username,
            )

    @router.callback_query(F.data == CALLBACK_PROFILE_ASSISTANT)
    async def profile_assistant_callback(callback: CallbackQuery) -> None:
        await callback.answer()
        profile = profile_service.get_profile(callback.from_user.id)
        enabled = not bool(profile and profile.assistant_enabled)
        if callback.message is not None:
            await _set_assistant_mode(
                callback.message,
                profile_service,
                callback.from_user.id,
                callback.from_user.username,
                enabled=enabled,
            )

    @router.callback_query(F.data == CALLBACK_PROFILE_TERMS)
    async def profile_terms_callback(callback: CallbackQuery) -> None:
        await callback.answer()
        if callback.message is not None:
            await _send_with_main_menu(
                callback.message,
                profile_service,
                callback.from_user.id,
                callback.from_user.username,
                _terms_text(),
            )

    @router.callback_query(F.data == CALLBACK_ACTIVITY_CHANGE)
    async def activity_change_callback(callback: CallbackQuery, state: FSMContext) -> None:
        await callback.answer()
        if callback.message is not None:
            await _prompt_activity_today(
                callback.message,
                state,
                profile_service,
                callback.from_user.id,
                callback.from_user.username,
            )

    @router.callback_query(F.data == CALLBACK_ACTIVITY_RESET)
    async def activity_reset_callback(callback: CallbackQuery) -> None:
        await callback.answer()
        if callback.message is not None:
            await _reset_activity_today(
                callback.message,
                profile_service,
                callback.from_user.id,
                callback.from_user.username,
            )

    @router.callback_query(F.data == CALLBACK_ACTIVITY_BACK)
    async def activity_back_callback(callback: CallbackQuery, state: FSMContext) -> None:
        await callback.answer()
        if callback.message is not None:
            await _show_profile(
                callback.message,
                state,
                profile_service,
                callback.from_user.id,
                callback.from_user.username,
            )

    @router.callback_query(F.data == CALLBACK_SEARCH_BACK)
    async def search_back_callback(callback: CallbackQuery) -> None:
        await callback.answer()
        if callback.message is not None:
            await _show_search_categories(
                callback.message,
                nutrition_service,
                profile_service,
                callback.from_user.id,
                callback.from_user.username,
            )

    @router.callback_query(F.data.startswith(CALLBACK_SEARCH_CATEGORY_PREFIX))
    async def search_category_callback(callback: CallbackQuery) -> None:
        await callback.answer()
        category_slug = str(callback.data).removeprefix(CALLBACK_SEARCH_CATEGORY_PREFIX)
        if callback.message is not None:
            await _show_category_products(
                callback.message,
                nutrition_service,
                profile_service,
                callback.from_user.id,
                callback.from_user.username,
                category_slug,
            )

    @router.callback_query(F.data == CALLBACK_ADD_FOOD_NEW)
    async def add_food_new_callback(callback: CallbackQuery, state: FSMContext) -> None:
        await callback.answer()
        if callback.message is not None:
            await _prompt_add_food_product(
                callback.message,
                state,
                profile_service,
                callback.from_user.id,
                callback.from_user.username,
            )

    @router.callback_query(F.data == CALLBACK_ADD_FOOD_LIST)
    async def add_food_list_callback(callback: CallbackQuery) -> None:
        await callback.answer()
        if callback.message is not None:
            await _show_user_products(
                callback.message,
                nutrition_service,
                profile_service,
                callback.from_user.id,
                callback.from_user.username,
            )

    @router.callback_query(F.data == CALLBACK_ADD_FOOD_BACK)
    async def add_food_back_callback(callback: CallbackQuery) -> None:
        await callback.answer()
        if callback.message is not None:
            await _show_add_food_menu(
                callback.message,
                profile_service,
                callback.from_user.id,
                callback.from_user.username,
            )

    @router.callback_query(F.data.startswith(CALLBACK_ADD_FOOD_DELETE_PREFIX))
    async def add_food_delete_callback(callback: CallbackQuery) -> None:
        product_id_text = str(callback.data).removeprefix(CALLBACK_ADD_FOOD_DELETE_PREFIX)
        product_id = _parse_int(product_id_text)
        deleted = product_id is not None and nutrition_service.delete_user_product(callback.from_user.id, product_id)
        await callback.answer("Удалено" if deleted else "Не найдено")
        if callback.message is not None:
            await _show_user_products(
                callback.message,
                nutrition_service,
                profile_service,
                callback.from_user.id,
                callback.from_user.username,
            )

    @router.message(F.text == BUTTON_ADD_FOOD)
    async def add_food_button_handler(message: Message, state: FSMContext) -> None:
        await state.clear()
        await _show_add_food_menu(message, profile_service, message.from_user.id, message.from_user.username)

    @router.message(F.text == BUTTON_CREATE_PROFILE)
    async def create_profile_button_handler(message: Message, state: FSMContext) -> None:
        await _show_profile(message, state, profile_service, message.from_user.id, message.from_user.username)

    @router.message(F.text == BUTTON_PROFILE)
    async def profile_button_handler(message: Message, state: FSMContext) -> None:
        await _show_profile(message, state, profile_service, message.from_user.id, message.from_user.username)

    @router.message(F.text == BUTTON_TODAY)
    async def today_button_handler(message: Message) -> None:
        await _show_today(
            message,
            nutrition_service,
            profile_service,
            message.from_user.id,
            message.from_user.username,
        )

    @router.message(F.text == BUTTON_ACTIVITY)
    async def activity_button_handler(message: Message, state: FSMContext) -> None:
        await state.clear()
        await _show_activity_screen(message, profile_service, message.from_user.id, message.from_user.username)

    @router.message(F.text == BUTTON_SEARCH)
    async def search_button_handler(message: Message, state: FSMContext) -> None:
        await state.clear()
        await _show_search_categories(message, nutrition_service, profile_service, message.from_user.id, message.from_user.username)

    @router.message(F.text == BUTTON_HELP)
    async def help_button_handler(message: Message) -> None:
        await _show_help(message, profile_service, message.from_user.id, message.from_user.username)

    @router.message(F.text == BUTTON_ASSISTANT_ON)
    async def assistant_on_button_handler(message: Message) -> None:
        await _set_assistant_mode(message, profile_service, message.from_user.id, message.from_user.username, enabled=True)

    @router.message(F.text == BUTTON_ASSISTANT_OFF)
    async def assistant_off_button_handler(message: Message) -> None:
        await _set_assistant_mode(message, profile_service, message.from_user.id, message.from_user.username, enabled=False)

    @router.message(ProfileEditStates.choosing_field)
    async def edit_profile_choose_field_handler(message: Message, state: FSMContext) -> None:
        text = (message.text or "").strip()
        if text == CANCEL_EDIT_PROFILE_TEXT:
            await state.clear()
            profile = profile_service.get_profile(message.from_user.id)
            targets = profile_service.get_daily_targets(message.from_user.id) if profile and profile.is_complete else None
            body = "Изменения не вносились."
            if profile is not None and targets is not None:
                body = f"{body}\n\n{_format_profile_card(profile, targets)}"
            await message.answer(
                body,
                reply_markup=build_main_menu(profile, bool(profile and profile.assistant_enabled)),
            )
            if profile is not None and profile.is_complete:
                await message.answer("Быстрые действия профиля:", reply_markup=build_profile_actions(profile))
            return

        config = EDIT_FIELD_CONFIG.get(text)
        if config is None:
            await message.answer(
                "Выбери поле: Пол, Возраст, Рост, Вес, Активность по умолчанию или Отмена."
            )
            return

        await state.update_data(edit_field=config["field"])
        await state.set_state(config["state"])
        await message.answer(config["prompt"], reply_markup=config["reply_markup"])

    @router.message(SearchStates.waiting_for_query)
    async def search_query_handler(message: Message, state: FSMContext) -> None:
        text = (message.text or "").strip()
        if text == CANCEL_SEARCH_TEXT:
            await state.clear()
            await _send_with_main_menu(
                message,
                profile_service,
                message.from_user.id,
                message.from_user.username,
                "Поиск отменен.",
            )
            return

        await state.clear()
        await _perform_search(
            message,
            nutrition_service,
            profile_service,
            message.from_user.id,
            message.from_user.username,
            text,
        )

    @router.message(AddFoodStates.waiting_for_product)
    async def add_food_product_handler(message: Message, state: FSMContext) -> None:
        text = (message.text or "").strip()
        if text == CANCEL_ADD_FOOD_TEXT:
            await state.clear()
            await _send_with_main_menu(
                message,
                profile_service,
                message.from_user.id,
                message.from_user.username,
                "Добавление еды отменено.",
            )
            return

        parsed = _parse_user_product_input(text)
        if parsed is None:
            await message.answer(
                "Не получилось разобрать продукт.\n"
                "Формат: <code>название; ккал; белки; жиры; углеводы</code>\n"
                "Пример: <code>сырники домашние; 210; 14; 9; 20</code>",
                reply_markup=ADD_FOOD_CANCEL_KEYBOARD,
            )
            return

        name_ru, calories, protein, fat, carbs = parsed
        nutrition_service.create_user_product(
            message.from_user.id,
            message.from_user.username,
            name_ru,
            calories,
            protein,
            fat,
            carbs,
        )
        await state.clear()
        await _send_with_main_menu(
            message,
            profile_service,
            message.from_user.id,
            message.from_user.username,
            "Сохранил личную еду:\n"
            f"<b>{name_ru}</b> на 100 г: {round(calories)} ккал, "
            f"Б {_format_number(protein)} / Ж {_format_number(fat)} / У {_format_number(carbs)}.\n\n"
            f"Теперь можно писать: <code>{name_ru} 150</code>",
        )

    @router.message(ProfileCreateStates.waiting_for_sex)
    async def profile_sex_handler(message: Message, state: FSMContext) -> None:
        value = (message.text or "").strip().lower()
        if value not in {"male", "female"}:
            await message.answer("Укажи пол: male или female.", reply_markup=SEX_KEYBOARD)
            return
        await state.update_data(sex=value)
        await state.set_state(ProfileCreateStates.waiting_for_age)
        await message.answer("Отправь возраст в годах.", reply_markup=ReplyKeyboardRemove())

    @router.message(ProfileCreateStates.waiting_for_age)
    async def profile_age_handler(message: Message, state: FSMContext) -> None:
        age = _parse_int(message.text)
        if age is None or age < 10 or age > 120:
            await message.answer("Возраст должен быть числом от 10 до 120.")
            return
        await state.update_data(age=age)
        await state.set_state(ProfileCreateStates.waiting_for_height)
        await message.answer("Отправь рост в см.")

    @router.message(ProfileCreateStates.waiting_for_height)
    async def profile_height_handler(message: Message, state: FSMContext) -> None:
        height_cm = _parse_float(message.text)
        if height_cm is None or height_cm < 80 or height_cm > 250:
            await message.answer("Рост должен быть числом от 80 до 250 см.")
            return
        await state.update_data(height_cm=height_cm)
        await state.set_state(ProfileCreateStates.waiting_for_weight)
        await message.answer("Отправь вес в кг.")

    @router.message(ProfileCreateStates.waiting_for_weight)
    async def profile_weight_handler(message: Message, state: FSMContext) -> None:
        weight_kg = _parse_float(message.text)
        if weight_kg is None or weight_kg < 20 or weight_kg > 300:
            await message.answer("Вес должен быть числом от 20 до 300 кг.")
            return
        await state.update_data(weight_kg=weight_kg)
        await state.set_state(ProfileCreateStates.waiting_for_activity_level)
        await message.answer("Выбери активность по умолчанию.", reply_markup=ACTIVITY_KEYBOARD)

    @router.message(ProfileCreateStates.waiting_for_activity_level)
    async def profile_activity_handler(message: Message, state: FSMContext) -> None:
        activity_level = _parse_activity_button(message.text)
        if activity_level is None:
            await message.answer("Выбери один из вариантов активности.", reply_markup=ACTIVITY_KEYBOARD)
            return

        data = await state.get_data()
        profile_service.update_profile(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            sex=str(data["sex"]),
            age=int(data["age"]),
            height_cm=float(data["height_cm"]),
            weight_kg=float(data["weight_kg"]),
            activity_level=activity_level,
        )
        await state.clear()
        profile = profile_service.get_profile(message.from_user.id)
        targets = profile_service.get_daily_targets(message.from_user.id)
        await message.answer(
            f"Профиль сохранен.\n\n{_format_profile_card(profile, targets)}",
            reply_markup=build_main_menu(profile, bool(profile and profile.assistant_enabled)),
        )
        if profile is not None:
            await message.answer("Быстрые действия профиля:", reply_markup=build_profile_actions(profile))

    @router.message(ProfileEditStates.waiting_for_sex)
    async def edit_profile_sex_handler(message: Message, state: FSMContext) -> None:
        value = (message.text or "").strip().lower()
        if value not in {"male", "female"}:
            await message.answer("Укажи пол: male или female.", reply_markup=SEX_KEYBOARD)
            return
        await _save_profile_edit(message, state, profile_service, "sex", value)

    @router.message(ProfileEditStates.waiting_for_age)
    async def edit_profile_age_handler(message: Message, state: FSMContext) -> None:
        age = _parse_int(message.text)
        if age is None or age < 10 or age > 120:
            await message.answer("Возраст должен быть числом от 10 до 120.")
            return
        await _save_profile_edit(message, state, profile_service, "age", age)

    @router.message(ProfileEditStates.waiting_for_height)
    async def edit_profile_height_handler(message: Message, state: FSMContext) -> None:
        height_cm = _parse_float(message.text)
        if height_cm is None or height_cm < 80 or height_cm > 250:
            await message.answer("Рост должен быть числом от 80 до 250 см.")
            return
        await _save_profile_edit(message, state, profile_service, "height_cm", height_cm)

    @router.message(ProfileEditStates.waiting_for_weight)
    async def edit_profile_weight_handler(message: Message, state: FSMContext) -> None:
        weight_kg = _parse_float(message.text)
        if weight_kg is None or weight_kg < 20 or weight_kg > 300:
            await message.answer("Вес должен быть числом от 20 до 300 кг.")
            return
        await _save_profile_edit(message, state, profile_service, "weight_kg", weight_kg)

    @router.message(ProfileEditStates.waiting_for_activity_level)
    async def edit_profile_activity_handler(message: Message, state: FSMContext) -> None:
        if (message.text or "").strip() == CANCEL_TEXT:
            await state.set_state(ProfileEditStates.choosing_field)
            await message.answer("Что хочешь изменить?", reply_markup=EDIT_PROFILE_KEYBOARD)
            return

        activity_level = _parse_activity_button(message.text)
        if activity_level is None:
            await message.answer("Выбери один из вариантов активности.", reply_markup=ACTIVITY_KEYBOARD)
            return
        await _save_profile_edit(message, state, profile_service, "activity_level", activity_level)

    @router.message(ActivityTodayStates.waiting_for_activity_level)
    async def activity_today_value_handler(message: Message, state: FSMContext) -> None:
        if (message.text or "").strip() == CANCEL_TEXT:
            await state.clear()
            await _show_activity_screen(
                message,
                profile_service,
                message.from_user.id,
                message.from_user.username,
            )
            return

        activity_level = _parse_activity_button(message.text)
        if activity_level is None:
            await message.answer("Выбери один из вариантов активности.", reply_markup=ACTIVITY_KEYBOARD)
            return

        profile_service.set_activity_override_for_today(message.from_user.id, activity_level)
        await state.clear()
        profile = profile_service.get_profile(message.from_user.id)
        targets = profile_service.get_daily_targets(message.from_user.id)
        await message.answer(
            "Активность на сегодня сохранена.\n"
            "Этот выбор действует только до конца текущего дня.\n\n"
            f"{_format_targets_short_block(targets)}",
            reply_markup=build_main_menu(profile, bool(profile and profile.assistant_enabled)),
        )

    @router.message(F.text)
    async def food_message_handler(message: Message, state: FSMContext) -> None:
        await state.clear()
        profile_service.ensure_user(message.from_user.id, message.from_user.username)
        result = nutrition_service.process_message(message.from_user.id, message.text or "")

        if result.assistant_enabled:
            nutrition_service.store_entries(message.from_user.id, result.recognized_items)
            today = nutrition_service.get_today_summary(message.from_user.id)
            targets = profile_service.get_daily_targets(message.from_user.id)
            reply = nutrition_service.format_assistant_reply(result, today, targets)
        else:
            reply = nutrition_service.format_calc_reply(result)

        await _send_with_main_menu(
            message,
            profile_service,
            message.from_user.id,
            message.from_user.username,
            reply,
        )

    dispatcher.include_router(router)


async def _show_welcome(
    output_message: Message,
    profile_service: ProfileService,
    telegram_id: int,
    username: str | None,
) -> None:
    await _send_with_main_menu(
        output_message,
        profile_service,
        telegram_id,
        username,
        "Бот готов.\n\n"
        "Отправь еду, например:\n"
        "<code>гречка 120, курица 180, помидор 80</code>\n\n"
        "Используй кнопки внизу для навигации.\n"
        "Короткая справка по метрикам: /terms.",
    )


async def _show_help(
    output_message: Message,
    profile_service: ProfileService,
    telegram_id: int,
    username: str | None,
) -> None:
    await _send_with_main_menu(
        output_message,
        profile_service,
        telegram_id,
        username,
        "Как пользоваться ботом:\n\n"
        "1. Отправь еду обычным текстом.\n"
        "Примеры:\n"
        "<code>гречка 120, курица 180</code>\n"
        "<code>рис 100\nпомидор 80</code>\n\n"
        f"2. {BUTTON_ADD_FOOD} — добавь личный продукт или готовое блюдо, если его нет в базе.\n"
        f"3. {BUTTON_PROFILE} или {BUTTON_CREATE_PROFILE} — настрой профиль.\n"
        f"4. {BUTTON_TODAY} — смотри итог за сегодня.\n"
        f"5. {BUTTON_ACTIVITY} — меняй активность на сегодня.\n"
        f"6. {BUTTON_SEARCH} — ищи продукты по базе.\n\n"
        "Команды тоже работают, но кнопки теперь основной способ навигации.\n"
        "Что такое BMR и TDEE: /terms",
    )


async def _show_profile(
    output_message: Message,
    state: FSMContext,
    profile_service: ProfileService,
    telegram_id: int,
    username: str | None,
) -> None:
    profile_service.ensure_user(telegram_id, username)
    profile = profile_service.get_profile(telegram_id)
    if profile is not None and profile.is_complete:
        await state.clear()
        targets = profile_service.get_daily_targets(telegram_id)
        await output_message.answer(
            _format_profile_card(profile, targets),
            reply_markup=build_main_menu(profile, bool(profile.assistant_enabled)),
        )
        await output_message.answer("Быстрые действия профиля:", reply_markup=build_profile_actions(profile))
        return

    await _start_profile_onboarding(output_message, state, profile)


async def _show_edit_profile(
    output_message: Message,
    state: FSMContext,
    profile_service: ProfileService,
    telegram_id: int,
    username: str | None,
) -> None:
    profile_service.ensure_user(telegram_id, username)
    profile = profile_service.get_profile(telegram_id)
    if profile is None or not profile.is_complete:
        await state.clear()
        await _send_with_main_menu(
            output_message,
            profile_service,
            telegram_id,
            username,
            "Профиль еще не заполнен полностью. Сначала используй /profile.",
        )
        return

    targets = profile_service.get_daily_targets(telegram_id)
    await state.set_state(ProfileEditStates.choosing_field)
    await output_message.answer(
        f"{_format_profile_card(profile, targets)}\n\nЧто хочешь изменить?",
        reply_markup=EDIT_PROFILE_KEYBOARD,
    )


async def _show_activity_screen(
    output_message: Message,
    profile_service: ProfileService,
    telegram_id: int,
    username: str | None,
) -> None:
    profile_service.ensure_user(telegram_id, username)
    profile = profile_service.get_profile(telegram_id)
    if profile is None or not profile.is_complete:
        await _send_with_main_menu(
            output_message,
            profile_service,
            telegram_id,
            username,
            "Чтобы открыть активность, сначала заполни профиль через /profile.",
        )
        return

    targets = profile_service.get_daily_targets(telegram_id)
    text = (
        "Активность:\n"
        f"По умолчанию: {targets.default_activity_label}\n"
        f"Для расчета сегодня: {targets.effective_activity_label}\n"
        f"{targets.activity_source_label}"
    )
    await output_message.answer(
        text,
        reply_markup=build_main_menu(profile, bool(profile.assistant_enabled)),
    )
    await output_message.answer("Действия:", reply_markup=build_activity_actions())


async def _prompt_activity_today(
    output_message: Message,
    state: FSMContext,
    profile_service: ProfileService,
    telegram_id: int,
    username: str | None,
) -> None:
    profile_service.ensure_user(telegram_id, username)
    profile = profile_service.get_profile(telegram_id)
    if profile is None or not profile.is_complete:
        await state.clear()
        await _send_with_main_menu(
            output_message,
            profile_service,
            telegram_id,
            username,
            "Чтобы выбрать активность на сегодня, сначала заполни профиль через /profile.",
        )
        return

    targets = profile_service.get_daily_targets(telegram_id)
    await state.set_state(ActivityTodayStates.waiting_for_activity_level)
    await output_message.answer(
        "Выбери активность на сегодня.\n\n"
        f"Сейчас для расчетов используется: {targets.effective_activity_label}\n"
        f"{targets.activity_source_label}",
        reply_markup=ACTIVITY_KEYBOARD,
    )


async def _reset_activity_today(
    output_message: Message,
    profile_service: ProfileService,
    telegram_id: int,
    username: str | None,
) -> None:
    profile_service.ensure_user(telegram_id, username)
    profile = profile_service.get_profile(telegram_id)
    if profile is None or profile.activity_level is None:
        await _send_with_main_menu(
            output_message,
            profile_service,
            telegram_id,
            username,
            "Сначала заполни профиль через /profile.",
        )
        return

    profile_service.clear_activity_override_for_today(telegram_id)
    targets = profile_service.get_daily_targets(telegram_id)
    await output_message.answer(
        "Активность на сегодня сброшена. Снова используется активность по умолчанию.\n\n"
        f"{_format_targets_short_block(targets)}",
        reply_markup=build_main_menu(profile, bool(profile.assistant_enabled)),
    )


async def _show_today(
    output_message: Message,
    nutrition_service: NutritionService,
    profile_service: ProfileService,
    telegram_id: int,
    username: str | None,
) -> None:
    profile_service.ensure_user(telegram_id, username)
    if not profile_service.has_complete_profile(telegram_id):
        await _send_with_main_menu(
            output_message,
            profile_service,
            telegram_id,
            username,
            "Профиль заполнен не полностью. Сначала используй /profile.",
        )
        return

    today = nutrition_service.get_today_summary(telegram_id)
    targets = profile_service.get_daily_targets(telegram_id)
    profile = profile_service.get_profile(telegram_id)
    await output_message.answer(
        nutrition_service.format_today_with_targets(today, targets),
        reply_markup=build_main_menu(profile, bool(profile and profile.assistant_enabled)),
    )


async def _prompt_search(
    output_message: Message,
    state: FSMContext,
    profile_service: ProfileService,
    telegram_id: int,
    username: str | None,
) -> None:
    await state.set_state(SearchStates.waiting_for_query)
    await output_message.answer(
        "Напиши название продукта для поиска.\nДля отмены нажми «Отмена».",
        reply_markup=SEARCH_CANCEL_KEYBOARD,
    )


async def _show_search_categories(
    output_message: Message,
    nutrition_service: NutritionService,
    profile_service: ProfileService,
    telegram_id: int,
    username: str | None,
) -> None:
    profile_service.ensure_user(telegram_id, username)
    categories = nutrition_service.list_categories()
    if not categories:
        await _send_with_main_menu(
            output_message,
            profile_service,
            telegram_id,
            username,
            "Категории пока недоступны.",
        )
        return

    profile = profile_service.get_profile(telegram_id)
    await output_message.answer(
        "Выбери категорию или напиши /search с названием продукта.",
        reply_markup=build_main_menu(profile, bool(profile and profile.assistant_enabled)),
    )
    await output_message.answer("Категории:", reply_markup=build_search_categories(categories))


async def _show_category_products(
    output_message: Message,
    nutrition_service: NutritionService,
    profile_service: ProfileService,
    telegram_id: int,
    username: str | None,
    category_slug: str,
) -> None:
    products = nutrition_service.list_products_by_category(category_slug)
    if not products:
        await _send_with_main_menu(
            output_message,
            profile_service,
            telegram_id,
            username,
            "В этой категории ничего не найдено.",
        )
        return

    lines = ["Продукты в категории:"]
    lines.extend(_format_product_summary(product) for product in products)
    await _send_with_main_menu(
        output_message,
        profile_service,
        telegram_id,
        username,
        "\n".join(lines),
    )
    await output_message.answer(
        "Можно отправить продукт обычным сообщением, например: <code>название 100</code>",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=BUTTON_BACK, callback_data=CALLBACK_SEARCH_BACK)]]
        ),
    )


async def _perform_search(
    output_message: Message,
    nutrition_service: NutritionService,
    profile_service: ProfileService,
    telegram_id: int,
    username: str | None,
    query: str,
) -> None:
    matches = nutrition_service.search_products(query, telegram_id)
    if not matches:
        await _send_with_main_menu(
            output_message,
            profile_service,
            telegram_id,
            username,
            f"По запросу <code>{query}</code> ничего не найдено.",
        )
        return

    lines = ["Найдено:"]
    lines.extend(f"- {name}" for name in matches)
    await _send_with_main_menu(
        output_message,
        profile_service,
        telegram_id,
        username,
        "\n".join(lines),
    )


async def _show_add_food_menu(
    output_message: Message,
    profile_service: ProfileService,
    telegram_id: int,
    username: str | None,
) -> None:
    profile_service.ensure_user(telegram_id, username)
    profile = profile_service.get_profile(telegram_id)
    await output_message.answer(
        "Что сделать с личной едой?",
        reply_markup=build_main_menu(profile, bool(profile and profile.assistant_enabled)),
    )
    await output_message.answer("Выбери действие:", reply_markup=build_add_food_actions())


async def _prompt_add_food_product(
    output_message: Message,
    state: FSMContext,
    profile_service: ProfileService,
    telegram_id: int,
    username: str | None,
) -> None:
    profile_service.ensure_user(telegram_id, username)
    await state.set_state(AddFoodStates.waiting_for_product)
    await output_message.answer(
        "Добавь личный продукт или готовое блюдо.\n\n"
        "Формат на 100 г:\n"
        "<code>название; ккал; белки; жиры; углеводы</code>\n\n"
        "Пример:\n"
        "<code>сырники домашние; 210; 14; 9; 20</code>\n\n"
        "Эта еда будет видна только тебе.",
        reply_markup=ADD_FOOD_CANCEL_KEYBOARD,
    )


async def _show_user_products(
    output_message: Message,
    nutrition_service: NutritionService,
    profile_service: ProfileService,
    telegram_id: int,
    username: str | None,
) -> None:
    profile_service.ensure_user(telegram_id, username)
    products = nutrition_service.list_user_products(telegram_id)
    if not products:
        await _send_with_main_menu(
            output_message,
            profile_service,
            telegram_id,
            username,
            "Личных продуктов пока нет. Нажми «Добавить продукт», чтобы сохранить свой вариант.",
        )
        await output_message.answer("Действия:", reply_markup=build_add_food_actions())
        return

    lines = ["Мои продукты:"]
    lines.extend(_format_product_summary(product) for product in products)
    await _send_with_main_menu(
        output_message,
        profile_service,
        telegram_id,
        username,
        "\n".join(lines),
    )
    await output_message.answer("Удаление:", reply_markup=build_user_product_actions(products))


async def _set_assistant_mode(
    output_message: Message,
    profile_service: ProfileService,
    telegram_id: int,
    username: str | None,
    enabled: bool,
) -> None:
    profile_service.ensure_user(telegram_id, username)
    if enabled and not profile_service.has_complete_profile(telegram_id):
        await _send_with_main_menu(
            output_message,
            profile_service,
            telegram_id,
            username,
            "Профиль заполнен не полностью. Сначала используй /profile.",
        )
        return

    profile_service.set_assistant_mode(telegram_id, enabled)
    profile = profile_service.get_profile(telegram_id)
    text = (
        "Assistant mode включен. Теперь ответы на еду будут содержать итоги за сегодня, BMR, TDEE и расчетную норму БЖУ."
        if enabled
        else "Assistant mode выключен. Бот снова отвечает только расчетом по сообщению."
    )
    await output_message.answer(text, reply_markup=build_main_menu(profile, bool(profile and profile.assistant_enabled)))


async def _send_with_main_menu(
    output_message: Message,
    profile_service: ProfileService,
    telegram_id: int,
    username: str | None,
    text: str,
) -> None:
    profile_service.ensure_user(telegram_id, username)
    profile = profile_service.get_profile(telegram_id)
    await output_message.answer(text, reply_markup=build_main_menu(profile, bool(profile and profile.assistant_enabled)))


async def _start_profile_onboarding(
    message: Message,
    state: FSMContext,
    profile: UserProfile | None,
) -> None:
    await state.clear()
    initial_data = {
        "sex": profile.sex if profile else None,
        "age": profile.age if profile else None,
        "height_cm": profile.height_cm if profile else None,
        "weight_kg": profile.weight_kg if profile else None,
    }
    await state.update_data(**initial_data)

    if profile is None or profile.sex is None:
        await state.set_state(ProfileCreateStates.waiting_for_sex)
        await message.answer(
            "Давай настроим профиль.\nУкажи пол: male или female.",
            reply_markup=SEX_KEYBOARD,
        )
        return
    if profile.age is None:
        await state.set_state(ProfileCreateStates.waiting_for_age)
        await message.answer("Отправь возраст в годах.", reply_markup=ReplyKeyboardRemove())
        return
    if profile.height_cm is None:
        await state.set_state(ProfileCreateStates.waiting_for_height)
        await message.answer("Отправь рост в см.", reply_markup=ReplyKeyboardRemove())
        return
    if profile.weight_kg is None:
        await state.set_state(ProfileCreateStates.waiting_for_weight)
        await message.answer("Отправь вес в кг.", reply_markup=ReplyKeyboardRemove())
        return

    await state.set_state(ProfileCreateStates.waiting_for_activity_level)
    await message.answer("Осталось выбрать активность по умолчанию.", reply_markup=ACTIVITY_KEYBOARD)


async def _save_profile_edit(
    message: Message,
    state: FSMContext,
    profile_service: ProfileService,
    field_name: str,
    value: str | int | float,
) -> None:
    profile_service.update_profile_field(message.from_user.id, message.from_user.username, field_name, value)
    await state.clear()
    profile = profile_service.get_profile(message.from_user.id)
    targets = profile_service.get_daily_targets(message.from_user.id)
    await message.answer(
        f"Профиль обновлен.\n\n{_format_profile_card(profile, targets)}",
        reply_markup=build_main_menu(profile, bool(profile and profile.assistant_enabled)),
    )
    if profile is not None:
        await message.answer("Быстрые действия профиля:", reply_markup=build_profile_actions(profile))


def _format_profile_card(profile: UserProfile | None, targets: DailyNutritionTargets) -> str:
    if profile is None or not profile.is_complete:
        return "Профиль еще не заполнен."

    sex_label = "Мужской" if profile.sex == "male" else "Женский"
    assistant_label = "включен" if profile.assistant_enabled else "выключен"
    return (
        "Твой профиль:\n"
        f"Пол: {sex_label}\n"
        f"Возраст: {profile.age}\n"
        f"Рост: {_format_number(profile.height_cm)} см\n"
        f"Вес: {_format_number(profile.weight_kg)} кг\n"
        f"Активность по умолчанию: {activity_label(str(profile.activity_level))}\n"
        f"Assistant mode: {assistant_label}\n\n"
        f"{_format_targets_short_block(targets)}"
    )


def _format_targets_short_block(targets: DailyNutritionTargets) -> str:
    return (
        f"BMR: <b>{round(targets.bmr)}</b> ккал\n"
        f"TDEE: <b>{round(targets.tdee)}</b> ккал\n"
        f"Активность для расчета сегодня: {targets.effective_activity_label}\n"
        f"{targets.activity_source_label}\n"
        "Расчетная дневная норма БЖУ (приблизительно):\n"
        f"Б: {_format_number(targets.protein_g)} г / "
        f"Ж: {_format_number(targets.fat_g)} г / "
        f"У: {_format_number(targets.carbs_g)} г\n"
        "BMR — расход в покое, TDEE — расход с учетом активности.\n"
        "Подробнее: /terms"
    )


def _terms_text() -> str:
    return (
        "Короткая справка по метрикам:\n\n"
        "BMR — базовый обмен веществ.\n"
        "Это сколько калорий организм тратит в покое: на дыхание, работу сердца, мозга и органов.\n\n"
        "TDEE — примерный расход калорий за день с учетом активности.\n"
        "Это BMR, умноженный на выбранный уровень активности.\n\n"
        "Расчетная дневная норма БЖУ — ориентир по белкам, жирам и углеводам, рассчитанный от TDEE.\n"
        "Это приблизительный расчет, а не медицинская рекомендация."
    )


def _parse_activity_button(value: str | None) -> str | None:
    if value is None:
        return None
    return ACTIVITY_VALUE_BY_BUTTON.get(value.strip())


def _format_number(value: float | int | None) -> str:
    if value is None:
        return "-"
    text = f"{float(value):.1f}"
    if text.endswith(".0"):
        return text[:-2]
    return text


def _format_product_summary(product) -> str:
    return (
        f"- {product.name}: {round(product.calories_per_100g)} ккал, "
        f"Б {_format_number(product.protein_per_100g)} / "
        f"Ж {_format_number(product.fat_per_100g)} / "
        f"У {_format_number(product.carbs_per_100g)}"
    )


def _parse_int(value: str | None) -> int | None:
    if value is None:
        return None
    try:
        return int(value.strip())
    except ValueError:
        return None


def _parse_float(value: str | None) -> float | None:
    if value is None:
        return None
    try:
        return float(value.strip().replace(",", "."))
    except ValueError:
        return None


def _parse_user_product_input(value: str) -> tuple[str, float, float, float, float] | None:
    parts = [part.strip() for part in value.split(";")]
    if len(parts) != 5:
        return None

    name_ru = parts[0]
    if len(name_ru) < 2:
        return None

    calories = _parse_float(parts[1])
    protein = _parse_float(parts[2])
    fat = _parse_float(parts[3])
    carbs = _parse_float(parts[4])
    if calories is None or protein is None or fat is None or carbs is None:
        return None

    if not (0 <= calories <= 1000):
        return None
    if not (0 <= protein <= 100 and 0 <= fat <= 100 and 0 <= carbs <= 100):
        return None

    return name_ru, calories, protein, fat, carbs
