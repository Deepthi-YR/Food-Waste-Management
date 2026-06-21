import streamlit as st
from database import run_query

st.title("Dashboard")

providers = run_query(
    "SELECT COUNT(*) total FROM providers"
)

receivers = run_query(
    "SELECT COUNT(*) total FROM receivers"
)

food = run_query(
    "SELECT SUM(Quantity) total FROM food_listings"
)

claims = run_query(
    "SELECT COUNT(*) total FROM claims"
)

c1,c2,c3,c4 = st.columns(4)

c1.metric("Providers", providers.iloc[0,0])
c2.metric("Receivers", receivers.iloc[0,0])
c3.metric("Food Quantity", food.iloc[0,0])
c4.metric("Claims", claims.iloc[0,0])