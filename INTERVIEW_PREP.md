# OTT Product & User Analytics: Complete Interview Preparation Guide

This guide is prepared specifically for analytics interviews at **JioStar / JioHotstar** or other streaming / consumer product companies.

---

## 🎙️ 1. The 90-Second Elevator Pitch (Memorize This!)

> "I built an end-to-end OTT Product & User Analytics project simulating the analytics workflow at a streaming platform like JioStar. 
> 
> The project models how user interaction data is processed from raw events to executive decision-making. 
> 
> First, I created a relational SQLite database with structured tables for users, content catalog, playback events, and an A/B experimentation table. 
> 
> Next, I wrote modular SQL queries to answer core business questions: evaluating content stickiness across genres, analyzing device usage between Mobile and Smart TV, identifying high vs. low engagement user cohorts, and calculating the uplift of a personalized recommendation feature.
> 
> I then built a Python and Pandas pipeline that executes these queries and exports clean, reusable analysis tables. 
> 
> Finally, I created an interactive Streamlit dashboard that visualizes these metrics with Plotly charts and translates the data into five actionable business recommendations—such as expanding regional language catalogs and optimizing the lean-back Smart TV experience. 
> 
> This project gave me hands-on experience in database schema design, SQL aggregation, ETL with Pandas, and data storytelling."

---

## 🏗️ 2. System Architecture Explained

Explain the 6-stage pipeline:

```
[Raw Event Stream] ──► [SQLite DB] ──► [SQL Queries] ──► [Python/Pandas] ──► [Analysis CSVs] ──► [Streamlit App]
```

1. **Raw Event Stream (`data/raw_data.csv`)**: Represents unaggregated JSON/CSV tracking events emitted when users play, pause, or complete videos.
2. **Relational Database (`database/ott_analytics.db`)**: Normalized storage separating entities (`users`, `content`, `events`, `experiment_results`) to eliminate redundancy and maintain referential integrity.
3. **SQL Layer (`sql/*.sql`)**: Analytical queries aggregating business metrics (e.g. watch time, completion rates, view share).
4. **Data Processing Pipeline (`src/analysis.py`)**: Uses Python's `sqlite3` and `pandas.read_sql_query()` to execute SQL and structure outputs into clean DataFrames.
5. **Analytical Data Store (`analysis_results/*.csv`)**: Reusable pre-aggregated summary tables (simulating a reporting mart or data warehouse layer).
6. **Streamlit UI (`app.py`)**: Front-end reporting layer reading the summary tables, providing interactive filters, and rendering dynamic KPI cards and Plotly charts.

---

## 🗄️ 3. Database Interview Questions & Answers

### Q1: Why did you use SQLite instead of storing everything in a single CSV?
**Answer:** A single CSV causes huge data redundancy (e.g. repeating user details and content title on every single play event) and lacks data integrity. SQLite provides a lightweight, ACID-compliant relational engine that allows us to join separate tables, enforce primary/foreign keys, and write real SQL queries.

### Q2: Why did you separate `users`, `content`, and `events` into separate tables?
**Answer:** This follows relational database normalization. `users` holds demographic attributes, `content` holds metadata about movies and shows, and `events` captures transactional playback actions. If a movie title or user city changes, it only needs to be updated in one row rather than millions of event logs.

### Q3: What is a Primary Key and what is a Foreign Key?
**Answer:** 
- **Primary Key (PK):** A column (or set of columns) that uniquely identifies each row in a table (e.g. `user_id` in `users`, `content_id` in `content`, `event_id` in `events`).
- **Foreign Key (FK):** A column in one table that references the primary key of another table (e.g. `user_id` and `content_id` inside `events`), establishing a verified relationship between tables.

### Q4: What is referential integrity?
**Answer:** It ensures that relationships between tables remain consistent. For example, an event cannot reference a `user_id` that does not exist in the `users` table.

---

## 💻 4. Core SQL Concepts & Line-by-Line Query Explanations

### Key SQL Functions Used:
- `GROUP BY`: Groups rows that have the same values in specified columns to calculate aggregates.
- `COUNT()`: Counts total rows or distinct occurrences (`COUNT(DISTINCT user_id)`).
- `SUM()`: Adds together numerical values (e.g. `SUM(watch_duration)`).
- `AVG()`: Computes the arithmetic mean of a column.
- `ORDER BY ... DESC`: Sorts results descending to rank top performers.
- `WHERE` vs `HAVING`: `WHERE` filters rows *before* aggregation; `HAVING` filters groups *after* aggregation (e.g. `HAVING COUNT(event_id) >= 15`).
- `INNER JOIN`: Combines rows from two tables where the join condition matches in both.
- `LEFT JOIN`: Returns all rows from the left table, and matched rows from the right table.
- `CASE WHEN`: Evaluates conditional statements in SQL, similar to if-else logic.

---

### Detailed Line-by-Line Breakdown of 5 Project Queries

