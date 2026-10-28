"""SQL-запросы веб-интерфейса.

Значения всегда передаются отдельным кортежем/списком и подставляются в
запрос через "?", поэтому SQL-инъекция невозможна.
"""

from datetime import date

CHANNELS = ("email", "push", "sms")

_SUBSCRIPTIONS_SELECT = """
    SELECT
        subscriptions.id,
        subscriptions.channel,
        subscriptions.end_date,
        subscriptions.is_active,
        subscriptions.end_date < ? AS is_expired,
        subscribers.name AS subscriber_name,
        subscribers.email AS subscriber_email,
        notification_types.name AS type_name
    FROM subscriptions
    JOIN subscribers ON subscriptions.subscriber_id = subscribers.id
    JOIN notification_types ON subscriptions.type_id = notification_types.id
"""


def _subscription_to_dict(row):
    """Строка БД -> словарь; end_date становится объектом date."""
    subscription = dict(row)
    subscription["end_date"] = date.fromisoformat(subscription["end_date"])
    return subscription


def get_notification_types(conn):
    return conn.execute(
        "SELECT id, name FROM notification_types ORDER BY id"
    ).fetchall()


def get_notification_type(conn, type_id):
    return conn.execute(
        "SELECT id, name FROM notification_types WHERE id = ?",
        (type_id,),
    ).fetchone()


def count_active_subscriptions(conn, type_id, today):
    row = conn.execute(
        """
        SELECT COUNT(*)
        FROM subscriptions
        WHERE type_id = ? AND is_active = 1 AND end_date >= ?
        """,
        (type_id, today.isoformat()),
    ).fetchone()
    return row[0]


def get_subscribers(conn):
    return conn.execute(
        "SELECT id, name, email FROM subscribers ORDER BY name"
    ).fetchall()


def get_subscriber(conn, subscriber_id):
    return conn.execute(
        "SELECT id, name, email FROM subscribers WHERE id = ?",
        (subscriber_id,),
    ).fetchone()


def get_subscriptions(conn, today, channel=None):
    """Все подписки; при заданном channel - только по этому каналу."""
    query = _SUBSCRIPTIONS_SELECT
    params = [today.isoformat()]
    if channel is not None:
        query += " WHERE subscriptions.channel = ?"
        params.append(channel)
    query += " ORDER BY subscriptions.id"
    rows = conn.execute(query, params).fetchall()
    return [_subscription_to_dict(row) for row in rows]


def get_subscription(conn, subscription_id, today):
    row = conn.execute(
        _SUBSCRIPTIONS_SELECT + " WHERE subscriptions.id = ?",
        (today.isoformat(), subscription_id),
    ).fetchone()
    if row is None:
        return None
    return _subscription_to_dict(row)


def get_available_types(conn, subscriber_id, on_date):
    """Типы, на которые у подписчика нет действующей подписки на дату."""
    return conn.execute(
        """
        SELECT id, name
        FROM notification_types
        WHERE id NOT IN (
            SELECT type_id
            FROM subscriptions
            WHERE subscriber_id = ? AND is_active = 1 AND end_date >= ?
        )
        ORDER BY id
        """,
        (subscriber_id, on_date.isoformat()),
    ).fetchall()


def count_rows(conn):
    """Количество записей в каждой таблице (для главной страницы)."""
    return {
        table: conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        for table in ("notification_types", "subscribers", "subscriptions")
    }


def get_type_statistics(conn):
    """Подписок на каждый тип, включая типы без подписок."""
    return conn.execute(
        """
        SELECT notification_types.name, COUNT(subscriptions.id) AS total
        FROM notification_types
        LEFT JOIN subscriptions
            ON subscriptions.type_id = notification_types.id
        GROUP BY notification_types.id, notification_types.name
        ORDER BY total DESC, notification_types.name
        """
    ).fetchall()


def get_channel_statistics(conn):
    return conn.execute(
        """
        SELECT channel, COUNT(*) AS total
        FROM subscriptions
        GROUP BY channel
        ORDER BY total DESC, channel
        """
    ).fetchall()


def get_popular_types(conn):
    """Типы, у которых больше одной подписки (HAVING)."""
    return conn.execute(
        """
        SELECT notification_types.name, COUNT(subscriptions.id) AS total
        FROM notification_types
        JOIN subscriptions ON subscriptions.type_id = notification_types.id
        GROUP BY notification_types.id, notification_types.name
        HAVING COUNT(subscriptions.id) > 1
        ORDER BY total DESC, notification_types.name
        """
    ).fetchall()
