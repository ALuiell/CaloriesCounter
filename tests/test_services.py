import sqlite3
from pathlib import Path

from app.db.database import Database
from app.db.seed import seed_products_if_empty
from app.handlers.bot import (
    BUTTON_ACTIVITY,
    BUTTON_ADD_FOOD,
    BUTTON_ASSISTANT_OFF,
    BUTTON_ASSISTANT_ON,
    BUTTON_CREATE_PROFILE,
    BUTTON_HELP,
    BUTTON_PROFILE,
    BUTTON_SEARCH,
    BUTTON_TODAY,
    CANCEL_EDIT_PROFILE_TEXT,
    CANCEL_SEARCH_TEXT,
    build_main_menu,
)
from app.services.nutrition import NutritionService
from app.services.profile import (
    ProfileService,
    calculate_bmr,
    calculate_daily_macro_norms,
    calculate_tdee,
)


def build_db(tmp_path: Path) -> Database:
    database = Database(tmp_path / "test.sqlite3", "Europe/Kiev")
    database.initialize()
    seed_products_if_empty(database, Path("data/seeds/starter_products_usda_sr_legacy.json"))
    return database


def create_complete_profile(profile_service: ProfileService, telegram_id: int = 1) -> None:
    profile_service.update_profile(
        telegram_id=telegram_id,
        username="tester",
        sex="male",
        age=30,
        height_cm=180,
        weight_kg=80,
        activity_level="moderate",
    )


def _keyboard_texts(markup) -> list[str]:
    return [button.text for row in markup.keyboard for button in row]


def test_main_menu_without_profile():
    texts = _keyboard_texts(build_main_menu(None, False))

    assert texts == [BUTTON_ADD_FOOD, BUTTON_CREATE_PROFILE, BUTTON_SEARCH, BUTTON_HELP]


def test_main_menu_with_profile_and_assistant_off(tmp_path: Path):
    database = build_db(tmp_path)
    profile_service = ProfileService(database)
    create_complete_profile(profile_service)
    profile = profile_service.get_profile(1)

    texts = _keyboard_texts(build_main_menu(profile, False))

    assert BUTTON_ADD_FOOD in texts
    assert BUTTON_PROFILE in texts
    assert BUTTON_SEARCH in texts
    assert BUTTON_HELP in texts
    assert BUTTON_ASSISTANT_ON in texts


def test_main_menu_with_profile_and_assistant_on(tmp_path: Path):
    database = build_db(tmp_path)
    profile_service = ProfileService(database)
    create_complete_profile(profile_service)
    profile_service.set_assistant_mode(1, True)
    profile = profile_service.get_profile(1)

    texts = _keyboard_texts(build_main_menu(profile, True))

    assert BUTTON_ADD_FOOD in texts
    assert BUTTON_TODAY in texts
    assert BUTTON_PROFILE in texts
    assert BUTTON_ACTIVITY in texts
    assert BUTTON_SEARCH in texts
    assert BUTTON_ASSISTANT_OFF in texts


def test_alias_lookup_and_calculation(tmp_path: Path):
    database = build_db(tmp_path)
    profile_service = ProfileService(database)
    profile_service.ensure_user(1, "tester")
    service = NutritionService(database)

    result = service.process_message(1, "рис 100, помидор 80")
    assert len(result.recognized_items) == 2
    assert not result.unrecognized_items
    assert round(result.total_calories) > 0


def test_common_russian_aliases_lookup(tmp_path: Path):
    database = build_db(tmp_path)
    profile_service = ProfileService(database)
    profile_service.ensure_user(1, "tester")
    service = NutritionService(database)

    result = service.process_message(1, "курица 100, куриное филе 100, белок 100")

    assert len(result.recognized_items) == 3
    assert not result.unrecognized_items
    assert result.recognized_items[0].display_name == "куриная грудка запеченная"
    assert result.recognized_items[1].display_name == "куриная грудка запеченная"
    assert result.recognized_items[2].display_name == "яичный белок сырой"


