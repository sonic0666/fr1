-- ==========================================
-- NotifyHub: структура базы данных
-- ==========================================

CREATE TABLE IF NOT EXISTS notification_types (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS subscribers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS subscriptions (
    id INTEGER PRIMARY KEY,
    subscriber_id INTEGER NOT NULL,
    type_id INTEGER NOT NULL,
    channel TEXT NOT NULL CHECK (channel IN ('email', 'push', 'sms')),
    end_date TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
    FOREIGN KEY (subscriber_id) REFERENCES subscribers(id),
    FOREIGN KEY (type_id) REFERENCES notification_types(id)
);
