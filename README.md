![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.2.10-092E20?logo=django&logoColor=white)
![Database](https://img.shields.io/badge/Database-SQLite-lightgrey?logo=sqlite&logoColor=white)
![Tool](https://img.shields.io/badge/Dependency%20Manager-uv-orange)

# SoftBox

SoftBox — анонимная платформа для создания и открытия сообщений по категориям.
Пользователь может:

* Создавать анонимные сообщения (box) раз в 24 часа
* Открывать случайное сообщение раз в 24 часа
* Просматривать созданные и открытые боксы в профиле
* Комментировать сообщения (на данный момент отключено)

## Основная логика

* Каждый box имеет:

  * уникальный `number`
  * категорию
  * текст
  * автора
* Пользователь может:

  * создать 1 сообщение в 24 часа
  * открыть 1 случайное сообщение в 24 часа
* При открытии:

  * нельзя открыть собственный box
  * нельзя открыть уже открытый ранее box
  * если подходящих нет — показывается модальное окно

---

# Технологии

* Python 3.11.12
* Django 5.2.10
* SQLite (по умолчанию)
* uv (менеджер зависимостей)

---

# Структура (в основном использованные)

core/
 ├── boxes/
 │    ├── models.py
 │    ├── views.py
 │    ├── urls.py
 ├── users/
 │    ├── models.py
 ├── core/
 │    ├── settings.py
 │    ├── urls.py
 ├── static/
 │    ├── css/
 │    ├── images/
 ├── templates/
 ├── manage.py
 └── db.sqlite3
.gitignore
pyproject.toml
README.md
uv.lock

---

# Как запустить проект локально

## 1. Клонировать репозиторий

```bash
git clone https://github.com/XEQU4/SoftBox.git
cd SoftBox
```

## 2. Создать виртуальное окружение через uv

```bash
uv venv
```

> Если у вас нету `uv`, установите его, следуя инструкциям на оффициальном сайте: https://docs.astral.sh/uv/getting-started/installation/#standalone-installer

Активировать:

Windows:

```bash
.venv\Scripts\activate
```

Linux / Mac:

```bash
source .venv/bin/activate
```

## 3. Установить зависимости

```bash
uv sync
```

---

## 4. Применить миграции

```bash
python manage.py migrate
```

---

## 5. Создать суперпользователя (опционально)

```bash
python manage.py createsuperuser
```

---

## 6. Запустить сервер

```bash
python manage.py runserver
```

Открыть в браузере:

```
http://127.0.0.1:8000/
```

---

# Ограничения MVP

* Используется SQLite
* Нет продакшн-настроек
* Нет системы жалоб/модерации
* Нет асинхронной обработки
* Плохая оптимизация и безопасность
* Не доработанное комментирование

---

# Для продакшена потребуется

* PostgreSQL
* Gunicorn / Uvicorn
* Nginx
* Настройка STATIC/MEDIA
* Переменные окружения
* DEBUG=False
* Улучшение безопасности и проверок
* Оптимизация

---

# Изначальные планы для первого продакшена

**Author:** [XEQU](https://github.com/XEQU4)

**Description:** [ObsidianNote](https://share.note.sx/27qecair#jOxa5qIVORk0Z++QYxax4EYEGMZXnUBvfOkLLPQxe7A)

**Figma:** [SoftBox](https://www.figma.com/design/oTitxHFeElXKEyxJ8ZFl9U/SoftBox?node-id=0-1&t=IuUPY4lhGpQTfsaK-1)

