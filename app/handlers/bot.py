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
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Message,
)

from app.db.database import Database
from app.services.nutrition import NutritionService
from app.services.profile import DailyNutritionTargets, ProfileService, UserProfile
from app.core.i18n import get_text


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


BUTTON_ADD_FOOD = get_text("ru", "btn_add_food")
BUTTON_CREATE_PROFILE = get_text("ru", "btn_create_profile")
BUTTON_PROFILE = get_text("ru", "btn_profile")
BUTTON_TODAY = get_text("ru", "btn_today")
BUTTON_ACTIVITY = get_text("ru", "btn_activity")
BUTTON_SEARCH = get_text("ru", "btn_search")
BUTTON_HELP = get_text("ru", "btn_help")
BUTTON_ASSISTANT_ON = get_text("ru", "btn_assistant_on")
BUTTON_ASSISTANT_OFF = get_text("ru", "btn_assistant_off")
CANCEL_TEXT = get_text("ru", "btn_cancel")
CANCEL_EDIT_PROFILE_TEXT = CANCEL_TEXT
CANCEL_SEARCH_TEXT = CANCEL_TEXT
CANCEL_ADD_FOOD_TEXT = CANCEL_TEXT


class AddFoodStates(StatesGroup):
    waiting_for_product = State()


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
CALLBACK_CHOOSE_LANG_PREFIX = "lang:set:"


def _get_user_lang(telegram_id: int, profile_service: ProfileService, from_user=None) -> str:
    profile = profile_service.get_profile(telegram_id)
    if profile:
        if profile.language_set:
            return profile.language
        if from_user and from_user.language_code:
            code = from_user.language_code.lower()
            if code in {"ru", "uk", "en"}:
                return code
        return profile.language
    if from_user and from_user.language_code:
        code = from_user.language_code.lower()
        if code in {"ru", "uk", "en"}:
            return code
    return "ru"


def build_sex_keyboard(lang: str = "ru") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=get_text(lang, "sex_male")), KeyboardButton(text=get_text(lang, "sex_female"))]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def build_activity_keyboard(lang: str = "ru") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_text(lang, "activity_sedentary")), KeyboardButton(text=get_text(lang, "activity_light"))],
            [KeyboardButton(text=get_text(lang, "activity_moderate")), KeyboardButton(text=get_text(lang, "activity_active"))],
            [KeyboardButton(text=get_text(lang, "activity_very_active"))],
            [KeyboardButton(text=get_text(lang, "btn_cancel"))],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def build_edit_profile_keyboard(lang: str = "ru") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_text(lang, "field_sex")), KeyboardButton(text=get_text(lang, "field_age"))],
            [KeyboardButton(text=get_text(lang, "field_height")), KeyboardButton(text=get_text(lang, "field_weight"))],
            [KeyboardButton(text=get_text(lang, "field_activity"))],
            [KeyboardButton(text=get_text(lang, "btn_cancel"))],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def build_search_cancel_keyboard(lang: str = "ru") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=get_text(lang, "btn_cancel"))]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def build_add_food_cancel_keyboard(lang: str = "ru") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=get_text(lang, "btn_cancel"))]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def build_main_menu(profile: UserProfile | None, assistant_enabled: bool, lang: str = "ru") -> ReplyKeyboardMarkup:
    if profile is None or not profile.is_complete:
        keyboard = [
            [KeyboardButton(text=get_text(lang, "btn_add_food")), KeyboardButton(text=get_text(lang, "btn_create_profile"))],
            [KeyboardButton(text=get_text(lang, "btn_search")), KeyboardButton(text=get_text(lang, "btn_help"))],
        ]
    elif assistant_enabled:
        keyboard = [
            [KeyboardButton(text=get_text(lang, "btn_add_food")), KeyboardButton(text=get_text(lang, "btn_today"))],
            [KeyboardButton(text=get_text(lang, "btn_profile")), KeyboardButton(text=get_text(lang, "btn_activity"))],
            [KeyboardButton(text=get_text(lang, "btn_search")), KeyboardButton(text=get_text(lang, "btn_assistant_off"))],
        ]
    else:
        keyboard = [
            [KeyboardButton(text=get_text(lang, "btn_add_food")), KeyboardButton(text=get_text(lang, "btn_profile"))],
            [KeyboardButton(text=get_text(lang, "btn_search")), KeyboardButton(text=get_text(lang, "btn_help"))],
            [KeyboardButton(text=get_text(lang, "btn_assistant_on"))],
        ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def build_profile_actions(profile: UserProfile, lang: str = "ru") -> InlineKeyboardMarkup:
    assistant_text = get_text(lang, "btn_assistant_off") if profile.assistant_enabled else get_text(lang, "btn_assistant_on")
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=get_text(lang, "btn_profile_edit"), callback_data=CALLBACK_PROFILE_EDIT)],
            [
                InlineKeyboardButton(text=get_text(lang, "btn_activity_today"), callback_data=CALLBACK_PROFILE_ACTIVITY_TODAY),
                InlineKeyboardButton(text=get_text(lang, "btn_activity_reset"), callback_data=CALLBACK_PROFILE_ACTIVITY_RESET),
            ],
            [
                InlineKeyboardButton(text=assistant_text, callback_data=CALLBACK_PROFILE_ASSISTANT),
                InlineKeyboardButton(text=get_text(lang, "btn_terms"), callback_data=CALLBACK_PROFILE_TERMS),
            ],
            [InlineKeyboardButton(text=get_text(lang, "btn_change_lang"), callback_data="profile:change_lang")],
        ]
    )


