import streamlit as st

# Data Manipulation
import pandas as pd

# Data visualization
import duckdb as db
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import seaborn as sns
import matplotlib.dates as mdates

# SQL function
def sql(sql_query):
    return db.sql(sql_query).to_df()

st.title("Social Media Analysis")

st.markdown("---")

st.markdown("""
### Background
<p style='text-align: justify; padding: 1px;'>

The large number of uses of social media every day provides huge business opportunities in marketing. Analyzing the use of social media can help a company in formulating business strategies and making decisions.
</p>
""", unsafe_allow_html=True)

# --- DATASET ---

st.markdown("""
### Dataset
<p style='text-align: justify; padding: 1px;'>
The dataset contains some sample data of social media in 2023.
</p>
""", unsafe_allow_html=True)

df = pd.read_csv('./assets/sample_social_media_data.csv', parse_dates=['post_date'])

# Change the string format of column names to make queries easier
df.columns = (
    df.columns.str.lower()
    .str.replace(' ', '_')
    .str.replace('(', '')
    .str.replace(')', '')
)

# Display the DataFrame in Streamlit
st.dataframe(df)

# --- users who use the platform more than 1 ---

st.markdown("""
### Total Interactions and Total Users per Month on 2023
""", unsafe_allow_html=True)

monthly = sql(
    """
    SELECT 
        username,
        strftime(post_date, '%Y %B') AS date,
        GROUP_CONCAT(DISTINCT platform) AS platforms,
        SUM(likes + comments + shares) AS total_interactions
    FROM df
    WHERE EXTRACT(YEAR FROM post_date) = 2023
    GROUP BY username, date, strftime(post_date, '%Y-%m')
    HAVING COUNT(DISTINCT platform) > 0
    ORDER BY strftime(post_date, '%Y-%m')
    """
)

st.dataframe(monthly)

# 1️⃣ Pisahkan platform (long-form)
platforms = monthly['platforms'].str.split(',', expand=True).stack().reset_index(level=1, drop=True)
platforms.name = 'platform'

# 2️⃣ Gabungkan dengan monthly DataFrame
platforms_long = monthly.join(platforms).reset_index()

# 3️⃣ Konversi 'date' ke datetime
platforms_long['date'] = pd.to_datetime(platforms_long['date'], format='%Y %B')

# 4️⃣ Buat objek fig dan ax
fig, ax = plt.subplots(figsize=(12, 6))

# 2️⃣ Plot line chart
sns.lineplot(
    data=platforms_long,
    x='date', 
    y='total_interactions', 
    hue='platform', 
    palette=['green', 'orange', 'blue'],
    marker='o',
    ci=None,  # Hilangkan bayangan (confidence interval)
    ax=ax
)

# 3️⃣ Tampilkan semua bulan (termasuk bulan genap) di sumbu X
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

# 4️⃣ Atur rotasi agar tidak bertumpuk
plt.xticks(rotation=65)

# 5️⃣ Tambahkan grid, label, dan judul
ax.grid(True, linestyle='--', alpha=0.7)
ax.set_title('Total Interactions per Month by Platform')
ax.set_xlabel('Date')
ax.set_ylabel('Total Interactions')

# 6️⃣ Tampilkan di Streamlit
st.pyplot(fig)

monthly_users = sql(
    """
    SELECT 
        strftime(post_date, '%Y %B') AS date,
        COUNT(DISTINCT username) AS total_users,
        GROUP_CONCAT(DISTINCT platform) AS platforms,
        SUM(likes + comments + shares) AS total_interactions,
        COUNT(DISTINCT CASE WHEN platform = 'Facebook' THEN username END) AS facebook,
        COUNT(DISTINCT CASE WHEN platform = 'Instagram' THEN username END) AS instagram,
        COUNT(DISTINCT CASE WHEN platform = 'Twitter' THEN username END) AS twitter
    FROM df
    WHERE EXTRACT(YEAR FROM post_date) = 2023
    GROUP BY date, strftime(post_date, '%Y-%m')
    HAVING COUNT(DISTINCT platform) > 0
    ORDER BY strftime(post_date, '%Y-%m')
    """
)

st.dataframe(monthly_users)

# 1️⃣ Konversi 'date' ke datetime
monthly_users['date'] = pd.to_datetime(monthly_users['date'], format='%Y %B')

# 2️⃣ Ubah ke long-form agar seaborn mudah memproses
platforms_longlest = monthly_users.melt(
    id_vars=['date'],
    value_vars=['facebook', 'instagram', 'twitter'],
    var_name='platforms',
    value_name='users_count'  # Hindari nama bentrok
)

