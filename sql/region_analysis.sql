-- =============================================================================
-- OTT PRODUCT & USER ANALYTICS: REGION ANALYSIS
-- =============================================================================
-- Database: ott_analytics.db
-- Objective: Analyze geographic viewing distribution across Indian metropolitan and regional markets.
-- =============================================================================

-- Query 1: Viewing Metrics by City
-- Computes total views, total watch time, unique active viewers, and average watch time per session.
SELECT 
    u.city,
    u.state,
    COUNT(DISTINCT u.user_id) AS unique_active_users,
    COUNT(e.event_id) AS total_views,
    SUM(e.watch_duration) AS total_watch_minutes,
    ROUND(AVG(e.watch_duration), 2) AS avg_watch_duration_minutes
FROM users u
INNER JOIN events e 
    ON u.user_id = e.user_id
GROUP BY u.city, u.state
ORDER BY total_views DESC;


-- Query 2: Top Active States by Watch Duration
-- Aggregates state-level consumption to highlight core regional markets.
SELECT 
    u.state,
    COUNT(DISTINCT u.user_id) AS total_users,
    COUNT(e.event_id) AS total_views,
    SUM(e.watch_duration) AS total_watch_minutes,
    ROUND(AVG(e.watch_duration), 2) AS avg_watch_duration_minutes
FROM users u
INNER JOIN events e 
    ON u.user_id = e.user_id
GROUP BY u.state
ORDER BY total_watch_minutes DESC;


-- Query 3: Regional Language Alignment
-- Checks how regional cities consume regional vs Hindi/English language content.
SELECT 
    u.city,
    c.language,
    COUNT(e.event_id) AS views_count
FROM users u
INNER JOIN events e 
    ON u.user_id = e.user_id
INNER JOIN content c 
    ON e.content_id = c.content_id
GROUP BY u.city, c.language
ORDER BY u.city, views_count DESC;
