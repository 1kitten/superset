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
