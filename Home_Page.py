import streamlit as st

# Title of App
st.title("Web Development Lab01")

# Assignment Data 
# Rubric Requirement: Display your Full Name and CS 1301
st.header("CS 1301")
st.subheader("Web Development") 
st.subheader("Kruthi Munnangi")


# Introduction
# Rubric Requirement: Write a quick description for your pages in the form:
#        1. **Page Name**: Description
#        2. **Page Name**: Description

st.write("""
Welcome to my Streamlit Web Development Lab01 app! You can navigate between the pages using the sidebar to the left. The following pages are:

1. **Portfolio**: A digital professional profile highlighting my background in neuroscience, teaching experience, and current research projects.
2. **Quiz**: An interactive trivia assessment module built natively using custom Streamlit input widgets.
""")
