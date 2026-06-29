import streamlit as st
import pandas as pd
import os
from datetime import datetime

DATA_FILE = "sleep_responses.csv"

st.title("😴 The Healthy Sleep Habits Quiz")
st.write("Test your bedtime routine parameters!")
st.markdown("### 🕒 Quick Stats")
col1, col2 = st.columns(2)
with col1:
    st.info("Estimated Time: 2 Mins")
with col2:
    st.success("Questions: 5 Items")

sleep_points = 0

st.header("1. Digital Hygiene")
st.image("Images/smartphone.webp", width=300)
q1 = st.radio(
    "Do you use your phone in bed right before falling asleep?",
    ["Every night", "Rarely or never"]
)
if q1 == "Rarely or never":
    sleep_points += 2

st.header("2. Pre-Bedtime Stimulants")
q2 = st.multiselect(
    "What do you routinely consume within 6 hours of bedtime?",
    ["Caffeine", "Energy drinks", "Heavy meals", "Just water"],
    key="stimulants"
)
if "Just water" in q2 and len(q2) == 1:
    sleep_points += 2

st.header("3. Sleep Duration")
st.image("Images/sleep tracker.jpg", width=300)
q3 = st.slider(
    "How many hours of sleep do you get on average?",
    min_value=4.0,
    max_value=12.0,
    value=7.0
)
if 7.0 <= q3 <= 9.0:
    sleep_points += 2

st.header("4. Sleep Environment")
q4 = st.selectbox(
    "What describes your bedroom environment?",
    ["Dark and cool", "Bright and warm"]
)
if q4 == "Dark and cool":
    sleep_points += 2

st.header("5. Routine Consistency")
st.image("Images/alarm clock.jpeg", width=300)
q5 = st.number_input(
    "How many days a week do you keep a consistent schedule?",
    min_value=0,
    max_value=7,
    value=4
)
if q5 >= 5:
    sleep_points += 2

st.markdown("---")
if st.button("Calculate Score"):
    # Save response to CSV
    response = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "phone_in_bed": q1,
        "stimulants": ", ".join(q2) if q2 else "None",
        "sleep_hours": q3,
        "sleep_environment": q4,
        "routine_days": q5,
        "score": sleep_points,
        "label": "Good" if sleep_points >= 6 else "Poor"
    }

    df_new = pd.DataFrame([response])
    if os.path.exists(DATA_FILE):
        df_existing = pd.read_csv(DATA_FILE)
        df = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df = df_new
    df.to_csv(DATA_FILE, index=False)

    st.subheader("Your Results")
    st.metric("Sleep Hygiene Score", f"{sleep_points} / 10")

    if sleep_points >= 7:
        st.balloons()
        st.success("🌟 Excellent Sleep Hygiene! Keep it up.")
    elif sleep_points >= 4:
        st.warning("😴 Pretty good — a few tweaks could help.")
    else:
        st.error("⚠️ Your routine needs some adjustments.")

    st.info("Check the **Dashboard** page to see how you compare to other users!")
