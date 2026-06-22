import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Food Wastage Management System",
    layout="wide"
)

# ---------------- Sample Data ----------------

providers_df = pd.DataFrame({
    "Provider_ID":[1,2,3,4,5],
    "Name":["ABC Hotel","Fresh Foods","City Restaurant","Food Hub","Green Kitchen"],
    "City":["Bangalore","Chennai","Mumbai","Delhi","Bangalore"],
    "Provider_Type":["Hotel","NGO","Restaurant","Caterer","Hotel"]
})

receivers_df = pd.DataFrame({
    "Receiver_ID":[1,2,3,4],
    "Name":["Helping Hands","Food Bank","Hope Trust","Care NGO"],
    "City":["Bangalore","Chennai","Delhi","Mumbai"]
})

food_df = pd.DataFrame({
    "Food_ID":[1,2,3,4,5],
    "Food_Name":["Rice","Chapati","Biryani","Salad","Veg Meals"],
    "Location":["Bangalore","Chennai","Mumbai","Delhi","Bangalore"],
    "Food_Type":["Vegetarian","Vegetarian","Non-Vegetarian","Vegan","Vegetarian"],
    "Quantity":[100,50,75,30,120]
})

claims_df = pd.DataFrame({
    "Claim_ID":[1,2,3,4,5],
    "Food_ID":[1,2,3,4,5],
    "Status":["Approved","Pending","Approved","Rejected","Approved"]
})

# ---------------- Sidebar ----------------

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Dashboard",
        "Food Search",
        "Provider Entry",
        "Visualizations",
        "SQL Analysis"
    ]
)

st.title("🍲 Local Food Wastage Management System")

# ---------------- Dashboard ----------------

if menu == "Dashboard":

    st.header("Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Providers", len(providers_df))
    c2.metric("Receivers", len(receivers_df))
    c3.metric("Food Listings", len(food_df))
    c4.metric("Claims", len(claims_df))

# ---------------- Food Search ----------------

elif menu == "Food Search":

    st.header("Food Availability Search")

    city = st.selectbox(
        "Select City",
        food_df["Location"].unique()
    )

    food_type = st.selectbox(
        "Food Type",
        ["All"] + list(food_df["Food_Type"].unique())
    )

    filtered = food_df[food_df["Location"] == city]

    if food_type != "All":
        filtered = filtered[
            filtered["Food_Type"] == food_type
        ]

    st.dataframe(filtered, use_container_width=True)

# ---------------- Provider Entry ----------------

elif menu == "Provider Entry":

    st.header("Provider Entry Form")

    with st.form("provider_form"):

        pid = st.number_input(
            "Provider ID",
            step=1
        )

        name = st.text_input(
            "Provider Name"
        )

        ptype = st.text_input(
            "Provider Type"
        )

        city = st.text_input(
            "City"
        )

        contact = st.text_input(
            "Contact"
        )

        submit = st.form_submit_button(
            "Add Provider"
        )

    if submit:
        st.success(
            f"Provider '{name}' Added Successfully!"
        )

# ---------------- Visualizations ----------------

elif menu == "Visualizations":

    st.header("Visualizations")

    city_counts = (
        providers_df.groupby("City")
        .size()
        .reset_index(name="Total Providers")
    )

    fig1 = px.bar(
        city_counts,
        x="City",
        y="Total Providers",
        title="Providers by City"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    status_counts = (
        claims_df["Status"]
        .value_counts()
        .reset_index()
    )

    status_counts.columns = [
        "Status",
        "Count"
    ]

    fig2 = px.pie(
        status_counts,
        names="Status",
        values="Count",
        title="Claim Status Distribution"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# ---------------- SQL Analysis ----------------

elif menu == "SQL Analysis":

    st.header("SQL Analysis - 15 Queries")

    queries = {
        "1. Total Providers":
            len(providers_df),

        "2. Total Receivers":
            len(receivers_df),

        "3. Total Food Listings":
            len(food_df),

        "4. Total Claims":
            len(claims_df),

        "5. Providers by City":
            providers_df.groupby("City").size(),

        "6. Receivers by City":
            receivers_df.groupby("City").size(),

        "7. Food Quantity Available":
            food_df["Quantity"].sum(),

        "8. Food Types Count":
            food_df["Food_Type"].value_counts(),

        "9. Average Quantity":
            food_df["Quantity"].mean(),

        "10. Maximum Quantity":
            food_df["Quantity"].max(),

        "11. Minimum Quantity":
            food_df["Quantity"].min(),

        "12. Approved Claims":
            len(claims_df[
                claims_df["Status"]=="Approved"
            ]),

        "13. Pending Claims":
            len(claims_df[
                claims_df["Status"]=="Pending"
            ]),

        "14. Rejected Claims":
            len(claims_df[
                claims_df["Status"]=="Rejected"
            ]),

        "15. Food by Location":
            food_df.groupby("Location").size()
    }

    for title, result in queries.items():

        st.subheader(title)

        if isinstance(
            result,
            (pd.Series, pd.DataFrame)
        ):
            st.dataframe(result)
        else:
            st.write(result)

        st.markdown("---")
