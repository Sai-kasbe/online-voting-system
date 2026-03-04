import streamlit as st
import pandas as pd
import sqlite3
import hashlib
from datetime import datetime
import os
from database import add_user

# ===== CONFIG =====
st.set_page_config(page_title="KGRCET ONLINE ELECTION SYSTEM", layout="wide")

# ===== UI STYLE =====
st.markdown("""
<style>
body { background-color: #0D1B2A; color: white; }
.stButton>button {
    background-color: #1B263B;
    color: white;
    border-radius: 10px;
    padding: 0.5rem 1.5rem;
    margin-top: 10px;
}
h1, h2, h3, h4 {
    color: #E0E1DD;
}
</style>
""", unsafe_allow_html=True)

# ===== DATABASE =====
def get_connection():
    conn = sqlite3.connect("voting_app.db", check_same_thread=False)
    return conn, conn.cursor()

def create_tables():
    conn, cursor = get_connection()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users(
        roll_no TEXT PRIMARY KEY,
        name TEXT,
        password TEXT,
        email TEXT,
        phone TEXT,
        image TEXT,
        has_voted INTEGER DEFAULT 0
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS candidates(
        candidate_name TEXT,
        roll_no TEXT PRIMARY KEY,
        department TEXT,
        year_sem TEXT,
        role TEXT,
        image TEXT,
        votes INTEGER DEFAULT 0
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS result_schedule(
        id INTEGER PRIMARY KEY,
        result_date TEXT,
        is_announced INTEGER DEFAULT 0
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS blockchain(
        vote_id INTEGER PRIMARY KEY AUTOINCREMENT,
        roll_no TEXT,
        candidate TEXT,
        vote_hash TEXT,
        timestamp TEXT
    )''')

    conn.commit()
    conn.close()

# ===== SECURITY =====
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ===== AUTH =====
def authenticate_user(roll_no, password):
    conn, cursor = get_connection()
    cursor.execute(
        "SELECT * FROM users WHERE roll_no=? AND password=?",
        (roll_no, hash_password(password))
    )
    row = cursor.fetchone()

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

# ===== BLOCKCHAIN LOG =====
def record_vote_hash(roll_no, candidate):
    vote_string = roll_no + candidate + datetime.now().isoformat()
    vote_hash = hashlib.sha256(vote_string.encode()).hexdigest()

    conn, cursor = get_connection()

    cursor.execute(
        "INSERT INTO blockchain (roll_no,candidate,vote_hash,timestamp) VALUES (?,?,?,?)",
        (roll_no, candidate, vote_hash, datetime.now().isoformat())
    )

    conn.commit()
    conn.close()

# ===== ADMIN =====
ADMIN_ID = "22QM1A6721"
ADMIN_PASS = hash_password("Sai7@99499")

# ===== USER LOGIN =====
def user_login():
    st.subheader("User Login")

    roll_no = st.text_input("Roll Number")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = authenticate_user(roll_no, password)

        if user:
            st.session_state.user_logged_in = True
            st.session_state.user_data = user
            st.rerun()
        else:
            st.error("Invalid credentials")

# ===== USER DASHBOARD =====
def user_dashboard(user):

    st.header("Voter Dashboard")

    col1, col2 = st.columns([1,2])

    with col1:
        if user["image"]:
            st.image(user["image"], width=150)

    with col2:
        st.write("Name:", user["name"])
        st.write("Roll:", user["roll_no"])
        st.write("Email:", user["email"])
        st.write("Phone:", user["phone"])

    if user["has_voted"] == 0:

        st.subheader("Cast Vote")

        conn, cursor = get_connection()

        candidates = pd.read_sql("SELECT * FROM candidates", conn)

        for _, row in candidates.iterrows():

            with st.expander(row["candidate_name"]):

                col1, col2 = st.columns([1,3])

                with col1:
                    st.image(row["image"], width=100)

                with col2:
                    st.write("Department:",row["department"])
                    st.write("Year:",row["year_sem"])
                    st.write("Role:",row["role"])

                if st.button("Vote", key=row["roll_no"]):

                    cursor.execute(
                        "UPDATE candidates SET votes=votes+1 WHERE roll_no=?",
                        (row["roll_no"],)
                    )

                    cursor.execute(
                        "UPDATE users SET has_voted=1 WHERE roll_no=?",
                        (user["roll_no"],)
                    )

                    conn.commit()

                    record_vote_hash(user["roll_no"], row["candidate_name"])

                    st.success("Vote Cast Successfully")

                    st.session_state.user_data["has_voted"]=1
                    st.rerun()

        conn.close()

    # RESULTS
    conn, cursor = get_connection()

    result = cursor.execute("SELECT * FROM result_schedule").fetchone()

    if result and result[2]==1:

        st.subheader("Election Results")

        result_df = pd.read_sql(
            "SELECT candidate_name,role,votes FROM candidates ORDER BY votes DESC",
            conn
        )

        st.dataframe(result_df)

    conn.close()

# ===== ADMIN LOGIN =====
def admin_login():

    st.subheader("Admin Login")

    username = st.text_input("Admin ID")
    password = st.text_input("Password",type="password")

    if st.button("Login"):

        if username==ADMIN_ID and hash_password(password)==ADMIN_PASS:

            st.session_state.admin_logged_in=True
            st.rerun()

        else:
            st.error("Invalid admin credentials")

# ===== ADMIN DASHBOARD =====
def admin_dashboard():

    st.header("Admin Dashboard")

    tab1,tab2,tab3 = st.tabs([
        "Add Candidate",
        "Users",
        "Results"
    ])

    # ADD CANDIDATE
    with tab1:

        name=st.text_input("Candidate Name")
        roll=st.text_input("Roll Number")
        dept=st.text_input("Department")
        year=st.text_input("Year/Sem")
        role=st.selectbox("Role",["President","Vice President","Secretary"])

        image=st.file_uploader("Upload Image")

        if st.button("Add Candidate"):

            os.makedirs("images",exist_ok=True)

            path="images/"+image.name

            with open(path,"wb") as f:
                f.write(image.getbuffer())

            conn,cursor=get_connection()

            cursor.execute("""
            INSERT INTO candidates VALUES(?,?,?,?,?,?,0)
            """,(name,roll,dept,year,role,path))

            conn.commit()

            st.success("Candidate Added")

    # USERS
    with tab2:

        conn,_=get_connection()

        df=pd.read_sql("SELECT * FROM users",conn)

        st.dataframe(df)

    # RESULTS
    with tab3:

        conn,cursor=get_connection()

        date=st.date_input("Result Date")

        if st.button("Schedule Result"):

            cursor.execute("""
            INSERT OR REPLACE INTO result_schedule
            VALUES(1,?,0)
            """,(str(date),))

            conn.commit()

            st.success("Result Scheduled")

        if st.button("Announce Result"):

            cursor.execute("""
            UPDATE result_schedule SET is_announced=1
            """)

            conn.commit()

            st.success("Result Announced")

# ===== REGISTER =====
def register():

    st.subheader("Register")

    name=st.text_input("Name")
    roll=st.text_input("Roll Number")
    email=st.text_input("Email")
    phone=st.text_input("Phone")
    password=st.text_input("Password",type="password")

   image = st.file_uploader("Upload Image")

if st.button("Register"):

    if image is None:
        st.error("Please upload an image")
        return

    os.makedirs("images", exist_ok=True)

    image_path = "images/" + image.name

    with open(image_path, "wb") as f:
        f.write(image.getbuffer())

    success = add_user(
        roll,
        name,
        password,
        email,
        phone,
        image_path
    )

    if success:
        st.success("Registered Successfully")
    else:
        st.error("User already exists")
        if success:
            st.success("Registered Successfully")
        else:
            st.error("User already exists")

# ===== MAIN =====
def main():

    st.title("KGRCET ONLINE ELECTION SYSTEM")

    create_tables()

    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in=False

    if "user_logged_in" not in st.session_state:
        st.session_state.user_logged_in=False

    if st.session_state.user_logged_in:

        user_dashboard(st.session_state.user_data)

        if st.button("Logout"):
            st.session_state.user_logged_in=False
            st.rerun()

    elif st.session_state.admin_logged_in:

        admin_dashboard()

        if st.button("Logout"):
            st.session_state.admin_logged_in=False
            st.rerun()

    else:

        page=st.sidebar.selectbox(
            "Menu",
            ["Home","User Login","Admin Login","Register"]
        )

        if page=="User Login":
            user_login()

        elif page=="Admin Login":
            admin_login()

        elif page=="Register":
            register()

        else:
            st.write("Welcome to KGRCET Blockchain Voting System")

if __name__=="__main__":
    main()