def test_seed_expansion_products_lookup(tmp_path: Path):
    database = build_db(tmp_path)
    profile_service = ProfileService(database)
    profile_service.ensure_user(1, "tester")
    service = NutritionService(database)

    result = service.process_message(
        1,
        (
            "\u043e\u043c\u043b\u0435\u0442 100, "
            "\u043a\u0435\u0442\u0447\u0443\u043f 20, "
            "\u043a\u0440\u0443\u0430\u0441\u0441\u0430\u043d 100, "
            "\u0433\u043e\u0440\u043e\u0448\u0435\u043a \u0438\u0437 \u0431\u0430\u043d\u043a\u0438 50"
        ),
    )

    assert not result.unrecognized_items
    assert [item.display_name for item in result.recognized_items] == [
        "\u043e\u043c\u043b\u0435\u0442",
        "\u043a\u0435\u0442\u0447\u0443\u043f",
        "\u043a\u0440\u0443\u0430\u0441\u0441\u0430\u043d \u0441\u043b\u0438\u0432\u043e\u0447\u043d\u044b\u0439",
        "\u0433\u043e\u0440\u043e\u0448\u0435\u043a \u0437\u0435\u043b\u0435\u043d\u044b\u0439 \u043a\u043e\u043d\u0441\u0435\u0440\u0432\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0439",
    ]


def test_external_source_products_lookup(tmp_path: Path):
    database = build_db(tmp_path)
    profile_service = ProfileService(database)
    profile_service.ensure_user(1, "tester")
    service = NutritionService(database)

    result = service.process_message(
        1,
        (
            "\u0430\u0439\u0440\u0430\u043d 200, "
            "\u043c\u0430\u0439\u043e\u043d\u0435\u0437 15, "
            "\u0441\u044b\u0440\u043d\u0438\u043a\u0438 150, "
            "\u0445\u0435\u043a 100"
        ),
    )

    assert not result.unrecognized_items
    assert [item.display_name for item in result.recognized_items] == [
        "\u0430\u0439\u0440\u0430\u043d",
        "\u043c\u0430\u0439\u043e\u043d\u0435\u0437",
        "\u0441\u044b\u0440\u043d\u0438\u043a\u0438",
        "\u0445\u0435\u043a \u0441\u044b\u0440\u043e\u0439",
    ]


def test_seed_sync_adds_missing_aliases_to_existing_database(tmp_path: Path):
    database = build_db(tmp_path)
    with database.connection() as conn:
        conn.execute("DELETE FROM product_aliases WHERE normalized_alias = ?", ("курица",))

    seed_products_if_empty(database, Path("data/seeds/starter_products_usda_sr_legacy.json"))
    profile_service = ProfileService(database)
    profile_service.ensure_user(1, "tester")
    service = NutritionService(database)
    result = service.process_message(1, "курица 100")

    assert len(result.recognized_items) == 1
    assert result.recognized_items[0].display_name == "куриная грудка запеченная"


def test_partial_success(tmp_path: Path):
    database = build_db(tmp_path)
    profile_service = ProfileService(database)
    profile_service.ensure_user(1, "tester")
    service = NutritionService(database)

    result = service.process_message(1, "рис 100, непонятная штука")
    assert len(result.recognized_items) == 1
    assert result.unrecognized_items == ["непонятная штука"]


def test_old_profile_without_activity_is_incomplete(tmp_path: Path):
    database = build_db(tmp_path)
    profile_service = ProfileService(database)
    profile_service.ensure_user(1, "tester")
    profile_service.update_profile_field(1, "tester", "sex", "male")
    profile_service.update_profile_field(1, "tester", "age", 30)
    profile_service.update_profile_field(1, "tester", "height_cm", 180)
    profile_service.update_profile_field(1, "tester", "weight_kg", 80)

    profile = profile_service.get_profile(1)

    assert profile is not None
    assert profile.activity_level is None
    assert not profile.is_complete
    assert not profile_service.has_complete_profile(1)


def test_bmr_tdee_and_macro_calculations():
    bmr = calculate_bmr("male", 30, 180, 80)
    tdee = calculate_tdee(bmr, "moderate")
    macros = calculate_daily_macro_norms(tdee)

    assert round(bmr) == 1780
    assert round(tdee) == 2759
    assert macros["protein_g"] == round(tdee * 0.25 / 4, 1)
    assert macros["fat_g"] == round(tdee * 0.30 / 9, 1)
    assert macros["carbs_g"] == round(tdee * 0.45 / 4, 1)


def test_daily_targets_and_today_summary(tmp_path: Path):
    database = build_db(tmp_path)
    profile_service = ProfileService(database)
    create_complete_profile(profile_service)
    profile_service.set_assistant_mode(1, True)
    service = NutritionService(database)

    result = service.process_message(1, "рис 100")
    service.store_entries(1, result.recognized_items)
    today = service.get_today_summary(1)
    targets = profile_service.get_daily_targets(1)

    assert round(targets.bmr) == 1780
    assert round(targets.tdee) == 2759
    assert today["count"] == 1
    assert today["calories"] > 0
    assert targets.activity_source == "default"
    assert targets.effective_activity_level == "moderate"


