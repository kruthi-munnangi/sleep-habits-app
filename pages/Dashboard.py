import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import numpy as np

DATA_FILE = "sleep_responses.csv"

st.title("📊 Sleep Habits Dashboard")
st.write("Aggregate insights from all quiz submissions.")

if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
    st.warning("No data yet! Take the quiz first to see insights here.")
    st.stop()

df = pd.read_csv(DATA_FILE)

if len(df) < 1:
    st.warning("No data yet! Take the quiz first.")
    st.stop()

st.markdown("---")
st.subheader("📈 Summary Stats")
col1, col2, col3 = st.columns(3)
col1.metric("Total Responses", len(df))
col2.metric("Avg Sleep Hours", f"{df['sleep_hours'].mean():.1f} hrs")
col3.metric("Avg Score", f"{df['score'].mean():.1f} / 10")

st.markdown("---")

# Chart 1: Score distribution
st.subheader("Score Distribution")
fig1, ax1 = plt.subplots()
ax1.hist(df["score"], bins=range(0, 12), color="#4C72B0", edgecolor="white", rwidth=0.8)
ax1.set_xlabel("Sleep Hygiene Score")
ax1.set_ylabel("Number of Users")
ax1.set_title("Distribution of Sleep Scores")
st.pyplot(fig1)

# Chart 2: Avg sleep hours by environment
st.subheader("Sleep Hours by Bedroom Environment")
env_group = df.groupby("sleep_environment")["sleep_hours"].mean()
fig2, ax2 = plt.subplots()
env_group.plot(kind="bar", ax=ax2, color=["#4C72B0", "#DD8452"], edgecolor="white")
ax2.set_ylabel("Avg Sleep Hours")
ax2.set_title("Sleep Hours by Environment")
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=0)
st.pyplot(fig2)

# Chart 3: Good vs Poor sleep quality breakdown
st.subheader("Sleep Quality Breakdown")
label_counts = df["label"].value_counts()
fig3, ax3 = plt.subplots()
ax3.pie(label_counts, labels=label_counts.index, autopct="%1.1f%%",
        colors=["#4CAF50", "#F44336"], startangle=90)
ax3.set_title("Good vs Poor Sleep Hygiene")
st.pyplot(fig3)

st.markdown("---")

# ML Model
st.subheader("🤖 Sleep Quality Predictor")
st.write("Based on all collected responses, our model predicts your sleep quality.")

if len(df) >= 5:
    try:
        df_ml = df.copy()
        le_phone = LabelEncoder()
        le_env = LabelEncoder()
        le_label = LabelEncoder()

        df_ml["phone_encoded"] = le_phone.fit_transform(df_ml["phone_in_bed"])
        df_ml["env_encoded"] = le_env.fit_transform(df_ml["sleep_environment"])
        df_ml["label_encoded"] = le_label.fit_transform(df_ml["label"])

        X = df_ml[["phone_encoded", "sleep_hours", "env_encoded", "routine_days"]]
        y = df_ml["label_encoded"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestClassifier(n_estimators=50, random_state=42)
        model.fit(X_train, y_train)

        accuracy = model.score(X_test, y_test) if len(X_test) > 0 else model.score(X_train, y_train)

        st.write("**Try the predictor:**")
        p_phone = st.radio("Phone in bed?", ["Every night", "Rarely or never"], key="ml_phone")
        p_hours = st.slider("Sleep hours", 4.0, 12.0, 7.0, key="ml_hours")
        p_env = st.selectbox("Environment", ["Dark and cool", "Bright and warm"], key="ml_env")
        p_days = st.slider("Consistent days/week", 0, 7, 4, key="ml_days")

        if st.button("Predict My Sleep Quality"):
            phone_enc = le_phone.transform([p_phone])[0]
            env_enc = le_env.transform([p_env])[0]
            prediction = model.predict([[phone_enc, p_hours, env_enc, p_days]])[0]
            label = le_label.inverse_transform([prediction])[0]

            if label == "Good":
                st.success(f"✅ Predicted Sleep Quality: **{label}**")
            else:
                st.error(f"⚠️ Predicted Sleep Quality: **{label}**")

            st.caption(f"Model trained on {len(df)} responses")

    except Exception as e:
        st.info("Need a few more responses to train the model accurately!")
else:
    st.info(f"Need at least 5 responses to train the ML model. Currently have {len(df)}.")