def build_activity_actions(lang: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=get_text(lang, "btn_activity_today"), callback_data=CALLBACK_ACTIVITY_CHANGE)],
            [InlineKeyboardButton(text=get_text(lang, "btn_activity_reset"), callback_data=CALLBACK_ACTIVITY_RESET)],
            [InlineKeyboardButton(text=get_text(lang, "btn_back"), callback_data=CALLBACK_ACTIVITY_BACK)],
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


def build_add_food_actions(lang: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=get_text(lang, "btn_add_product"), callback_data=CALLBACK_ADD_FOOD_NEW)],
            [InlineKeyboardButton(text=get_text(lang, "btn_my_products"), callback_data=CALLBACK_ADD_FOOD_LIST)],
        ]
    )


def build_user_product_actions(products, lang: str = "ru") -> InlineKeyboardMarkup:
    rows = [
        [
            InlineKeyboardButton(
                text=get_text(lang, "btn_delete_product", name=product.name),
                callback_data=f"{CALLBACK_ADD_FOOD_DELETE_PREFIX}{product.id}",
            )
        ]
        for product in products
    ]
    rows.append([InlineKeyboardButton(text=get_text(lang, "btn_back"), callback_data=CALLBACK_ADD_FOOD_BACK)])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def build_language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇷🇺 Русский (RU)", callback_data=f"{CALLBACK_CHOOSE_LANG_PREFIX}ru"),
                InlineKeyboardButton(text="🇺🇦 Українська (UK)", callback_data=f"{CALLBACK_CHOOSE_LANG_PREFIX}uk"),
            ],
            [
                InlineKeyboardButton(text="🇬🇧 English (EN)", callback_data=f"{CALLBACK_CHOOSE_LANG_PREFIX}en"),
            ]
        ]
    )


