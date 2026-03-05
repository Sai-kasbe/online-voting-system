import streamlit as st
import pandas as pd
import os
from database import create_tables, add_user, authenticate_user, get_connection

# Ensure image folder exists
os.makedirs("images", exist_ok=True)

st.set_page_config(page_title="KGRCET ONLINE ELECTION SYSTEM", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>
body { background-color:#0D1B2A; color:white; }
.stButton>button {
background-color:#1B263B;
color:white;
border-radius:10px;
}
h1,h2,h3 { color:#E0E1DD; }
</style>
""", unsafe_allow_html=True)


# ---------------- ADMIN ----------------
ADMIN_ID = "22QM1A6721"
ADMIN_PASS = "Sai7@99499"


# ---------------- USER LOGIN ----------------
def user_login():

    st.subheader("User Login")

    roll = st.text_input("Roll Number")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        user = authenticate_user(roll, password)

        if user:
            st.session_state.user_logged_in = True
            st.session_state.user_data = user
            st.rerun()
        else:
            st.error("Invalid credentials")


# ---------------- USER DASHBOARD ----------------
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

        df = pd.read_sql("SELECT * FROM candidates", conn)

        if df.empty:
            st.warning("No candidates available")

        for _, row in df.iterrows():

            with st.expander(row["candidate_name"]):

                c1, c2 = st.columns([1,3])

                with c1:
                    if row["image"]:
                        st.image(row["image"], width=100)

                with c2:
                    st.write("Department:", row["department"])
                    st.write("Year:", row["year_sem"])
                    st.write("Role:", row["role"])

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

                    st.success("Vote cast successfully")

                    st.session_state.user_data["has_voted"] = 1
                    st.rerun()

        conn.close()


# ---------------- ADMIN LOGIN ----------------
def admin_login():

    st.subheader("Admin Login")

    user = st.text_input("Admin ID")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if user == ADMIN_ID and password == ADMIN_PASS:
            st.session_state.admin_logged_in = True
            st.rerun()
        else:
            st.error("Invalid admin login")


# ---------------- ADMIN DASHBOARD ----------------
def admin_dashboard():

    st.header("Admin Dashboard")

    tab1, tab2 = st.tabs(["Add Candidate","Users"])

    with tab1:

        name = st.text_input("Candidate Name")
        roll = st.text_input("Roll Number")
        dept = st.text_input("Department")
        year = st.text_input("Year/Sem")
        role = st.selectbox("Role",["President","Vice President","Secretary"])

        image = st.file_uploader("Upload Image")

        if st.button("Add Candidate"):

            image_path = None

            if image is not None:

                image_path = "images/" + image.name

                with open(image_path,"wb") as f:
                    f.write(image.getbuffer())

            conn, cursor = get_connection()

            cursor.execute("""
            INSERT INTO candidates
            (candidate_name,roll_no,department,year_sem,role,image,votes)
            VALUES (?,?,?,?,?,?,0)
            """,(name,roll,dept,year,role,image_path))

            conn.commit()

            st.success("Candidate added")


    with tab2:

        conn,_ = get_connection()

        df = pd.read_sql(
        "SELECT roll_no,name,email,phone,has_voted FROM users",
        conn
        )

        st.dataframe(df)


# ---------------- REGISTER ----------------
def register():

    st.subheader("Register")

    name = st.text_input("Full Name")
    roll = st.text_input("Roll Number")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    password = st.text_input("Password", type="password")

    image = st.file_uploader("Upload Image")

    if st.button("Register"):

        image_path = None

        if image is not None:

            image_path = "images/" + image.name

            with open(image_path,"wb") as f:
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
            st.success("Registration successful")
        else:
            st.error("User already exists")


# ---------------- MAIN ----------------
def main():

    st.title("KGRCET ONLINE ELECTION SYSTEM")

    create_tables()

    if "user_logged_in" not in st.session_state:
        st.session_state.user_logged_in = False

    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False


    if st.session_state.user_logged_in:

        user_dashboard(st.session_state.user_data)

        if st.button("Logout"):
            st.session_state.user_logged_in = False
            st.rerun()

    elif st.session_state.admin_logged_in:

        admin_dashboard()

        if st.button("Logout"):
            st.session_state.admin_logged_in = False
            st.rerun()

    else:

        page = st.sidebar.selectbox(
        "Menu",
        ["Home","User Login","Admin Login","Register"]
        )

        if page == "User Login":
            user_login()

        elif page == "Admin Login":
            admin_login()

        elif page == "Register":
            register()

        else:
            st.write("Welcome to KGRCET Secure Voting System")


if __name__ == "__main__":
    main()
