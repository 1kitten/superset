"""Кастомная конфигурация Superset для production-образа.

Секции добавляются отдельными PR:
  * PR #2 — favicon
"""

import os


def env(key: str, default: str | None = None) -> str | None:
    return os.environ.get(key, default)


# ---------------------------------------------------------------------------
# PR #2 — Favicon
# favicon.svg кладётся в /app/superset/static/assets/images/ на этапе сборки.
# ---------------------------------------------------------------------------
FAVICONS = [{"href": "/static/assets/images/favicon.svg"}]

# ---------------------------------------------------------------------------
# PR #3 — Логотип
# logo.svg кладётся в /app/superset/static/assets/images/ на этапе сборки.
# Имя файла НЕ содержит "superset-logo-horiz" — благодаря этому Superset
# автоматически скрывает watermark "Powered by Apache Superset" (см. PR #4).
# ---------------------------------------------------------------------------
APP_NAME = env("APP_NAME", "Analytics")
APP_ICON = "/static/assets/images/logo.svg"
APP_ICON_WIDTH = 130
LOGO_TOOLTIP = APP_NAME

# ID стартового dashboard (используется логотипом и landing-редиректом, PR #5).
DEFAULT_DASHBOARD_ID = env("SUPERSET_DEFAULT_DASHBOARD_ID", "1")

# Клик по логотипу ведёт на стартовый dashboard (чистый URL, nginx переписывает).
LOGO_TARGET_PATH = f"/dashboard/{DEFAULT_DASHBOARD_ID}/"
