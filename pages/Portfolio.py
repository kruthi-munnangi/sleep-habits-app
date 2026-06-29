import streamlit as st
import info
import pandas as pd

# 1. About Me Section
def about_me_section():
    st.header("About Me")
    st.image(info.profile_picture, width=200)
    st.write(info.about_me)
    st.write("---")

# 2. Sidebar Links Section
def links_section():
    st.sidebar.header("links")
    st.sidebar.write("connect with me on LinkedIn")
    
    linkedin_link = f'<a href="{info.my_linkedin_url}"><img src="{info.linkedin_image_url}" width="75" height="75"></a>'
    st.sidebar.markdown(linkedin_link, unsafe_allow_html=True)
    
    st.sidebar.write("check out my GitHub")
    github_link = f'<a href="{info.my_github_url}"><img src="{info.github_image_url}" width="75" height="75"></a>'
    st.sidebar.markdown(github_link, unsafe_allow_html=True)
    
    st.sidebar.write("Email me")
    email_link = f'<a href="mailto:{info.my_email_address}"><img src="{info.email_image_url}" width="75" height="75"></a>'
    st.sidebar.markdown(email_link, unsafe_allow_html=True)

# 3. Education Section
def education_section(education_data, course_data):
    st.header("Education")
    st.subheader(education_data["Institution"])
    st.write(f"**Degree:** {education_data['Degree']}")
    st.write(f"**Graduation Date:** {education_data['Graduation Date']}")
    st.write(f"**GPA:** {education_data['GPA']}")
    
    st.write("**Relevant Coursework**")
    
    coursework = pd.DataFrame(course_data)
    st.dataframe(
        coursework,
        column_config={
            "code": "Course Code",
            "names": "Course Name",
            "semester_taken": "Semester Taken",
            "skills": "What I Learned"
        },
        hide_index=True
    )
    st.write("---")

# 4. Professional Experience Section
def experience_section(experience_data):
    st.header("Professional Experience")
    for job_title, (job_description, image) in experience_data.items():
        expander = st.expander(job_title)
        expander.image(image, width=250)
        for bullet in job_description:
            expander.write(bullet)
    st.write("---")

# 5. Project Section
def project_section(projects_data):
    st.header("Projects")
    for project_name, project_description in projects_data.items():
        expander = st.expander(project_name)
        expander.write(project_description)
    st.write("---")

# 6. Skills Section
def skills_section(programming_data, spoken_data):
    st.header("Skills")
    st.subheader("Programming Languages")
    for skill, percentage in programming_data.items():
        st.write(f"{skill} {info.programming_icons.get(skill, '')}")
        st.progress(percentage)
        
    st.subheader("Spoken Languages")
    for spoken, proficiency in spoken_data.items():
        st.write(f"{spoken} {info.spoken_icons.get(spoken, '')} {proficiency}")
    st.write("---")

# 7. Activities Section
def activity_section(leadership_data, activity_data):
    st.header("Activities")
    tab1, tab2 = st.tabs(["Leadership", "Community Service"])
    
    with tab1:
        st.subheader("Leadership")
        for title, (details, image) in leadership_data.items():
            expander = st.expander(title)
            expander.image(image, width=250)
            for bullet in details:
                expander.write(bullet)
                
    with tab2:
        st.subheader("Community Service")
        for title, details in activity_data.items():
            expander = st.expander(title)
            for bullet in details:
                expander.write(bullet)
    st.write("---")

# ==========================================
# MAIN EXECUTION ENGINE CALLS
# ==========================================
about_me_section()
links_section()
education_section(info.education_data, info.course_data)
experience_section(info.experience_data)
project_section(info.projects_data)
skills_section(info.programming_data, info.spoken_data)
activity_section(info.leadership_data, info.activity_data)
