-- =============================================================================
-- OTT PRODUCT & USER ANALYTICS: CONTENT ANALYSIS
-- =============================================================================
-- Database: ott_analytics.db
-- Objective: Understand catalog performance, popular titles, genres, and languages.
-- =============================================================================

-- Query 1: Find Top 10 Most Viewed Content Titles
-- Discovers which titles attract the highest volume of plays.
SELECT 
    c.content_id,
    c.content_title,
    c.genre,
    c.language,
    c.content_type,
    COUNT(e.event_id) AS total_views,
    SUM(e.watch_duration) AS total_watch_minutes,
    ROUND(AVG(e.watch_duration), 2) AS avg_watch_duration
FROM content c
INNER JOIN events e 
    ON c.content_id = e.content_id
GROUP BY c.content_id, c.content_title, c.genre, c.language, c.content_type
ORDER BY total_views DESC
LIMIT 10;


-- Query 2: Find Content with Highest Average Watch Duration
-- Identifies sticky, deeply engaging titles where users spend significant time.
SELECT 
    c.content_id,
    c.content_title,
    c.genre,
    c.content_duration AS total_duration_minutes,
    COUNT(e.event_id) AS total_views,
    ROUND(AVG(e.watch_duration), 2) AS avg_watch_minutes,
    ROUND(SUM(e.completed) * 100.0 / COUNT(e.event_id), 2) AS completion_rate_percentage
FROM content c
INNER JOIN events e 
    ON c.content_id = e.content_id
GROUP BY c.content_id, c.content_title, c.genre, c.content_duration
HAVING COUNT(e.event_id) >= 15
ORDER BY avg_watch_minutes DESC
LIMIT 10;


-- Query 3: Find Most Popular Genres by Total Views
-- Shows audience genre preferences (e.g., Sports vs Reality vs Drama).
SELECT 
    c.genre,
    COUNT(e.event_id) AS total_views,
    ROUND(COUNT(e.event_id) * 100.0 / (SELECT COUNT(*) FROM events), 2) AS view_share_percentage
FROM content c
INNER JOIN events e 
    ON c.content_id = e.content_id
GROUP BY c.genre
ORDER BY total_views DESC;


-- Query 4: Find Average Watch Duration by Genre
-- Reveals which genres keep viewers hooked the longest.
SELECT 
    c.genre,
    COUNT(e.event_id) AS total_views,
    SUM(e.watch_duration) AS total_watch_minutes,
    ROUND(AVG(e.watch_duration), 2) AS avg_watch_duration_minutes,
    ROUND(SUM(e.completed) * 100.0 / COUNT(e.event_id), 2) AS completion_rate_pct
FROM content c
INNER JOIN events e 
    ON c.content_id = e.content_id
GROUP BY c.genre
ORDER BY avg_watch_duration_minutes DESC;


-- Query 5: Compare Content Performance Across Content Types (Movies vs Series vs Shows vs Sports)
-- Determines how long-form formats compare against episodic or live formats.
SELECT 
    c.content_type,
    COUNT(DISTINCT c.content_id) AS number_of_titles,
    COUNT(e.event_id) AS total_views,
    SUM(e.watch_duration) AS total_watch_minutes,
    ROUND(AVG(e.watch_duration), 2) AS avg_watch_minutes_per_view,
    ROUND(SUM(e.completed) * 100.0 / COUNT(e.event_id), 2) AS completion_rate_pct
FROM content c
INNER JOIN events e 
    ON c.content_id = e.content_id
GROUP BY c.content_type
ORDER BY total_views DESC;


-- Query 6: Find Most Popular Content Languages
-- Demonstrates regional language demand (Hindi, Tamil, Telugu, English, etc.).
SELECT 
    c.language,
    COUNT(e.event_id) AS total_views,
    SUM(e.watch_duration) AS total_watch_minutes,
    ROUND(AVG(e.watch_duration), 2) AS avg_watch_duration_minutes,
    ROUND(COUNT(e.event_id) * 100.0 / (SELECT COUNT(*) FROM events), 2) AS view_percentage
FROM content c
INNER JOIN events e 
    ON c.content_id = e.content_id
GROUP BY c.language
ORDER BY total_views DESC;
