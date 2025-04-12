import streamlit as st
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ---------------------------
# Google Sheets Setup
# ---------------------------
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Wedding RSVP Responses").sheet1

# ---------------------------
# Streamlit Page Configuration
# ---------------------------
st.set_page_config(page_title="Craig & Ashmi's Wedding", page_icon="💍", layout="centered")

# ---------------------------
# Styling
# ---------------------------
st.markdown("""
    <style>
    .title {
        font-size: 80px;
        font-family: "Brush Script MT", cursive;
        text-align: center;
        color: #8b5e3c;
        margin-top: 20px;
    }
    .subtitle {
        font-size: 32px;
        font-family: "Brush Script MT", cursive;
        text-align: center;
        color: #444;
        margin-bottom: 30px;
    }
    .date-box {
        background-color: #fff5e6;
        border: 2px solid #ffddb0;
        padding: 12px 20px;
        border-radius: 10px;
        font-size: 20px;
        color: #8b5e3c;
        font-weight: bold;
        text-align: center;
        width: fit-content;
        margin: 0 auto;
    }
    .message {
        text-align: center;
        font-size: 18px;
        color: #333;
        max-width: 600px;
        margin: 30px auto 0 auto;
    }
    hr {
        border: none;
        border-top: 1px solid #e0c9a6;
        margin: 40px 0;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------
# Sidebar Navigation
# ---------------------------
page = st.sidebar.radio("Navigate", ["💒 Home", "💌 RSVP"])

# ---------------------------
# Home Page
# ---------------------------
if page == "💒 Home":
    st.markdown('<div class="title">Craig & Ashmi</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">'
        'Together with their families invite you to celebrate the union of their marriage'
        '</div>', unsafe_allow_html=True
    )

    st.markdown('<div class="date-box">Thursday 7th May 2026</div>', unsafe_allow_html=True)
    st.markdown('<div class="date-box" style="margin-top: 10px;">Ameres, Portugal</div>', unsafe_allow_html=True)

    st.markdown("""
    <p style='
        font-family: "Brush Script MT", cursive;
        font-size: 26px;
        color: #000;
        text-align: center;
        margin-top: 40px;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    '>
        We are excited to share this special day with you. <br/>
        Please RSVP using the menu on the left.
    </p>
""", unsafe_allow_html=True)
    

# ---------------------------
# RSVP Form Page
# ---------------------------
if page == "💌 RSVP":
    st.markdown('<div class="title">RSVP Form</div>', unsafe_allow_html=True)
    st.markdown("<hr />", unsafe_allow_html=True)

    full_name = st.text_input("Full Name", max_chars=100)
    email = st.text_input("Email Address", max_chars=100)

    attending = st.radio("Will you be attending?", ["Yes", "No"])
    guest_count = st.number_input("Number of guests (including you)", min_value=1, max_value=2, step=1)

    bringing_plus_one = st.radio("Are you bringing a +1?", ["No", "Yes"])

    plus_one_name = ""
    plus_one_email = ""
    plus_one_phone = ""
    if bringing_plus_one == "Yes":
        st.subheader("Plus One Details ✨")
        plus_one_name = st.text_input("+1 Full Name", max_chars=100)
        plus_one_email = st.text_input("+1 Email Address", max_chars=100)
        plus_one_phone = st.text_input("+1 Phone Number", max_chars=20)

    st.subheader("Extras")
    dietary = st.text_area("Any dietary requirements?")
    song_request = st.text_input("Song request")
    notes = st.text_area("Any notes or questions?")

    if st.button("Submit RSVP"):
        if not full_name:
            st.error("Please enter your full name.")
        else:
            submission = [
                full_name,
                email,
                attending,
                guest_count,
                plus_one_name if bringing_plus_one == "Yes" else "",
                plus_one_email if bringing_plus_one == "Yes" else "",
                plus_one_phone if bringing_plus_one == "Yes" else "",
                dietary,
                song_request,
                notes,
                datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            ]

            sheet.append_row(submission, value_input_option='USER_ENTERED')
            st.success("Thank you for RSVPing! We can’t wait to celebrate with you 💕")
            st.markdown("[Visit our Wedding Website](https://your-squarespace-url.com)")
