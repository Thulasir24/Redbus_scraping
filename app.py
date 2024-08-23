import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error


def fetch_data_from_database(query, params=None):
    """Fetch data from MySQL database based on the query and parameters."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="tulsitulsi",  # Replace with your MySQL password
            database="redbus_data"  # Replace with your MySQL database name
        )

        df = pd.read_sql(query, connection, params=params)
        return df

    except Error as e:
        st.error(f"Error: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error

    finally:
        if connection.is_connected():
            connection.close()


def main():
    st.title("Redbus Data Filter and Visualization")

    # User inputs for filtering
    route_name = st.text_input("Route Name")
    bus_type = st.text_input("Bus Type")
    min_price = st.number_input("Min Price", value=0)
    max_price = st.number_input("Max Price", value=10000)

    # Construct SQL query with filters
    query = """
    SELECT * FROM bus_routes
    WHERE (route_name LIKE %s)
    AND (bus_type LIKE %s)
    AND (CAST(REPLACE(price, '₹', '') AS DECIMAL(10,2)) BETWEEN %s AND %s)
    """
    params = (f"%{route_name}%", f"%{bus_type}%", min_price, max_price)

    # Fetch and display filtered data
    data = fetch_data_from_database(query, params)

    if not data.empty:
        st.write(data)
    else:
        st.write("No data found matching the criteria.")


if __name__ == "__main__":
    main()
