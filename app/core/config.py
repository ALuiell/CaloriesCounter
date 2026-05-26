from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
DEFAULT_ENV_PATH = ROOT_DIR / ".env"


def _load_dotenv(path: Path) -> None:
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


@dataclass(frozen=True)
class Settings:
    bot_token: str
    app_timezone: str
    database_path: Path
    seed_path: Path


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    _load_dotenv(DEFAULT_ENV_PATH)

    bot_token = os.environ.get("BOT_TOKEN", "").strip()
    if not bot_token:
        raise RuntimeError("BOT_TOKEN is not configured. Set it in .env.")

    timezone_name = os.environ.get("APP_TIMEZONE", "Europe/Kiev").strip()
    database_raw = os.environ.get("DATABASE_PATH", "data/calories_counter.sqlite3").strip()
    database_path = Path(database_raw)
    if not database_path.is_absolute():
        database_path = ROOT_DIR / database_path

    seed_path = ROOT_DIR / "data" / "seeds" / "starter_products_usda_sr_legacy.json"
    return Settings(
        bot_token=bot_token,
        app_timezone=timezone_name,
        database_path=database_path,
        seed_path=seed_path,
    )
