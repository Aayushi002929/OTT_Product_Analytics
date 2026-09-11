"""
=============================================================================
OTT Product & User Analytics - Database Creation & Synthetic Data Generator
=============================================================================
This script:
1. Generates realistic synthetic data for an Indian OTT platform (JioStar style).
2. Saves the raw event log to data/raw_data.csv.
3. Creates SQLite database: database/ott_analytics.db.
4. Creates 4 relational tables: users, content, events, experiment_results.
5. Inserts the generated records and verifies row counts.
=============================================================================
"""

import sqlite3
import random
import csv
import os
from datetime import datetime, timedelta

# Fix seed for reproducibility
random.seed(42)

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "ott_analytics.db")
RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw_data.csv")

def generate_users(num_users=750):
    """Generate realistic OTT user profiles across Indian cities."""
    age_groups = ["18-25", "26-35", "36-45", "46+"]
    age_weights = [0.40, 0.35, 0.15, 0.10]
    
    genders = ["Male", "Female", "Other"]
    gender_weights = [0.52, 0.46, 0.02]
    
    city_state_map = [
        ("Mumbai", "Maharashtra"),
        ("Delhi", "Delhi"),
        ("Bengaluru", "Karnataka"),
        ("Chennai", "Tamil Nadu"),
        ("Hyderabad", "Telangana"),
        ("Kolkata", "West Bengal"),
        ("Pune", "Maharashtra"),
        ("Ahmedabad", "Gujarat"),
        ("Jaipur", "Rajasthan"),
        ("Lucknow", "Uttar Pradesh"),
        ("Kochi", "Kerala"),
        ("Patna", "Bihar")
    ]
    city_weights = [0.18, 0.16, 0.14, 0.10, 0.10, 0.08, 0.06, 0.05, 0.04, 0.04, 0.03, 0.02]
    
    subscription_plans = ["Free", "VIP", "Premium"]
    sub_weights = [0.45, 0.35, 0.20]
    
    start_date = datetime(2025, 6, 1)
    
    users = []
    for i in range(1, num_users + 1):
        user_id = f"U{1000 + i}"
        age_group = random.choices(age_groups, weights=age_weights)[0]
        gender = random.choices(genders, weights=gender_weights)[0]
        
        city_idx = random.choices(range(len(city_state_map)), weights=city_weights)[0]
        city, state = city_state_map[city_idx]
        
        subscription_plan = random.choices(subscription_plans, weights=sub_weights)[0]
        
        # Random signup date in the last 8 months
        days_offset = random.randint(0, 240)
        signup_date = (start_date + timedelta(days=days_offset)).strftime("%Y-%m-%d")
        
        users.append((user_id, age_group, gender, city, state, subscription_plan, signup_date))
        
    return users


