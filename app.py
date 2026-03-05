import streamlit as st
import pandas as pd
import os
from database import create_tables, add_user, authenticate_user, get_connection

# ---------- CONFIG ----------
st.set_page_config(page_title="KGRCET ONLINE ELECTION SYSTEM", layout="wide")

os.makedirs("images", exist_ok=True)

# ---------- STYLE ----------
st.markdown("""
<style>
body {background-color:#0D1B2A;color:white;}
.stButton>button {
background-color:#1B263B;
color:white;
border-radius:10px;
padding:0.5rem 1rem;
}
.card {
background-color:#1B263B;
padding:15px;
border-radius:10px;
margin-bottom:10px;
}
</style>
""", unsafe_allow_html=True)

# ---------- ADMIN LOGIN ----------
ADMIN_ID = "22QM1A6721"
ADMIN_PASS = "Sai7@99499"


# ---------- HOME ----------
def home():

    st.title("KGRCET ONLINE ELECTION SYSTEM")

    st.markdown("""
This platform enables **secure digital elections** using blockchain-style hashing.

### Features
• Secure authentication  
• One person one vote  
• Admin managed candidates  
• Blockchain vote hashing  
• Transparent election results  

### Demo Credentials
Admin  
ID: 22QM1A6721  
Password: Sai7@99499
""")

    st.image("https://images.unsplash.com/photo-1551836022-d5d88e9218df")


# ---------- USER LOGIN ----------
def user_login():

    st.header("User Login")

    roll = st.text_input("Roll Number")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        user = authenticate_user(roll, password)

        if user:
            st.session_state.user = user
            st.session_state.logged = True
            st.rerun()

        else:
            st.error("Invalid login")


# ---------- USER DASHBOARD ----------
def user_dashboard():

    user = st.session_state.user

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

    if user["has_voted"] == 1:
        st.success("You already voted")
        return

    st.subheader("Cast Your Vote")

    conn, cursor = get_connection()

    df = pd.read_sql("SELECT * FROM candidates", conn)

    if df.empty:
        st.warning("No candidates available")

    for _, row in df.iterrows():

        with st.container():

            col1, col2 = st.columns([1,3])

            with col1:
                if row["image"]:
                    st.image(row["image"], width=120)

            with col2:
                st.markdown(f"### {row['candidate_name']}")
                st.write("Department:", row["department"])
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

                    st.success("Vote recorded")

                    st.session_state.user["has_voted"] = 1
                    st.rerun()

    conn.close()


# ---------- ADMIN LOGIN ----------
def admin_login():

    st.header("Admin Login")

    user = st.text_input("Admin ID")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if user == ADMIN_ID and password == ADMIN_PASS:

            st.session_state.admin = True
            st.rerun()

        else:
            st.error("Invalid admin credentials")


# ---------- ADMIN DASHBOARD ----------
def admin_dashboard():

    st.header("Admin Dashboard")

    tab1, tab2 = st.tabs(["Add Candidate","Users"])

    with tab1:

        name = st.text_input("Candidate Name")
        roll = st.text_input("Roll Number")
        dept = st.text_input("Department")
        year = st.text_input("Year/Sem")

        role = st.selectbox(
        "Role",
        ["President","Vice President","Secretary"]
        )

        image = st.file_uploader("Upload Image")

        if st.button("Add Candidate"):

            path = None

            if image is not None:

                path = "images/" + image.name

                with open(path,"wb") as f:
                    f.write(image.getbuffer())

            conn, cursor = get_connection()

            cursor.execute("""
            INSERT INTO candidates
            (candidate_name,roll_no,department,year_sem,role,image,votes)
            VALUES (?,?,?,?,?,?,0)
            """,(name,roll,dept,year,role,path))

            conn.commit()

            st.success("Candidate added")


    with tab2:

        conn,_ = get_connection()

        df = pd.read_sql(
        "SELECT roll_no,name,email,phone,has_voted FROM users",
        conn
        )

        st.dataframe(df)


# ---------- REGISTER ----------
def register():

    st.header("Register")

    name = st.text_input("Full Name")
    roll = st.text_input("Roll Number")
    email = st.text_input("Email")
    phone = st.text_input("Phone")

    password = st.text_input("Password", type="password")

    image = st.file_uploader("Upload Image")

    if st.button("Register"):

        path = None

        if image is not None:

            path = "images/" + image.name

            with open(path,"wb") as f:
                f.write(image.getbuffer())

        success = add_user(
            roll,
            name,
            password,
            email,
            phone,
            path
        )

        if success:
            st.success("Registration successful")

        else:
            st.error("User already exists")


# ---------- RESULTS ----------
def results():

    st.header("Election Results")

    conn,_ = get_connection()

    df = pd.read_sql(
    "SELECT candidate_name,votes FROM candidates",
    conn
    )

    if df.empty:

        st.warning("No results yet")

        return

    st.dataframe(df)

    st.bar_chart(df.set_index("candidate_name"))


# ---------- BLOCKCHAIN ----------
def transparency():

    st.header("Vote Transparency")

    conn,_ = get_connection()

    df = pd.read_sql(
    "SELECT vote_id,roll_no,candidate,vote_hash,timestamp FROM blockchain",
    conn
    )

    if df.empty:

        st.warning("No votes recorded")

        return

    st.dataframe(df)


# ---------- MAIN ----------
def main():

    create_tables()

    if "logged" not in st.session_state:
        st.session_state.logged = False

    if "admin" not in st.session_state:
        st.session_state.admin = False


    menu = st.sidebar.selectbox(
    "Menu",
    [
    "Home",
    "User Login",
    "Admin Login",
    "Register",
    "Results",
    "Vote Transparency"
    ]
    )


    if st.session_state.logged:

        user_dashboard()

        if st.button("Logout"):

            st.session_state.logged = False
            st.rerun()

        return


    if st.session_state.admin:

        admin_dashboard()

        if st.button("Logout"):

            st.session_state.admin = False
            st.rerun()

        return


    if menu == "Home":
        home()

    elif menu == "User Login":
        user_login()

    elif menu == "Admin Login":
        admin_login()

    elif menu == "Register":
        register()

    elif menu == "Results":
        results()

    elif menu == "Vote Transparency":
        transparency()


if __name__ == "__main__":
    main()