def test_profile_can_be_read_and_updated_field_by_field(tmp_path: Path):
    database = build_db(tmp_path)
    profile_service = ProfileService(database)
    create_complete_profile(profile_service)

    profile_service.update_profile_field(1, "tester", "weight_kg", 82.5)
    profile_service.update_profile_field(1, "tester", "activity_level", "active")
    profile = profile_service.get_profile(1)
    targets = profile_service.get_daily_targets(1)

    assert profile is not None
    assert profile.is_complete
    assert profile.sex == "male"
    assert profile.age == 30
    assert profile.height_cm == 180
    assert profile.weight_kg == 82.5
    assert profile.activity_level == "active"
    assert round(targets.bmr) == 1805
    assert round(targets.tdee) == round(1805 * 1.725)


def test_search_products_returns_matches(tmp_path: Path):
    database = build_db(tmp_path)
    profile_service = ProfileService(database)
    profile_service.ensure_user(1, "tester")
    service = NutritionService(database)

    matches = service.search_products("греч")

    assert matches
    assert len(matches) <= 10
    assert len(matches) == len(set(matches))
    assert any("греч" in item.lower() for item in matches)


def test_categories_and_category_products_are_listed(tmp_path: Path):
    database = build_db(tmp_path)
    service = NutritionService(database)

    categories = service.list_categories()
    category_names = {category.name for category in categories}
    vegetables = next(category for category in categories if category.name == "овощи")
    products = service.list_products_by_category(vegetables.slug)

    assert "овощи" in category_names
    assert vegetables.count > 0
    assert products
    assert any(product.name == "помидор" for product in products)


def test_user_product_is_visible_only_to_owner(tmp_path: Path):
    database = build_db(tmp_path)
    profile_service = ProfileService(database)
    profile_service.ensure_user(1, "owner")
    profile_service.ensure_user(2, "other")
    service = NutritionService(database)

    service.create_user_product(1, "owner", "сырники домашние", 210, 14, 9, 20)

    owner_result = service.process_message(1, "сырники домашние 150")
    other_result = service.process_message(2, "сырники домашние 150")

    assert len(owner_result.recognized_items) == 1
    assert owner_result.recognized_items[0].product_source == "user"
    assert round(owner_result.total_calories) == 315
    assert other_result.unrecognized_items == ["сырники домашние 150"]


def test_user_products_can_be_listed_and_deleted(tmp_path: Path):
    database = build_db(tmp_path)
    profile_service = ProfileService(database)
    profile_service.ensure_user(1, "owner")
    service = NutritionService(database)

    service.create_user_product(1, "owner", "сырники домашние", 210, 14, 9, 20)
    products = service.list_user_products(1)
    deleted = service.delete_user_product(1, products[0].id)
    result = service.process_message(1, "сырники домашние 100")

    assert len(products) == 1
    assert products[0].name == "сырники домашние"
    assert deleted
    assert service.list_user_products(1) == []
    assert result.unrecognized_items == ["сырники домашние 100"]


def test_user_product_search_is_scoped_to_owner(tmp_path: Path):
    database = build_db(tmp_path)
    profile_service = ProfileService(database)
    profile_service.ensure_user(1, "owner")
    profile_service.ensure_user(2, "other")
    service = NutritionService(database)

    service.create_user_product(1, "owner", "сырники домашние", 210, 14, 9, 20)

    owner_matches = service.search_products("сыр", telegram_id=1)
    other_matches = service.search_products("сыр", telegram_id=2)

    assert "сырники домашние (личное)" in owner_matches
    assert "сырники домашние (личное)" not in other_matches


def test_user_product_can_be_stored_in_today_summary(tmp_path: Path):
    database = build_db(tmp_path)
    profile_service = ProfileService(database)
    create_complete_profile(profile_service)
    profile_service.set_assistant_mode(1, True)
    service = NutritionService(database)
    service.create_user_product(1, "tester", "сырники домашние", 210, 14, 9, 20)

    result = service.process_message(1, "сырники домашние 100")
    service.store_entries(1, result.recognized_items)
    today = service.get_today_summary(1)

    assert today["count"] == 1
    assert round(float(today["calories"])) == 210


