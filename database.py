import sqlite3
import hashlib
from datetime import datetime

# ===== Database Connection =====
def get_connection():
    conn = sqlite3.connect("voting_app.db", check_same_thread=False)
    cursor = conn.cursor()
    return conn, cursor


# ===== Password Hashing =====
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ===== Create Tables =====
def create_tables():
    conn, cursor = get_connection()

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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS result_schedule (
        id INTEGER PRIMARY KEY,
        result_date TEXT,
        is_announced INTEGER DEFAULT 0
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS blockchain (
        vote_id INTEGER PRIMARY KEY AUTOINCREMENT,
        roll_no TEXT,
        candidate TEXT,
        vote_hash TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()


# ===== Add User =====
def add_user(roll_no, name, password, email, phone, image):
    conn, cursor = get_connection()

    try:
        cursor.execute("""
        INSERT INTO users
        (roll_no, name, password, email, phone, image, has_voted)
        VALUES (?, ?, ?, ?, ?, ?, 0)
        """, (roll_no, name, hash_password(password), email, phone, image))

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


# ===== Authenticate User =====
def authenticate_user(roll_no, password):
    conn, cursor = get_connection()

    cursor.execute(
        "SELECT * FROM users WHERE roll_no=? AND password=?",
        (roll_no, hash_password(password))
    )

    user = cursor.fetchone()

    conn.close()

    if user:
        return {
            "roll_no": user[0],
            "name": user[1],
            "email": user[3],
            "phone": user[4],
            "image": user[5],
            "has_voted": user[6]
        }

    return None


# ===== Add Candidate =====
def add_candidate(name, roll_no, dept, year_sem, role, image):
    conn, cursor = get_connection()

    try:
        cursor.execute("""
        INSERT INTO candidates
        (candidate_name, roll_no, department, year_sem, role, image, votes)
        VALUES (?, ?, ?, ?, ?, ?, 0)
        """, (name, roll_no, dept, year_sem, role, image))

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


# ===== Record Vote =====
def cast_vote(user_roll, candidate_roll, candidate_name):

    conn, cursor = get_connection()

    cursor.execute(
        "SELECT has_voted FROM users WHERE roll_no=?",
        (user_roll,)
    )

    status = cursor.fetchone()

    if status and status[0] == 1:
        conn.close()
        return False

    cursor.execute(
        "UPDATE candidates SET votes=votes+1 WHERE roll_no=?",
        (candidate_roll,)
    )

    cursor.execute(
        "UPDATE users SET has_voted=1 WHERE roll_no=?",
        (user_roll,)
    )

    vote_string = user_roll + candidate_name + datetime.now().isoformat()

    vote_hash = hashlib.sha256(vote_string.encode()).hexdigest()

    cursor.execute("""
    INSERT INTO blockchain
    (roll_no,candidate,vote_hash,timestamp)
    VALUES (?,?,?,?)
    """, (user_roll, candidate_name, vote_hash, datetime.now().isoformat()))

    conn.commit()
    conn.close()

    return True


# ===== Get Candidates =====
def get_candidates():

    conn, cursor = get_connection()

    cursor.execute("SELECT * FROM candidates")

    data = cursor.fetchall()

    conn.close()

    return data


# ===== Get Results =====
def get_results():

    conn, cursor = get_connection()

    cursor.execute("""
    SELECT candidate_name, role, votes
    FROM candidates
    ORDER BY votes DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data