def _parse_activity_button(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    for lang in ["ru", "uk", "en"]:
        if cleaned == get_text(lang, "activity_sedentary"):
            return "sedentary"
        if cleaned == get_text(lang, "activity_light"):
            return "light"
        if cleaned == get_text(lang, "activity_moderate"):
            return "moderate"
        if cleaned == get_text(lang, "activity_active"):
            return "active"
        if cleaned == get_text(lang, "activity_very_active"):
            return "very_active"
    return None


def register_handlers(dispatcher: Dispatcher, database: Database) -> None:
    router = Router()
    nutrition_service = NutritionService(database)
    profile_service = ProfileService(database)

    @router.message(Command("start"))
    async def start_handler(message: Message, state: FSMContext) -> None:
        await state.clear()
        lang = _get_user_lang(message.from_user.id, profile_service, message.from_user)
        profile_service.ensure_user(message.from_user.id, message.from_user.username, default_lang=lang)
        await _show_welcome(message, profile_service, message.from_user.id, message.from_user.username)

    @router.message(Command("lang"))
    async def lang_handler(message: Message) -> None:
        lang = _get_user_lang(message.from_user.id, profile_service, message.from_user)
        await message.answer(
            get_text(lang, "lang_choose"),
            reply_markup=build_language_keyboard(),
        )

    @router.callback_query(F.data.startswith(CALLBACK_CHOOSE_LANG_PREFIX))
    async def choose_lang_callback(callback: CallbackQuery) -> None:
        await callback.answer()
        lang_code = callback.data.removeprefix(CALLBACK_CHOOSE_LANG_PREFIX)
        profile_service.ensure_user(callback.from_user.id, callback.from_user.username)
        profile_service.update_profile_language(callback.from_user.id, lang_code)
        profile = profile_service.get_profile(callback.from_user.id)
        if callback.message is not None:
            await callback.message.delete()
            await callback.message.answer(
                get_text(lang_code, "lang_changed"),
                reply_markup=build_main_menu(profile, bool(profile and profile.assistant_enabled), lang_code)
            )

    @router.callback_query(F.data == "profile:change_lang")
    async def profile_change_lang_callback(callback: CallbackQuery) -> None:
        await callback.answer()
        lang = _get_user_lang(callback.from_user.id, profile_service, callback.from_user)
        if callback.message is not None:
            await callback.message.answer(
                get_text(lang, "lang_choose"),
                reply_markup=build_language_keyboard(),
            )

    @router.message(Command("help"))
    @router.message(Command("calc"))
    async def help_handler(message: Message) -> None:
        await _show_help(message, profile_service, message.from_user.id, message.from_user.username)

    @router.message(Command("terms"))
    async def terms_handler(message: Message) -> None:
        lang = _get_user_lang(message.from_user.id, profile_service, message.from_user)
        await _send_with_main_menu(
            message,
            profile_service,
            message.from_user.id,
            message.from_user.username,
            get_text(lang, "terms"),
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
        lang = _get_user_lang(callback.from_user.id, profile_service, callback.from_user)
        if callback.message is not None:
            await _send_with_main_menu(
                callback.message,
                profile_service,
                callback.from_user.id,
                callback.from_user.username,
                get_text(lang, "terms"),
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
        lang = _get_user_lang(callback.from_user.id, profile_service, callback.from_user)
        product_id_text = str(callback.data).removeprefix(CALLBACK_ADD_FOOD_DELETE_PREFIX)
        product_id = _parse_int(product_id_text)
        deleted = product_id is not None and nutrition_service.delete_user_product(callback.from_user.id, product_id)
        await callback.answer(get_text(lang, "personal_product_deleted") if deleted else get_text(lang, "personal_product_not_found"))
        if callback.message is not None:
            await _show_user_products(
                callback.message,
                nutrition_service,
                profile_service,
                callback.from_user.id,
                callback.from_user.username,
            )

    @router.message(F.text.in_({get_text("ru", "btn_add_food"), get_text("uk", "btn_add_food"), get_text("en", "btn_add_food")}))
    async def add_food_button_handler(message: Message, state: FSMContext) -> None:
        await state.clear()
        await _show_add_food_menu(message, profile_service, message.from_user.id, message.from_user.username)

    @router.message(F.text.in_({get_text("ru", "btn_create_profile"), get_text("uk", "btn_create_profile"), get_text("en", "btn_create_profile")}))
    async def create_profile_button_handler(message: Message, state: FSMContext) -> None:
        await _show_profile(message, state, profile_service, message.from_user.id, message.from_user.username)

    @router.message(F.text.in_({get_text("ru", "btn_profile"), get_text("uk", "btn_profile"), get_text("en", "btn_profile")}))
    async def profile_button_handler(message: Message, state: FSMContext) -> None:
        await _show_profile(message, state, profile_service, message.from_user.id, message.from_user.username)

    @router.message(F.text.in_({get_text("ru", "btn_today"), get_text("uk", "btn_today"), get_text("en", "btn_today")}))
    async def today_button_handler(message: Message) -> None:
        await _show_today(
            message,
            nutrition_service,
            profile_service,
            message.from_user.id,
            message.from_user.username,
        )

    @router.message(F.text.in_({get_text("ru", "btn_activity"), get_text("uk", "btn_activity"), get_text("en", "btn_activity")}))
    async def activity_button_handler(message: Message, state: FSMContext) -> None:
        await state.clear()
        await _show_activity_screen(message, profile_service, message.from_user.id, message.from_user.username)

    @router.message(F.text.in_({get_text("ru", "btn_search"), get_text("uk", "btn_search"), get_text("en", "btn_search")}))
    async def search_button_handler(message: Message, state: FSMContext) -> None:
        await state.clear()
        await _show_search_categories(message, nutrition_service, profile_service, message.from_user.id, message.from_user.username)

    @router.message(F.text.in_({get_text("ru", "btn_help"), get_text("uk", "btn_help"), get_text("en", "btn_help")}))
    async def help_button_handler(message: Message) -> None:
        await _show_help(message, profile_service, message.from_user.id, message.from_user.username)

    @router.message(F.text.in_({get_text("ru", "btn_assistant_on"), get_text("uk", "btn_assistant_on"), get_text("en", "btn_assistant_on")}))
    async def assistant_on_button_handler(message: Message) -> None:
        await _set_assistant_mode(message, profile_service, message.from_user.id, message.from_user.username, enabled=True)

    @router.message(F.text.in_({get_text("ru", "btn_assistant_off"), get_text("uk", "btn_assistant_off"), get_text("en", "btn_assistant_off")}))
    async def assistant_off_button_handler(message: Message) -> None:
        await _set_assistant_mode(message, profile_service, message.from_user.id, message.from_user.username, enabled=False)

    @router.message(ProfileEditStates.choosing_field)
    async def edit_profile_choose_field_handler(message: Message, state: FSMContext) -> None:
        lang = _get_user_lang(message.from_user.id, profile_service, message.from_user)
        text = (message.text or "").strip()
        
        if text in {get_text("ru", "btn_cancel"), get_text("uk", "btn_cancel"), get_text("en", "btn_cancel")}:
            await state.clear()
            profile = profile_service.get_profile(message.from_user.id)
            targets = profile_service.get_daily_targets(message.from_user.id) if profile and profile.is_complete else None
            body = get_text(lang, "changes_not_made")
            if profile is not None and targets is not None:
                body = f"{body}\n\n{_format_profile_card(profile, targets, lang)}"
            await message.answer(
                body,
                reply_markup=build_main_menu(profile, bool(profile and profile.assistant_enabled), lang),
            )
            if profile is not None and profile.is_complete:
                await message.answer(get_text(lang, "profile_quick_actions"), reply_markup=build_profile_actions(profile, lang))
            return

        # Check field choice across all languages to route correctly
        field_choice = None
        for l in ["ru", "uk", "en"]:
            if text == get_text(l, "field_sex"):
                field_choice = "sex"
            elif text == get_text(l, "field_age"):
                field_choice = "age"
            elif text == get_text(l, "field_height"):
                field_choice = "height"
            elif text == get_text(l, "field_weight"):
                field_choice = "weight"
            elif text == get_text(l, "field_activity"):
                field_choice = "activity"

        if field_choice == "sex":
            await state.update_data(edit_field="sex")
            await state.set_state(ProfileEditStates.waiting_for_sex)
            await message.answer(get_text(lang, "prompt_sex_new"), reply_markup=build_sex_keyboard(lang))
        elif field_choice == "age":
            await state.update_data(edit_field="age")
            await state.set_state(ProfileEditStates.waiting_for_age)
            await message.answer(get_text(lang, "prompt_age_new"), reply_markup=ReplyKeyboardRemove())
        elif field_choice == "height":
            await state.update_data(edit_field="height_cm")
            await state.set_state(ProfileEditStates.waiting_for_height)
            await message.answer(get_text(lang, "prompt_height_new"), reply_markup=ReplyKeyboardRemove())
        elif field_choice == "weight":
            await state.update_data(edit_field="weight_kg")
            await state.set_state(ProfileEditStates.waiting_for_weight)
            await message.answer(get_text(lang, "prompt_weight_new"), reply_markup=ReplyKeyboardRemove())
        elif field_choice == "activity":
            await state.update_data(edit_field="activity_level")
            await state.set_state(ProfileEditStates.waiting_for_activity_level)
            await message.answer(get_text(lang, "prompt_activity_new"), reply_markup=build_activity_keyboard(lang))
        else:
            await message.answer(get_text(lang, "choose_field_to_edit_invalid"))

    @router.message(SearchStates.waiting_for_query)
    async def search_query_handler(message: Message, state: FSMContext) -> None:
        lang = _get_user_lang(message.from_user.id, profile_service, message.from_user)
        text = (message.text or "").strip()
        if text in {get_text("ru", "btn_cancel"), get_text("uk", "btn_cancel"), get_text("en", "btn_cancel")}:
            await state.clear()
            await _send_with_main_menu(
                message,
                profile_service,
                message.from_user.id,
                message.from_user.username,
                get_text(lang, "search_cancelled"),
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
        lang = _get_user_lang(message.from_user.id, profile_service, message.from_user)
        text = (message.text or "").strip()
        if text in {get_text("ru", "btn_cancel"), get_text("uk", "btn_cancel"), get_text("en", "btn_cancel")}:
            await state.clear()
            await _send_with_main_menu(
                message,
                profile_service,
                message.from_user.id,
                message.from_user.username,
                get_text(lang, "add_food_cancelled"),
            )
            return

        parsed = _parse_user_product_input(text)
        if parsed is None:
            await message.answer(
                get_text(lang, "personal_product_parse_error"),
                reply_markup=build_add_food_cancel_keyboard(lang),
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
            input_lang=lang,
        )
        await state.clear()
        
        # Display localized name back to user
        name_display = name_ru
        if lang == "en":
            from app.services.translator import translate_food_name
            name_display = translate_food_name(name_ru, "en")
        elif lang == "uk":
            from app.services.translator import translate_food_name
            name_display = translate_food_name(name_ru, "uk")

        await _send_with_main_menu(
            message,
            profile_service,
            message.from_user.id,
            message.from_user.username,
            get_text(
                lang,
                "personal_product_saved",
                name=name_display,
                calories=round(calories),
                protein=_format_number(protein),
                fat=_format_number(fat),
                carbs=_format_number(carbs),
            )
        )

    @router.message(ProfileCreateStates.waiting_for_sex)
    async def profile_sex_handler(message: Message, state: FSMContext) -> None:
        lang = _get_user_lang(message.from_user.id, profile_service, message.from_user)
        value = (message.text or "").strip().lower()
        if value not in {"male", "female"}:
            await message.answer(get_text(lang, "prompt_sex"), reply_markup=build_sex_keyboard(lang))
            return
        await state.update_data(sex=value)
        await state.set_state(ProfileCreateStates.waiting_for_age)
        await message.answer(get_text(lang, "prompt_age"), reply_markup=ReplyKeyboardRemove())

    @router.message(ProfileCreateStates.waiting_for_age)
    async def profile_age_handler(message: Message, state: FSMContext) -> None:
        lang = _get_user_lang(message.from_user.id, profile_service, message.from_user)
        age = _parse_int(message.text)
        if age is None or age < 10 or age > 120:
            await message.answer(get_text(lang, "error_age_range"))
            return
        await state.update_data(age=age)
        await state.set_state(ProfileCreateStates.waiting_for_height)
        await message.answer(get_text(lang, "prompt_height"))

    @router.message(ProfileCreateStates.waiting_for_height)
    async def profile_height_handler(message: Message, state: FSMContext) -> None:
        lang = _get_user_lang(message.from_user.id, profile_service, message.from_user)
        height_cm = _parse_float(message.text)
        if height_cm is None or height_cm < 80 or height_cm > 250:
            await message.answer(get_text(lang, "error_height_range"))
            return
        await state.update_data(height_cm=height_cm)
        await state.set_state(ProfileCreateStates.waiting_for_weight)
        await message.answer(get_text(lang, "prompt_weight"))

    @router.message(ProfileCreateStates.waiting_for_weight)
    async def profile_weight_handler(message: Message, state: FSMContext) -> None:
        lang = _get_user_lang(message.from_user.id, profile_service, message.from_user)
        weight_kg = _parse_float(message.text)
        if weight_kg is None or weight_kg < 20 or weight_kg > 300:
            await message.answer(get_text(lang, "error_weight_range"))
            return
        await state.update_data(weight_kg=weight_kg)
        await state.set_state(ProfileCreateStates.waiting_for_activity_level)
        await message.answer(get_text(lang, "prompt_activity"), reply_markup=build_activity_keyboard(lang))

    @router.message(ProfileCreateStates.waiting_for_activity_level)
    async def profile_activity_handler(message: Message, state: FSMContext) -> None:
        lang = _get_user_lang(message.from_user.id, profile_service, message.from_user)
        activity_level = _parse_activity_button(message.text)
        if activity_level is None:
            await message.answer(get_text(lang, "prompt_activity"), reply_markup=build_activity_keyboard(lang))
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
            f"{get_text(lang, 'profile_saved')}\n\n{_format_profile_card(profile, targets, lang)}",
            reply_markup=build_main_menu(profile, bool(profile and profile.assistant_enabled), lang),
        )
        if profile is not None:
            await message.answer(get_text(lang, "profile_quick_actions"), reply_markup=build_profile_actions(profile, lang))

    @router.message(ProfileEditStates.waiting_for_sex)
    async def edit_profile_sex_handler(message: Message, state: FSMContext) -> None:
        lang = _get_user_lang(message.from_user.id, profile_service, message.from_user)
        value = (message.text or "").strip().lower()
        if value not in {"male", "female"}:
            await message.answer(get_text(lang, "prompt_sex"), reply_markup=build_sex_keyboard(lang))
            return
        await _save_profile_edit(message, state, profile_service, "sex", value)

    @router.message(ProfileEditStates.waiting_for_age)
    async def edit_profile_age_handler(message: Message, state: FSMContext) -> None:
        lang = _get_user_lang(message.from_user.id, profile_service, message.from_user)
        age = _parse_int(message.text)
        if age is None or age < 10 or age > 120:
            await message.answer(get_text(lang, "error_age_range"))
            return
        await _save_profile_edit(message, state, profile_service, "age", age)

    @router.message(ProfileEditStates.waiting_for_height)
    async def edit_profile_height_handler(message: Message, state: FSMContext) -> None:
        lang = _get_user_lang(message.from_user.id, profile_service, message.from_user)
        height_cm = _parse_float(message.text)
        if height_cm is None or height_cm < 80 or height_cm > 250:
            await message.answer(get_text(lang, "error_height_range"))
            return
        await _save_profile_edit(message, state, profile_service, "height_cm", height_cm)

    @router.message(ProfileEditStates.waiting_for_weight)
    async def edit_profile_weight_handler(message: Message, state: FSMContext) -> None:
        lang = _get_user_lang(message.from_user.id, profile_service, message.from_user)
        weight_kg = _parse_float(message.text)
        if weight_kg is None or weight_kg < 20 or weight_kg > 300:
            await message.answer(get_text(lang, "error_weight_range"))
            return
        await _save_profile_edit(message, state, profile_service, "weight_kg", weight_kg)

    @router.message(ProfileEditStates.waiting_for_activity_level)
    async def edit_profile_activity_handler(message: Message, state: FSMContext) -> None:
        lang = _get_user_lang(message.from_user.id, profile_service, message.from_user)
        text_val = (message.text or "").strip()
        if text_val in {get_text("ru", "btn_cancel"), get_text("uk", "btn_cancel"), get_text("en", "btn_cancel")}:
            await state.set_state(ProfileEditStates.choosing_field)
            await message.answer(get_text(lang, "choose_field_to_edit"), reply_markup=build_edit_profile_keyboard(lang))
            return

        activity_level = _parse_activity_button(message.text)
        if activity_level is None:
            await message.answer(get_text(lang, "prompt_activity"), reply_markup=build_activity_keyboard(lang))
            return
        await _save_profile_edit(message, state, profile_service, "activity_level", activity_level)

    @router.message(ActivityTodayStates.waiting_for_activity_level)
    async def activity_today_value_handler(message: Message, state: FSMContext) -> None:
        lang = _get_user_lang(message.from_user.id, profile_service, message.from_user)
        text_val = (message.text or "").strip()
        if text_val in {get_text("ru", "btn_cancel"), get_text("uk", "btn_cancel"), get_text("en", "btn_cancel")}:
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
            await message.answer(get_text(lang, "prompt_activity"), reply_markup=build_activity_keyboard(lang))
            return

        profile_service.set_activity_override_for_today(message.from_user.id, activity_level)
        await state.clear()
        profile = profile_service.get_profile(message.from_user.id)
        targets = profile_service.get_daily_targets(message.from_user.id)
        
        # Format targets block
        macros_text = get_text(
            lang,
            "macro_norms_values",
            protein=_format_number(targets.protein_g),
            fat=_format_number(targets.fat_g),
            carbs=_format_number(targets.carbs_g),
        )
        targets_block = (
            get_text(lang, "bmr_label", bmr=round(targets.bmr)) + "\n" +
            get_text(lang, "tdee_label", tdee=round(targets.tdee)) + "\n" +
            get_text(lang, "activity_for_calc", activity=targets.effective_activity_label(lang)) + "\n" +
            targets.activity_source_label(lang) + "\n" +
            get_text(lang, "macro_norms_header") + "\n" +
            macros_text
        )

        await message.answer(
            get_text(lang, "activity_saved_today", targets=targets_block),
            reply_markup=build_main_menu(profile, bool(profile and profile.assistant_enabled), lang),
        )

    @router.message(F.text)
    async def food_message_handler(message: Message, state: FSMContext) -> None:
        await state.clear()
        lang = _get_user_lang(message.from_user.id, profile_service, message.from_user)
        profile_service.ensure_user(message.from_user.id, message.from_user.username, default_lang=lang)
        result = nutrition_service.process_message(message.from_user.id, message.text or "")

        if result.assistant_enabled:
            nutrition_service.store_entries(message.from_user.id, result.recognized_items)
            today = nutrition_service.get_today_summary(message.from_user.id)
            targets = profile_service.get_daily_targets(message.from_user.id)
            reply = nutrition_service.format_assistant_reply(result, today, targets, lang)
        else:
            reply = nutrition_service.format_calc_reply(result, lang)

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
    lang = _get_user_lang(telegram_id, profile_service, output_message.from_user)
    await _send_with_main_menu(
        output_message,
        profile_service,
        telegram_id,
        username,
        get_text(lang, "welcome"),
    )


async def _show_help(
    output_message: Message,
    profile_service: ProfileService,
    telegram_id: int,
    username: str | None,
) -> None:
    lang = _get_user_lang(telegram_id, profile_service, output_message.from_user)
    await _send_with_main_menu(
        output_message,
        profile_service,
        telegram_id,
        username,
        get_text(
            lang,
            "help",
            btn_add_food=get_text(lang, "btn_add_food"),
            btn_profile=get_text(lang, "btn_profile"),
            btn_create_profile=get_text(lang, "btn_create_profile"),
            btn_today=get_text(lang, "btn_today"),
            btn_activity=get_text(lang, "btn_activity"),
            btn_search=get_text(lang, "btn_search"),
        ),
    )


async def _show_profile(
    output_message: Message,
    state: FSMContext,
    profile_service: ProfileService,
    telegram_id: int,
    username: str | None,
) -> None:
    lang = _get_user_lang(telegram_id, profile_service, output_message.from_user)
    profile_service.ensure_user(telegram_id, username, default_lang=lang)
    profile = profile_service.get_profile(telegram_id)
    if profile is not None and profile.is_complete:
        await state.clear()
        targets = profile_service.get_daily_targets(telegram_id)
        await output_message.answer(
            _format_profile_card(profile, targets, lang),
            reply_markup=build_main_menu(profile, bool(profile.assistant_enabled), lang),
        )
        await output_message.answer(get_text(lang, "profile_quick_actions"), reply_markup=build_profile_actions(profile, lang))
        return

    await _start_profile_onboarding(output_message, state, profile, lang)


async def _show_edit_profile(
    output_message: Message,
    state: FSMContext,
    profile_service: ProfileService,
    telegram_id: int,
    username: str | None,
) -> None:
    lang = _get_user_lang(telegram_id, profile_service, output_message.from_user)
    profile_service.ensure_user(telegram_id, username, default_lang=lang)
    profile = profile_service.get_profile(telegram_id)
    if profile is None or not profile.is_complete:
        await state.clear()
        await _send_with_main_menu(
            output_message,
            profile_service,
            telegram_id,
            username,
            get_text(lang, "profile_incomplete"),
        )
        return

    targets = profile_service.get_daily_targets(telegram_id)
    await state.set_state(ProfileEditStates.choosing_field)
    await output_message.answer(
        f"{_format_profile_card(profile, targets, lang)}\n\n{get_text(lang, 'choose_field_to_edit')}",
        reply_markup=build_edit_profile_keyboard(lang),
    )


async def _show_activity_screen(
    output_message: Message,
    profile_service: ProfileService,
    telegram_id: int,
    username: str | None,
) -> None:
    lang = _get_user_lang(telegram_id, profile_service, output_message.from_user)
    profile_service.ensure_user(telegram_id, username, default_lang=lang)
    profile = profile_service.get_profile(telegram_id)
    if profile is None or not profile.is_complete:
        await _send_with_main_menu(
            output_message,
            profile_service,
            telegram_id,
            username,
            get_text(lang, "profile_incomplete_activity"),
        )
        return

    targets = profile_service.get_daily_targets(telegram_id)
    text = (
        get_text(lang, "activity_header") + "\n" +
        get_text(lang, "activity_default", activity=targets.default_activity_label(lang)) + "\n" +
        get_text(lang, "activity_for_calc", activity=targets.effective_activity_label(lang)) + "\n" +
        targets.activity_source_label(lang)
    )
    await output_message.answer(
        text,
        reply_markup=build_main_menu(profile, bool(profile.assistant_enabled), lang),
    )
    await output_message.answer(get_text(lang, "actions_header"), reply_markup=build_activity_actions(lang))


async def _prompt_activity_today(
    output_message: Message,
    state: FSMContext,
    profile_service: ProfileService,
    telegram_id: int,
    username: str | None,
) -> None:
    lang = _get_user_lang(telegram_id, profile_service, output_message.from_user)
    profile_service.ensure_user(telegram_id, username, default_lang=lang)
    profile = profile_service.get_profile(telegram_id)
    if profile is None or not profile.is_complete:
        await state.clear()
        await _send_with_main_menu(
            output_message,
            profile_service,
            telegram_id,
            username,
            get_text(lang, "profile_incomplete_activity_today"),
        )
        return

    targets = profile_service.get_daily_targets(telegram_id)
    await state.set_state(ActivityTodayStates.waiting_for_activity_level)
    await output_message.answer(
        get_text(lang, "prompt_activity_today") + "\n\n" +
        get_text(lang, "activity_for_calc", activity=targets.effective_activity_label(lang)) + "\n" +
        targets.activity_source_label(lang),
        reply_markup=build_activity_keyboard(lang),
    )


async def _reset_activity_today(
    output_message: Message,
    profile_service: ProfileService,
    telegram_id: int,
    username: str | None,
) -> None:
    lang = _get_user_lang(telegram_id, profile_service, output_message.from_user)
    profile_service.ensure_user(telegram_id, username, default_lang=lang)
    profile = profile_service.get_profile(telegram_id)
    if profile is None or profile.activity_level is None:
        await _send_with_main_menu(
            output_message,
            profile_service,
            telegram_id,
            username,
            get_text(lang, "profile_incomplete_activity_reset"),
        )
        return

    profile_service.clear_activity_override_for_today(telegram_id)
    targets = profile_service.get_daily_targets(telegram_id)
    
    # Format targets block
    macros_text = get_text(
        lang,
        "macro_norms_values",
        protein=_format_number(targets.protein_g),
        fat=_format_number(targets.fat_g),
        carbs=_format_number(targets.carbs_g),
    )
    targets_block = (
        get_text(lang, "bmr_label", bmr=round(targets.bmr)) + "\n" +
        get_text(lang, "tdee_label", tdee=round(targets.tdee)) + "\n" +
        get_text(lang, "activity_for_calc", activity=targets.effective_activity_label(lang)) + "\n" +
        targets.activity_source_label(lang) + "\n" +
        get_text(lang, "macro_norms_header") + "\n" +
        macros_text
    )

    await output_message.answer(
        get_text(lang, "activity_reset_today", targets=targets_block),
        reply_markup=build_main_menu(profile, bool(profile.assistant_enabled), lang),
    )


async def _show_today(
    output_message: Message,
    nutrition_service: NutritionService,
    profile_service: ProfileService,
    telegram_id: int,
    username: str | None,
) -> None:
    lang = _get_user_lang(telegram_id, profile_service, output_message.from_user)
    profile_service.ensure_user(telegram_id, username, default_lang=lang)
    if not profile_service.has_complete_profile(telegram_id):
        await _send_with_main_menu(
            output_message,
            profile_service,
            telegram_id,
            username,
            get_text(lang, "profile_incomplete_today"),
        )
        return

    today = nutrition_service.get_today_summary(telegram_id)
    targets = profile_service.get_daily_targets(telegram_id)
    profile = profile_service.get_profile(telegram_id)
    await output_message.answer(
        nutrition_service.format_today_with_targets(today, targets, lang),
        reply_markup=build_main_menu(profile, bool(profile and profile.assistant_enabled), lang),
    )


async def _prompt_search(
    output_message: Message,
    state: FSMContext,
    profile_service: ProfileService,
    telegram_id: int,
    username: str | None,
) -> None:
    lang = _get_user_lang(telegram_id, profile_service, output_message.from_user)
    await state.set_state(SearchStates.waiting_for_query)
    await output_message.answer(
        get_text(lang, "prompt_search_query"),
        reply_markup=build_search_cancel_keyboard(lang),
    )


async def _show_search_categories(
    output_message: Message,
    nutrition_service: NutritionService,
    profile_service: ProfileService,
    telegram_id: int,
    username: str | None,
) -> None:
    lang = _get_user_lang(telegram_id, profile_service, output_message.from_user)
    profile_service.ensure_user(telegram_id, username, default_lang=lang)
    categories = nutrition_service.list_categories(lang=lang)
    if not categories:
        await _send_with_main_menu(
            output_message,
            profile_service,
            telegram_id,
            username,
            get_text(lang, "categories_not_available"),
        )
        return

    profile = profile_service.get_profile(telegram_id)
    await output_message.answer(
        get_text(lang, "choose_category_or_search"),
        reply_markup=build_main_menu(profile, bool(profile and profile.assistant_enabled), lang),
    )
    await output_message.answer(get_text(lang, "categories_header"), reply_markup=build_search_categories(categories))


async def _show_category_products(
    output_message: Message,
    nutrition_service: NutritionService,
    profile_service: ProfileService,
    telegram_id: int,
    username: str | None,
    category_slug: str,
) -> None:
    lang = _get_user_lang(telegram_id, profile_service, output_message.from_user)
    products = nutrition_service.list_products_by_category(category_slug, lang=lang)
    if not products:
        await _send_with_main_menu(
            output_message,
            profile_service,
            telegram_id,
            username,
            get_text(lang, "category_empty"),
        )
        return

    lines = [get_text(lang, "category_products_header")]
    lines.extend(_format_product_summary(product) for product in products)
    await _send_with_main_menu(
        output_message,
        profile_service,
        telegram_id,
        username,
        "\n".join(lines),
    )
    await output_message.answer(
        get_text(lang, "category_how_to_send"),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=get_text(lang, "btn_back"), callback_data=CALLBACK_SEARCH_BACK)]]
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
    lang = _get_user_lang(telegram_id, profile_service, output_message.from_user)
    matches = nutrition_service.search_products(query, telegram_id)
    if not matches:
        await _send_with_main_menu(
            output_message,
            profile_service,
            telegram_id,
            username,
            get_text(lang, "search_not_found", query=query),
        )
        return

    lines = [get_text(lang, "search_found")]
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
    lang = _get_user_lang(telegram_id, profile_service, output_message.from_user)
    profile_service.ensure_user(telegram_id, username, default_lang=lang)
    profile = profile_service.get_profile(telegram_id)
    await output_message.answer(
        get_text(lang, "add_food_menu_header"),
        reply_markup=build_main_menu(profile, bool(profile and profile.assistant_enabled), lang),
    )
    await output_message.answer(get_text(lang, "prompt_choose_action"), reply_markup=build_add_food_actions(lang))


async def _prompt_add_food_product(
    output_message: Message,
    state: FSMContext,
    profile_service: ProfileService,
    telegram_id: int,
    username: str | None,
) -> None:
    lang = _get_user_lang(telegram_id, profile_service, output_message.from_user)
    profile_service.ensure_user(telegram_id, username, default_lang=lang)
    await state.set_state(AddFoodStates.waiting_for_product)
    await output_message.answer(
        get_text(lang, "prompt_add_food_product"),
        reply_markup=build_add_food_cancel_keyboard(lang),
    )


async def _show_user_products(
    output_message: Message,
    nutrition_service: NutritionService,
    profile_service: ProfileService,
    telegram_id: int,
    username: str | None,
) -> None:
    lang = _get_user_lang(telegram_id, profile_service, output_message.from_user)
    profile_service.ensure_user(telegram_id, username, default_lang=lang)
    products = nutrition_service.list_user_products(telegram_id, lang=lang)
    if not products:
        await _send_with_main_menu(
            output_message,
            profile_service,
            telegram_id,
            username,
            get_text(lang, "personal_products_empty"),
        )
        await output_message.answer(get_text(lang, "prompt_choose_action"), reply_markup=build_add_food_actions(lang))
        return

    lines = [get_text(lang, "personal_products_header")]
    lines.extend(_format_product_summary(product) for product in products)
    await _send_with_main_menu(
        output_message,
        profile_service,
        telegram_id,
        username,
        "\n".join(lines),
    )
    await output_message.answer(get_text(lang, "actions_header"), reply_markup=build_user_product_actions(products, lang))


async def _set_assistant_mode(
    output_message: Message,
    profile_service: ProfileService,
    telegram_id: int,
    username: str | None,
    enabled: bool,
) -> None:
    lang = _get_user_lang(telegram_id, profile_service, output_message.from_user)
    profile_service.ensure_user(telegram_id, username, default_lang=lang)
    if enabled and not profile_service.has_complete_profile(telegram_id):
        await _send_with_main_menu(
            output_message,
            profile_service,
            telegram_id,
            username,
            get_text(lang, "profile_incomplete_assistant"),
        )
        return

    profile_service.set_assistant_mode(telegram_id, enabled)
    profile = profile_service.get_profile(telegram_id)
    text = (
        get_text(lang, "assistant_enabled_msg")
        if enabled
        else get_text(lang, "assistant_disabled_msg")
    )
    await output_message.answer(text, reply_markup=build_main_menu(profile, bool(profile and profile.assistant_enabled), lang))


async def _send_with_main_menu(
    output_message: Message,
    profile_service: ProfileService,
    telegram_id: int,
    username: str | None,
    text: str,
) -> None:
    lang = _get_user_lang(telegram_id, profile_service, output_message.from_user)
    profile_service.ensure_user(telegram_id, username, default_lang=lang)
    profile = profile_service.get_profile(telegram_id)
    await output_message.answer(text, reply_markup=build_main_menu(profile, bool(profile and profile.assistant_enabled), lang))


async def _start_profile_onboarding(
    message: Message,
    state: FSMContext,
    profile: UserProfile | None,
    lang: str = "ru",
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
            get_text(lang, "prompt_sex"),
            reply_markup=build_sex_keyboard(lang),
        )
        return
    if profile.age is None:
        await state.set_state(ProfileCreateStates.waiting_for_age)
        await message.answer(get_text(lang, "prompt_age"), reply_markup=ReplyKeyboardRemove())
        return
    if profile.height_cm is None:
        await state.set_state(ProfileCreateStates.waiting_for_height)
        await message.answer(get_text(lang, "prompt_height"), reply_markup=ReplyKeyboardRemove())
        return
    if profile.weight_kg is None:
        await state.set_state(ProfileCreateStates.waiting_for_weight)
        await message.answer(get_text(lang, "prompt_weight"), reply_markup=ReplyKeyboardRemove())
        return

    await state.set_state(ProfileCreateStates.waiting_for_activity_level)
    await message.answer(get_text(lang, "prompt_activity"), reply_markup=build_activity_keyboard(lang))


async def _save_profile_edit(
    message: Message,
    state: FSMContext,
    profile_service: ProfileService,
    field_name: str,
    value: str | int | float,
) -> None:
    lang = _get_user_lang(message.from_user.id, profile_service, message.from_user)
    profile_service.update_profile_field(message.from_user.id, message.from_user.username, field_name, value)
    await state.clear()
    profile = profile_service.get_profile(message.from_user.id)
    targets = profile_service.get_daily_targets(message.from_user.id)
    await message.answer(
        f"{get_text(lang, 'profile_updated')}\n\n{_format_profile_card(profile, targets, lang)}",
        reply_markup=build_main_menu(profile, bool(profile and profile.assistant_enabled), lang),
    )
    if profile is not None:
        await message.answer(get_text(lang, "profile_quick_actions"), reply_markup=build_profile_actions(profile, lang))


def _format_profile_card(profile: UserProfile | None, targets: DailyNutritionTargets, lang: str = "ru") -> str:
    if profile is None or not profile.is_complete:
        return get_text(lang, "profile_incomplete")

    sex_label = get_text(lang, "sex_male_label") if profile.sex == "male" else get_text(lang, "sex_female_label")
    assistant_label = get_text(lang, "profile_status_enabled") if profile.assistant_enabled else get_text(lang, "profile_status_disabled")
    
    # Format targets block
    macros_text = get_text(
        lang,
        "macro_norms_values",
        protein=_format_number(targets.protein_g),
        fat=_format_number(targets.fat_g),
        carbs=_format_number(targets.carbs_g),
    )
    targets_block = (
        get_text(lang, "bmr_label", bmr=round(targets.bmr)) + "\n" +
        get_text(lang, "tdee_label", tdee=round(targets.tdee)) + "\n" +
        get_text(lang, "activity_for_calc", activity=targets.effective_activity_label(lang)) + "\n" +
        targets.activity_source_label(lang) + "\n" +
        get_text(lang, "macro_norms_header") + "\n" +
        macros_text + "\n" +
        get_text(lang, "bmr_tdee_hint")
    )

    return (
        get_text(lang, "profile_card_header") + "\n" +
        get_text(lang, "profile_sex_label", sex=sex_label) + "\n" +
        get_text(lang, "profile_age_label", age=profile.age) + "\n" +
        get_text(lang, "profile_height_label", height=_format_number(profile.height_cm)) + "\n" +
        get_text(lang, "profile_weight_label", weight=_format_number(profile.weight_kg)) + "\n" +
        get_text(lang, "profile_activity_label", activity=targets.default_activity_label(lang)) + "\n" +
        get_text(lang, "profile_assistant_label", status=assistant_label) + "\n\n" +
        targets_block
    )


def _format_number(value: float | int | None) -> str:
    if value is None:
        return "-"
    text = f"{float(value):.1f}"
    if text.endswith(".0"):
        return text[:-2]
    return text


def _format_product_summary(product) -> str:
    return (
        f"- {product.name}: {round(product.calories_per_100g)} kcal, "
        f"P {_format_number(product.protein_per_100g)} / "
        f"F {_format_number(product.fat_per_100g)} / "
        f"C {_format_number(product.carbs_per_100g)}"
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
