import sqlite3
import hashlib
import os
from datetime import datetime

# ensure data folder exists
os.makedirs("data", exist_ok=True)

def get_connection():
    conn = sqlite3.connect("data/voting_app.db", check_same_thread=False)
    cursor = conn.cursor()
    return conn, cursor


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ---------------- CREATE TABLES ----------------
def create_tables():

    conn, cursor = get_connection()

    # USERS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        roll_no TEXT PRIMARY KEY,
        name TEXT,
        password TEXT,
        email TEXT,
        phone TEXT,
        image TEXT,
        has_voted INTEGER DEFAULT 0
    )
    """)

    # CANDIDATES TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidates (
        candidate_name TEXT,
        roll_no TEXT PRIMARY KEY,
        department TEXT,
        year_sem TEXT,
        role TEXT,
        image TEXT,
        votes INTEGER DEFAULT 0
    )
    """)

    # RESET BLOCKCHAIN TABLE (important fix)
    cursor.execute("DROP TABLE IF EXISTS blockchain")

    cursor.execute("""
    CREATE TABLE blockchain (
        vote_id INTEGER PRIMARY KEY AUTOINCREMENT,
        roll_no TEXT,
        candidate TEXT,
        vote_hash TEXT,
        previous_hash TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()


# ---------------- ADD USER ----------------
def add_user(roll_no, name, password, email, phone, image):

    conn, cursor = get_connection()

    try:

        cursor.execute("""
        INSERT INTO users
        (roll_no,name,password,email,phone,image,has_voted)
        VALUES (?,?,?,?,?,?,0)
        """,
        (roll_no,name,hash_password(password),email,phone,image)
        )

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()


# ---------------- AUTH USER ----------------
def authenticate_user(roll_no, password):

    conn, cursor = get_connection()

    cursor.execute(
        "SELECT * FROM users WHERE roll_no=? AND password=?",
        (roll_no, hash_password(password))
    )

    row = cursor.fetchone()

    conn.close()

    if row:

        return {
            "roll_no": row[0],
            "name": row[1],
            "email": row[3],
            "phone": row[4],
            "image": row[5],
            "has_voted": row[6]
        }

    return None


# ---------------- BLOCKCHAIN RECORD ----------------
def record_vote_block(roll_no, candidate):

    conn, cursor = get_connection()

    cursor.execute(
        "SELECT vote_hash FROM blockchain ORDER BY vote_id DESC LIMIT 1"
    )

    last = cursor.fetchone()

    previous_hash = last[0] if last else "GENESIS"

    vote_string = roll_no + candidate + previous_hash + datetime.now().isoformat()

    vote_hash = hashlib.sha256(vote_string.encode()).hexdigest()

    cursor.execute("""
    INSERT INTO blockchain
    (roll_no,candidate,vote_hash,previous_hash,timestamp)
    VALUES (?,?,?,?,?)
    """,
    (roll_no,candidate,vote_hash,previous_hash,datetime.now().isoformat())
    )

    conn.commit()
    conn.close()
