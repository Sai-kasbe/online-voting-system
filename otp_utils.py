import smtplib
import random
import os
from email.message import EmailMessage


# ===== EMAIL CONFIGURATION =====
# Use environment variables for security
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "your_email@gmail.com")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "your_app_password")


# ===== OTP GENERATOR =====
def generate_otp(length=6):
    """Generate numeric OTP"""
    return "".join([str(random.randint(0, 9)) for _ in range(length)])


# ===== SEND OTP EMAIL =====
def send_otp_email(receiver_email, otp):
    """
    Sends OTP to the given email address.
    Returns True if successful, else returns error message.
    """

    msg = EmailMessage()

    msg["Subject"] = "OTP Verification - KGRCET Voting System"
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email

    msg.set_content(f"""
Hello,

Your OTP for the KGRCET Online Voting System is:

{otp}

This OTP is valid for a short time.

If you did not request this, please ignore this email.

Regards,
KGRCET Voting System
""")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)

        return True

    except Exception as e:
        return f"Error sending email: {str(e)}"
