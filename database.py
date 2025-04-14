import sqlite3

DB_NAME = "pakistan_connect.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            city TEXT,
            country TEXT,
            job_title TEXT,
            industry TEXT,
            experience_years INTEGER,
            expertise TEXT,
            help_areas TEXT,
            linkedin TEXT,
            UNIQUE(email, phone)
        )
    """)
    conn.commit()
    conn.close()

def add_user(data):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO users (name, email, phone, city, country, job_title, industry, experience_years, expertise, help_areas, linkedin)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, data)
        conn.commit()
        return True, "User added successfully."
    except sqlite3.IntegrityError:
        return False, "User with this email and phone already exists."
    finally:
        conn.close()

def update_user(data, email, phone):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        UPDATE users SET
            name = ?, city = ?, country = ?, job_title = ?, industry = ?,
            experience_years = ?, expertise = ?, help_areas = ?, linkedin = ?
        WHERE email = ? AND phone = ?
    """, data + (email, phone))
    conn.commit()
    conn.close()

def get_user(email, phone):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        SELECT * FROM users WHERE email = ? AND phone = ?
    """, (email, phone))
    user = c.fetchone()
    conn.close()
    return user

def search_users(query):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    pattern = f"%{query.lower()}%"
    cursor.execute('''
        SELECT * FROM users
        WHERE LOWER(name) LIKE ?
        OR LOWER(city) LIKE ?
        OR LOWER(job_title) LIKE ?
        OR LOWER(expertise) LIKE ?
        OR LOWER(help_areas) LIKE ?
    ''', (pattern, pattern, pattern, pattern, pattern))
    results = cursor.fetchall()
    conn.close()
    return results

