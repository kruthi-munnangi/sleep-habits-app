import streamlit as st

st.title("😴 Sleep Habits Analytics App")
st.subheader("By Kruthi Munnangi")

st.write("""
Welcome! This app collects and analyzes sleep habit data to help users understand their sleep hygiene.
Navigate using the sidebar to explore the pages below:
""")

st.markdown("""
1. **Quiz** — Take a 5-question sleep habits assessment and get your personalized sleep hygiene score.
2. **Dashboard** — Explore aggregate data visualizations and a machine learning model that predicts sleep quality based on collected responses.
""")

st.info("👈 Use the sidebar to get started!")