def generate_content():
    """Generate realistic OTT content catalog (Movies, Series, Sports, Reality, News, Kids)."""
    content_list = [
        # Sports
        ("C101", "IND vs AUS T20 Cup Highlights", "Sports", "Sports", "Hindi", 45, 2026),
        ("C102", "IPL Mega Auction Live Replay", "Sports", "Sports", "Hindi", 90, 2026),
        ("C103", "Premier League Weekly Showdown", "Sports", "Sports", "English", 60, 2026),
        ("C104", "IND vs ENG Test Day 3 Highlights", "Sports", "Sports", "English", 50, 2026),
        ("C105", "Pro Kabaddi League Finals", "Sports", "Sports", "Tamil", 70, 2025),
        ("C106", "WPL T20 Blockbuster Match", "Sports", "Sports", "Hindi", 60, 2026),
        ("C107", "Champions Trophy Pre-Show", "Sports", "Sports", "Telugu", 40, 2026),
        ("C108", "ISL Football Clash of Titans", "Sports", "Sports", "Bengali", 60, 2025),
        
        # Drama
        ("C109", "Special Ops: Desert Falcon", "Series", "Drama", "Hindi", 45, 2025),
        ("C110", "Anupama: New Beginnings", "Show", "Drama", "Hindi", 25, 2026),
        ("C111", "Yeh Rishta: Family Bonds", "Show", "Drama", "Hindi", 22, 2026),
        ("C112", "City of Dreams: The Succession", "Series", "Drama", "Hindi", 50, 2024),
        ("C113", "Kaithi Revenge Chronicles", "Movie", "Drama", "Tamil", 140, 2025),
        ("C114", "Telugu Royal Heritage", "Series", "Drama", "Telugu", 45, 2025),
        ("C115", "Bengal Courtroom Secrets", "Series", "Drama", "Bengali", 40, 2025),
        ("C116", "Kolkata Love Diary", "Movie", "Drama", "Bengali", 125, 2024),
        ("C117", "Ghar Ek Mandir Classic", "Show", "Drama", "Marathi", 24, 2026),
        ("C118", "Kerala Waterfront Mystery", "Series", "Drama", "Malayalam", 48, 2025),
        ("C119", "The Crown Dynasty Legacy", "Series", "Drama", "English", 55, 2024),
        ("C120", "Succession Politics India", "Series", "Drama", "Hindi", 45, 2025),
        
        # Comedy
        ("C121", "The Great Indian Comedy Lab", "Show", "Comedy", "Hindi", 35, 2026),
        ("C122", "Taarak Laugh Fest Episodes", "Show", "Comedy", "Hindi", 22, 2026),
        ("C123", "Sarabhai Classic Revival", "Series", "Comedy", "Hindi", 25, 2025),
        ("C124", "Standup Special: Bangalore Humor", "Show", "Comedy", "English", 65, 2025),
        ("C125", "Chennai Roast Arena", "Show", "Comedy", "Tamil", 40, 2026),
        ("C126", "Telugu Comedy Superstars", "Show", "Comedy", "Telugu", 30, 2025),
        ("C127", "Pune Pun Factory", "Show", "Comedy", "Marathi", 30, 2025),
        ("C128", "College Boys Chaos", "Movie", "Comedy", "Hindi", 115, 2024),
        
        # Action
        ("C129", "Tiger Underground Strike", "Movie", "Action", "Hindi", 155, 2025),
        ("C130", "Vikram: Shadow Commander", "Movie", "Action", "Tamil", 165, 2024),
        ("C131", "Devara Storm Rising", "Movie", "Action", "Telugu", 160, 2025),
        ("C132", "Commando Force Mumbai", "Series", "Action", "Hindi", 42, 2026),
        ("C133", "Rudra: The Edge of Darkness", "Series", "Action", "Hindi", 48, 2024),
        ("C134", "Night Hunter Squad", "Movie", "Action", "English", 130, 2025),
        ("C135", "Fighter Wing Alpha", "Movie", "Action", "Hindi", 145, 2025),
        ("C136", "Speed Street Heist", "Movie", "Action", "English", 120, 2024),
        
        # Reality
        ("C137", "Bigg Boss All-Stars Hindi", "Show", "Reality", "Hindi", 60, 2026),
        ("C138", "Bigg Boss Tamil Season 8", "Show", "Reality", "Tamil", 60, 2026),
        ("C139", "Bigg Boss Telugu Live", "Show", "Reality", "Telugu", 60, 2026),
        ("C140", "Dance India Dance Championship", "Show", "Reality", "Hindi", 50, 2025),
        ("C141", "Shark Pitch India S4", "Show", "Reality", "Hindi", 55, 2026),
        ("C142", "Master Chef Kitchen Wars", "Show", "Reality", "Hindi", 45, 2025),
        ("C143", "Roadies Quest", "Show", "Reality", "Hindi", 45, 2025),
        ("C144", "Koffee Spotlight Lounge", "Show", "Reality", "English", 45, 2025),
        
        # Kids & Animation
        ("C145", "Chhota Bheem Himalayan Tour", "Movie", "Kids", "Hindi", 85, 2025),
        ("C146", "Motu Patlu Space Adventure", "Movie", "Kids", "Hindi", 75, 2024),
        ("C147", "Little Singham Rescue Mission", "Series", "Kids", "Hindi", 20, 2026),
        ("C148", "Doraemon Magic Gadgets", "Series", "Kids", "Hindi", 20, 2025),
        ("C149", "Shinchan Laugh Club", "Series", "Kids", "Tamil", 20, 2025),
        ("C150", "Super Bheem Galactic Battle", "Series", "Kids", "Telugu", 22, 2026),
        
        # News & Documentary
        ("C151", "Daily Headlines 360", "News", "News", "Hindi", 30, 2026),
        ("C152", "Global Tech & Economy Report", "News", "News", "English", 25, 2026),
        ("C153", "India at 2030: Space Ambitions", "Show", "News", "English", 50, 2025),
        ("C154", "Elections Ground Pulse", "News", "News", "Hindi", 35, 2026),
        ("C155", "Wildlife Wonders: Western Ghats", "Show", "News", "English", 52, 2024),
        ("C156", "Cricket Icons: The Untold Story", "Show", "News", "Hindi", 45, 2025),
        ("C157", "Startup Founders Blueprint", "Show", "News", "English", 40, 2025),
        ("C158", "State Express News Tamil", "News", "News", "Tamil", 30, 2026),
        ("C159", "Bengal Morning Bulletin", "News", "News", "Bengali", 25, 2026),
        ("C160", "Maharashtra Maha News", "News", "News", "Marathi", 30, 2026)
    ]
    return content_list


