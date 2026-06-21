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

    cursor.execute("""
        INSERT INTO providers
        (Provider_ID,Name,Type,City,Contact)
        VALUES(%s,%s,%s,%s,%s)
    """,(pid,name,ptype,city,contact))

    conn.commit()

    conn.close()

    st.success("Provider Added")