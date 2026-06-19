# Разбивка на Pull Request'ы

Каждая задача — отдельный PR на базе `6.1.0`, влитый в `main`.

| PR | Задача | Файлы | Решение |
|----|--------|-------|---------|
| [#1](https://github.com/1kitten/superset/pull/1) | `clickhouse-connect` | `docker/requirements-local.txt`, `Dockerfile.custom` | `pip install` поверх официального образа |
| [#2](https://github.com/1kitten/superset/pull/2) | favicon | `assets/favicon.svg`, `docker/superset_config.py`, `Dockerfile.custom` | `FAVICONS` + копирование ассета |
| [#3](https://github.com/1kitten/superset/pull/3) | логотип | `assets/logo.svg`, `docker/superset_config.py`, `Dockerfile.custom` | `APP_ICON`/`LOGO_TARGET_PATH` |
| [#4](https://github.com/1kitten/superset/pull/4) | «Powered by Apache Superset» | `Dockerfile.custom` | force `show_watermark=False` в `views/base.py` |
| [#5](https://github.com/1kitten/superset/pull/5) | стартовый dashboard | `docker/superset_config.py` | `FLASK_APP_MUTATOR` + `before_request` |
| [#6](https://github.com/1kitten/superset/pull/6) | URL без `/superset/` | `docker/nginx/superset.conf` | reverse-proxy rewrite + sub_filter |
| [#7](https://github.com/1kitten/superset/pull/7) | README + compose | `README.md`, `docker-compose.yml`, `.env.example`, базовый `superset_config.py` | инфраструктура запуска |

Порядок мёржа: `#1 → #2 → … → #7`. Каждая ветка резалась от актуального `main`
после мёржа предыдущего PR — поэтому конфликтов по общим файлам
(`Dockerfile.custom`, `superset_config.py`) нет.
