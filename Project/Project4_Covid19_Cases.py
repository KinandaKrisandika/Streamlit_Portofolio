import streamlit as st

# Data manipulation
import pandas as pd

# Data viz
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import folium

# SQL query
import duckdb as db

# SQL function
def sql(sql_query):
    return db.sql(sql_query).to_df()

# choose chart style
import matplotlib as mpl
mpl.style.use('ggplot')

st.title("COVID-19 Case Distribution in Indonesia", anchor=False)

st.markdown("---")

# --- BACKGROUND ---

st.markdown("""
### Background
<p style='text-align: justify; padding: 1px;'>
Covid 19 is a major epidemic that occurs throughout the world, 
This epidemic is dangerous because it causes death,
The total number of cases obtained was quite large,
The purpose of analyzing this data is to provide a reference when a new outbreak such as Covid-19 occurs.
</p>
""", unsafe_allow_html=True)


# --- DATASET ---

st.markdown("""
### Dataset
<p style='text-align: justify; padding: 1px;'>
The dataset contains COVID-19 data spanning from March 2020 to September 2022.
</p>
""", unsafe_allow_html=True)


df = pd.read_csv('./Assets/covid_19.csv', parse_dates=['Date'])

# Change the string format of column names to make queries easier
df.columns = (
    df.columns.str.lower()
    .str.replace(' ', '_')
    .str.replace('(', '')
    .str.replace(')', '')
)

# drop unused columns
df = (
    df.drop([
        'province',
        'country',
        'continent',
    ], axis= 1)
)

df = df[df['location_level']=='Province']

df = df.dropna(axis=1).reset_index(drop=True)

# --- Trend of New Cases per Month ---

st.markdown("""
### Trend of New Cases per Month
""", unsafe_allow_html=True)

# create data frame of new cases per month
new_cases_per_month_num = sql(
    """
    WITH monthly_cases AS (
        SELECT 
            DATE_TRUNC('month', date) AS month,
            SUM(new_cases) AS total_new_cases
        FROM df
        GROUP BY month
        ORDER BY month
    )
    SELECT 
        month,
        total_new_cases
    FROM monthly_cases
    ORDER BY month
    """
)

new_cases_per_month_name = sql(
    """
    SELECT 
        STRFTIME(month, '%b %Y') AS month_year,
        total_new_cases,
    FROM new_cases_per_month_num
    """
)

def plot_new_cases_per_month():
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(new_cases_per_month_name['month_year'], new_cases_per_month_name['total_new_cases'],
            label='Total New Cases', color='blue')

    plt.title('COVID New Cases per Month')
    plt.xticks(rotation=65)
    ax.ticklabel_format(axis='y', style='plain', useOffset=False)
    ax.yaxis.set_major_locator(plt.MultipleLocator(100000))

    plt.annotate('',  
                 xy=(15, 1200000), 
                 xytext=(13.9, 300000),  
                 xycoords='data',  
                 arrowprops=dict(arrowstyle='->', connectionstyle='arc3', color='orange', lw=2))

    plt.annotate('Eid al-Fitr Celebration (May 2021)',
                 xy=(13.3, 400000),  
                 rotation=84.4,  
                 va='bottom', 
                 ha='left',
                 fontsize=11)

    plt.annotate('',  
                 xy=(22, 1170000), 
                 xytext=(21, 200000),  
                 xycoords='data',  
                 arrowprops=dict(arrowstyle='->', connectionstyle='arc3', color='orange', lw=2))

    plt.annotate('Omicron Variant Wave (Jan-Feb 2022)',
                 xy=(20.4, 250000),  
                 rotation=85.3,  
                 va='bottom', 
                 ha='left',
                 fontsize=11)

    st.pyplot(fig)

plot_new_cases_per_month()