#### 1. Content Popularity & Stickiness (`sql/content_analysis.sql`)
```sql
SELECT 
    c.content_title,
    c.genre,
    COUNT(e.event_id) AS total_views,
    ROUND(AVG(e.watch_duration), 2) AS avg_watch_minutes,
    ROUND(SUM(e.completed) * 100.0 / COUNT(e.event_id), 2) AS completion_rate_pct
FROM content c
INNER JOIN events e 
    ON c.content_id = e.content_id
GROUP BY c.content_id, c.content_title, c.genre
ORDER BY total_views DESC
LIMIT 10;
```
* **Line 1-6:** Selects content title, genre, counts total playback events, calculates rounded average watch duration, and calculates completion percentage `(completed / total_events) * 100`.
* **Line 7-9:** Joins `content` table `c` with `events` table `e` on the common key `content_id`.
* **Line 10:** Groups rows by unique content items so aggregations apply per title.
* **Line 11-12:** Sorts from highest to lowest view count and returns the top 10 titles.

---

#### 2. User Engagement Segmentation (`sql/engagement_analysis.sql`)
```sql
SELECT 
    user_engagement_tier,
    COUNT(user_id) AS total_users,
    ROUND(AVG(total_watch_minutes), 2) AS avg_watch_minutes_in_tier
FROM (
    SELECT 
        user_id,
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
```
* **Inner Query (Lines 4-15):** Groups events per user, calculates their total watch duration, and assigns each user to a High, Medium, or Low tier using a `CASE WHEN` statement.
* **Outer Query (Lines 1-3, 16-17):** Aggregates across the derived tiers to count how many users belong to each segment and their average watch time.

---

#### 3. Device Consumption Overview (`sql/device_analysis.sql`)
```sql
SELECT 
    device,
    COUNT(event_id) AS total_views,
    ROUND(COUNT(event_id) * 100.0 / (SELECT COUNT(*) FROM events), 2) AS view_share_pct,
    ROUND(AVG(watch_duration), 2) AS avg_watch_duration_minutes,
    ROUND(SUM(completed) * 100.0 / COUNT(event_id), 2) AS completion_rate_pct
FROM events
GROUP BY device
ORDER BY total_views DESC;
```
* **Line 4:** Uses a scalar subquery `(SELECT COUNT(*) FROM events)` to compute the total event count dynamically and calculate each device's share percentage.
* **Line 5-7:** Computes avg duration and completion rate per device group.

---

#### 4. Top Active Users (`sql/user_analysis.sql`)
```sql
SELECT 
    u.user_id,
    u.subscription_plan,
    u.city,
    COUNT(e.event_id) AS total_sessions,
    SUM(e.watch_duration) AS total_watch_minutes
FROM users u
INNER JOIN events e 
    ON u.user_id = e.user_id
GROUP BY u.user_id, u.subscription_plan, u.city
ORDER BY total_watch_minutes DESC
LIMIT 10;
```
* Identifies power streamers by joining user profiles with event logs, grouping by user details, summing watch time, and limiting to the top 10.

---

#### 5. A/B Experiment Percentage Uplift (`sql/experiment_analysis.sql`)
```sql
SELECT 
    'Treatment vs Control' AS comparison,
    ROUND(((t.avg_watch - c.avg_watch) / c.avg_watch) * 100.0, 2) AS watch_duration_uplift_pct
FROM (
    SELECT AVG(watch_duration) AS avg_watch FROM experiment_results WHERE group_name = 'Control'
) AS c
CROSS JOIN (
    SELECT AVG(watch_duration) AS avg_watch FROM experiment_results WHERE group_name = 'Treatment'
) AS t;
```
* Uses subqueries to compute average watch duration for Control (`c`) and Treatment (`t`), then applies a `CROSS JOIN` to calculate the percentage uplift formula: `((Treatment - Control) / Control) * 100`.

---

## 🐍 5. Python & Pandas Interview Questions

### Q1: Why did you use Pandas in this project?
**Answer:** While SQL is great for querying and filtering databases, Pandas is ideal for manipulating tabular data in memory, handling missing values, calculating summary statistics, and passing structured DataFrames to Streamlit and Plotly.

### Q2: How does Python connect to SQLite and run SQL queries?
**Answer:** We use Python's built-in `sqlite3` library to create a connection (`conn = sqlite3.connect(DB_PATH)`), and then use `pd.read_sql_query(sql_statement, conn)` which executes the query and directly returns a Pandas DataFrame.

### Q3: Why save pre-computed CSVs in `analysis_results/` instead of running SQL queries directly on every Streamlit page reload?
**Answer:** In production analytics, running heavy analytical queries against a live database on every user interaction slows down the application and overburdens the database. Pre-aggregating data into analytical tables / data marts creates a decoupled, fast, and scalable reporting layer.

---

## 📊 6. Streamlit & Data Storytelling Questions

### Q1: How does Streamlit fit into this analytics workflow?
**Answer:** Streamlit serves as the business intelligence and reporting interface. It translates CSV summary tables into interactive KPI cards, bar charts, pie charts, and data tables with sidebar filters, making insights accessible to non-technical stakeholders.

