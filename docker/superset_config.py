"""Кастомная конфигурация Superset для production-образа.

Секции добавляются отдельными PR:
  * PR #2 — favicon
  * PR #3 — логотип
  * PR #5 — стартовый dashboard как landing page
"""

import os

from flask import redirect, request


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


# ---------------------------------------------------------------------------
# PR #5 — Стартовый dashboard как landing page для ВСЕХ ролей.
#
# before_request-хук: аутентифицированного пользователя, попавшего на корень
# или welcome, отправляем на нужный dashboard.
#
# Почему так:
#   * срабатывает ТОЛЬКО для аутентифицированных (current_user.is_authenticated),
#     поэтому неавторизованный спокойно доходит до /login/ — нет петли 302;
#   * не зависит от роли — работает и для не-Admin;
#   * dashboard рендерится штатной вьюхой => права проверяются штатно
#     (dashboard должен быть published и выдан роли пользователя — см. README).
# ---------------------------------------------------------------------------
def FLASK_APP_MUTATOR(app):  # noqa: N802 (имя фиксировано Superset'ом)
    from flask_login import current_user

    # Flask видит пути с префиксом /superset/ (nginx переписывает /welcome).
    LANDING_PATHS = {
        "/",
        "/superset/welcome",
        "/superset/welcome/",
        "/welcome",
        "/welcome/",
    }

    @app.before_request
    def _redirect_to_default_dashboard():
        if request.path not in LANDING_PATHS:
            return None
        if not getattr(current_user, "is_authenticated", False):
            return None  # неавторизованный идёт на /login/ — лишнего 302 нет
        return redirect(f"/dashboard/{DEFAULT_DASHBOARD_ID}/")


# ---------------------------------------------------------------------------
# Feature flags
# DASHBOARD_RBAC — точечная выдача дашбордов ролям (нужно для доступа не-Admin).
# ---------------------------------------------------------------------------
FEATURE_FLAGS = {
    "DASHBOARD_RBAC": True,
    "ALERT_REPORTS": True,
    "DRILL_TO_DETAIL": True,
}