def generate_events(users, content_list, num_events=7500):
    """Generate realistic OTT playback interaction events."""
    devices = ["Mobile", "Smart TV", "Web", "Tablet"]
    device_weights = [0.55, 0.25, 0.15, 0.05]
    
    # Content popularity weights: Sports, Reality, Drama have highest demand
    content_weight_map = {}
    for c in content_list:
        cid, title, ctype, genre, lang, duration, year = c
        if genre == "Sports":
            w = 3.5
        elif genre == "Reality":
            w = 2.8
        elif genre == "Drama":
            w = 2.4
        elif genre == "Action":
            w = 2.0
        elif genre == "Comedy":
            w = 1.8
        elif genre == "Kids":
            w = 1.2
        else: # News
            w = 0.8
        content_weight_map[cid] = w

    c_ids = [c[0] for c in content_list]
    c_weights = [content_weight_map[cid] for cid in c_ids]
    
    # Map user id to subscription and age
    user_info = {u[0]: {"age": u[1], "plan": u[5], "city": u[3]} for u in users}
    u_ids = [u[0] for u in users]
    
    # Generate random activity tiers for users (80/20 rule: ~20% heavy watchers)
    user_activity_tier = {}
    for uid in u_ids:
        r = random.random()
        if r < 0.15:
            user_activity_tier[uid] = 4.0 # Super active
        elif r < 0.45:
            user_activity_tier[uid] = 2.0 # Moderate
        else:
            user_activity_tier[uid] = 0.8 # Casual
            
    events = []
    start_date = datetime(2026, 1, 1)
    
    for i in range(1, num_events + 1):
        event_id = f"E{10000 + i}"
        
        # Select user with activity weight
        uid = random.choices(u_ids, weights=[user_activity_tier[u] for u in u_ids])[0]
        u_data = user_info[uid]
        
        # Select content
        cid = random.choices(c_ids, weights=c_weights)[0]
        content_item = next(c for c in content_list if c[0] == cid)
        _, title, ctype, genre, lang, total_duration, year = content_item
        
        device = random.choices(devices, weights=device_weights)[0]
        
        # Realistic watch duration & completion calculation
        # Smart TV users tend to watch longer than Mobile users
        device_multiplier = {"Smart TV": 1.25, "Web": 1.0, "Tablet": 1.1, "Mobile": 0.85}[device]
        
        # Premium users watch slightly more
        plan_multiplier = {"Premium": 1.2, "VIP": 1.05, "Free": 0.9}[u_data["plan"]]
        
        # Base completion tendency
        completion_chance = 0.45 * (device_multiplier / 1.0) * (plan_multiplier / 1.0)
        
        is_completed = 1 if random.random() < completion_chance else 0
        
        if is_completed == 1:
            # Watched almost full duration (90% to 100%)
            watch_duration = int(total_duration * random.uniform(0.90, 1.0))
            event_type = "complete"
        else:
            # Watched partial (10% to 75% of content duration)
            watch_duration = max(2, int(total_duration * random.uniform(0.10, 0.75) * (device_multiplier / 1.1)))
            event_type = "pause" if random.random() < 0.65 else "play"
            
        watch_duration = min(watch_duration, total_duration)
        
        # Random event timestamp over past 60 days
        event_date = (start_date + timedelta(days=random.randint(0, 59))).strftime("%Y-%m-%d")
        
        events.append((event_id, uid, cid, event_type, event_date, device, watch_duration, is_completed))
        
    return events


def generate_experiment(users, num_experiment_users=600):
    """
    Generate Control vs Treatment experiment table.
    Simulating an A/B test on a new 'Personalized AI Content Tray' on the Home Feed.
    Treatment group shows higher sessions, higher avg watch duration, and higher completion rate.
    """
    sampled_users = random.sample(users, min(num_experiment_users, len(users)))
    
    experiment_records = []
    exp_id = "EXP_HOMEPAGE_TRAY_V2"
    
    for i, user in enumerate(sampled_users):
        uid = user[0]
        # 50/50 split
        group_name = "Treatment" if i % 2 == 0 else "Control"
        
        if group_name == "Control":
            # Baseline behavior
            sessions = random.randint(3, 14)
            # Avg session length around 22-38 mins
            watch_duration = sum(random.randint(15, 45) for _ in range(sessions))
            # Completion rate around 35-42%
            completed = int(sessions * random.uniform(0.30, 0.45))
        else:
            # Treatment behavior: Uplift (+12% to +18% watch time and completion)
            sessions = random.randint(4, 16)
            watch_duration = sum(random.randint(20, 55) for _ in range(sessions))
            completed = int(sessions * random.uniform(0.42, 0.60))
            
        experiment_records.append((exp_id, uid, group_name, sessions, watch_duration, completed))
        
    return experiment_records


