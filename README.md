# Apache Superset 6.1.0 — кастомный production-образ

Кастомизация официального Superset `6.1.0`: доустановка `clickhouse-connect`, своя
айдентика (логотип + favicon, без «Powered by Apache Superset»), стартовый dashboard
для всех ролей и чистые URL без префикса `/superset/`.

Тестовое задание — в [`TASK.md`](./TASK.md). Разбивка на PR — в [`PRS.md`](./PRS.md).
Оригинальные файлы Superset сохранены как `README.upstream.md` и `docker-compose.upstream.yml`.

## Что и где сделано

| Задача | PR | Реализация |
|--------|----|-----------|
| Установка `clickhouse-connect` | [#1](https://github.com/1kitten/superset/pull/1) | `docker/requirements-local.txt` + `Dockerfile.custom` |
| Замена favicon | [#2](https://github.com/1kitten/superset/pull/2) | `assets/favicon.svg` + `FAVICONS` |
| Замена логотипа | [#3](https://github.com/1kitten/superset/pull/3) | `assets/logo.svg` + `APP_ICON` |
| Убрать «Powered by Apache Superset» | [#4](https://github.com/1kitten/superset/pull/4) | force `show_watermark=False` (sed в `Dockerfile.custom`) |
| Стартовый dashboard для всех ролей | [#5](https://github.com/1kitten/superset/pull/5) | `FLASK_APP_MUTATOR` (before_request) |
| URL без `/superset/` | [#6](https://github.com/1kitten/superset/pull/6) | reverse-proxy `docker/nginx/superset.conf` |
| README + compose | [#7](https://github.com/1kitten/superset/pull/7) | этот файл + `docker-compose.yml` |

## Ключевые файлы

```
Dockerfile.custom              # образ на базе apache/superset:6.1.0
docker-compose.yml             # nginx + gunicorn + worker + postgres + redis
.env.example                   # переменные окружения
assets/{logo.svg, favicon.svg} # айдентика
docker/superset_config.py      # конфиг: infra + favicon/logo + landing dashboard
docker/nginx/superset.conf     # снятие префикса /superset/
```

---

## 1. Как собрать Docker-образ

```bash
docker build -f Dockerfile.custom -t custom-superset:6.1.0 .
```

Образ на базе `apache/superset:6.1.0`:
- `pip install` для `clickhouse-connect` (PR #1);
- копирование `favicon.svg` и `logo.svg` (PR #2, #3);
- `sed`, форсящий `show_watermark=False` (PR #4).

Пересборка фронтенда не нужна: watermark убирается бэкенд-флагом, favicon/логотип —
через конфиг.

---

## 2. Как запустить Superset

```bash
cp .env.example .env
#  -> задайте SUPERSET_SECRET_KEY:  openssl rand -base64 42
#  -> при желании SUPERSET_LOAD_EXAMPLES=yes (демо-дашборды для проверки)

docker compose up -d --build
docker compose logs -f superset-init    # дождаться "Init Step 3/3 Complete"
```

UI: **http://localhost/** (через nginx). Логин по умолчанию `admin / admin`.

### Назначить стартовый dashboard (PR #5)

1. Создайте/откройте dashboard — ID виден в адресе `/dashboard/<ID>/`.
2. Опубликуйте его (**Publish**) и выдайте нужным ролям
   (**Edit dashboard → свойства → Roles**, включён `DASHBOARD_RBAC`).
3. Пропишите `SUPERSET_DEFAULT_DASHBOARD_ID=<ID>` в `.env` и `docker compose up -d`.

### Проверки требований

| Что | Как |
|-----|-----|
| Нет некорректного 302 | Неавторизованный заход на `/` → один редирект на `/login/`, без петли (хук срабатывает только для `is_authenticated`). |
| Не-Admin попадает на dashboard | Gamma-пользователь с выданным dashboard после логина видит его. |
| Dashboard доступен после логина | `curl -IL` для залогиненного: `/` → `302 /dashboard/<id>/` → `200`. |
| Чистые URL | `curl -I http://localhost/dashboard/1` → 200; `http://localhost/superset/dashboard/1/` тоже 200. |

---

## 3. Что ещё стоит изменить для Production

**URL без `/superset/` — довести «по-честному».** Текущее nginx-решение (rewrite запросов +
`sub_filter` ссылок в HTML) рабочее и не трогает ядро, но часть ссылок генерится в
JS-бандле и остаётся с префиксом (работают через passthrough). Каноничный путь —
изменить `route_base`/`url_for` в самом Superset и пересобрать фронтенд; это отдельный
инвазивный PR, который стоит согласовать с апстримом.

**Секреты.** `SECRET_KEY`, пароли БД, логин админа — из secret-стора (Vault / Docker
secrets / CI), не из `.env` в репозитории. Принудительный HTTPS (`PREFERRED_URL_SCHEME=https`,
Talisman/HSTS), смена дефолтного `admin/admin`, ротация ключей.

**Хранилища и HA.** Managed Postgres (реплики, бэкапы, PITR) и Redis с persistence/HA
вместо контейнеров. Для ClickHouse-аналитики — отдельный пул и таймауты.

**Масштабирование.** Несколько реплик `superset` за балансировщиком, пул Celery worker'ов
+ `celery beat` для alerts & reports, автоскейл; тюнинг gunicorn под CPU.

**Аутентификация.** SSO через OAuth2/OIDC/LDAP (`CUSTOM_SECURITY_MANAGER`), маппинг групп
на роли, отключение саморегистрации, ограничение `PUBLIC_ROLE`.

**Наблюдаемость.** Логи в stdout → Loki/ELK, метрики (StatsD/Prometheus), Sentry,
healthchecks (уже заведены в compose).

**Сборка/поставка.** Pin npm и базового образа по digest, multi-arch, скан уязвимостей
(Trivy), приватный registry, теги по версии + git sha.
