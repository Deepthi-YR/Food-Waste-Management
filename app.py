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

st.header("SQL Analysis - 15 Queries")

food_data = pd.DataFrame({
    "Food_ID":[1,2,3,4,5,6],
    "Food_Name":["Rice","Biryani","Salad","Chapati","Pasta","Meals"],
    "Location":["Bangalore","Chennai","Mumbai","Bangalore","Mumbai","Chennai"],
    "Food_Type":["Vegetarian","Non-Vegetarian","Vegan","Vegetarian","Vegetarian","Vegetarian"],
    "Quantity":[100,80,40,60,70,90]
})

provider_data = pd.DataFrame({
    "Provider_ID":[1,2,3,4,5],
    "Provider_Name":["Hotel A","NGO B","Restaurant C","Hotel D","NGO E"],
    "City":["Bangalore","Chennai","Mumbai","Bangalore","Delhi"],
    "Provider_Type":["Hotel","NGO","Restaurant","Hotel","NGO"]
})

receiver_data = pd.DataFrame({
    "Receiver_ID":[1,2,3,4],
    "Receiver_Name":["Trust A","Trust B","NGO C","Shelter D"],
    "City":["Bangalore","Mumbai","Chennai","Delhi"]
})

claim_data = pd.DataFrame({
    "Claim_ID":[1,2,3,4,5],
    "Food_ID":[1,2,3,1,5],
    "Status":["Approved","Pending","Approved","Rejected","Approved"]
})

queries = {

    "1. Total Providers":
        pd.DataFrame({"Total Providers":[len(provider_data)]}),

    "2. Total Receivers":
        pd.DataFrame({"Total Receivers":[len(receiver_data)]}),

    "3. Total Food Listings":
        pd.DataFrame({"Food Listings":[len(food_data)]}),

    "4. Total Food Quantity":
        pd.DataFrame({"Total Quantity":[food_data["Quantity"].sum()]}),

    "5. Providers per City":
        provider_data.groupby("City").size().reset_index(name="Count"),

    "6. Receivers per City":
        receiver_data.groupby("City").size().reset_index(name="Count"),

    "7. Food Listings per City":
        food_data.groupby("Location").size().reset_index(name="Listings"),

    "8. Quantity by City":
        food_data.groupby("Location")["Quantity"].sum().reset_index(),

    "9. Food Type Distribution":
        food_data.groupby("Food_Type").size().reset_index(name="Count"),

    "10. Average Quantity":
        pd.DataFrame({"Average Quantity":[food_data["Quantity"].mean()]}),

    "11. Maximum Quantity":
        pd.DataFrame({"Maximum Quantity":[food_data["Quantity"].max()]}),

    "12. Minimum Quantity":
        pd.DataFrame({"Minimum Quantity":[food_data["Quantity"].min()]}),

    "13. Claims by Status":
        claim_data.groupby("Status").size().reset_index(name="Count"),

    "14. Approved Claims":
        pd.DataFrame({
            "Approved Claims":[
                len(claim_data[
                    claim_data["Status"]=="Approved"
                ])
            ]
        }),

    "15. Top Food Quantities":
        food_data.sort_values(
            "Quantity",
            ascending=False
        )[["Food_Name","Quantity"]]
}

selected_query = st.selectbox(
    "Select Query",
    list(queries.keys())
)

result = queries[selected_query]

st.dataframe(
    result,
    use_container_width=True
)

# ---------------- Dynamic Graphs ----------------

st.subheader("Visualization")

try:

    if selected_query == "5. Providers per City":

        fig = px.bar(
            result,
            x="City",
            y="Count",
            title="Providers by City"
        )
        st.plotly_chart(fig)

    elif selected_query == "6. Receivers per City":

        fig = px.bar(
            result,
            x="City",
            y="Count",
            title="Receivers by City"
        )
        st.plotly_chart(fig)

    elif selected_query == "7. Food Listings per City":

        fig = px.bar(
            result,
            x="Location",
            y="Listings",
            title="Food Listings by City"
        )
        st.plotly_chart(fig)

    elif selected_query == "8. Quantity by City":

        fig = px.bar(
            result,
            x="Location",
            y="Quantity",
            title="Food Quantity by City"
        )
        st.plotly_chart(fig)

    elif selected_query == "9. Food Type Distribution":

        fig = px.pie(
            result,
            names="Food_Type",
            values="Count",
            title="Food Type Distribution"
        )
        st.plotly_chart(fig)

    elif selected_query == "13. Claims by Status":

        fig = px.pie(
            result,
            names="Status",
            values="Count",
            title="Claims Status Distribution"
        )
        st.plotly_chart(fig)

    elif selected_query == "15. Top Food Quantities":

        fig = px.bar(
            result,
            x="Food_Name",
            y="Quantity",
            title="Food Quantities"
        )
        st.plotly_chart(fig)

except:
    pass
