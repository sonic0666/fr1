# Сервис управления подписками на уведомления (NotifyHub)

## Назначение
Приложение позволяет пользователям управлять подписками на различные типы
уведомлений (email, push, SMS) и отслеживать статус каждой подписки
(активна, приостановлена, истекла). Консольная версия приложения (ПР3)
дополнена веб-интерфейсом на Django: страницы формируются шаблонами Django
(ПР5–ПР6), а данные хранятся в базе SQLite (ПР7).

Приложение позволяет:
- просматривать типы уведомлений в браузере;
- просматривать информацию о конкретном типе уведомлений и количестве
  активных подписок на него;
- просматривать список подписок в браузере (с фильтром по каналу);
- просматривать информацию о конкретной подписке и её статус;
- (консольная версия) добавлять и искать подписчиков и типы уведомлений,
  оформлять и отменять подписки, формировать текст уведомления,
  сортировать типы уведомлений;
- узнать, на какие типы уведомлений подписчик ещё не подписан на выбранную дату;
- смотреть статистику подписок (по типам, по каналам, популярные типы);
- хранить данные между запусками приложения.

## Используемые технологии
- Python 3;
- Django 5.2 – веб-фреймворк;
- Django Template Language (DTL) – шаблоны страниц;
- HTML5, CSS3, JavaScript;
- Bootstrap 5.3 – базовая вёрстка (CDN);
- SQLite и язык SQL (модуль `sqlite3`) – хранение данных;
- JSON – исходные данные консольной версии и источник импорта в БД;
- Git, pytest, flake8.

## Целевая аудитория
- пользователи веб- и мобильных сервисов, желающие гибко настраивать,
  какие уведомления и по каким каналам они получают;
- администраторы сервисов-интеграторов, которым нужно управлять рассылками
  и контролировать статус подписок пользователей.

## Предметная область
Управление подписками пользователей на уведомления: выбор канала доставки
(email, push, SMS), выбор типа уведомлений (новости, акции, системные
оповещения), контроль срока действия подписки и её текущего статуса.

Подписчик может оформить подписку на тип уведомлений по определённому
каналу на заданный срок. На один и тот же тип и канал нельзя иметь две
активные подписки одновременно. Приостановленная подписка не удаляется из
истории и не блокирует повторное оформление.

## Основные сущности
Предметная область представлена тремя классами пакета `models/` (ПР3).

### NotificationType — тип уведомлений
Атрибуты: `id`, `name`. Метод: `__str__()`.

### Subscriber — подписчик
Атрибуты: `id`, `name`, `email`.
Методы: `validate_email()` (`@staticmethod`), `from_data()`
(`@classmethod`), `__str__()`.

### Subscription — подписка
Связывает объекты `Subscriber` и `NotificationType` через канал доставки.
Атрибуты: `id`, `subscriber`, `notification_type`, `channel`, `end_date`,
`is_active`.
Методы и свойства:
- `cancel()` — приостанавливает подписку (объект остаётся в истории);
- `is_expired` (`@property`) — истёк ли срок на сегодняшнюю дату;
- `days_until_renewal(current_date)` — количество дней до окончания;
- `get_status(current_date)` — статус подписки (через функцию
  `check_subscription_status()`, созданную в ПР1);
- `format_notification(current_date)` — текст уведомления для подписчика;
- `__str__()` — строковое представление с учётом статуса.

## Веб-интерфейс

### Страницы и маршруты

| URL | Имя маршрута | Страница | View-функция |
|---|---|---|---|
| `/` | `homepage:index` | главная | `index()` |
| `/types/` | `notification_types:list` | список типов уведомлений | `notification_types()` |
| `/types/<int:type_id>/` | `notification_types:detail` | страница типа | `notification_type_detail()` |
| `/subscriptions/` | `subscriptions:list` | список подписок | `subscriptions()` |
| `/subscriptions/<int:subscription_id>/` | `subscriptions:detail` | страница подписки | `subscription_detail()` |
| `/types/available/` | `notification_types:available` | доступные подписчику типы | `available_types()` |
| `/subscriptions/statistics/` | `subscriptions:statistics` | статистика | `statistics()` |

Если тип уведомлений или подписка не найдены, страница возвращает код 404
(`status=404` в `render()`). Для любого несуществующего адреса в корневом
`urls.py` подключён обработчик `handler404 = "homepage.views.page_not_found"`,
который показывает шаблон `templates/404.html`.

