import streamlit as st

# Hero Section
st.title("About Me")
col_photo, col_about = st.columns([0.5, 3], gap="Medium", vertical_alignment="center")

with col_photo:
    st.image("Assets/IMG-20200911-WA0030.png", width=260)
    
with col_about:
    st.write("""
             Hi, I'm Kinanda Krisandika Nurseto, who had interest in data analytics field
             
             Have a basic understanding of data analytics principles, be able to use various data analytics tools 
             to analyze and understand the data such as python, SQL, Excel/SpreadSheet and be able to visualize data 
             that are attractive and easy to understand
             """)

    col2_1, col2_2, col2_3 = st.columns(3)

    with col2_1:
        st.markdown("[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/kinanda/)", unsafe_allow_html=True)
    with col2_2:
        st.markdown("[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/KinandaKrisandika)", unsafe_allow_html=True)
    
# Experience & Skills Section
col_exp, col_skills = st.columns(2, gap="medium")

with col_exp:
    st.title("Experience")
    st.write("""
             - 3 years experiences as a staff reporting analyst
             - Have experience from training data analyst
             - Strong analytical and problem solving skills
             - Good Understanding knowledge about Python and Excel
             - Excellent communication and good at team work
             """)

with col_skills:
    st.title("Skills")
    st.write("""
             - Programing Languages: Python, SQL
             - Databases : MySQL, SQL Server
             - Data Visualization: Matplotlib, Seaborn, Plotly
             - Microsoft Excel
             - BigQuery
             - Tableau
             - Microsoft Power BI
             """)
    
# Project Section
st.title("Projects")
st.write("""
         - [E-Commerce Data Analysis](https://github.com/KinandaKrisandika/python_fundamental/tree/Data_Analyst)
         - [Financial Data Analysis](https://github.com/KinandaKrisandika/python_fundamental/tree/Data_Analyst)
         - [Social Media Analysis](https://github.com/KinandaKrisandika/python_fundamental/tree/Data_Analyst)
         - [Covid-19 Case Analysis](https://github.com/KinandaKrisandika/python_fundamental/tree/Data_Analyst)
         """)