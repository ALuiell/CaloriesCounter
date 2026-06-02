from __future__ import annotations

LOCALES = {
    "ru": {
        # Buttons & Labels
        "btn_add_food": "Добавить еду",
        "btn_create_profile": "Профиль+",
        "btn_profile": "Профиль",
        "btn_today": "Сегодня",
        "btn_activity": "Активность",
        "btn_search": "Поиск",
        "btn_help": "Помощь",
        "btn_assistant_on": "Вкл. assistant",
        "btn_assistant_off": "Выкл. assistant",
        "btn_cancel": "Отмена",
        "btn_activity_today": "Активность на сегодня",
        "btn_activity_reset": "Сбросить активность",
        "btn_profile_edit": "Изменить профиль",
        "btn_terms": "Что такое BMR и TDEE",
        "btn_back": "Назад",
        "btn_add_product": "Добавить продукт",
        "btn_my_products": "Мои продукты",
        "btn_delete_product": "Удалить: {name}",

        # Sex Keyboard
        "sex_male": "male",
        "sex_female": "female",

        # Activity Keyboard
        "activity_sedentary": "Спокойный день",
        "activity_light": "Легкая активность",
        "activity_moderate": "Умеренная активность",
        "activity_active": "Высокая активность",
        "activity_very_active": "Очень высокая активность",

        # Profile Fields Keyboard
        "field_sex": "Пол",
        "field_age": "Возраст",
        "field_height": "Рост",
        "field_weight": "Вес",
        "field_activity": "Активность по умолчанию",

        # Prompts & Inputs
        "prompt_sex": "Укажи пол: male или female.",
        "prompt_sex_new": "Укажи новый пол: male или female.",
        "prompt_age": "Отправь возраст в годах.",
        "prompt_age_new": "Отправь новый возраст в годах.",
        "prompt_height": "Отправь рост в см.",
        "prompt_height_new": "Отправь новый рост в см.",
        "prompt_weight": "Отправь вес в кг.",
        "prompt_weight_new": "Отправь новый вес в кг.",
        "prompt_activity": "Выбери активность по умолчанию.",
        "prompt_activity_new": "Выбери новую активность по умолчанию.",
        "prompt_activity_today": "Выбери активность на сегодня.",
        "prompt_search_query": "Напиши название продукта для поиска.\nДля отмены нажми «Отмена».",
        "prompt_add_food_product": (
            "Добавь личный продукт или готовое блюдо.\n\n"
            "Формат на 100 г:\n"
            "<code>название; ккал; белки; жиры; углеводы</code>\n\n"
            "Пример:\n"
            "<code>сырники домашние; 210; 14; 9; 20</code>\n\n"
            "Эта еда будет видна только тебе."
        ),
        "prompt_choose_action": "Выбери действие:",

        # Success / Status Messages
        "profile_saved": "Профиль сохранен.",
        "profile_updated": "Профиль обновлен.",
        "profile_incomplete": "Профиль еще не заполнен полностью. Сначала используй /profile.",
        "profile_incomplete_activity": "Чтобы открыть активность, сначала заполни профиль через /profile.",
        "profile_incomplete_activity_today": "Чтобы выбрать активность на сегодня, сначала заполни профиль через /profile.",
        "profile_incomplete_activity_reset": "Сначала заполни профиль через /profile.",
        "profile_incomplete_today": "Профиль заполнен не полностью. Сначала используй /profile.",
        "profile_incomplete_assistant": "Профиль заполнен не полностью. Сначала используй /profile.",
        "profile_quick_actions": "Быстрые действия профиля:",
        "profile_card_header": "Твой профиль:",
        "profile_sex_label": "Пол: {sex}",
        "profile_age_label": "Возраст: {age}",
        "profile_height_label": "Рост: {height} см",
        "profile_weight_label": "Вес: {weight} кг",
        "profile_activity_label": "Активность по умолчанию: {activity}",
        "profile_assistant_label": "Assistant mode: {status}",
        "profile_status_enabled": "включен",
        "profile_status_disabled": "выключен",
        "sex_male_label": "Мужской",
        "sex_female_label": "Женский",
        "changes_not_made": "Изменения не вносились.",
        "choose_field_to_edit": "Что хочешь изменить?",
        "choose_field_to_edit_invalid": "Выбери поле: Пол, Возраст, Рост, Вес, Активность по умолчанию или Отмена.",
        "error_age_range": "Возраст должен быть числом от 10 до 120.",
        "error_height_range": "Рост должен быть числом от 80 до 250 см.",
        "error_weight_range": "Вес должен быть числом от 20 до 300 кг.",

        # Activity Screen / Today
        "activity_header": "Активность:",
        "activity_default": "По умолчанию: {activity}",
        "activity_for_calc": "Для расчета сегодня: {activity}",
        "activity_override_active": "На сегодня используется override активности.",
        "activity_default_used": "Использована активность по умолчанию.",
        "activity_saved_today": (
            "Активность на сегодня сохранена.\n"
            "Этот выбор действует только до конца текущего дня.\n\n"
            "{targets}"
        ),
        "activity_reset_today": (
            "Активность на сегодня сброшена. Снова используется активность по умолчанию.\n\n"
            "{targets}"
        ),
        "actions_header": "Действия:",
        "bmr_label": "BMR: <b>{bmr}</b> ккал",
        "tdee_label": "TDEE: <b>{tdee}</b> ккал",
        "macro_norms_header": "Расчетная дневная норма БЖУ (приблизительно):",
        "macro_norms_values": "Б: {protein} г / Ж: {fat} г / У: {carbs} г",
        "bmr_tdee_hint": "BMR — расход в покое, TDEE — расход с учетом активности.\nПодробнее: /terms",

        # Search & Food
        "categories_not_available": "Категории пока недоступны.",
        "choose_category_or_search": "Выбери категорию или напиши /search с названием продукта.",
        "categories_header": "Категории:",
        "category_empty": "В этой категории ничего не найдено.",
        "category_products_header": "Продукты в категории:",
        "category_how_to_send": "Можно отправить продукт обычным сообщением, например: <code>название 100</code>",
        "search_not_found": "По запросу <code>{query}</code> ничего не найдено.",
        "search_found": "Найдено:",
        "add_food_menu_header": "Что сделать с личной едой?",
        "personal_products_empty": "Личных продуктов пока нет. Нажми «Добавить продукт», чтобы сохранить свой вариант.",
        "personal_products_header": "Мои продукты:",
        "personal_product_summary": "- {name}: {calories} ккал, Б {protein} / Ж {fat} / У {carbs}",
        "personal_product_deleted": "Удалено",
        "personal_product_not_found": "Не найдено",
        "personal_product_parse_error": (
            "Не получилось разобрать продукт.\n"
            "Формат: <code>название; ккал; белки; жиры; углеводы</code>\n"
            "Пример: <code>сырники домашние; 210; 14; 9; 20</code>"
        ),
        "personal_product_saved": (
            "Сохранил личную еду:\n"
            "<b>{name}</b> на 100 г: {calories} ккал, Б {protein} / Ж {fat} / У {carbs}.\n\n"
            "Теперь можно писать: <code>{name} 150</code>"
        ),
        "search_cancelled": "Поиск отменен.",
        "add_food_cancelled": "Добавление еды отменено.",
        "personal_label": "{name} (личное)",

        # Calculations
        "calc_header": "Посчитано:",
        "calc_unrecognized": "Не удалось распознать:",
        "calc_empty": (
            "Ничего не удалось посчитать.\n"
            "Используй формат: <code>продукт + граммы</code>\n"
            "Пример: <code>гречка 120, курица 180</code>"
        ),
        "calc_item": "- {name} {weight} г: {calories} ккал, Б {protein} / Ж {fat} / У {carbs}",
        "calc_total": "Итого:\n{calories} ккал\nБелки: {protein} г\nЖиры: {fat} г\nУглеводы: {carbs} г",
        "calc_today": "За сегодня:\n{calories} ккал\nБелки: {protein} г\nЖиры: {fat} г\nУглеводы: {carbs} г",

        # Assistant Mode
        "assistant_enabled_msg": "Assistant mode включен. Теперь ответы на еду будут содержать итоги за сегодня, BMR, TDEE и расчетную норму БЖУ.",
        "assistant_disabled_msg": "Assistant mode выключен. Бот снова отвечает только расчетом по сообщению.",

        # Core / Commands
        "welcome": (
            "Бот готов.\n\n"
            "Отправь еду, например:\n"
            "<code>гречка 120, курица 180, помидор 80</code>\n\n"
            "Используй кнопки внизу для навигации.\n"
            "Короткая справка по метрикам: /terms."
        ),
        "help": (
            "Как пользоваться ботом:\n\n"
            "1. Отправь еду обычным текстом.\n"
            "Примеры:\n"
            "<code>гречка 120, курица 180</code>\n"
            "<code>рис 100\nпомидор 80</code>\n\n"
            "2. {btn_add_food} — добавь личный продукт или готовое блюдо, если его нет в базе.\n"
            "3. {btn_profile} или {btn_create_profile} — настрой профиль.\n"
            "4. {btn_today} — смотри итог за сегодня.\n"
            "5. {btn_activity} — меняй активность на сегодня.\n"
            "6. {btn_search} — ищи продукты по базе.\n\n"
            "Команды тоже работают, но кнопки теперь основной способ навигации.\n"
            "Что такое BMR и TDEE: /terms"
        ),
        "terms": (
            "Короткая справка по метрикам:\n\n"
            "BMR — базовый обмен веществ.\n"
            "Это сколько калорий организм тратит в покое: на дыхание, работу сердца, мозга и органов.\n\n"
            "TDEE — примерный расход калорий за день с учетом активности.\n"
            "Это BMR, умноженный на выбранный уровень активности.\n\n"
            "Расчетная дневная норма БЖУ — ориентир по белкам, жирам и углеводам, рассчитанный от TDEE.\n"
            "Это приблизительный расчет, а не медицинская рекомендация."
        ),

        # Language selection
        "lang_choose": "Choose interface language / Оберіть мову інтерфейсу / Выбери язык интерфейса:",
        "lang_changed": "Язык интерфейса изменен на Русский. 🇷🇺",
        "btn_change_lang": "Сменить язык EN/UA/RU",
    },
    "uk": {
        # Buttons & Labels
        "btn_add_food": "Додати їжу",
        "btn_create_profile": "Профіль+",
        "btn_profile": "Профіль",
        "btn_today": "Сьогодні",
        "btn_activity": "Активність",
        "btn_search": "Пошук",
        "btn_help": "Допомога",
        "btn_assistant_on": "Увімк. assistant",
        "btn_assistant_off": "Вимк. assistant",
        "btn_cancel": "Скасувати",
        "btn_activity_today": "Активність на сьогодні",
        "btn_activity_reset": "Скинути активність",
        "btn_profile_edit": "Змінити профіль",
        "btn_terms": "Що таке BMR та TDEE",
        "btn_back": "Назад",
        "btn_add_product": "Додати продукт",
        "btn_my_products": "Мої продукти",
        "btn_delete_product": "Видалити: {name}",

        # Sex Keyboard
        "sex_male": "male",
        "sex_female": "female",

        # Activity Keyboard
        "activity_sedentary": "Спокійний день",
        "activity_light": "Легка активність",
        "activity_moderate": "Помірна активність",
        "activity_active": "Висока активність",
        "activity_very_active": "Дуже висока активність",

        # Profile Fields Keyboard
        "field_sex": "Стать",
        "field_age": "Вік",
        "field_height": "Зріст",
        "field_weight": "Вага",
        "field_activity": "Активність за замовчуванням",

        # Prompts & Inputs
        "prompt_sex": "Вкажи стать: male або female.",
        "prompt_sex_new": "Вкажи нову стать: male або female.",
        "prompt_age": "Надішли вік у роках.",
        "prompt_age_new": "Надішли новий вік у роках.",
        "prompt_height": "Надішли зріст у см.",
        "prompt_height_new": "Надішли новий зріст у см.",
        "prompt_weight": "Надішли вагу в кг.",
        "prompt_weight_new": "Надішли нову вагу в кг.",
        "prompt_activity": "Обери активність за замовчуванням.",
        "prompt_activity_new": "Обери нову активність за замовчуванням.",
        "prompt_activity_today": "Обери активність на сьогодні.",
        "prompt_search_query": "Напиши назву продукту для пошуку.\nДля скасування натисни «Скасувати».",
        "prompt_add_food_product": (
            "Додай особистий продукт або готову страву.\n\n"
            "Формат на 100 г:\n"
            "<code>назва; ккал; білки; жири; вуглеводи</code>\n\n"
            "Приклад:\n"
            "<code>сырники домашние; 210; 14; 9; 20</code>\n\n"
            "Ця їжа буде видна тільки тобі."
        ),
        "prompt_choose_action": "Обери дію:",

        # Success / Status Messages
        "profile_saved": "Профіль збережено.",
        "profile_updated": "Профіль оновлено.",
        "profile_incomplete": "Профіль ще не заповнений повністю. Спочатку використовуй /profile.",
        "profile_incomplete_activity": "Щоб відкрити активність, спочатку заповни профіль через /profile.",
        "profile_incomplete_activity_today": "Щоб обрати активність на сьогодні, спочатку заповни профіль через /profile.",
        "profile_incomplete_activity_reset": "Спочатку заповни профіль через /profile.",
        "profile_incomplete_today": "Профіль заповнений не повністю. Спочатку використовуй /profile.",
        "profile_incomplete_assistant": "Профіль заповнений не повністю. Спочатку використовуй /profile.",
        "profile_quick_actions": "Швидкі дії профілю:",
        "profile_card_header": "Твій профіль:",
        "profile_sex_label": "Стать: {sex}",
        "profile_age_label": "Вік: {age}",
        "profile_height_label": "Зріст: {height} см",
        "profile_weight_label": "Вага: {weight} кг",
        "profile_activity_label": "Активність за замовчуванням: {activity}",
        "profile_assistant_label": "Assistant mode: {status}",
        "profile_status_enabled": "увімкнено",
        "profile_status_disabled": "вимкнено",
        "sex_male_label": "Чоловіча",
        "sex_female_label": "Жіноча",
        "changes_not_made": "Зміни не вносилися.",
        "choose_field_to_edit": "Що хочеш змінити?",
        "choose_field_to_edit_invalid": "Обери поле: Стать, Вік, Зріст, Вага, Активність за замовчуванням або Скасувати.",
        "error_age_range": "Вік має бути числом від 10 до 120.",
        "error_height_range": "Зріст має бути числом від 80 до 250 см.",
        "error_weight_range": "Вага має бути числом від 20 до 300 кг.",

        # Activity Screen / Today
        "activity_header": "Активність:",
        "activity_default": "За замовчуванням: {activity}",
        "activity_for_calc": "Для розрахунку сьогодні: {activity}",
        "activity_override_active": "На сьогодні використовується override активності.",
        "activity_default_used": "Використано активність за замовчуванням.",
        "activity_saved_today": (
            "Активність на сьогодні збережена.\n"
            "Цей вибір діє тільки до кінця поточного дня.\n\n"
            "{targets}"
        ),
        "activity_reset_today": (
            "Активність на сьогодні скинута. Знову використовується активність за замовчуванням.\n\n"
            "{targets}"
        ),
        "actions_header": "Дії:",
        "bmr_label": "BMR: <b>{bmr}</b> ккал",
        "tdee_label": "TDEE: <b>{tdee}</b> ккал",
        "macro_norms_header": "Розрахункова денна норма БЖВ (приблизно):",
        "macro_norms_values": "Б: {protein} г / Ж: {fat} г / В: {carbs} г",
        "bmr_tdee_hint": "BMR — витрата у спокої, TDEE — витрата з урахуванням активності.\nДетальніше: /terms",

        # Search & Food
        "categories_not_available": "Категорії поки недоступні.",
        "choose_category_or_search": "Обери категорію або напиши /search з назвою продукту.",
        "categories_header": "Категорії:",
        "category_empty": "У цій категорії нічого не знайдено.",
        "category_products_header": "Продукти в категорії:",
        "category_how_to_send": "Можна надіслати продукт звичайним повідомленням, наприклад: <code>назва 100</code>",
        "search_not_found": "За запитом <code>{query}</code> нічого не знайдено.",
        "search_found": "Знайдено:",
        "add_food_menu_header": "Що зробити з особистою їжею?",
        "personal_products_empty": "Особистих продуктів поки немає. Натисни «Додати продукт», щоб зберегти свій варіант.",
        "personal_products_header": "Мої продукти:",
        "personal_product_summary": "- {name}: {calories} ккал, Б {protein} / Ж {fat} / В {carbs}",
        "personal_product_deleted": "Видалено",
        "personal_product_not_found": "Не знайдено",
        "personal_product_parse_error": (
            "Не вдалося розібрати продукт.\n"
            "Формат: <code>назва; ккал; білки; жири; вуглеводи</code>\n"
            "Приклад: <code>сирники домашні; 210; 14; 9; 20</code>"
        ),
        "personal_product_saved": (
            "Зберіг особисту їжу:\n"
            "<b>{name}</b> на 100 г: {calories} ккал, Б {protein} / Ж {fat} / В {carbs}.\n\n"
            "Тепер можна писати: <code>{name} 150</code>"
        ),
        "search_cancelled": "Пошук скасовано.",
        "add_food_cancelled": "Додавання їжі скасовано.",
        "personal_label": "{name} (особисте)",

        # Calculations
        "calc_header": "Пораховано:",
        "calc_unrecognized": "Не вдалося розпізнати:",
        "calc_empty": (
            "Нічого не вдалося порахувати.\n"
            "Використовуй формат: <code>продукт + грами</code>\n"
            "Приклад: <code>гречка 120, курка 180</code>"
        ),
        "calc_item": "- {name} {weight} г: {calories} ккал, Б {protein} / Ж {fat} / В {carbs}",
        "calc_total": "Разом:\n{calories} ккал\nБілки: {protein} г\nЖири: {fat} г\nВуглеводи: {carbs} г",
        "calc_today": "За сьогодні:\n{calories} ккал\nБілки: {protein} г\nЖири: {fat} г\nВуглеводи: {carbs} г",

        # Assistant Mode
        "assistant_enabled_msg": "Assistant mode увімкнено. Тепер відповіді на їжу міститимуть підсумки за сьогодні, BMR, TDEE та розрахункову норму БЖВ.",
        "assistant_disabled_msg": "Assistant mode вимкнено. Бот знову відповідає лише розрахунком за повідомленням.",

        # Core / Commands
        "welcome": (
            "Бот готовий.\n\n"
            "Надішли їжу, наприклад:\n"
            "<code>гречка 120, курка 180, помідор 80</code>\n\n"
            "Використовуй кнопки внизу для навігації.\n"
            "Коротка довідка щодо метрик: /terms."
        ),
        "help": (
            "Як користуватися ботом:\n\n"
            "1. Надішли їжу звичайним текстом.\n"
            "Приклади:\n"
            "<code>гречка 120, курка 180</code>\n"
            "<code>рис 100\nпомідор 80</code>\n\n"
            "2. {btn_add_food} — додай особистий продукт або готову страву, якщо її немає в базі.\n"
            "3. {btn_profile} або {btn_create_profile} — налаштуй профіль.\n"
            "4. {btn_today} — дивись підсумок за сьогодні.\n"
            "5. {btn_activity} — змінюй активність на сьогодні.\n"
            "6. {btn_search} — шукай продукти по базі.\n\n"
            "Команди також працюють, але кнопки тепер основний спосіб навігації.\n"
            "Що таке BMR та TDEE: /terms"
        ),
        "terms": (
            "Коротка довідка щодо метрик:\n\n"
            "BMR — базовий обмін речовин.\n"
            "Це скільки калорій організм витрачає у спокої: на дихання, роботу серця, мозку та органів.\n\n"
            "TDEE — приблизна витрата калорій за день з урахуванням активності.\n"
            "Це BMR, помножений на обраний рівень активності.\n\n"
            "Розрахункова денна норма БЖВ — орієнтир по білках, жирах та вуглеводах, розрахований від TDEE.\n"
            "Це приблизний розрахунок, а не медична рекомендація."
        ),

        # Language selection
        "lang_choose": "Choose interface language / Оберіть мову інтерфейсу / Выбери язык интерфейса:",
        "lang_changed": "Мову інтерфейсу змінено на Українську. 🇺🇦",
        "btn_change_lang": "Змінити мову EN/UA/RU",
    },
    "en": {
        # Buttons & Labels
        "btn_add_food": "Add food",
        "btn_create_profile": "Profile+",
        "btn_profile": "Profile",
        "btn_today": "Today",
        "btn_activity": "Activity",
        "btn_search": "Search",
        "btn_help": "Help",
        "btn_assistant_on": "Turn on assistant",
        "btn_assistant_off": "Turn off assistant",
        "btn_cancel": "Cancel",
        "btn_activity_today": "Activity for today",
        "btn_activity_reset": "Reset activity",
        "btn_profile_edit": "Edit profile",
        "btn_terms": "What is BMR and TDEE",
        "btn_back": "Back",
        "btn_add_product": "Add product",
        "btn_my_products": "My products",
        "btn_delete_product": "Delete: {name}",

        # Sex Keyboard
        "sex_male": "male",
        "sex_female": "female",

        # Activity Keyboard
        "activity_sedentary": "Sedentary day",
        "activity_light": "Light activity",
        "activity_moderate": "Moderate activity",
        "activity_active": "High activity",
        "activity_very_active": "Very high activity",

        # Profile Fields Keyboard
        "field_sex": "Sex",
        "field_age": "Age",
        "field_height": "Height",
        "field_weight": "Weight",
        "field_activity": "Default activity",

        # Prompts & Inputs
        "prompt_sex": "Choose sex: male or female.",
        "prompt_sex_new": "Choose new sex: male or female.",
        "prompt_age": "Send age in years.",
        "prompt_age_new": "Send new age in years.",
        "prompt_height": "Send height in cm.",
        "prompt_height_new": "Send new height in cm.",
        "prompt_weight": "Send weight in kg.",
        "prompt_weight_new": "Send new weight in kg.",
        "prompt_activity": "Choose default activity.",
        "prompt_activity_new": "Choose new default activity.",
        "prompt_activity_today": "Choose activity for today.",
        "prompt_search_query": "Type product name for search.\nTo cancel press 'Cancel'.",
        "prompt_add_food_product": (
            "Add personal product or ready meal.\n\n"
            "Format per 100 g:\n"
            "<code>name; kcal; protein; fat; carbs</code>\n\n"
            "Example:\n"
            "<code>cottage cheese pancakes; 210; 14; 9; 20</code>\n\n"
            "This food will be visible only to you."
        ),
        "prompt_choose_action": "Choose action:",

        # Success / Status Messages
        "profile_saved": "Profile saved.",
        "profile_updated": "Profile updated.",
        "profile_incomplete": "Profile is not fully filled. Use /profile first.",
        "profile_incomplete_activity": "To open activity, fill profile first via /profile.",
        "profile_incomplete_activity_today": "To choose activity for today, fill profile first via /profile.",
        "profile_incomplete_activity_reset": "Fill profile first via /profile.",
        "profile_incomplete_today": "Profile is incomplete. Use /profile first.",
        "profile_incomplete_assistant": "Profile is incomplete. Use /profile first.",
        "profile_quick_actions": "Profile quick actions:",
        "profile_card_header": "Your profile:",
        "profile_sex_label": "Sex: {sex}",
        "profile_age_label": "Age: {age}",
        "profile_height_label": "Height: {height} cm",
        "profile_weight_label": "Weight: {weight} kg",
        "profile_activity_label": "Default activity: {activity}",
        "profile_assistant_label": "Assistant mode: {status}",
        "profile_status_enabled": "enabled",
        "profile_status_disabled": "disabled",
        "sex_male_label": "Male",
        "sex_female_label": "Female",
        "changes_not_made": "No changes made.",
        "choose_field_to_edit": "What do you want to change?",
        "choose_field_to_edit_invalid": "Choose field: Sex, Age, Height, Weight, Default activity or Cancel.",
        "error_age_range": "Age must be between 10 and 120.",
        "error_height_range": "Height must be between 80 and 250 cm.",
        "error_weight_range": "Weight must be between 20 and 300 kg.",

        # Activity Screen / Today
        "activity_header": "Activity:",
        "activity_default": "Default: {activity}",
        "activity_for_calc": "For today's calculations: {activity}",
        "activity_override_active": "Activity override is used for today.",
        "activity_default_used": "Default activity is used.",
        "activity_saved_today": (
            "Activity for today is saved.\n"
            "This choice is valid only until the end of today.\n\n"
            "{targets}"
        ),
        "activity_reset_today": (
            "Activity for today is reset. Default activity is used again.\n\n"
            "{targets}"
        ),
        "actions_header": "Actions:",
        "bmr_label": "BMR: <b>{bmr}</b> kcal",
        "tdee_label": "TDEE: <b>{tdee}</b> kcal",
        "macro_norms_header": "Estimated daily macro norms (approximate):",
        "macro_norms_values": "P: {protein} g / F: {fat} g / C: {carbs} g",
        "bmr_tdee_hint": "BMR is resting energy expenditure, TDEE is expenditure including activity.\nMore details: /terms",

        # Search & Food
        "categories_not_available": "Categories are not available yet.",
        "choose_category_or_search": "Choose category or type /search with product name.",
        "categories_header": "Categories:",
        "category_empty": "Nothing found in this category.",
        "category_products_header": "Products in category:",
        "category_how_to_send": "You can send product as a regular message, e.g.: <code>name 100</code>",
        "search_not_found": "Nothing found for <code>{query}</code>.",
        "search_found": "Found:",
        "add_food_menu_header": "What to do with personal food?",
        "personal_products_empty": "No personal products yet. Click 'Add product' to save your own.",
        "personal_products_header": "My products:",
        "personal_product_summary": "- {name}: {calories} kcal, P {protein} / F {fat} / C {carbs}",
        "personal_product_deleted": "Deleted",
        "personal_product_not_found": "Not found",
        "personal_product_parse_error": (
            "Couldn't parse the product.\n"
            "Format: <code>name; kcal; protein; fat; carbs</code>\n"
            "Example: <code>cottage cheese pancakes; 210; 14; 9; 20</code>"
        ),
        "personal_product_saved": (
            "Saved personal food:\n"
            "<b>{name}</b> per 100 g: {calories} kcal, P {protein} / F {fat} / C {carbs}.\n\n"
            "Now you can type: <code>{name} 150</code>"
        ),
        "search_cancelled": "Search cancelled.",
        "add_food_cancelled": "Adding food cancelled.",
        "personal_label": "{name} (personal)",

        # Calculations
        "calc_header": "Calculated:",
        "calc_unrecognized": "Unrecognized items:",
        "calc_empty": (
            "Nothing was calculated.\n"
            "Use format: <code>product + grams</code>\n"
            "Example: <code>rice 120, chicken 180</code>"
        ),
        "calc_item": "- {name} {weight} g: {calories} kcal, P {protein} / F {fat} / C {carbs}",
        "calc_total": "Total:\n{calories} kcal\nProtein: {protein} g\nFat: {fat} g\nCarbs: {carbs} g",
        "calc_today": "Today's total:\n{calories} kcal\nProtein: {protein} g\nFat: {fat} g\nCarbs: {carbs} g",

        # Assistant Mode
        "assistant_enabled_msg": "Assistant mode is enabled. Food replies will now contain today's summary, BMR, TDEE, and macro norms.",
        "assistant_disabled_msg": "Assistant mode is disabled. The bot will reply only with calculation for the message.",

        # Core / Commands
        "welcome": (
            "Bot is ready.\n\n"
            "Send food, e.g.:\n"
            "<code>rice 120, chicken 180, tomato 80</code>\n\n"
            "Use buttons below for navigation.\n"
            "Short guide on metrics: /terms."
        ),
        "help": (
            "How to use the bot:\n\n"
            "1. Send food in plain text.\n"
            "Examples:\n"
            "<code>rice 120, chicken 180</code>\n"
            "<code>rice 100\ntomato 80</code>\n\n"
            "2. {btn_add_food} — add personal product or ready meal if it's not in the database.\n"
            "3. {btn_profile} or {btn_create_profile} — adjust profile.\n"
            "4. {btn_today} — view today's total.\n"
            "5. {btn_activity} — change today's activity.\n"
            "6. {btn_search} — search products in database.\n\n"
            "Commands also work, but buttons are now the main navigation method.\n"
            "What is BMR and TDEE: /terms"
        ),
        "terms": (
            "Short guide on metrics:\n\n"
            "BMR — Basal Metabolic Rate.\n"
            "This is how many calories the body burns at rest: for breathing, heart, brain, and organ function.\n\n"
            "TDEE — Total Daily Energy Expenditure.\n"
            "This is BMR multiplied by your chosen activity level.\n\n"
            "Estimated daily macro norms — approximate guidelines for protein, fat, and carbs based on TDEE.\n"
            "This is an estimation, not a medical recommendation."
        ),

        # Language selection
        "lang_choose": "Choose interface language / Оберіть мову інтерфейсу / Выбери язык интерфейса:",
        "lang_changed": "Interface language changed to English. 🇬🇧",
        "btn_change_lang": "Change language EN/UA/RU",
    }
}


def get_text(lang: str, key: str, **kwargs) -> str:
    # Safely fallback to Russian if language or key not found
    lang_translations = LOCALES.get(lang, LOCALES["ru"])
    text = lang_translations.get(key, LOCALES["ru"].get(key, key))
    if kwargs:
        try:
            return text.format(**kwargs)
        except KeyError:
            return text
    return text