### Шаблоны Django (ПР6)
HTML в Python-коде больше не формируется: view-функция загружает данные,
готовит словарь контекста и вызывает
`render(request, "имя_шаблона.html", context)`. Функция `page()` из ПР5
удалена.

- **Базовый шаблон** `templates/base.html` — общая структура страницы:
  `<head>`, подключение Bootstrap и собственного CSS, шапка с логотипом и
  навигацией, контейнер, подвал, JavaScript. Содержит блоки
  `{% block title %}` и `{% block content %}`.
- **Наследование**: дочерние шаблоны начинаются с
  `{% extends "base.html" %}` и переопределяют блоки.
- **Включаемые шаблоны** (`{% include %}`): навигация
  `templates/includes/navigation.html`, карточка типа
  `notification_types/includes/type_card.html`, статус подписки
  `subscriptions/includes/subscription_status.html`.
- **Контекст**: например `{"notification_types": types_list}` во view,
  `{% for notification_type in notification_types %}` в шаблоне.
- **Циклы и условия**: `{% for %}` / `{% empty %}` для списков,
  `{% if %}` — для отсутствующего объекта и статуса подписки
  (приостановлена / истекла / активна).
- **Именованные URL и пространства имён**: `app_name` в `urls.py`
  приложений, ссылки через `{% url 'notification_types:detail' id %}`,
  жёстко заданных адресов в шаблонах нет.
- **Фильтры**: `|length` (количество типов), `|default:"Без названия"`
  (имя типа), `|date:"d.m.Y"` (срок подписки).
- **Статические файлы** (`homepage/static/homepage/`): `css/style.css`
  (собственные стили), `js/main.js` (текущий год в подвале),
  `img/logo.png` (логотип); подключаются через `{% load static %}` и
  `{% static %}`.

Шаблоны приложений лежат в `<приложение>/templates/<приложение>/`,
общие — в `templates/` (настроено в `TEMPLATES["DIRS"]`).

## Основные операции

### Используется в веб-интерфейсе
- просмотр списка типов уведомлений и страницы типа;
- просмотр списка подписок и страницы подписки со статусом.

### Отложено до следующих работ
Эти операции реализованы в консольной версии (ПР2–ПР3) и появятся в вебе,
когда будут добавлены формы и POST-запросы:
- добавление подписчика и типа уведомлений;
- поиск и сортировка;
- оформление и приостановка подписки;
- формирование текста уведомления.

## База данных SQLite (ПР7)

Веб-интерфейс читает данные из файла `data/notifyhub.sqlite` через
стандартный модуль `sqlite3`. Django ORM пока не используется.

### Таблицы и ключи
| Таблица | Поля |
|---|---|
| `notification_types` | `id` (PRIMARY KEY), `name` (NOT NULL) |
| `subscribers` | `id` (PRIMARY KEY), `name` (NOT NULL), `email` (NOT NULL) |
| `subscriptions` | `id` (PRIMARY KEY), `subscriber_id` (FOREIGN KEY -> `subscribers.id`), `type_id` (FOREIGN KEY -> `notification_types.id`), `channel` (CHECK: email / push / sms), `end_date` (дата в формате ГГГГ-ММ-ДД), `is_active` (0 или 1, по умолчанию 1) |

Связи: один подписчик - много подписок, один тип - много подписок
(`subscriptions` связывает две другие таблицы). Внешние ключи включаются
командой `PRAGMA foreign_keys = ON` при каждом подключении
(`db/database.py`), поэтому запись с несуществующим `subscriber_id` или
`type_id` отклоняется.

### Создание и заполнение базы
```text
python -c "import sqlite3; c = sqlite3.connect('data/notifyhub.sqlite'); c.executescript(open('sql/schema.sql', encoding='utf-8').read()); c.close()"
python -m db.import_json
```
Первая команда создаёт таблицы по `sql/schema.sql`, вторая переносит данные
из JSON-файлов (`data/notification_types.json`, `data/subscribers.json`,
`data/subscriptions.json`) в таблицы. Импорт идёт в порядке «сначала
родительские таблицы» и выполняется в одной транзакции: при ошибке
выполняется `rollback`.

### SQL-запросы
- `sql/queries.sql` - 15 учебных запросов: выборка, `WHERE`, `LIKE`,
  `BETWEEN`, `ORDER BY`, `JOIN` трёх таблиц, подзапрос `NOT IN`, `COUNT`,
  `MIN`/`MAX`, `GROUP BY`, `LEFT JOIN`, `HAVING`, `LIMIT`/`OFFSET`;