st.markdown("""
<p style='text-align: justify; padding: 1px;'>
We observe two prominent spikes in cases, occurring in May-July 2021 and January-February 2022, which we will explore further.
<br>            
<b>First Spike: May-July 2021</b>
<br>           
In mid 2021, there was a significant increase in new cases. Although direct supporting data for this analysis is lacking, this spike coincides with the period following the Eid al-Fitr 
celebration, one of the largest holidays in Indonesia. Traditionally, this celebration is accompanied by mass travel, known as 'mudik', potentially leading to increased social interactions and mobility.

Without definitive data to link the spike solely to the Eid celebration—such as mobility reports or social interaction levels—it's reasonable to hypothesize that major events like Eid al-Fitr 
could potentially influence the spread of the virus, based on general understandings of infectious disease transmission.

<b>Second Spike: January-February 2022</b>
<br>
A significant increase occurred in early 2022, coinciding with the emergence of the highly transmissible Omicron variant globally. Again, while specific data to prove direct causality in 
Indonesia is absent, global patterns suggest that the spread of the Omicron variant contributed to increased cases in many countries, likely including Indonesia

<b>Discussion</b>
<br>
When analyzing this data, it's important to remember that seeing a trend doesn't necessarily mean one event causes another. Without more data, we should avoid making firm conclusions. 
Nonetheless, these observations point out the need for more detailed analysis to better understand the factors affecting COVID-19 case trends.
<br>
<b>Conclusion</b>
<br>
This chart provides valuable insights into the dynamics of COVID-19 spread in Indonesia, illustrating the importance of public health policies and effective monitoring. Furthermore, it 
underscores the necessity for preparedness in facing potential future surges, which could be triggered by large social events or the emergence of new variants.
</p>
""", unsafe_allow_html=True)

st.markdown("""
### Total New Cases vs New Deaths vs New Recovered per Month
""", unsafe_allow_html=True)

compare_trend_num = sql(
    """
    SELECT 
        DATE_TRUNC('month', date) AS month,
        SUM(new_cases) AS total_new_cases,
        SUM(new_deaths) AS total_new_deaths,
        SUM(new_recovered) AS total_new_recovered
    FROM df
    GROUP BY month
    ORDER BY month
    """
)

compare_trend_name = sql(
    """
    SELECT 
        STRFTIME(month, '%b %Y') AS month_year,
        total_new_cases,
        total_new_deaths,
        total_new_recovered
    FROM compare_trend_num
    """
)

fig, ax = plt.subplots(figsize= (12, 6))

ax.plot(compare_trend_name['month_year'], compare_trend_name['total_new_cases'], label= 'Total New Cases')
ax.plot(compare_trend_name['month_year'], compare_trend_name['total_new_deaths'], label= 'Total New Deaths')
ax.plot(compare_trend_name['month_year'], compare_trend_name['total_new_recovered'], label= 'Total New Recovered')

ax.set_xlabel('')
ax.set_ylabel('')
ax.set_title('Total New Cases vs New Deaths vs New Recovered per Month')
ax.legend()

plt.xticks(rotation= 65)
ax.ticklabel_format(axis= 'y', style= 'plain', useOffset= False)
ax.yaxis.set_major_locator(plt.MultipleLocator(100000))
st.pyplot(fig)

st.markdown("""
<p style='text-align: justify; padding: 1px;'>
<b>Second Spike: January-February 2022</b><br>
The graph shows a strong correlation between the rise and fall of new cases and new recoveries. 
This suggests that as more people are diagnosed with COVID-19, more people recover, likely due to the concurrent handling of these cases within the healthcare system.
<br><b>Second Spike: January-February 2022</b><br>
There is a noticeable increase in deaths that accompanies the rise in new cases during 2021. However, during the surge in 2022, the increase in deaths is less 
pronounced compared to the increase in cases. This could potentially be attributed to several factors, such as improved treatments or higher vaccination rates.
</p>
""", unsafe_allow_html=True)

st.markdown("""
### Distribution of COVID-19 Cases in Indonesia by Location
""", unsafe_allow_html=True)

new_cases_by_location = sql(
    """
    SELECT 
        island,
        location,
        SUM(new_cases) AS total_new_cases
    FROM df
    GROUP BY island, location
    ORDER BY island, location
    """
)

