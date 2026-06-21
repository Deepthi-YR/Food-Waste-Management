import streamlit as st

st.set_page_config(
    page_title="Food Wastage Management System",
    layout="wide"
)

st.title("🍲 Local Food Wastage Management System")

st.write(
    "Use the sidebar to navigate through the application."
)

import streamlit as st

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

import streamlit as st

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

query = f
SELECT *
FROM food_listings
WHERE Location='{city}'

df = run_query(query)

if food_type != "All":
    df = df[df["Food_Type"] == food_type]

st.dataframe(df)


import streamlit as st

st.title("CRUD Operations")

with st.form("provider_form"):

    pid = st.number_input("Provider ID")

    name = st.text_input("Provider Name")

    ptype = st.text_input("Provider Type")

    city = st.text_input("City")

    contact = st.text_input("Contact")

    submit = st.form_submit_button("Add Provider")

if submit:

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        INSERT INTO providers
        (Provider_ID,Name,Type,City,Contact)
        VALUES(%s,%s,%s,%s,%s),(pid,name,ptype,city,contact))

    conn.commit()

    conn.close()

    st.success("Provider Added")

import streamlit as st
import plotly.express as px

Providers by city
SELECT City,
COUNT(*) Total_Providers
FROM providers
GROUP BY City
)

fig = px.bar(
    df,
    x="City",
    y="Total_Providers",
    title="Providers by City"
)

st.plotly_chart(fig)

claim status distribution
df = run_query(
SELECT Status,
COUNT(*) Count
FROM claims
GROUP BY Status
)

fig = px.pie(
    df,
    values="Count",
    names="Status"
)

st.plotly_chart(fig)

import streamlit as st

st.title("SQL Analysis")

queries = {
    "Providers per City":
    SELECT City,
           COUNT(*) Total_Providers
    FROM providers
    GROUP BY City
}

selected = st.selectbox(
    "Choose Query",
    list(queries.keys())
)

df = run_query(queries[selected])