- `db/queries.py` - те же запросы для веб-интерфейса. Значения всегда
  передаются параметрами (`?`), а не вставляются в строку, поэтому
  SQL-инъекция невозможна.

Открыть базу вручную:
```text
python -m sqlite3 data/notifyhub.sqlite
```

## Хранение данных
- **Веб-интерфейс** - SQLite-файл `data/notifyhub.sqlite`;
- **консольная версия** (`main.py`) - JSON-файлы в `data/`;
  при загрузке (`storage.py`) данные преобразуются в объекты
  `NotificationType`, `Subscriber` и `Subscription`.

## Структура проекта
```text
fr1/
├── README.md
├── requirements.txt
├── setup.cfg
├── pytest.ini
├── manage.py
├── main.py
├── storage.py
├── utils.py
│
├── db/
│   ├── database.py             (подключение к SQLite)
│   ├── import_json.py          (импорт JSON -> SQLite)
│   └── queries.py              (SQL-запросы веб-интерфейса)
├── sql/
│   ├── schema.sql              (создание таблиц)
│   └── queries.sql             (учебные запросы)
│
├── notifyhub/                  (настройки Django-проекта)
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── templates/
│   ├── base.html
│   ├── 404.html
│   └── includes/
│       └── navigation.html
│
├── homepage/
│   ├── static/homepage/
│   │   ├── css/style.css
│   │   ├── js/main.js
│   │   └── img/logo.png
│   ├── templates/homepage/index.html
│   ├── urls.py
│   └── views.py
│
├── notification_types/
│   ├── templates/notification_types/
│   │   ├── type_list.html
│   │   ├── type_detail.html
│   │   └── includes/type_card.html
│   ├── urls.py
│   └── views.py
│
├── subscriptions/
│   ├── templates/subscriptions/
│   │   ├── subscription_list.html
│   │   ├── subscription_detail.html
│   │   └── includes/subscription_status.html
│   ├── urls.py
│   └── views.py
│
├── models/                     (классы предметной области, ПР3)
├── data/                       (JSON-файлы и notifyhub.sqlite)
└── tests/                      (pytest)
```
В каждом Django-приложении также есть служебные файлы `startapp`
(`admin.py`, `apps.py`, `models.py`, `tests.py`, `migrations/`); Django-модели
появятся на следующих практических работах.

## Назначение модулей
- `main.py` — консольная версия приложения (сохранена с ПР3);
- `notifyhub/` — настройки проекта (`settings.py`), маршрутизация верхнего
  уровня и `handler404` (`urls.py`), точки входа серверов;
- `homepage/` — главная страница и обработчик 404, статические файлы сайта;
- `notification_types/`, `subscriptions/` — страницы типов уведомлений и
  подписок (view-функции, маршруты, шаблоны);
- `models/` — классы предметной области и функции работы с ними;
- `storage.py` — преобразование JSON <-> объекты Python (консольная версия);
- `db/` — подключение к SQLite, импорт из JSON, SQL-запросы;
- `sql/` — схема базы данных и учебные запросы;
- `tests/` — автоматизированные тесты (классы ПР3, маршруты, шаблоны и
  статика веб-интерфейса).

## Запуск приложения
```text
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
После запуска открыть в браузере `http://127.0.0.1:8000/`.
Консольная версия: `python main.py`.

## Тестирование и качество кода
```text
python manage.py check
pytest -v
flake8 .
```

## Git
Исходный код хранится в Git-репозитории. Каждый коммит практической работы
начинается с метки (`PR5:`, `PR6:` и т. д.).

## Текущее состояние и план развития
Реализовано:
- консольное приложение с объектной моделью (ПР1–ПР3);
- Django-проект и три приложения, маршрутизация, обработка 404 (ПР5);
- шаблонная архитектура: базовый шаблон, наследование, include, контекст,
  циклы и условия, фильтры, именованные URL с пространствами имён, статические
  файлы, собственные CSS и JavaScript (ПР6);
- база данных SQLite: схема с первичными и внешними ключами, импорт из JSON,
  SQL-запросы с JOIN, GROUP BY, HAVING, подзапросами, параметризованные
  запросы в веб-интерфейсе, страницы «Доступные типы» и «Статистика» (ПР7).

Планируется:
- Django ORM: перенос сущностей в модели Django;
- формы создания и изменения подписок;
- разработка API;
- контейнеризация приложения;
- настройка CI/CD.
