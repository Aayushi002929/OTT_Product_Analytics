# OTT Product & User Analytics

An end-to-end, SQL-driven analytics project simulating product and viewer engagement workflows at a large-scale streaming platform (inspired by **JioStar / JioHotstar**).

---

## 📌 Project Overview & Architecture

This project demonstrates the complete real-world analytics lifecycle:

```
Raw Product Events (data/raw_data.csv)
       │
       ▼
Relational Database (database/ott_analytics.db - SQLite)
       │
       ▼
SQL Analysis Layer (sql/*.sql)
       │
       ▼
Python / Pandas Pipeline (src/analysis.py)
       │
       ▼
Reusable Analysis Tables (analysis_results/*.csv)
       │
       ▼
Streamlit Reporting Layer (app.py)
       │
       ▼
Actionable Business Insights & Strategy
```

---

## 🎯 Problem Statement

Streaming platforms generate millions of playback events daily across devices (Mobile, Smart TV, Web, Tablet) and regional markets. Product managers and content strategists need answers to critical questions:
- Which genres and content titles drive deep viewer stickiness vs high churn?
- How do viewing habits vary between mobile-first casual users and living-room Smart TV viewers?
- Does an AI-powered personalized homepage tray boost overall watch time and video completions?

This project models and answers these questions using clean relational schemas, modular SQL queries, automated Python ETL, and an interactive reporting dashboard.

---

## 🗄️ Database Schema & Design

The database (`database/ott_analytics.db`) is built using **SQLite** with 4 relational tables:

```
+--------------------+       +----------------------+
|       users        |       |       content        |
+--------------------+       +----------------------+
| user_id (PK)       |       | content_id (PK)      |
| age_group          |       | content_title        |
| gender             |       | content_type         |
| city               |       | genre                |
| state              |       | language             |
| subscription_plan  |       | content_duration     |
| signup_date        |       | release_year         |
+--------------------+       +----------------------+
          │                              │
          │         +-----------------+  │
          └────────►|     events      |◄─┘
                    +-----------------+
                    | event_id (PK)   |
                    | user_id (FK)    |
                    | content_id (FK) |
                    | event_type      |
                    | event_date      |
                    | device          |
                    | watch_duration  |
                    | completed       |
                    +-----------------+

          +--------------------+
          | experiment_results |
          +--------------------+
          | experiment_id (PK) |
          | user_id (FK)       |
          | group_name         |
          | sessions           |
          | watch_duration     |
          | completed          |
          +--------------------+
```

### Table Descriptions:
1. **`users`** (750 records): User demographic data including `age_group`, `gender`, `city`, `state`, `subscription_plan` (Free, VIP, Premium), and `signup_date`.
2. **`content`** (60 records): Catalog of OTT titles across Sports, Drama, Comedy, Action, Reality, News, and Kids in multiple regional languages (Hindi, English, Tamil, Telugu, Bengali, Marathi, Malayalam).
3. **`events`** (7,500 records): Granular user interactions with `event_type` (`play`, `pause`, `complete`), `device` (`Mobile`, `Smart TV`, `Web`, `Tablet`), `watch_duration` in minutes, and `completed` binary flag.
4. **`experiment_results`** (600 records): A/B test comparing `Control` (standard feed) vs `Treatment` (personalized AI content tray).

---

## 🔍 Analytics Questions Answered by SQL

The project organizes queries into 6 modular SQL files in `sql/`:

| SQL File | Key Questions Answered |
| :--- | :--- |
| **`sql/user_analysis.sql`** | Total users, subscriber tier split, regional user penetration, top 10 most active users, average watch duration by age cohort. |
| **`sql/content_analysis.sql`** | Top 10 most viewed titles, highest average watch duration titles, most popular genres, content format comparison (Movies vs Series vs Shows), regional language popularity. |
| **`sql/device_analysis.sql`** | Device view share, average watch duration per device, completion rate by form factor, device usage by subscription tier. |
| **`sql/region_analysis.sql`** | City and state-level viewing volumes, average watch time by city, regional language preferences by city. |
| **`sql/engagement_analysis.sql`** | Platform video completion rate, user segmentation into High (>300 mins), Medium (100-300 mins), and Low (<100 mins) tiers, churn risk identification. |
| **`sql/experiment_analysis.sql`** | Control vs Treatment A/B test comparison: users, total sessions, sessions per user, avg watch duration, completion rate, and direct % uplift calculation. |

---

## 🛠️ Technical Concepts Used

### 1. SQL Concepts
- `SELECT`, `FROM`, `WHERE`: Filtering specific records.
- `GROUP BY`, `ORDER BY`: Aggregating metrics across dimensions and sorting results.
- `COUNT`, `SUM`, `AVG`: Calculating summary statistics.
- `INNER JOIN`, `LEFT JOIN`: Combining user demographics, content metadata, and playback event logs.
- `CASE WHEN`: Conditional logic for user tier segmentation and frequency buckets.
- `LIMIT`, `HAVING`: Extracting top N records and filtering grouped aggregations.

### 2. Python & Pandas Concepts
- `sqlite3`: Built-in lightweight SQL database connector.
- `pd.read_sql_query()`: Executing SQL queries directly into Pandas DataFrames.
- `to_csv()`: Exporting query results into reusable analytical tables in `analysis_results/`.
- File system management with `os` and modular procedural pipelines.

### 3. Streamlit & Plotly
- Interactive dashboard with metric cards, interactive bar charts, pie charts, and data tables.
- Dynamic calculations for uplifts and executive callout text (no hardcoded static numbers).
- Sidebar filters for Genre, Language, Device, City, and Subscription Plan.

---

## 🚀 How to Run the Project

### 1. Clone & Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Create the Database & Generate Synthetic Data
```bash
python database/create_database.py
```
*Output: Creates `database/ott_analytics.db` and exports `data/raw_data.csv`.*

### 3. Run the SQL & Pandas Analytics Pipeline
```bash
python src/analysis.py
```
*Output: Executes SQL queries, prints summaries, and creates 7 CSV tables in `analysis_results/`.*

### 4. Launch the Streamlit Dashboard
```bash
streamlit run app.py
```
*Opens the interactive dashboard in your browser (typically `http://localhost:8501`).*

---

## 🏢 How This Project Relates to JioStar / JioHotstar Analytics

| Analytics Area | Implementation in This Project |
| :--- | :--- |
| **1. Data** | Simulates raw streaming event logs (play, pause, complete) and structures them into clean relational tables. |
| **2. Reporting** | Builds reusable analytical tables and a Streamlit dashboard mirroring executive reporting dashboards. |
| **3. Inquisitive Analysis** | Uses SQL to investigate root causes of watch time differences across content genres, age groups, and devices. |
| **4. Experimentation** | Analyzes a realistic A/B test (Control vs Treatment) to evaluate engagement uplift for a personalized recommendation feature. |
| **5. Strategic Inputs** | Converts quantitative data into business actions: sports hub promotion, regional dubbing, and Smart TV UX enhancements. |

> **Disclaimer:** This project is an independent educational simulation built for portfolio and interview preparation. It is inspired by common OTT industry workflows and does not use proprietary data or internal infrastructure of JioStar, Disney+ Hotstar, or any third party.
