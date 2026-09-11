-- =============================================================================
-- OTT PRODUCT & USER ANALYTICS: USER ANALYSIS
-- =============================================================================
-- Database: ott_analytics.db
-- Objective: Understand user base demographics, subscription tiers, and engagement.
-- =============================================================================

-- Query 1: Find Total Number of Registered Users
-- Explains how big our total user base is.
SELECT 
    COUNT(user_id) AS total_users
FROM users;


-- Query 2: Find Number of Users by Subscription Plan
-- Helps understand subscriber tier distribution (Free vs VIP vs Premium).
SELECT 
    subscription_plan,
    COUNT(user_id) AS total_users,
    ROUND(COUNT(user_id) * 100.0 / (SELECT COUNT(*) FROM users), 2) AS user_percentage
FROM users
GROUP BY subscription_plan
ORDER BY total_users DESC;


-- Query 3: Find Number of Users by City (Top Regions)
-- Shows regional penetration across Indian metropolitan & tier-2 cities.
SELECT 
    city,
    state,
    COUNT(user_id) AS total_users
FROM users
GROUP BY city, state
ORDER BY total_users DESC;


-- Query 4: Find Top 10 Most Active Users Based on Total Watch Duration
-- Identifies power viewers / super users on the platform.
SELECT 
    u.user_id,
    u.subscription_plan,
    u.city,
    u.age_group,
    COUNT(e.event_id) AS total_sessions,
    SUM(e.watch_duration) AS total_watch_minutes,
    ROUND(AVG(e.watch_duration), 2) AS avg_watch_minutes_per_session
FROM users u
INNER JOIN events e 
    ON u.user_id = e.user_id
GROUP BY u.user_id, u.subscription_plan, u.city, u.age_group
ORDER BY total_watch_minutes DESC
LIMIT 10;


-- Query 5: Find Average Watch Duration by Age Group
-- Shows which demographic cohorts spend the most time streaming.
SELECT 
    u.age_group,
    COUNT(DISTINCT u.user_id) AS unique_viewers,
    COUNT(e.event_id) AS total_views,
    ROUND(AVG(e.watch_duration), 2) AS avg_watch_duration_minutes,
    SUM(e.watch_duration) AS total_watch_minutes
FROM users u
INNER JOIN events e 
    ON u.user_id = e.user_id
GROUP BY u.age_group
ORDER BY avg_watch_duration_minutes DESC;
