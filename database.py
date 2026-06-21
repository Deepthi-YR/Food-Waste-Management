import mysql.connector
import pandas as pd

def get_connection():

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Welcome@123",
        database="food_wastage"
    )

    return conn


def run_query(query):

    conn = get_connection()

    df = pd.read_sql(query, conn)

    conn.close()

    return df