### Q2: How did you ensure insights are dynamic rather than hardcoded?
**Answer:** All metric callouts (e.g. top viewed title, % uplift, completion rates) are computed directly from the loaded DataFrames using Pandas operations (e.g. `df.sort_values().iloc[0]` or `(trt - ctrl) / ctrl * 100`), ensuring that any update to the database automatically updates the insights.

---

## 🎯 7. JioStar / Hotstar Practical Analytics Scenarios

### Scenario 1: How would you investigate a sudden drop in platform watch time?
**Answer:**
1. **Dimension Breakdown:** Slice watch time by platform dimensions: Device (App vs Web vs Smart TV), Region/City, Network (CDN/ISP), and Content Genre.
2. **Funnel Analysis:** Check whether the drop is due to fewer users opening the app (acquisition/login issue) or lower session duration (content/buffering issue).
3. **Technical vs Content Causes:** Check if error logs show increased buffering rates, video playback failure errors (VPF), or if a major sporting tournament just concluded.

### Scenario 2: How would you decide which content titles to promote on the home screen carousel?
**Answer:**
Look at two key metrics together: **View Volume (CTR)** and **Completion Rate (Stickiness)**. A title with high CTR but low completion indicates clickbait; a title with high completion rate but low views is a "hidden gem" that will benefit the most from top-of-funnel carousel promotion.

### Scenario 3: How would you design and evaluate an A/B test on JioHotstar?
**Answer:**
1. **Hypothesis:** "Adding personalized genre shortcuts will increase average watch time."
2. **Randomization:** Split active users 50/50 into Control (standard UI) and Treatment (personalized shortcuts).
3. **Primary Metric:** Average watch duration per user.
4. **Secondary Metrics:** Session frequency, video completion rate, search exit rate.
5. **Guardrail Metrics:** App crash rate, video playback start latency.
6. **Decision:** If primary metric shows significant positive uplift without harming guardrails, roll out to 100%.

### Scenario 4: What key events would you track in a video playback session?
**Answer:**
- `video_click`: When user selects a thumbnail.
- `video_start`: When the first video frame renders (measures startup time).
- `heartbeat_ping`: Periodic event every 30-60 seconds logging current watch time and bitrate.
- `pause` / `resume` / `seek`: User playback interactions.
- `video_complete`: Triggered when watch progress reaches >90%.
- `playback_error`: Logs error code if stream fails.

### Scenario 5: What would you do if event data is missing or corrupted?
**Answer:**
1. Compare row counts against daily active users (DAU) to quantify missingness.
2. Check client-side tracking SDK version releases for broken telemetry.
3. In analysis queries, use `COALESCE()` or `NULLIF()` to avoid division-by-zero or `NULL` aggregation errors.
4. Document the missing time window when sharing reports with stakeholders.

---

## 📝 8. Top 15 Likely Interview Questions & Rapid Answers

| # | Question | Rapid 1-Sentence Answer |
| :--- | :--- | :--- |
| 1 | What is the difference between `WHERE` and `HAVING`? | `WHERE` filters individual records before grouping, while `HAVING` filters aggregated groups after `GROUP BY`. |
| 2 | What is the difference between `INNER JOIN` and `LEFT JOIN`? | `INNER JOIN` returns only matching rows from both tables, while `LEFT JOIN` returns all rows from the left table and matching rows from the right. |
| 3 | What is a foreign key constraint? | A rule ensuring that a value in a child table must match a valid primary key in the parent table. |
| 4 | How do you calculate percentage share in SQL? | Multiply the group count by `100.0` and divide by a subquery selecting the total count `(SELECT COUNT(*) FROM table)`. |
| 5 | What is `COALESCE()` used for? | It returns the first non-null value in a list of arguments, replacing nulls with a default (e.g. 0). |
| 6 | How did you segment users by engagement? | Used a `CASE WHEN` clause on total watch minutes (>300 = High, 100-300 = Medium, <100 = Low). |
| 7 | What is the completion rate formula? | `(SUM(completed_events) * 100.0) / COUNT(total_events)`. |
| 8 | Why is Smart TV watch time longer than Mobile? | Smart TV is a lean-back, shared living room experience with longer sessions, whereas Mobile is short-burst and on-the-go. |
| 9 | What is an A/B test? | A randomized controlled experiment where users are split between variant A (Control) and variant B (Treatment) to measure metric changes. |
| 10 | How is percentage uplift calculated? | `((Treatment Metric - Control Metric) / Control Metric) * 100`. |
| 11 | What is `pd.read_sql_query()`? | A Pandas function that executes a SQL query through a database connection and returns the result as a DataFrame. |
| 12 | What is a DataFrame? | A 2-dimensional labeled data structure in Pandas with columns of potentially different types, similar to a spreadsheet or SQL table. |
| 13 | Why did you separate the SQL execution from the Streamlit UI? | To decouple analytical data processing from presentation, improving speed and reusability. |
| 14 | How do you identify churn risks? | Users with multiple app opens/sessions but low total watch time (<60 mins) who are dropping off before finding content. |
| 15 | What is the biggest strategic takeaway from your project? | Sports and Drama drive platform engagement, while personalized recommendation trays increase watch time by reducing search friction. |
