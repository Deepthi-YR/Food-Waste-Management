import streamlit as st
from database import run_query

st.title("Food Availability Search")

city = st.selectbox(
    "Select City",
    run_query(
        "SELECT DISTINCT Location FROM food_listings"
    )["Location"]
)

food_type = st.selectbox(
    "Food Type",
    ["All","Vegetarian","Non-Vegetarian","Vegan"]
)

query = f"""
SELECT *
FROM food_listings
WHERE Location='{city}'
"""

df = run_query(query)

if food_type != "All":
    df = df[df["Food_Type"] == food_type]

st.dataframe(df)