# Architecture

## Базовый подход

Для MVP лучше выбрать простую модульную архитектуру:

- `bot` - Telegram handlers и сценарии;
- `services` - бизнес-логика;
- `repositories` - работа с БД;
- `models` - ORM-модели;
- `schemas` - входные и выходные структуры;
- `parsers` - разбор текстовых сообщений;
- `utils` - вспомогательные функции.

## Предлагаемая структура

```text
CaloriesCounter/
  app/
    bot/
      handlers/
      keyboards/
      middlewares/
    core/
      config.py
      logging.py
    db/
      models/
      repositories/
      migrations/
    services/
      profile_service.py
      nutrition_service.py
      diary_service.py
    parsers/
      food_parser.py
    schemas/
      user.py
      food_entry.py
      nutrition.py
    main.py
  docs/
  tests/
```

## Основные модули

### Profile Service

Отвечает за:

- создание профиля;
- обновление анкеты;
- расчет дневной цели.

### Nutrition Service

Отвечает за:

- поиск продуктов;
- расчет калорий и БЖУ;
- суммирование результатов.

### Diary Service

Отвечает за:

- сохранение записей;
- получение итогов за день;
- редактирование и удаление записей.

### Food Parser

Отвечает за:

- разбиение сообщения на строки;
- выделение продукта и веса;
- нормализацию текста;
- возврат структурированных данных.

## Почему такой подход хорош

- легко тестировать по модулям;
- удобно менять БД;
- проще расширять функциональность;
- Telegram-часть не смешивается с расчетами и парсингом.
