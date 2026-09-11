-- =============================================================================
-- OTT PRODUCT & USER ANALYTICS: DEVICE ANALYSIS
-- =============================================================================
-- Database: ott_analytics.db
-- Objective: Evaluate platform usage patterns across Mobile, Web, Smart TV, and Tablet.
-- =============================================================================

-- Query 1: Device Performance Overview
-- Compares volume of views, average session watch duration, and completion rates by device.
SELECT 
    device,
    COUNT(event_id) AS total_views,
    ROUND(COUNT(event_id) * 100.0 / (SELECT COUNT(*) FROM events), 2) AS view_share_pct,
    SUM(watch_duration) AS total_watch_minutes,
    ROUND(AVG(watch_duration), 2) AS avg_watch_duration_minutes,
    SUM(completed) AS completed_views,
    ROUND(SUM(completed) * 100.0 / COUNT(event_id), 2) AS completion_rate_pct
FROM events
GROUP BY device
ORDER BY total_views DESC;


-- Query 2: Device Usage by Subscription Plan
-- Checks whether Premium/VIP users prefer Smart TV while Free users stream predominantly on Mobile.
SELECT 
    u.subscription_plan,
    e.device,
    COUNT(e.event_id) AS total_views,
    ROUND(AVG(e.watch_duration), 2) AS avg_watch_duration_minutes
FROM events e
INNER JOIN users u 
    ON e.user_id = u.user_id
GROUP BY u.subscription_plan, e.device
ORDER BY u.subscription_plan, total_views DESC;


-- Query 3: Top Genres Streamed on Smart TV vs Mobile
-- Demonstrates device-specific content consumption habits.
SELECT 
    e.device,
    c.genre,
    COUNT(e.event_id) AS total_views,
    ROUND(AVG(e.watch_duration), 2) AS avg_watch_duration_minutes
FROM events e
INNER JOIN content c 
    ON e.content_id = c.content_id
WHERE e.device IN ('Smart TV', 'Mobile')
GROUP BY e.device, c.genre
ORDER BY e.device, total_views DESC;
