import streamlit as st

# Data Manipulation
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# Data visualization
import duckdb as db
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as mcolors
import matplotlib.ticker as mticker
from matplotlib.ticker import MaxNLocator

# choose chart style
import matplotlib as mpl
mpl.style.use('ggplot')

# SQL function
def sql(sql_query):
    return db.sql(sql_query).to_df()

st.title("Financial Data Analysis")

st.markdown("---")

# --- BACKGROUND ---

st.markdown("""
### Background
<p style='text-align: justify; padding: 1px;'>
A company needs calculations on all factors, it needs to analyze this financial data to find out the ratio between revenue, profit, and expenses every month for 1 year in order to develop the company itself in the future.
</p>
""", unsafe_allow_html=True)

# --- DATASET ---

st.markdown("""
### Dataset
<p style='text-align: justify; padding: 1px;'>
The dataset contains Financial data from a company in 2023.
</p>
""", unsafe_allow_html=True)

df = pd.read_csv('./Assets/financial_data.csv', parse_dates=['Date'])

# Change the string format of column names to make queries easier
df.columns = (
    df.columns.str.lower()
    .str.replace(' ', '_')
    .str.replace('(', '')
    .str.replace(')', '')
)

# Display the DataFrame in Streamlit
st.dataframe(df)

# --- Comparison between Revenue, Expenses and Profit every month in 2023 ---

st.markdown("""
<p style='text-align: justify; padding: 1px;'>
With the data set that we have above, we can find out the comparison between total revenue, 
total profit obtained and total expenses through the tabel and graph below :
</p>
""", unsafe_allow_html=True)

st.markdown("""
### Comparison between Revenue, Expenses and Profit every month in 2023
""", unsafe_allow_html=True)

Comparison = sql(
    """
    SELECT 
        DATE_TRUNC('month', Date) AS month,
        SUM(Revenue) AS total_revenue,
        SUM(Expenses) AS total_expenses, 
        SUM(Profit) AS total_profit
    FROM df
    GROUP BY month
    ORDER BY month
    """
)

Comparison_per_month = sql(
    """
    SELECT 
        STRFTIME(month, '%b %Y') AS month_year,
        total_revenue,
        total_expenses,
        total_profit
    FROM Comparison
    """
)

Comparison_per_month = Comparison_per_month.set_index('month_year')

st.dataframe(Comparison_per_month)


fig, ax = plt.subplots(figsize=(16, 8)) 

bar_width = 0.3  
spacing = 0.4    
index = np.arange(len(Comparison_per_month.index)) * (bar_width * 3 + spacing)

ax.bar(index, Comparison_per_month['total_revenue'], bar_width, color='red', label='Total Revenue')

ax.bar(index + bar_width, Comparison_per_month['total_expenses'], bar_width, color='yellow', label='Total Expenses')

ax.bar(index + bar_width * 2, Comparison_per_month['total_profit'], bar_width, color='green', label='Total Profit')

ax.set_xticks(index + bar_width)
ax.set_xticklabels(Comparison_per_month.index, rotation=35)

ax.yaxis.set_major_locator(mticker.MultipleLocator(100000))
ax.yaxis.set_minor_locator(mticker.AutoMinorLocator())
ax.yaxis.set_major_formatter('{x:,.0f}')

ax.set_title('Comparison Between Revenue, Expenses and Profit Every Month')
ax.set_xlabel('Month')
ax.set_ylabel('Amount')

ax.tick_params(axis='y', labelsize=10)

ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))

plt.tight_layout()
st.pyplot(fig)

st.markdown("""
<p style='text-align: justify; padding: 1px;'>
Here we can find out the developments and declines that occur every month in 2023, 
through these tables and graphs it can be a financial reference for the company 
to continue to progress and develop in the future, 
by evaluating sales ups and downs every month.
<br><br>
We can also see a comparison graph between total revenue and total expenses each month 
for 1 year to analyze and predict future profits as a consideration for the company 
using linear regression.
</p>
""", unsafe_allow_html=True)

