import streamlit as st

# Data manipulation
import pandas as pd
import numpy as np
from scipy.stats import f_oneway

# Data viz
import duckdb as db
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objs as ply

# SQL function
def sql(sql_query):
    return db.sql(sql_query).to_df()

# --- Title ---
st.title("E-commerce Analytics for a Company's Sales Strategy ")

st.markdown("---")

# --- BACKGROUND ---

st.markdown("""
### Background
<p style='text-align: justify; padding: 1px;'>
E-commerce data analysis is the process of collecting, 
analyzing and interpreting data related to the activities of a business. 
This data is used to understand business performance and improve it.
</p>
""", unsafe_allow_html=True)

st.markdown("---")

# --- DATASET ---

st.markdown("""
### Dataset
<p style='text-align: justify; padding: 1px;'>
The data used is information about E-commerce X's customer accounts.
</p>
""", unsafe_allow_html=True)

df = pd.read_csv('./assets/ecommerce_data.csv', parse_dates=['Order_Date', 'Delivery_Date'])

df.loc[df.duplicated()]

df = df.dropna(subset= ['Order_ID', 'Customer_ID', 'Price', 'Product_ID', 'Product_Name', 'Order_Date', 'Delivery_Date'])

df.reset_index(drop= True, inplace= True)

# Menampilkan DataFrame di Streamlit
st.dataframe(df)

st.markdown("---")

st.markdown("""
### Sales trends every month
<p style='text-align: justify; padding: 1px;'>
Companies can analyze sales in each month from 2020 - 2023 in each month via the graph below:
</p>
""", unsafe_allow_html=True)

Sales_EveryMonths = sql(
    """
    with sales as(
        select
            Quantity * Price as total_sales,
            Order_Date
        from df
        )
    SELECT 
        strftime(Order_Date, '%Y - %m') AS month,
        SUM(total_sales) as sales_every_month
    FROM sales
    GROUP BY month
    ORDER BY month
    """
)

st.dataframe(Sales_EveryMonths)

fig = plt.figure(figsize=(12, 6))
sns.lineplot(data= Sales_EveryMonths, x= 'month', y= 'sales_every_month')

plt.xlabel('Month')
plt.ylabel('Total Sales')
plt.title('Sales trends every month')
plt.xticks(rotation=60)

st.pyplot(fig)

st.markdown("""
<p style='text-align: justify; padding: 1px;'>
From the graph shown above, 
this can help a company to know whether sales are increasing or decreasing each month.
</p>
<br>
<p style='text-align: justify; padding: 1px;'>
The company can evaluate why there has been a decline in sales every month for the last 3 years, 
it could be through delays in the delivery of stuff which has influenced the decline in sales.
</p>
Below are patterns of delivery delays based on delivery method or product category :
""", unsafe_allow_html=True)

Delay_Delivery = sql(
    """
        SELECT 
            CASE 
            WHEN DATE_PART('day', Delivery_Date - Order_Date) == 0 THEN 'On Time or Early'
            WHEN DATE_PART('day', Delivery_Date - Order_Date) BETWEEN 1 AND 1 THEN '1 Day Late'
            WHEN DATE_PART('day', Delivery_Date - Order_Date) BETWEEN 2 AND 3 THEN '2-3 Days Late'
            WHEN DATE_PART('day', Delivery_Date - Order_Date) > 3 THEN '4+ Days Late'
        END AS Delay_Category,
        COUNT(Order_ID) AS Total_Orders,
        ROUND(COUNT(Order_ID) * 100.0 / (SELECT COUNT(*) FROM df), 2) AS Percentage
        FROM df
        GROUP BY Delay_Category
        ORDER BY Percentage DESC;
    """
)
st.title("Delivery Delay Analysis")

st.dataframe(Delay_Delivery)

labels = Delay_Delivery["Delay_Category"]
values = Delay_Delivery["Total_Orders"]
explode = [0.1 if i == max(values) else 0 for i in values]

fig = ply.Figure(
    data=[ply.Pie(labels=labels, values=values, pull=explode)]
)
fig.update_layout(title_text="Delivery Delay Distribution")

# Tampilkan di Streamlit
st.plotly_chart(fig)

st.markdown("""
<p style='text-align: justify; padding: 1px;'>
Looking at the chart above, it can be concluded that many deliveries take more than 4 days, 
which is likely to cause a decline in sales because it makes 
customers wait a long time to receive the goods they ordered.
</p>
""", unsafe_allow_html=True)

st.markdown("""
<p style='text-align: justify; padding: 1px;'>
Companies can also see what methods are used by customers to make payments. 
By knowing what methods are used, companies can manage incoming income from the chart below :
</p>
""", unsafe_allow_html=True)

Payment = sql(
    """
    SELECT
        Payment_Method,
        COUNT(Payment_Method) as Total_Method
    FROM df
    GROUP BY Payment_Method
    ORDER BY Total_Method DESC
    """
)

st.title("Payment Method Analysis")

st.dataframe(Payment)

count_labels = Payment["Payment_Method"]
count_value = Payment["Total_Method"]
explode = [0.1 if i == max(count_value) else 0 for i in count_value]

fig2 = ply.Figure(
    data=[ply.Pie(labels=count_labels, values=count_value, pull=explode)]
)
fig2.update_layout(title_text="Distribution of Payment Methods")

st.plotly_chart(fig2)

st.markdown("""
### Conclusion
<p style='text-align: justify; padding: 1px;'>
From this visual we can see several points of analysis:
</p>
<ul style='text-align: justify; padding: 10px;'>       
<li>The graph displayed every month for the last 3 years can be a reference 
for sales in terms of increasing or decreasing each month</li>
<li>Delays in delivery can be a factor in decreasing sales, 
because customers expect fast delivery from sellers</li>
<li>Having many payment methods makes it easier for customers to buy goods, 
especially in e-commerce, because not all customers carry cash nowadays</li>
</ul>
""", unsafe_allow_html=True)