import streamlit as st

st.title("SQL Analysis")

queries = {
    "Providers per City":
    """
    SELECT City,
           COUNT(*) Total_Providers
    FROM providers
    GROUP BY City
    """
}

selected = st.selectbox(
    "Choose Query",
    list(queries.keys())
)

df = run_query(queries[selected])

st.dataframe(df)