fig2, ax = plt.subplots(figsize=(12, 6))
Comparison_per_month['total_revenue'].plot(kind='bar', ax=ax, color='mediumslateblue', label='Total Revenue')
Comparison_per_month['total_expenses'].plot(kind='bar', ax=ax, color='lightblue', label='Total Profit')

ax.set_title('Revenue and Expenses by Month')
ax.set_xlabel('Month')
ax.set_ylabel('Amount')

ax.legend()

plt.xticks(rotation=45)
ax.ticklabel_format(axis= 'y', style= 'plain', useOffset= False)
ax.yaxis.set_major_locator(plt.MultipleLocator(100000))

st.pyplot(fig2, use_container_width=False)

st.markdown("""
<p style='text-align: justify; padding: 1px;'>
With the results of the graphic comparison above, 
we can get the results of linear regression as follows:
</p>
""", unsafe_allow_html=True)

Comparison_per_month = Comparison_per_month.reset_index()

a = np.array(Comparison_per_month['total_expenses']).reshape(-1, 1)
b = np.array(Comparison_per_month['total_revenue'])

model = LinearRegression()
model.fit(a, b)

predicted_revenue = model.predict(a)

# Streamlit UI
st.write(f"### Linear Regression Analysis")
st.write(f"##### Slope (β1): {model.coef_[0]:.2f}")
st.write(f"##### Intercept (β0): {model.intercept_:.2f}")



# Gunakan style yang bersih
sns.set_style("whitegrid")

# Buat plot dengan ukuran yang pas
fig3, ax = plt.subplots(figsize=(10, 6))

# Plot data
ax.scatter(a, b, color='blue', label='Actual Data')
ax.plot(a, predicted_revenue, color='red', label='Regression Line')

# Format sumbu dan label
ax.set_xlabel('Expenses')
ax.set_ylabel('Revenue')
ax.legend()
ax.grid(True, linestyle="--", alpha=0.6)

# Pastikan label tidak berputar
plt.xticks(rotation=0)

plt.ticklabel_format(style='plain', axis='y')

# Tampilkan di Streamlit tanpa auto-resize
st.pyplot(fig3, use_container_width=False)

st.markdown("""
<p style='text-align: justify; padding: 1px;'>
<b>The image above presents :</b>
</p>
<ul style='text-align: justify; padding: 10px;'>
<li><b><i>The Blue Dot as actual data, 
which shows the relationship between expenses and company revenue every month</li>
<li><b><i>Red Line as Linear regression line, predicted relationship between 
expenses and revenue based on linear regression models, its mean 
The higher the expenses, the higher the revenue. 
This shows that there is a positive relationship between expenses and revenue </li>
<br><br>
<p style='text-align: justify; padding: 1px;'>
<b>The results of the linear regression above show:</b>
</p>
<ul style='text-align: justify; padding: 10px;'>
<li><b><i>Slope (β₁) = 2.01
→ For every 1 unit increase in Expenses, Revenue increases by around 2.01 units.
→ This means that if the company spends an additional IDR 1 million on expenses, 
then its income will increase by IDR 2.01 million.</li>
<li><b><i>Intercept (β₀) = 25013.25
→ If Expenses = 0, then Revenue is predicted to be 25,013.25
→ In business terms, this means that even though there are no expenses, 
the company still has potential initial income of IDR 25,013.25 
(can be from fixed income or other factors). </li>
""", unsafe_allow_html=True)

st.markdown("""
### Conclusion
<ul style='text-align: justify; padding: 10px;'>
<li><b><i>To understand financial analysis of data, you need at least company financial report data, 
such as reports on revenue, expenses and profits incurred and earned by the company.</li>
<li><b><i>This business is quite profitable, because Revenue increases greater than Expenses.</li>
<li><b><i>This model can be used to project income based on planned expenses.</li>
</ul>
""", unsafe_allow_html=True)