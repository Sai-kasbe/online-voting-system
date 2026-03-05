# 🗳️ Blockchain-Based Online Voting System

A **secure, transparent, and decentralized-inspired online voting platform** developed using **Python, Streamlit, SQLite, and blockchain-style vote hashing**.

This system allows voters to **register, log in, and cast votes securely**, while administrators can **manage candidates, monitor election activity, and publish results**.
To ensure transparency and tamper resistance, each vote is recorded with a **cryptographic hash chain inspired by blockchain technology**.

---

# 🌐 Live Application

🔗 **Live Demo:**
[https://online-voting-system-kdlgdtqbpwnfmcvnckmlkb.streamlit.app](https://online-voting-system-kdlgdtqbpwnfmcvnckmlkb.streamlit.app)

This application is deployed using **Streamlit Cloud** and can be accessed directly through a web browser.

---

# 📌 Project Objective

Traditional voting systems face challenges such as:

* Lack of transparency
* Vote tampering risks
* Manual vote counting
* Limited accessibility
* Security concerns

The objective of this project is to design a **secure digital voting system** that:

* Ensures **one voter – one vote**
* Provides **transparent vote tracking**
* Uses **cryptographic hashing for vote integrity**
* Allows **real-time result monitoring**
* Improves **accessibility through web technology**

---

# 🚀 Key Features

## 🔐 Secure Authentication

* User registration with unique roll number
* Secure password hashing using **SHA-256**
* Admin and voter login systems

---

## 👤 Voter Registration System

Voters can register using:

* Full Name
* Roll Number
* Email
* Phone Number
* Password
* Profile Image

The system validates user input before storing data securely.

---

## 🧑‍💼 Admin Dashboard

The administrator has full control over the election system.

Admin can:

* Add candidates
* View registered voters
* Manage election data
* Monitor voting activity
* Publish election results

---

## 🗳️ Candidate Management

Admin can add candidates with:

* Candidate name
* Roll number
* Department
* Year/Semester
* Election role
* Candidate image

Supported election roles include:

* President
* Vice President
* Secretary
* Treasurer

---

## 🛑 One-Person-One-Vote Rule

Each registered user can vote **only once**.

Once a vote is cast:

* The database updates `has_voted = 1`
* The voter cannot vote again
* This prevents duplicate votes

---

## 🔗 Blockchain-Inspired Vote Transparency

Each vote is stored as a **block containing cryptographic hashes**.

Every block contains:

* Voter roll number
* Candidate selected
* Vote hash
* Previous vote hash
* Timestamp

This creates a **chain of votes similar to blockchain**.

Example:

| Vote ID | Roll No    | Candidate   | Vote Hash | Previous Hash |
| ------- | ---------- | ----------- | --------- | ------------- |
| 1       | 22QM1A6722 | Candidate A | hash1     | GENESIS       |
| 2       | 22QM1A6733 | Candidate B | hash2     | hash1         |

This ensures:

✔ Tamper detection
✔ Data transparency
✔ Vote verification

---

## 📊 Election Result System

The system calculates votes automatically and displays:

* Candidate names
* Election roles
* Total votes received

Results are displayed in a **clean table format**.

Future improvement can include **graphical charts and analytics**.

---

# 🧠 Blockchain Concept Used

Although this project does not implement a **distributed blockchain network**, it uses important blockchain principles:

### Cryptographic Hashing

Each vote is hashed using **SHA-256**.

```
vote_hash = SHA256(roll_no + candidate + timestamp)
```

---

### Hash Linking

Every block stores the **previous block's hash**.

```
previous_hash → vote_hash → next_hash
```

This ensures that **changing one vote breaks the entire chain**.

---

### Transparency Layer

Users can view the **Vote Transparency page** where all vote blocks are displayed.

This increases trust in the election process.

---

# 🛠️ Technology Stack

| Technology      | Purpose                   |
| --------------- | ------------------------- |
| Python          | Backend programming       |
| Streamlit       | Web application framework |
| SQLite          | Database storage          |
| Pandas          | Data analysis             |
| SHA-256         | Cryptographic hashing     |
| Streamlit Cloud | Web deployment            |

---

# 📂 Project Folder Structure

```
online-voting-system
│
├── app.py
│       Main Streamlit application
│
├── database.py
│       Database management functions
│
├── otp_utils.py
│       OTP email verification utilities
│
├── requirements.txt
│       Python dependencies
│
├── data/
│       SQLite database storage
│       voting_app.db
│
├── images/
│       Uploaded user and candidate images
│
└── README.md
        Project documentation
```

---

# ⚙️ Installation Guide

## Step 1 — Clone the Repository

```
git clone https://github.com/Sai-kasbe/online-voting-system.git
```

---

## Step 2 — Navigate to Project Directory

```
cd online-voting-system
```

---

## Step 3 — Install Dependencies

```
pip install -r requirements.txt
```

---

## Step 4 — Run the Application

```
streamlit run app.py
```

---

## Step 5 — Open Browser

The application will run at:

```
http://localhost:8501
```

---

# 🔑 Demo Credentials

## Admin Login

```
Admin ID: 22QM1A6721
Password: Sai7@99499
```

---

## Voter Login

Users must **register first** to participate in voting.

---

# 📊 System Workflow

### Step 1

User registers with personal details.

↓

### Step 2

User logs in using roll number and password.

↓

### Step 3

User views available candidates.

↓

### Step 4

User casts vote.

↓

### Step 5

Vote is recorded in:

* Candidate vote count
* Blockchain vote log

↓

### Step 6

Admin monitors election activity.

↓

### Step 7

Results are displayed.

---

# 🔒 Security Measures

The system includes several security features:

### Password Hashing

Passwords are hashed using SHA-256.

---

### SQL Injection Prevention

Parameterized queries are used for database operations.

---

### One-Vote Restriction

Database flag prevents multiple voting.

---

### Blockchain Vote Logs

Ensures vote data integrity.

---

# 📈 Future Improvements

Possible enhancements for this system:

* OTP verification for voter registration
* Multi-factor authentication
* Smart contract integration
* Distributed blockchain network
* Graphical vote analytics
* Biometric voter authentication
* Mobile application support

---

# 🎓 Academic Relevance

This project demonstrates knowledge of:

* Blockchain concepts
* Secure web application development
* Database management
* Authentication systems
* Data transparency mechanisms

It is suitable for:

* **Computer Science final year projects**
* **Blockchain technology demonstrations**
* **Web development portfolios**

---

# 👨‍💻 Author

**Sai Kasbe**
Computer Science Engineer
Python Developer

GitHub Profile
[https://github.com/Sai-kasbe](https://github.com/Sai-kasbe)

---

# 📜 License

This project is developed for **educational and research purposes**.

It can be used for learning and demonstration of **secure digital voting systems**.

---

# ⭐ Support

If you found this project helpful:

⭐ Star the repository
🍴 Fork the project
📢 Share with others

---
