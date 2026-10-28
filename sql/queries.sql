-- Учебные SQL-запросы к базе data/notifyhub.sqlite (ПР7).
-- Запросы разделены служебной строкой-разделителем и выполняются по одному.
-- В коде приложения те же запросы пишутся с параметрами "?".

-- 1. Все типы уведомлений
SELECT id, name
FROM notification_types;
-- ;;

-- 2. Все подписчики, отсортированные по имени
SELECT id, name, email
FROM subscribers
ORDER BY name;
-- ;;

-- 3. Поиск типов уведомлений по части названия (LIKE)
SELECT id, name
FROM notification_types
WHERE name LIKE '%скид%';
-- ;;

-- 4. Подписки по каналу email (WHERE)
SELECT id, subscriber_id, type_id, channel, end_date
FROM subscriptions
WHERE channel = 'email';
-- ;;

-- 5. Активные подписки со сроком не раньше выбранной даты (AND)
SELECT id, subscriber_id, type_id, end_date
FROM subscriptions
WHERE is_active = 1 AND end_date >= '2026-10-29'
ORDER BY end_date;
-- ;;

-- 6. Подписки, заканчивающиеся в заданном диапазоне дат (BETWEEN)
SELECT id, subscriber_id, type_id, end_date
FROM subscriptions
WHERE end_date BETWEEN '2026-01-01' AND '2026-12-31';
-- ;;

-- 7. Подписки с названием типа и именем подписчика (JOIN трёх таблиц)
SELECT
    subscriptions.id AS subscription_id,
    subscribers.name AS subscriber_name,
    notification_types.name AS type_name,
    subscriptions.channel,
    subscriptions.end_date
FROM subscriptions
JOIN subscribers ON subscriptions.subscriber_id = subscribers.id
JOIN notification_types ON subscriptions.type_id = notification_types.id
ORDER BY subscriptions.id;
-- ;;

-- 8. Типы, на которые подписчик 1 ещё не подписан (подзапрос NOT IN)
SELECT id, name
FROM notification_types
WHERE id NOT IN (
    SELECT type_id
    FROM subscriptions
    WHERE subscriber_id = 1 AND is_active = 1 AND end_date >= '2026-10-29'
);
-- ;;

-- 9. Общее количество подписок (COUNT)
SELECT COUNT(*) AS total_subscriptions
FROM subscriptions;
-- ;;

-- 10. Ближайшая и самая поздняя дата окончания (MIN / MAX)
SELECT MIN(end_date) AS first_end, MAX(end_date) AS last_end
FROM subscriptions;
-- ;;

-- 11. Количество подписок по каналам (GROUP BY)
SELECT channel, COUNT(*) AS total
FROM subscriptions
GROUP BY channel
ORDER BY total DESC;
-- ;;

-- 12. Количество подписок по каждому типу, включая типы без подписок
--     (LEFT JOIN + GROUP BY)
SELECT notification_types.name, COUNT(subscriptions.id) AS total
FROM notification_types
LEFT JOIN subscriptions ON subscriptions.type_id = notification_types.id
GROUP BY notification_types.id, notification_types.name
ORDER BY total DESC, notification_types.name;
-- ;;

-- 13. Типы, у которых больше одной подписки (HAVING)
SELECT notification_types.name, COUNT(subscriptions.id) AS total
FROM notification_types
JOIN subscriptions ON subscriptions.type_id = notification_types.id
GROUP BY notification_types.id, notification_types.name
HAVING COUNT(subscriptions.id) > 1;
-- ;;

-- 14. Подписчики, у которых нет ни одной подписки (LEFT JOIN + IS NULL)
SELECT subscribers.id, subscribers.name
FROM subscribers
LEFT JOIN subscriptions ON subscriptions.subscriber_id = subscribers.id
WHERE subscriptions.id IS NULL;
-- ;;

-- 15. Постраничный вывод подписок: вторая страница по 2 записи (LIMIT / OFFSET)
SELECT id, subscriber_id, type_id, channel
FROM subscriptions
ORDER BY id
LIMIT 2 OFFSET 2;
