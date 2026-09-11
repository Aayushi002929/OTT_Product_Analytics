-- =============================================================================
-- OTT PRODUCT & USER ANALYTICS: ENGAGEMENT ANALYSIS
-- =============================================================================
-- Database: ott_analytics.db
-- Objective: Segment users by activity depth, measure completion rate, and detect churn risks.
-- =============================================================================

-- Query 1: Overall Platform Video Completion Rate
-- Formula: (Total Completed Events / Total Playback Events) * 100
SELECT 
    COUNT(event_id) AS total_events,
    SUM(completed) AS total_completed_events,
    ROUND(SUM(completed) * 100.0 / COUNT(event_id), 2) AS platform_completion_rate_pct
FROM events;


-- Query 2: User Engagement Segmentation (High vs Medium vs Low)
-- Uses CASE WHEN on total watch duration:
-- - High Engagement: > 300 minutes
-- - Medium Engagement: 100 to 300 minutes
-- - Low Engagement: < 100 minutes
SELECT 
    user_engagement_tier,
    COUNT(user_id) AS total_users,
    ROUND(COUNT(user_id) * 100.0 / (SELECT COUNT(DISTINCT user_id) FROM events), 2) AS user_percentage,
    ROUND(AVG(total_watch_minutes), 2) AS avg_watch_minutes_in_tier,
    ROUND(AVG(total_sessions), 2) AS avg_sessions_in_tier
FROM (
    SELECT 
        user_id,
        COUNT(event_id) AS total_sessions,
        SUM(watch_duration) AS total_watch_minutes,
        CASE 
            WHEN SUM(watch_duration) > 300 THEN 'High Engagement (>300 mins)'
            WHEN SUM(watch_duration) >= 100 THEN 'Medium Engagement (100-300 mins)'
            ELSE 'Low Engagement (<100 mins)'
        END AS user_engagement_tier
    FROM events
    GROUP BY user_id
) AS user_tiers
GROUP BY user_engagement_tier
ORDER BY total_users DESC;


-- Query 3: High vs Low Engagement by Subscription Tier
-- Evaluates whether paid subscribers (VIP / Premium) demonstrate higher retention & watch depth.
SELECT 
    u.subscription_plan,
    COUNT(DISTINCT u.user_id) AS total_subscribers,
    COUNT(e.event_id) AS total_playback_sessions,
    SUM(e.watch_duration) AS total_watch_minutes,
    ROUND(AVG(e.watch_duration), 2) AS avg_watch_minutes_per_session,
    ROUND(SUM(e.completed) * 100.0 / COUNT(e.event_id), 2) AS completion_rate_pct
FROM users u
INNER JOIN events e 
    ON u.user_id = e.user_id
GROUP BY u.subscription_plan
ORDER BY avg_watch_minutes_per_session DESC;


-- Query 4: Identifying Low-Engagement Users at Risk of Churn
-- Users with low watch time (< 60 minutes) despite having multiple app sessions.
SELECT 
    u.user_id,
    u.subscription_plan,
    u.city,
    COUNT(e.event_id) AS total_sessions,
    SUM(e.watch_duration) AS total_watch_minutes,
    SUM(e.completed) AS total_completed
FROM users u
INNER JOIN events e 
    ON u.user_id = e.user_id
GROUP BY u.user_id, u.subscription_plan, u.city
HAVING SUM(e.watch_duration) < 60 AND COUNT(e.event_id) >= 2
ORDER BY total_watch_minutes ASC
LIMIT 15;