def save_raw_csv(events, users, content_list):
    """Export a consolidated raw dataset representing incoming event stream."""
    os.makedirs(os.path.dirname(RAW_DATA_PATH), exist_ok=True)
    
    u_map = {u[0]: u for u in users}
    c_map = {c[0]: c for c in content_list}
    
    headers = [
        "event_id", "user_id", "content_id", "event_type", "event_date", "device",
        "watch_duration", "completed", "age_group", "gender", "city", "state",
        "subscription_plan", "content_title", "content_type", "genre", "language", "content_duration"
    ]
    
    with open(RAW_DATA_PATH, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for ev in events:
            eid, uid, cid, etype, edate, dev, wdur, comp = ev
            u = u_map[uid]
            c = c_map[cid]
            # row format
            row = [
                eid, uid, cid, etype, edate, dev, wdur, comp,
                u[1], u[2], u[3], u[4], u[5],
                c[1], c[2], c[3], c[4], c[5]
            ]
            writer.writerow(row)
            
    print(f" Raw events CSV saved to: {RAW_DATA_PATH} ({len(events)} rows)")


def create_and_populate_db():
    """Create SQLite database and tables."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f" Existing database removed: {DB_PATH}")
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Users table
    cursor.execute("""
    CREATE TABLE users (
        user_id TEXT PRIMARY KEY,
        age_group TEXT NOT NULL,
        gender TEXT NOT NULL,
        city TEXT NOT NULL,
        state TEXT NOT NULL,
        subscription_plan TEXT NOT NULL,
        signup_date TEXT NOT NULL
    );
    """)
    
    # 2. Content table
    cursor.execute("""
    CREATE TABLE content (
        content_id TEXT PRIMARY KEY,
        content_title TEXT NOT NULL,
        content_type TEXT NOT NULL,
        genre TEXT NOT NULL,
        language TEXT NOT NULL,
        content_duration INTEGER NOT NULL,
        release_year INTEGER NOT NULL
    );
    """)
    
    # 3. Events table
    cursor.execute("""
    CREATE TABLE events (
        event_id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        content_id TEXT NOT NULL,
        event_type TEXT NOT NULL,
        event_date TEXT NOT NULL,
        device TEXT NOT NULL,
        watch_duration INTEGER NOT NULL,
        completed INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (content_id) REFERENCES content(content_id)
    );
    """)
    
    # 4. Experiment results table
    cursor.execute("""
    CREATE TABLE experiment_results (
        experiment_id TEXT NOT NULL,
        user_id TEXT NOT NULL,
        group_name TEXT NOT NULL,
        sessions INTEGER NOT NULL,
        watch_duration INTEGER NOT NULL,
        completed INTEGER NOT NULL,
        PRIMARY KEY (experiment_id, user_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    """)
    
    print(" Database tables created successfully.")
    
    # Generate data
    users_data = generate_users(750)
    content_data = generate_content()
    events_data = generate_events(users_data, content_data, 7500)
    experiment_data = generate_experiment(users_data, 600)
    
    # Insert data
    cursor.executemany("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?);", users_data)
    cursor.executemany("INSERT INTO content VALUES (?, ?, ?, ?, ?, ?, ?);", content_data)
    cursor.executemany("INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, ?);", events_data)
    cursor.executemany("INSERT INTO experiment_results VALUES (?, ?, ?, ?, ?, ?);", experiment_data)
    
    conn.commit()
    
    # Save raw CSV
    save_raw_csv(events_data, users_data, content_data)
    
    # Verify counts
    cursor.execute("SELECT COUNT(*) FROM users;")
    u_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM content;")
    c_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM events;")
    e_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM experiment_results;")
    exp_count = cursor.fetchone()[0]
    
    conn.close()
    
    print("\n=======================================================")
    print(" DATABASE SETUP COMPLETE")
    print("=======================================================")
    print(f"Database Location: {DB_PATH}")
    print(f"Users records:             {u_count}")
    print(f"Content records:           {c_count}")
    print(f"Events records:            {e_count}")
    print(f"Experiment records:        {exp_count}")
    print("=======================================================\n")

if __name__ == "__main__":
    create_and_populate_db()
