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
    assert CANCEL_EDIT_PROFILE_TEXT == "Отмена"
    assert CANCEL_SEARCH_TEXT == "Отмена"