fig = px.sunburst(
    new_cases_by_location,
    path=['island', 'location'], 
    values='total_new_cases',
    title='Total Cases Over Time',
    template='plotly',        
    width=1000, 
    height=1000
)

fig.update_traces(textinfo='label+percent parent') 

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
<p style='text-align: justify; padding: 1px;'>
The chart reveals that the island of Java, particularly DKI Jakarta, is the most affected by COVID-19 cases in Indonesia. DKI Jakarta alone comprises 32% of the cases, the highest among all regions. Collectively, the 
provinces on Java—including DKI Jakarta, Jawa Barat, Jawa Tengah, and Jawa Timur—account for 69% of the total cases, indicating a significant concentration of the pandemic within this island.
</p>
""", unsafe_allow_html=True)

st.markdown("""
### Geographic Analysis
<p style='text-align: justify; padding: 1px;'>
To see the distribution of cases in Indonesia, we can make a map by utilizing the folium library.   
</p>
""", unsafe_allow_html=True)

geo_data = sql(
    """
    SELECT
        location,
        MAX(total_cases) AS total_cases,
        AVG(latitude) AS latitude,
        AVG(longitude) AS longitude
    FROM df
    GROUP BY location;
    """
)

m = folium.Map(location=[geo_data['latitude'].mean(), geo_data['longitude'].mean()], zoom_start=5)

# Add markers for each province

for i, row in geo_data.iterrows():
    folium.Circle(
        location=[row['latitude'], row['longitude']],
        radius=row['total_cases']/5 ,  
        color='crimson',  
        fill=True,
        fill_color='crimson',  
        tooltip=f"{row['location']}: {row['total_cases']} cases",  
    ).add_to(m)

map_html = m._repr_html_()
st.components.v1.html(map_html, height=500)

st.markdown("""
### Total Cases vs Population Density
""", unsafe_allow_html=True)

cases_vs_popdens = sql(
    """
    SELECT 
        location,
        MAX(total_cases) total_cases,
        AVG(population_density) as population_density
    FROM df
    GROUP BY location
    ORDER BY total_cases DESC
    """
)

plt.style.use('default')

fig, ax1 = plt.subplots(figsize=(12, 6))

ax1.bar(cases_vs_popdens['location'], cases_vs_popdens['total_cases'])
ax1.set_xlabel('')
ax1.set_ylabel('Total Cases')   
ax1.tick_params(axis='x', rotation=90)

ax2 = ax1.twinx()
ax2.plot(cases_vs_popdens['location'], cases_vs_popdens['population_density'], color='r', marker='o')
ax2.set_ylabel('Average Population Density')

plt.title('Comparison of Total Cases and Population Density per Province')
st.pyplot(fig)

st.markdown("""
<p style='text-align: justify; padding: 1px;'>
Generally, there appears to be a correlation between population density and the number of COVID-19 cases. 
Provinces with higher population densities tend to have more cases. This pattern suggests that transmission rates could be influenced by the population concentration. 
</p>
""", unsafe_allow_html=True)

st.markdown("""
### Conclusion
<p style='text-align: justify; padding: 1px;'>
The analysis of COVID-19 data in Indonesia from March 2020 to September 2022 shows significant fluctuations in case numbers, with prominent spikes in May-July 2021 and January-February 2022. 
These increases align with major events such as Eid al-Fitr and the global emergence of the Omicron variant. The island of Java, particularly DKI Jakarta, exhibits the highest concentration of cases, significantly impacted by factors like population density, which correlates with the spread of the virus.
</p>
""", unsafe_allow_html=True)

st.markdown("""
### Recommendations
<ul style='text-align: justify; padding: 10px;'>
<li>Implement more stringent monitoring and preventive measures during and after major holidays or events like Eid al-Fitr, when increased travel and social interaction heighten the risk of virus spread.</li>
<li>Strengthen health infrastructure in areas with high population density, particularly on Java, to manage surges more effectively.</li>
<li>Maintain and enhance data collection and analysis capabilities to identify emerging trends and respond quickly to potential future surges in cases.</li>
</ul>
""", unsafe_allow_html=True)