# 3️⃣ Plot line chart dengan seaborn
fig2, ax2 = plt.subplots(figsize=(12, 6))
sns.lineplot(
    data=platforms_longlest,
    x='date',
    y='users_count',
    hue='platforms',
    palette=['blue', 'orange', 'green'],
    marker='o'
)

# 4️⃣ Tambahkan label, grid, dan rotasi tanggal
ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=1))  # Tampilkan setiap bulan
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))  # Format bulan singkat
plt.xticks(rotation=65)
plt.title('Total Users per Platform per Month (2023)')
plt.xlabel('Date')
plt.ylabel('Total Users')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(title='Platform')

# Tampilkan di Streamlit
st.pyplot(fig2)


st.markdown("""
<p style='text-align: justify; padding: 1px;'>
Through the table and graph above, we can see how many users and total interactions 
there will be on several social media in 2023 from January to December.
This will be very useful, especially for startups starting out in running their business.
</p>
<br>
<p style='text-align: justify; padding: 1px;'>
From the total interactions and total users who experienced rapid increases and decreases each month,
we can see from what trends occurred in that month, and how big the impact of interactions on each platform
will be on trends that are being widely discussed, 
because this can also be a reference material for preparing business strategies 
and making decisions for a company.
</p>
<br>
<p style='text-align: justify; padding: 1px;'>
From here we can also see the activity of users using any platform every hour 
with the table and graph below :
</p>
""", unsafe_allow_html=True)

df['hour'] = df['post_date'].dt.hour

per_hour = sql(
    """
    SELECT 
        COUNT(DISTINCT username) AS total_users,
        ANY_VALUE(post_date) AS date,
        hour,
        SUM(CASE WHEN platform = 'Instagram' THEN 1 ELSE 0 END) AS Instagram,
        SUM(CASE WHEN platform = 'Facebook' THEN 1 ELSE 0 END) AS Facebook,
        SUM(CASE WHEN platform = 'Twitter' THEN 1 ELSE 0 END) AS Twitter
    FROM df
    WHERE EXTRACT(YEAR FROM post_date) = 2023  -- Ambil data untuk tahun 2023
    GROUP BY hour
    HAVING COUNT(DISTINCT platform) > 0
    ORDER BY date
    """
)

st.dataframe(per_hour)

per_hour_melted = per_hour.melt(id_vars=["hour"], value_vars=["Instagram", "Facebook", "Twitter"], var_name="platform", value_name="total_user")



fig3 = plt.figure(figsize=(12, 6))
sns.lineplot(data=per_hour_melted, x='hour', y='total_user', hue='platform', marker='o', ci=None)

plt.title('Hourly Platform Usage in 2023', fontsize=14)
plt.xlabel('Hour', fontsize=12)
plt.ylabel('Total Users', fontsize=12)

plt.xticks(range(0, 24))
plt.legend(title='Platform')

st.pyplot(fig3)


st.markdown("""
<p style='text-align: justify; padding: 1px;'>
With the three tables and graphs above, 
the company will have an idea on what platform and at what time it should start advertising.
<br>
After the company determines what platform it wants to use for advertising, 
the company needs an influencer who has a lot of influence on the platform that the company has chosen.
</p>
<br>
The table below can be a reference for which influencers are suitable for the platform
determined by the company :
""", unsafe_allow_html=True)

user = sql(
    """
    SELECT 
        username,
        ANY_VALUE(post_date) as Date,
        GROUP_CONCAT(DISTINCT platform) AS platforms,
        SUM(likes + comments + shares) AS total_interactions
    FROM df
    GROUP BY username
    HAVING COUNT (DISTINCT platform) > 0
    ORDER BY total_interactions DESC
    limit 10
    """
)

st.dataframe(user)

st.markdown("""
### Conclusion
<p style='text-align: justify; padding: 1px;'>
<b>Stages of Social Media Data Analysis :</b>
</p> 
<ul style='text-align: justify; padding: 10px;'>
<li><b><i>Collect data from various sources</li>
<li><b><i>Extracting information related to data.</li>
<li><b><i>Perform advanced analysis of available data.</li>
</ul>
<p style='text-align: justify; padding: 1px;'>
<b>Benefits of Social Media Data Analysis:</b>
</p> 
<ul style='text-align: justify; padding: 10px;'>
<li><b><i>Understand user preferences and interests</li>
<li><b><i>Understand market segments and audiences</li>
<li><b><i>Know what customers are looking for</li>
<li><b><i>Measuring the effectiveness of advertising campaigns</li>
<li><b><i>Optimizing marketing strategies</li>
</ul>
""", unsafe_allow_html=True)