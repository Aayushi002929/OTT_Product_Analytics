-- =============================================================================
-- OTT PRODUCT & USER ANALYTICS: EXPERIMENT ANALYSIS (A/B TESTING)
-- =============================================================================
-- Database: ott_analytics.db
-- Objective: Compare Control vs Treatment group performance on the 'Personalized Content Tray' feature.
-- =============================================================================

-- Query 1: Overall Experiment Summary Table (Control vs Treatment)
-- Calculates total users, total sessions, avg sessions per user, avg watch duration, and completion rate.
SELECT 
    group_name,
    COUNT(user_id) AS total_users,
    SUM(sessions) AS total_sessions,
    ROUND(AVG(sessions), 2) AS avg_sessions_per_user,
    SUM(watch_duration) AS total_watch_minutes,
    ROUND(AVG(watch_duration), 2) AS avg_watch_duration_per_user,
    ROUND(SUM(watch_duration) * 1.0 / SUM(sessions), 2) AS avg_watch_minutes_per_session,
    SUM(completed) AS total_completed_sessions,
    ROUND(SUM(completed) * 100.0 / SUM(sessions), 2) AS completion_rate_pct
FROM experiment_results
GROUP BY group_name
ORDER BY group_name ASC;


-- Query 2: Distribution of Sessions Between Control and Treatment
-- Shows how many users engaged deeply (e.g. > 10 sessions) in each variant.
SELECT 
    group_name,
    CASE 
        WHEN sessions >= 10 THEN 'High Frequency (>= 10 sessions)'
        WHEN sessions >= 6 THEN 'Medium Frequency (6-9 sessions)'
        ELSE 'Low Frequency (< 6 sessions)'
    END AS frequency_segment,
    COUNT(user_id) AS user_count,
    ROUND(AVG(watch_duration), 2) AS avg_watch_duration
FROM experiment_results
GROUP BY group_name, frequency_segment
ORDER BY group_name, user_count DESC;


-- Query 3: Uplift Calculation Between Variants
-- Computes the direct percentage difference: ((Treatment - Control) / Control) * 100
SELECT 
    'Treatment vs Control' AS comparison,
    ROUND(((t.avg_watch - c.avg_watch) / c.avg_watch) * 100.0, 2) AS watch_duration_uplift_pct,
    ROUND(((t.avg_sess - c.avg_sess) / c.avg_sess) * 100.0, 2) AS session_frequency_uplift_pct,
    ROUND(((t.comp_rate - c.comp_rate) / c.comp_rate) * 100.0, 2) AS completion_rate_uplift_pct
FROM (
    SELECT 
        AVG(watch_duration) AS avg_watch,
        AVG(sessions) AS avg_sess,
        SUM(completed) * 100.0 / SUM(sessions) AS comp_rate
    FROM experiment_results
    WHERE group_name = 'Control'
) AS c
CROSS JOIN (
    SELECT 
        AVG(watch_duration) AS avg_watch,
        AVG(sessions) AS avg_sess,
        SUM(completed) * 100.0 / SUM(sessions) AS comp_rate
    FROM experiment_results
    WHERE group_name = 'Treatment'
) AS t;
