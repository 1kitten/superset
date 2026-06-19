# Задание: кастомизация production-образа Apache Superset 6.1.0

Склонировать официальный репозиторий Apache Superset и создать отдельные Pull Request
с изменениями на базе ветки `6.1.0`.

## Требования

1. Собрать production Docker-образ Superset `6.1.0` из исходников.
2. Доустановить в образ Python-пакет `clickhouse-connect`.
3. Убрать надпись "Powered by Apache Superset" из меню (Settings → About).
4. Заменить favicon на любой другой.
5. Заменить логотип Superset на любой другой.
6. Настроить один dashboard как стартовую страницу вместо дефолтной `/superset/welcome/`.
   Стартовая страница должна открываться корректно для обычных пользователей, не только Admin:
   * нет некорректного редиректа `302`;
   * пользователь без роли Admin попадает на нужный dashboard;
   * dashboard доступен после логина.
7. Убрать префикс `/superset/` из всех URL
   (`domain/superset/dashboard/1 → domain/dashboard/1`, `domain/superset/welcome → domain/welcome`).

## Ожидаемый результат

Отдельные PR для каждой задачи, влитые в `main`, + `docker-compose.yml` (имитация
production) и `README.md`.

## README.md должен содержать

1. как собрать Docker-образ;
2. как запустить Superset;
3. что ещё стоит изменить для Production.
