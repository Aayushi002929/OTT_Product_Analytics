"""
=============================================================================
OTT Product & User Analytics - SQL Execution & Analysis Pipeline
=============================================================================
This script:
1. Connects to SQLite database (database/ott_analytics.db).
2. Executes clean, modular SQL queries to answer product & business questions.
3. Loads query outputs into Pandas DataFrames.
4. Generates and saves reusable CSV analysis tables into analysis_results/.
5. Prints clear executive summaries to the console.
=============================================================================
"""

import sqlite3
import pandas as pd
import os

# Define relative paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "ott_analytics.db")
OUTPUT_DIR = os.path.join(BASE_DIR, "analysis_results")


def run_query(conn, query_sql):
    """Helper function to execute SQL and return a Pandas DataFrame."""
    return pd.read_sql_query(query_sql, conn)


def execute_analytics_pipeline():
    """Main pipeline executing SQL queries and creating analysis CSV tables."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("=======================================================")
    print(" STARTING OTT ANALYTICS SQL PIPELINE")
    print(f" Database: {DB_PATH}")
    print("=======================================================\n")
    
    conn = sqlite3.connect(DB_PATH)
    
    # ---------------------------------------------------------
    # 1. USER INSIGHTS
    # ---------------------------------------------------------
    user_sql = """
    SELECT 
        u.user_id,
        u.age_group,
        u.gender,
        u.city,
        u.state,
        u.subscription_plan,
        u.signup_date,
        COUNT(e.event_id) AS total_sessions,
        COALESCE(SUM(e.watch_duration), 0) AS total_watch_minutes,
        ROUND(COALESCE(AVG(e.watch_duration), 0), 2) AS avg_watch_minutes_per_session,
        COALESCE(SUM(e.completed), 0) AS completed_sessions
    FROM users u
    LEFT JOIN events e 
        ON u.user_id = e.user_id
    GROUP BY u.user_id, u.age_group, u.gender, u.city, u.state, u.subscription_plan, u.signup_date;
    """
    df_users = run_query(conn, user_sql)
    df_users.to_csv(os.path.join(OUTPUT_DIR, "user_insights.csv"), index=False)
    print(f" [1/7] Saved user_insights.csv ({len(df_users)} rows)")
    
    # ---------------------------------------------------------
    # 2. CONTENT INSIGHTS
    # ---------------------------------------------------------
    content_sql = """
    SELECT 
        c.content_id,
        c.content_title,
        c.content_type,
        c.genre,
        c.language,
        c.content_duration AS total_duration,
        c.release_year,
        COUNT(e.event_id) AS total_views,
        COALESCE(SUM(e.watch_duration), 0) AS total_watch_minutes,
        ROUND(COALESCE(AVG(e.watch_duration), 0), 2) AS avg_watch_minutes,
        COALESCE(SUM(e.completed), 0) AS total_completions,
        ROUND(COALESCE(SUM(e.completed) * 100.0 / NULLIF(COUNT(e.event_id), 0), 0), 2) AS completion_rate_pct
    FROM content c
    LEFT JOIN events e 
        ON c.content_id = e.content_id
    GROUP BY c.content_id, c.content_title, c.content_type, c.genre, c.language, c.content_duration, c.release_year
    ORDER BY total_views DESC;
    """
    df_content = run_query(conn, content_sql)
    df_content.to_csv(os.path.join(OUTPUT_DIR, "content_insights.csv"), index=False)
    print(f" [2/7] Saved content_insights.csv ({len(df_content)} rows)")
    
    # ---------------------------------------------------------
    # 3. GENRE INSIGHTS
    # ---------------------------------------------------------
    genre_sql = """
    SELECT 
        c.genre,
        COUNT(DISTINCT c.content_id) AS total_titles,
        COUNT(e.event_id) AS total_views,
        SUM(e.watch_duration) AS total_watch_minutes,
        ROUND(AVG(e.watch_duration), 2) AS avg_watch_duration_minutes,
        SUM(e.completed) AS total_completed_views,
        ROUND(SUM(e.completed) * 100.0 / COUNT(e.event_id), 2) AS completion_rate_pct
    FROM content c
    INNER JOIN events e 
        ON c.content_id = e.content_id
    GROUP BY c.genre
    ORDER BY total_views DESC;
    """
    df_genre = run_query(conn, genre_sql)
    df_genre.to_csv(os.path.join(OUTPUT_DIR, "genre_insights.csv"), index=False)
    print(f" [3/7] Saved genre_insights.csv ({len(df_genre)} rows)")
    
    # ---------------------------------------------------------
    # 4. DEVICE INSIGHTS
    # ---------------------------------------------------------
    device_sql = """
    SELECT 
        device,
        COUNT(event_id) AS total_views,
        ROUND(COUNT(event_id) * 100.0 / (SELECT COUNT(*) FROM events), 2) AS view_share_pct,
        SUM(watch_duration) AS total_watch_minutes,
        ROUND(AVG(watch_duration), 2) AS avg_watch_duration_minutes,
        SUM(completed) AS total_completed,
        ROUND(SUM(completed) * 100.0 / COUNT(event_id), 2) AS completion_rate_pct
    FROM events
    GROUP BY device
    ORDER BY total_views DESC;
    """
    df_device = run_query(conn, device_sql)
    df_device.to_csv(os.path.join(OUTPUT_DIR, "device_insights.csv"), index=False)
    print(f" [4/7] Saved device_insights.csv ({len(df_device)} rows)")
    
    # ---------------------------------------------------------
    # 5. REGION INSIGHTS
    # ---------------------------------------------------------
    region_sql = """
    SELECT 
        u.city,
        u.state,
        COUNT(DISTINCT u.user_id) AS registered_users,
        COUNT(e.event_id) AS total_views,
        SUM(e.watch_duration) AS total_watch_minutes,
        ROUND(AVG(e.watch_duration), 2) AS avg_watch_duration_minutes,
        ROUND(SUM(e.completed) * 100.0 / COUNT(e.event_id), 2) AS completion_rate_pct
    FROM users u
    INNER JOIN events e 
        ON u.user_id = e.user_id
    GROUP BY u.city, u.state
    ORDER BY total_views DESC;
    """
    df_region = run_query(conn, region_sql)
    df_region.to_csv(os.path.join(OUTPUT_DIR, "region_insights.csv"), index=False)
    print(f" [5/7] Saved region_insights.csv ({len(df_region)} rows)")
    
    # ---------------------------------------------------------
    # 6. ENGAGEMENT INSIGHTS
    # ---------------------------------------------------------
    engagement_sql = """
    SELECT 
        user_engagement_tier,
        COUNT(user_id) AS total_users,
        ROUND(COUNT(user_id) * 100.0 / (SELECT COUNT(DISTINCT user_id) FROM events), 2) AS user_percentage,
        ROUND(AVG(total_watch_minutes), 2) AS avg_watch_minutes,
        ROUND(AVG(total_sessions), 2) AS avg_sessions
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
    ) AS tiers
    GROUP BY user_engagement_tier
    ORDER BY total_users DESC;
    """
    df_engagement = run_query(conn, engagement_sql)
    df_engagement.to_csv(os.path.join(OUTPUT_DIR, "engagement_insights.csv"), index=False)
    print(f" [6/7] Saved engagement_insights.csv ({len(df_engagement)} rows)")
    
    # ---------------------------------------------------------
    # 7. EXPERIMENT INSIGHTS
    # ---------------------------------------------------------
    experiment_sql = """
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
    """
    df_experiment = run_query(conn, experiment_sql)
    df_experiment.to_csv(os.path.join(OUTPUT_DIR, "experiment_insights.csv"), index=False)
    print(f" [7/7] Saved experiment_insights.csv ({len(df_experiment)} rows)")
    
    conn.close()
    
    print("\n=======================================================")
    print(" ALL ANALYSIS TABLES GENERATED SUCCESSFULLY")
    print(f" Output Location: {OUTPUT_DIR}")
    print("=======================================================\n")
    
    # Print Executive Highlights
    top_content = df_content.iloc[0]['content_title']
    top_genre = df_genre.iloc[0]['genre']
    top_device = df_device.iloc[0]['device']
    
    ctrl = df_experiment[df_experiment['group_name'] == 'Control'].iloc[0]
    trt = df_experiment[df_experiment['group_name'] == 'Treatment'].iloc[0]
    uplift = round(((trt['avg_watch_duration_per_user'] - ctrl['avg_watch_duration_per_user']) / ctrl['avg_watch_duration_per_user']) * 100, 2)
    
    print("Executive Summary Snapshot:")
    print(f" - Top Viewed Title:    {top_content}")
    print(f" - Top Genre by Volume: {top_genre}")
    print(f" - Primary Device:      {top_device} ({df_device.iloc[0]['view_share_pct']}% share)")
    print(f" - Experiment Uplift:   Treatment delivered +{uplift}% average watch duration over Control.")
    print("=======================================================\n")


if __name__ == "__main__":
    execute_analytics_pipeline()
