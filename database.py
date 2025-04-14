import sqlite3

DB_FILE = "pakistan_connect.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            city TEXT,
            country TEXT,
            job_title TEXT,
            industry TEXT,
            experience INTEGER,
            expertise TEXT,
            help_areas TEXT,
            linkedin TEXT,
            UNIQUE(email, phone)
        )
    ''')
    conn.commit()
    conn.close()

def save_user(name, email, phone, city, country, job_title, industry, experience, expertise, help_areas, linkedin):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO users
        (id, name, email, phone, city, country, job_title, industry, experience, expertise, help_areas, linkedin)
        VALUES (
            (SELECT id FROM users WHERE email=? AND phone=?),
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
    ''', (email, phone, name, email, phone, city, country, job_title, industry, experience, expertise, help_areas, linkedin))
    conn.commit()
    conn.close()

def get_user_by_keys(email, phone):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email=? AND phone=?', (email, phone))
    user = cursor.fetchone()
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

def get_all_users():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()
    conn.close()
    return rows