def test_legacy_food_entries_schema_migrates_for_user_products(tmp_path: Path):
    database_path = tmp_path / "legacy.sqlite3"
    with sqlite3.connect(database_path) as conn:
        conn.executescript(
            """
            CREATE TABLE products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                slug TEXT NOT NULL UNIQUE,
                name_ru TEXT NOT NULL,
                normalized_name_ru TEXT NOT NULL UNIQUE,
                category TEXT NOT NULL,
                state TEXT NOT NULL,
                usda_description TEXT NOT NULL,
                fdc_id INTEGER NOT NULL,
                usda_category TEXT NOT NULL,
                calories_per_100g REAL NOT NULL,
                protein_per_100g REAL NOT NULL,
                fat_per_100g REAL NOT NULL,
                carbs_per_100g REAL NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE TABLE product_aliases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
                alias TEXT NOT NULL,
                normalized_alias TEXT NOT NULL UNIQUE,
                language TEXT NOT NULL DEFAULT 'ru',
                created_at TEXT NOT NULL
            );
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER NOT NULL UNIQUE,
                username TEXT,
                assistant_enabled INTEGER NOT NULL DEFAULT 0,
                sex TEXT,
                age INTEGER,
                height_cm REAL,
                weight_kg REAL,
                activity_level TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE TABLE food_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
                raw_item_text TEXT NOT NULL,
                product_text TEXT NOT NULL,
                weight_g REAL NOT NULL,
                calories REAL NOT NULL,
                protein_g REAL NOT NULL,
                fat_g REAL NOT NULL,
                carbs_g REAL NOT NULL,
                consumed_at TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            INSERT INTO products (
                slug,
                name_ru,
                normalized_name_ru,
                category,
                state,
                usda_description,
                fdc_id,
                usda_category,
                calories_per_100g,
                protein_per_100g,
                fat_per_100g,
                carbs_per_100g,
                created_at,
                updated_at
            ) VALUES ('rice', 'рис', 'рис', 'grain', 'cooked', 'Rice', 1, 'Grain', 130, 2.7, 0.3, 28, 'now', 'now');
            INSERT INTO users (telegram_id, username, created_at, updated_at)
            VALUES (1, 'tester', 'now', 'now');
            INSERT INTO food_entries (
                user_id,
                product_id,
                raw_item_text,
                product_text,
                weight_g,
                calories,
                protein_g,
                fat_g,
                carbs_g,
                consumed_at,
                created_at
            ) VALUES (1, 1, 'рис 100', 'рис', 100, 130, 2.7, 0.3, 28, 'now', 'now');
            """
        )

    database = Database(database_path, "Europe/Kiev")
    database.initialize()

    with database.connection() as conn:
        food_entry_columns = {row["name"]: row for row in conn.execute("PRAGMA table_info(food_entries)").fetchall()}
        entry_row = conn.execute("SELECT product_source, product_id, user_product_id FROM food_entries").fetchone()
        table_names = {
            row["name"] for row in conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchall()
        }

    assert food_entry_columns["product_id"]["notnull"] == 0
    assert "user_products" in table_names
    assert entry_row["product_source"] == "base"
    assert entry_row["product_id"] == 1
    assert entry_row["user_product_id"] is None


def test_legacy_user_products_schema_backfills_multilingual_names(tmp_path: Path):
    database_path = tmp_path / "legacy_user_products.sqlite3"
    with sqlite3.connect(database_path) as conn:
        conn.executescript(
            """
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER NOT NULL UNIQUE,
                username TEXT,
                assistant_enabled INTEGER NOT NULL DEFAULT 0,
                sex TEXT,
                age INTEGER,
                height_cm REAL,
                weight_kg REAL,
                activity_level TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE TABLE user_products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                name_ru TEXT NOT NULL,
                normalized_name_ru TEXT NOT NULL,
                calories_per_100g REAL NOT NULL,
                protein_per_100g REAL NOT NULL,
                fat_per_100g REAL NOT NULL,
                carbs_per_100g REAL NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                UNIQUE(user_id, normalized_name_ru)
            );
            INSERT INTO users (telegram_id, username, created_at, updated_at)
            VALUES (1, 'tester', 'now', 'now');
            INSERT INTO user_products (
                user_id,
                name_ru,
                normalized_name_ru,
                calories_per_100g,
                protein_per_100g,
                fat_per_100g,
                carbs_per_100g,
                created_at,
                updated_at
            ) VALUES (1, 'сырники домашние', 'сырники домашние', 210, 14, 9, 20, 'now', 'now');
            """
        )

    database = Database(database_path, "Europe/Kiev")
    database.initialize()
    profile_service = ProfileService(database)
    profile_service.update_profile_language(1, "en")
    nutrition_service = NutritionService(database)

    with database.connection() as conn:
        row = conn.execute(
            """
            SELECT name_en, normalized_name_en, name_uk, normalized_name_uk
            FROM user_products
            WHERE user_id = 1
            """
        ).fetchone()

    assert row["name_en"] == "Syrniki homemade"
    assert row["normalized_name_en"] == "syrniki homemade"
    assert row["name_uk"] == "сирники домашні"
    assert row["normalized_name_uk"] == "сирники домашні"
    assert "Syrniki homemade (personal)" in nutrition_service.search_products("syrniki", telegram_id=1)

    result = nutrition_service.process_message(1, "syrniki homemade 150")
    assert len(result.recognized_items) == 1
    assert result.recognized_items[0].product_source == "user"
    assert round(result.total_calories) == 315


