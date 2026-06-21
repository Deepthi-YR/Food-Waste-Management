import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Food Wastage Management System",
    layout="wide"
)

st.title("🍲 Local Food Wastage Management System")

st.write("Use the sidebar to navigate through the application.")

# ---------------- Dashboard ----------------

st.header("Dashboard")

providers = 25
receivers = 18
food = 500
claims = 45

c1, c2, c3, c4 = st.columns(4)

c1.metric("Providers", providers)
c2.metric("Receivers", receivers)
c3.metric("Food Quantity", food)
c4.metric("Claims", claims)

# ---------------- Food Search ----------------

st.header("Food Availability Search")

sample_data = pd.DataFrame({
    "Location": ["Bangalore", "Chennai", "Bangalore", "Mumbai"],
    "Food_Type": ["Vegetarian", "Vegan", "Non-Vegetarian", "Vegetarian"],
    "Quantity": [100, 50, 75, 60]
})

city = st.selectbox(
    "Select City",
    sample_data["Location"].unique()
)

food_type = st.selectbox(
    "Food Type",
    ["All", "Vegetarian", "Non-Vegetarian", "Vegan"]
)

df = sample_data[sample_data["Location"] == city]

if food_type != "All":
    df = df[df["Food_Type"] == food_type]

st.dataframe(df)

# ---------------- CRUD ----------------

st.header("Provider Entry Form")

with st.form("provider_form"):

    pid = st.number_input("Provider ID", step=1)

    name = st.text_input("Provider Name")

    ptype = st.text_input("Provider Type")

    city_input = st.text_input("City")

    contact = st.text_input("Contact")

    submit = st.form_submit_button("Add Provider")

if submit:
    st.success("Provider Added Successfully")

# ---------------- Visualizations ----------------

st.header("Visualizations")

provider_df = pd.DataFrame({
    "City": ["Bangalore", "Chennai", "Mumbai"],
    "Total_Providers": [12, 8, 10]
})

fig = px.bar(
    provider_df,
    x="City",
    y="Total_Providers",
    title="Providers by City"
)

st.plotly_chart(fig)

claim_df = pd.DataFrame({
    "Status": ["Pending", "Approved", "Rejected"],
    "Count": [15, 25, 5]
})

fig2 = px.pie(
    claim_df,
    values="Count",
    names="Status",
    title="Claim Status Distribution"
)

st.plotly_chart(fig2)

# ---------------- SQL Analysis ----------------

st.header("SQL Analysis")

queries = {
    "Providers per City": pd.DataFrame({
        "City": ["Bangalore", "Chennai", "Mumbai"],
        "Total_Providers": [12, 8, 10]
    })
}

selected = st.selectbox(
    "Choose Query",
    list(queries.keys())
)

st.dataframe(queries[selected])
