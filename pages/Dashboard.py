import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

QUIZ_FILE = "sleep_responses.csv"
DATASET_URL = "https://raw.githubusercontent.com/Dfranzani/Bases-de-datos-para-cursos/main/2023-1/sleep2.csv"

st.title("📊 Sleep Habits Dashboard")

# Load real dataset
@st.cache_data
def load_real_data():
    df = pd.read_csv(DATASET_URL)
    df.columns = df.columns.str.strip().str.replace(".", "_", regex=False)
    return df

df_real = load_real_data()

st.markdown("---")
st.subheader("🌍 Global Sleep Health Insights")
st.caption("Based on a dataset of 400 individuals across various occupations and lifestyles.")

col1, col2, col3 = st.columns(3)
col1.metric("Total Participants", len(df_real))
col2.metric("Avg Sleep Duration", f"{df_real['Sleep_Duration'].mean():.1f} hrs")
col3.metric("Avg Sleep Quality", f"{df_real['Quality_of_Sleep'].mean():.1f} / 10")

st.markdown("---")

# Chart 1: Sleep duration distribution
st.subheader("Sleep Duration Distribution")
fig1, ax1 = plt.subplots()
ax1.hist(df_real["Sleep_Duration"], bins=15, color="#4C72B0", edgecolor="white", rwidth=0.85)
ax1.set_xlabel("Sleep Duration (hours)")
ax1.set_ylabel("Number of People")
ax1.set_title("How Long Are People Sleeping?")
st.pyplot(fig1)

# Chart 2: Sleep quality vs stress level
st.subheader("Sleep Quality vs Stress Level")
fig2, ax2 = plt.subplots()
ax2.scatter(df_real["Stress_Level"], df_real["Quality_of_Sleep"],
            alpha=0.5, color="#DD8452", edgecolors="white", linewidth=0.5)
ax2.set_xlabel("Stress Level (1-10)")
ax2.set_ylabel("Sleep Quality (1-10)")
ax2.set_title("Higher Stress = Worse Sleep?")
st.pyplot(fig2)

# Chart 3: Sleep disorder breakdown
st.subheader("Sleep Disorder Breakdown")
disorder_counts = df_real["Sleep_Disorder"].value_counts()
fig3, ax3 = plt.subplots()
ax3.pie(disorder_counts, labels=disorder_counts.index, autopct="%1.1f%%",
        colors=["#4CAF50", "#F44336", "#FF9800"], startangle=90)
ax3.set_title("Sleep Disorder Distribution")
st.pyplot(fig3)

# Chart 4: Physical activity vs sleep quality
st.subheader("Physical Activity vs Sleep Quality")
fig4, ax4 = plt.subplots()
ax4.scatter(df_real["Physical_Activity_Level"], df_real["Quality_of_Sleep"],
            alpha=0.5, color="#4C72B0", edgecolors="white", linewidth=0.5)
ax4.set_xlabel("Physical Activity (min/day)")
ax4.set_ylabel("Sleep Quality (1-10)")
ax4.set_title("Does Exercise Improve Sleep?")
st.pyplot(fig4)

st.markdown("---")

# ML Model trained on real data
st.subheader("🤖 Sleep Disorder Predictor")
st.write("This model is trained on 400 real participants to predict sleep disorder risk.")

le_gender = LabelEncoder()
le_disorder = LabelEncoder()
df_ml = df_real.copy()
df_ml["Gender_enc"] = le_gender.fit_transform(df_ml["Gender"])
df_ml["Disorder_enc"] = le_disorder.fit_transform(df_ml["Sleep_Disorder"])

X = df_ml[["Gender_enc", "Age", "Sleep_Duration", "Physical_Activity_Level", "Stress_Level", "Heart_Rate"]]
y = df_ml["Disorder_enc"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
accuracy = model.score(X_test, y_test)

st.caption(f"Model accuracy: {accuracy*100:.1f}%")

col1, col2 = st.columns(2)
with col1:
    p_gender = st.selectbox("Gender", ["Male", "Female"])
    p_age = st.slider("Age", 18, 65, 25)
    p_sleep = st.slider("Avg Sleep Hours", 4.0, 10.0, 7.0)
with col2:
    p_activity = st.slider("Physical Activity (min/day)", 0, 90, 30)
    p_stress = st.slider("Stress Level (1-10)", 1, 10, 5)
    p_heart = st.slider("Resting Heart Rate (bpm)", 55, 100, 70)

if st.button("Predict Sleep Disorder Risk"):
    gender_enc = le_gender.transform([p_gender])[0]
    pred = model.predict([[gender_enc, p_age, p_sleep, p_activity, p_stress, p_heart]])[0]
    result = le_disorder.inverse_transform([pred])[0]

    if result == "None":
        st.success("✅ Low risk of sleep disorder based on your inputs.")
    else:
        st.warning(f"⚠️ Possible risk: **{result}** — consider consulting a doctor.")
    st.caption(f"Model trained on {len(df_real)} participants with {accuracy*100:.1f}% accuracy.")

st.markdown("---")

# Quiz responses section
st.subheader("📝 Your Quiz Responses")
if os.path.exists(QUIZ_FILE) and os.path.getsize(QUIZ_FILE) > 0:
    df_quiz = pd.read_csv(QUIZ_FILE)
    st.metric("Quiz Submissions", len(df_quiz))
    st.dataframe(df_quiz[["timestamp", "sleep_hours", "routine_days", "score", "label"]])
else:
    st.info("No quiz responses yet — take the quiz to see your data here!")