def test_activity_override_affects_today_targets_only(tmp_path: Path):
    database = build_db(tmp_path)
    profile_service = ProfileService(database)
    create_complete_profile(profile_service)

    default_targets = profile_service.get_daily_targets(1)
    profile_service.set_activity_override_for_today(1, "active")
    override_targets = profile_service.get_daily_targets(1)

    user_id = profile_service.get_user_id(1)
    yesterday = "2000-01-01"
    now = database.now_iso()
    with database.connection() as conn:
        conn.execute("DELETE FROM user_activity_overrides WHERE user_id = ?", (user_id,))
        conn.execute(
            """
            INSERT INTO user_activity_overrides (user_id, activity_level, activity_date, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, "very_active", yesterday, now, now),
        )
    expired_targets = profile_service.get_daily_targets(1)

    assert default_targets.activity_source == "default"
    assert override_targets.activity_source == "override"
    assert override_targets.effective_activity_level == "active"
    assert round(override_targets.tdee) > round(default_targets.tdee)
    assert expired_targets.activity_source == "default"
    assert expired_targets.effective_activity_level == "moderate"


def test_activity_reset_clears_today_override(tmp_path: Path):
    database = build_db(tmp_path)
    profile_service = ProfileService(database)
    create_complete_profile(profile_service)

    profile_service.set_activity_override_for_today(1, "very_active")
    profile_service.clear_activity_override_for_today(1)
    targets = profile_service.get_daily_targets(1)

    assert targets.activity_source == "default"
    assert targets.effective_activity_level == "moderate"


def test_assistant_reply_contains_targets_and_non_medical_copy(tmp_path: Path):
    database = build_db(tmp_path)
    profile_service = ProfileService(database)
    create_complete_profile(profile_service)
    profile_service.set_assistant_mode(1, True)
    service = NutritionService(database)

    result = service.process_message(1, "рис 100")
    service.store_entries(1, result.recognized_items)
    today = service.get_today_summary(1)
    targets = profile_service.get_daily_targets(1)
    reply = service.format_assistant_reply(result, today, targets)

    assert "TDEE" in reply
    assert "Расчетная дневная норма БЖУ (приблизительно)" in reply
    assert "remaining calories" not in reply.lower()
    assert "нужно съесть" not in reply.lower()
    assert "Белки:" in reply
    assert "Подробнее: /terms" in reply


def test_cancel_labels_are_stable():
    assert BUTTON_ADD_FOOD == "Добавить еду"
    assert CANCEL_EDIT_PROFILE_TEXT == "Отмена"
    assert CANCEL_SEARCH_TEXT == "Отмена"


def test_multilingual_profile_language_get_set(tmp_path: Path):
    database = build_db(tmp_path)
    profile_service = ProfileService(database)
    
    # 1. Default creation sets default language
    profile_service.ensure_user(1, "tester", default_lang="uk")
    profile = profile_service.get_profile(1)
    assert profile.language == "uk"
    
    # 2. Update language updates correctly
    profile_service.update_profile_language(1, "en")
    profile = profile_service.get_profile(1)
    assert profile.language == "en"


def test_multilingual_product_search_and_calculation(tmp_path: Path):
    database = build_db(tmp_path)
    profile_service = ProfileService(database)
    profile_service.ensure_user(1, "tester", default_lang="en")
    service = NutritionService(database)
    
    # 1. Search product in English
    matches_en = service.search_products("rice", telegram_id=1)
    assert matches_en
    assert any("rice" in m.lower() for m in matches_en)
    
    # 2. Process message in English
    result_en = service.process_message(1, "rice 150")
    assert len(result_en.recognized_items) == 1
    assert result_en.recognized_items[0].display_name == "Rice white cooked"
    assert result_en.recognized_items[0].weight_g == 150.0
    
    # 3. Ukrainian support
    profile_service.update_profile_language(1, "uk")
    result_uk = service.process_message(1, "рис 150")
    assert len(result_uk.recognized_items) == 1
    assert result_uk.recognized_items[0].display_name == "рис білий варений"


def test_multilingual_formatting_replies(tmp_path: Path):
    database = build_db(tmp_path)
    profile_service = ProfileService(database)
    create_complete_profile(profile_service, telegram_id=1)
    profile_service.update_profile_language(1, "en")
    service = NutritionService(database)
    
    # Process message in English
    result = service.process_message(1, "rice 100")
    reply = service.format_calc_reply(result, lang="en")
    
    assert "Total:" in reply
    assert "Protein:" in reply
    assert "Fat:" in reply
    assert "Carbs:" in reply


def test_multilingual_personal_product_creation_and_parsing(tmp_path: Path):
    database = build_db(tmp_path)
    profile_service = ProfileService(database)
    profile_service.ensure_user(1, "tester", default_lang="en")
    service = NutritionService(database)

    # 1. Create personal product in English
    service.create_user_product(
        telegram_id=1,
        username="tester",
        name_input="syrniki",
        calories_per_100g=210,
        protein_per_100g=14,
        fat_per_100g=9,
        carbs_per_100g=20,
        input_lang="en"
    )

    # 2. Search for it in English
    matches_en = service.search_products("syrniki", telegram_id=1)
    assert matches_en
    assert "Syrniki (personal)" in matches_en

    # 3. Parse it in English
    result_en = service.process_message(1, "syrniki 150")
    assert len(result_en.recognized_items) == 1
    assert result_en.recognized_items[0].product_source == "user"
    assert round(result_en.total_calories) == 315


def test_multilingual_language_autodetection(tmp_path: Path):
    from unittest.mock import Mock
    database = build_db(tmp_path)
    profile_service = ProfileService(database)
    
    # Simulate a user migrated with 'ru' and language_set=0
    profile_service.ensure_user(1, "legacy_user", default_lang="ru")
    with database.connection() as conn:
        conn.execute("UPDATE users SET language_set = 0 WHERE telegram_id = 1")
    
    # Now simulate they send a message with English TG client
    from app.handlers.bot import _get_user_lang
    mock_from_user = Mock()
    mock_from_user.language_code = "en"
    
    # 1. _get_user_lang should return "en" because language_set is 0
    detected_lang = _get_user_lang(1, profile_service, mock_from_user)
    assert detected_lang == "en"
    
    # 2. ensure_user is called with the detected_lang
    profile_service.ensure_user(1, "legacy_user", default_lang=detected_lang)
    
    # 3. The database should now have 'en', but language_set should still be 0
    profile = profile_service.get_profile(1)
    assert profile.language == "en"
    assert not profile.language_set
    
    # 4. If they explicitly change it
    profile_service.update_profile_language(1, "uk")
    profile = profile_service.get_profile(1)
    assert profile.language == "uk"
    assert profile.language_set
    
    # 5. _get_user_lang should now stick to "uk" even if TG is "en"
    detected_lang_again = _get_user_lang(1, profile_service, mock_from_user)
    assert detected_lang_again == "uk"


def test_format_product_summary_localization():
    from app.handlers.bot import _format_product_summary
    from dataclasses import dataclass

    @dataclass
    class DummyProduct:
        name: str
        calories_per_100g: float
        protein_per_100g: float
        fat_per_100g: float
        carbs_per_100g: float

    product = DummyProduct(
        name="test_food",
        calories_per_100g=150.0,
        protein_per_100g=10.0,
        fat_per_100g=5.0,
        carbs_per_100g=20.0
    )

    # Russian
    res_ru = _format_product_summary(product, "ru")
    assert "ккал" in res_ru
    assert "Б 10" in res_ru
    assert "Ж 5" in res_ru
    assert "У 20" in res_ru

    # English
    res_en = _format_product_summary(product, "en")
    assert "kcal" in res_en
    assert "P 10" in res_en
    assert "F 5" in res_en
    assert "C 20" in res_en

    # Ukrainian
    res_uk = _format_product_summary(product, "uk")
    assert "ккал" in res_uk
    assert "Б 10" in res_uk
    assert "Ж 5" in res_uk
    assert "В 20" in res_uk  # Ukrainian 'В' for Carbs (Вуглеводи)

