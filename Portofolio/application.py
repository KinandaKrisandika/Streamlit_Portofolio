import streamlit as st

st.set_page_config(layout="wide")

#Page Setup
about_me_page = st.Page(
    page = "Project/about_me.py",
    title = "About Me",
    icon = ":material/account_circle:",
    default = True
)

project1_page = st.Page(
    page = "Project/Project1_Ecommerce_Analysis.py",
    title = "Project 1 (E-Commerce Analysis)",
    icon = ":material/bar_chart:",
)

project2_page = st.Page(
    page = "Project/Project2_Financial_Analysis.py",
    title = "Project 2 (Finansial Analysis)",
    icon = ":material/bar_chart:",
)

project3_page = st.Page(
    page = "Project/Project3_Social_Media_analysis.py",
    title = "Project 3 (Social Media Analysis)",
    icon = ":material/bar_chart:",
)

project4_page = st.Page(
    page = "Project/Project4_Covid19_Cases.py",
    title = "Project 4 ( Covid 19 Cases Analysis)",
    icon = ":material/bar_chart:",
)

# Navigation

pg = st.navigation(
    {
        "Info": [about_me_page],
        "Projects": [project1_page, project2_page, project3_page, project4_page]
    }
)

# --- SHARED ON ALL PAGES ---
st.sidebar.markdown("""
    <p style='text-align: justify; padding: 1px;'>
    Notes:
    </p>
    <ul style='text-align: justify; padding: 10px;'>       
    <li>To find out the complete code of the project, go to the about me page and scroll down, 
        and you will see link at the project.</li>
    </ul>

    """, unsafe_allow_html=True)

pg.run()