import streamlit as st
import pandas as pd
import plotly.express as px

from database import run_query, get_connection

st.set_page_config(
    page_title="Food Wastage Management System",
    layout="wide"
)

st.title("🍲 Local Food Wastage Management System")

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Dashboard",
        "Food Search",
        "Add Provider",
        "SQL Analysis"
    ]
)

# =====================================================
# DASHBOARD
# =====================================================

if menu == "Dashboard":

    st.header("Dashboard")

    providers = run_query(
        "SELECT COUNT(*) AS total FROM providers"
    )

    receivers = run_query(
        "SELECT COUNT(*) AS total FROM receivers"
    )

    food = run_query(
        "SELECT SUM(Quantity) AS total FROM food_listings"
    )

    claims = run_query(
        "SELECT COUNT(*) AS total FROM claims"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Providers", providers.iloc[0, 0])
    c2.metric("Receivers", receivers.iloc[0, 0])
    c3.metric("Food Quantity", food.iloc[0, 0])
    c4.metric("Claims", claims.iloc[0, 0])

# =====================================================
# FOOD SEARCH
# =====================================================

elif menu == "Food Search":

    st.header("Food Availability Search")

    city_df = run_query(
        "SELECT DISTINCT Location FROM food_listings"
    )

    city = st.selectbox(
        "Select City",
        city_df["Location"]
    )

    food_type = st.selectbox(
        "Food Type",
        ["All", "Vegetarian", "Non-Vegetarian", "Vegan"]
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

# =====================================================
# CRUD
# =====================================================

elif menu == "Add Provider":

    st.header("Add Provider")

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

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO providers
            (Provider_ID, Name, Type, City, Contact)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (pid, name, ptype, city, contact)
        )

        conn.commit()

        conn.close()

        st.success(
            "Provider Added Successfully"
        )

# =====================================================
# SQL ANALYSIS
# =====================================================

elif menu == "SQL Analysis":

    st.header("SQL Analysis")

    queries = {

        "1. Number of Providers in Each City":
        """
        SELECT City,
               COUNT(*) AS Total_Providers
        FROM providers
        GROUP BY City
        ORDER BY Total_Providers DESC
        """,

        "2. Number of Receivers in Each City":
        """
        SELECT City,
               COUNT(*) AS Total_Receivers
        FROM receivers
        GROUP BY City
        ORDER BY Total_Receivers DESC
        """,

        "3. Provider Type Contributing Most Food":
        """
        SELECT Provider_Type,
               SUM(Quantity) AS Total_Food_Donated
        FROM food_listings
        GROUP BY Provider_Type
        ORDER BY Total_Food_Donated DESC
        """,

        "4. Providers in Chicago":
        """
        SELECT Name,
               Type,
               Contact
        FROM providers
        WHERE City='Chicago'
        """,

        "5. Receivers Claiming Most Food":
        """
        SELECT r.Name,
               COUNT(c.Claim_ID) AS Total_Claims
        FROM receivers r
        JOIN claims c
        ON r.Receiver_ID=c.Receiver_ID
        GROUP BY r.Name
        ORDER BY Total_Claims DESC
        """,

        "6. Total Food Available":
        """
        SELECT SUM(Quantity) AS Total_Food_Available
        FROM food_listings
        """,

        "7. City with Highest Food Listings":
        """
        SELECT Location,
               COUNT(*) AS Listings
        FROM food_listings
        GROUP BY Location
        ORDER BY Listings DESC
        """,

        "8. Most Common Food Types":
        """
        SELECT Food_Type,
               COUNT(*) AS Count
        FROM food_listings
        GROUP BY Food_Type
        ORDER BY Count DESC
        """,

        "9. Claims Made Per Food Item":
        """
        SELECT f.Food_Name,
               COUNT(c.Claim_ID) AS Total_Claims
        FROM food_listings f
        LEFT JOIN claims c
        ON f.Food_ID=c.Food_ID
        GROUP BY f.Food_Name
        ORDER BY Total_Claims DESC
        """,

        "10. Provider with Highest Successful Claims":
        """
        SELECT p.Name,
               COUNT(*) AS Successful_Claims
        FROM providers p
        JOIN food_listings f
        ON p.Provider_ID=f.Provider_ID
        JOIN claims c
        ON f.Food_ID=c.Food_ID
        WHERE c.Status='Completed'
        GROUP BY p.Name
        ORDER BY Successful_Claims DESC
        """,

        "11. Claim Status Percentage":
        """
        SELECT Status,
               ROUND(COUNT(*) * 100.0 /
               (SELECT COUNT(*) FROM claims),2)
               AS Percentage
        FROM claims
        GROUP BY Status
        """,

        "12. Average Quantity Claimed Per Receiver":
        """
        SELECT r.Name,
               ROUND(AVG(f.Quantity),2)
               AS Avg_Quantity
        FROM receivers r
        JOIN claims c
        ON r.Receiver_ID=c.Receiver_ID
        JOIN food_listings f
        ON c.Food_ID=f.Food_ID
        GROUP BY r.Name
        ORDER BY Avg_Quantity DESC
        """,

        "13. Most Claimed Meal Type":
        """
        SELECT f.Meal_Type,
               COUNT(*) AS Total_Claims
        FROM food_listings f
        JOIN claims c
        ON f.Food_ID=c.Food_ID
        GROUP BY f.Meal_Type
        ORDER BY Total_Claims DESC
        """,

        "14. Total Quantity Donated by Each Provider":
        """
        SELECT p.Name,
               SUM(f.Quantity) AS Total_Donated
        FROM providers p
        JOIN food_listings f
        ON p.Provider_ID=f.Provider_ID
        GROUP BY p.Name
        ORDER BY Total_Donated DESC
        """,

        "15. Food Expiring Soon":
        """
        SELECT Food_Name,
               Quantity,
               Expiry_Date
        FROM food_listings
        WHERE Expiry_Date <= CURDATE() + INTERVAL 3 DAY
        """
    }

    selected_query = st.selectbox(
        "Choose Query",
        list(queries.keys())
    )

    result = run_query(
        queries[selected_query]
    )

    st.dataframe(result)
