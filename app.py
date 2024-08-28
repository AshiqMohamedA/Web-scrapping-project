import streamlit as st
import pandas as pd
import mysql.connector
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to convert total minutes to HH:MM format
def convert_minutes_to_hhmm(minutes):
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours:02d}:{mins:02d}"

# Function to fetch data from MySQL database with filters applied
def fetch_filtered_data(db_name, table_name, bus_route=None, bus_type=None, max_rating=None, min_price=None, max_price=None, start_time=None, end_time=None):
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Abdul@1973",
            database=db_name
        )
        cursor = conn.cursor(dictionary=True)

        # Start building the SQL query
        query = f"SELECT * FROM {table_name} WHERE 1=1"
        params = []

        # Add conditions based on user inputs
        if bus_route:
            query += " AND `Bus Route Name` = %s"
            params.append(bus_route)
        
        if bus_type:
            query += " AND `Bus Type` = %s"
            params.append(bus_type)
            logging.info(f"Filtering by Bus Type: {bus_type}")  # Debugging: Log the Bus Type being filtered
        
        if max_rating is not None:
            query += " AND CAST(`Star Rating` AS DECIMAL(3,2)) <= %s"
            params.append(max_rating)
        
        if min_price is not None:
            query += " AND CAST(REPLACE(REPLACE(`Price`, 'INR ', ''), ',', '') AS DECIMAL(10,2)) >= %s"
            params.append(min_price)
        
        if max_price is not None:
            query += " AND CAST(REPLACE(REPLACE(`Price`, 'INR ', ''), ',', '') AS DECIMAL(10,2)) <= %s"
            params.append(max_price)
        
        if start_time is not None and end_time is not None:
            query += " AND (CAST(SUBSTRING_INDEX(`Departing Time`, ':', 1) AS UNSIGNED) * 60 + CAST(SUBSTRING_INDEX(`Departing Time`, ':', -1) AS UNSIGNED)) BETWEEN %s AND %s"
            params.extend([start_time, end_time])

        # Debug: Log the constructed query and parameters
        logging.debug(f"Constructed Query: {query}")
        logging.debug(f"Parameters: {params}")

        cursor.execute(query, params)
        result = cursor.fetchall()
        df = pd.DataFrame(result)

        # Debug: Log the number of results returned
        logging.info(f"Number of rows returned: {len(df)}")

        cursor.close()
        conn.close()

        return df
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return pd.DataFrame()  # Return an empty DataFrame in case of an error

# Function to fetch maximum price from the database
def get_max_price(db_name, table_name):
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Abdul@1973",
            database=db_name
        )
        query = f"SELECT MAX(CAST(REPLACE(REPLACE(`Price`, 'INR ', ''), ',', '') AS DECIMAL(10,2))) AS max_price FROM {table_name}"
        df = pd.read_sql(query, conn)
        conn.close()
        return df['max_price'].values[0] if not df.empty else 0.0
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return 0.0  # Return 0.0 if there's an error

def main():
    st.title('Bus Data Filtering Application')
    st.subheader('Choose the State')

    states = ["Kerala", "Kadamba", "Southbengal", "Bihar", "Telengana", 
              "Rajasthan", "Northbengal", "Chandigarh", "Punjab", "Assam"]

    selected_state = st.selectbox('Select State', [''] + states)

    if selected_state:
        db_name = "redbus"
        table_name = selected_state.lower().replace(' ', '')

        st.sidebar.header('Filters')

        try:
            conn = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="Abdul@1973",
                database=db_name
            )
            cursor = conn.cursor(dictionary=True)
            cursor.execute(f"SELECT DISTINCT `Bus Route Name` FROM {table_name}")
            bus_routes = [row['Bus Route Name'] for row in cursor.fetchall()]

            cursor.execute(f"SELECT DISTINCT `Bus Type` FROM {table_name}")
            bus_types = [row['Bus Type'] for row in cursor.fetchall()]
            
            # Debugging: Log all distinct bus types retrieved
            logging.debug(f"Bus Types Retrieved: {bus_types}")

            max_price_value = get_max_price(db_name, table_name)

            cursor.close()
            conn.close()
        except Exception as e:
            st.error(f"Error accessing database: {e}")
            return

        selected_route = st.sidebar.selectbox('Select Bus Route', [''] + bus_routes)
        selected_type = st.sidebar.selectbox('Select Bus Type', [''] + bus_types)

        max_rating = st.sidebar.slider('Maximum Rating', min_value=0.0, max_value=5.0, step=0.1, value=5.0)
        min_price = st.sidebar.number_input('Minimum Price', min_value=0.0, step=1.0, value=0.0)
        max_price = st.sidebar.number_input('Maximum Price', min_value=0.0, max_value=max_price_value, step=1.0, value=max_price_value)

        start_time_min, end_time_min = st.sidebar.slider(
            'Select Departure Time Range',
            min_value=0, max_value=1439, value=(0, 1439), step=1,
            format="HH:MM"
        )

        start_time_hhmm = convert_minutes_to_hhmm(start_time_min)
        end_time_hhmm = convert_minutes_to_hhmm(end_time_min)

        st.sidebar.write(f"Departure Time Range: {start_time_hhmm} to {end_time_hhmm}")

        filtered_df = fetch_filtered_data(db_name, table_name, selected_route, selected_type, max_rating, min_price, max_price, start_time_min, end_time_min)

        st.subheader('Filtered Bus Details')
        st.dataframe(filtered_df)

        st.write(f"Number of buses filtered: {len(filtered_df)}")

if __name__ == '__main__':
    main()
