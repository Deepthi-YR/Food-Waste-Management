import streamlit as st
import plotly.express as px


Providers by city
SELECT City,
COUNT(*) Total_Providers
FROM providers
GROUP BY City
""")

fig = px.bar(
    df,
    x="City",
    y="Total_Providers",
    title="Providers by City"
)

st.plotly_chart(fig)

claim status distribution
df = run_query("""
SELECT Status,
COUNT(*) Count
FROM claims
GROUP BY Status
""")

fig = px.pie(
    df,
    values="Count",
    names="Status"
)

st.plotly_chart(fig)