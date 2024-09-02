import streamlit as st  # Import Streamlit for creating web applications
import pandas as pd  # Import Pandas for data manipulation
import mysql.connector  # Import MySQL connector for database interaction
import logging  # Import logging for debugging and tracking information

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to convert total minutes to HH:MM format
def convert_minutes_to_hhmm(minutes):
    hours = minutes // 60  # Calculate hours
    mins = minutes % 60  # Calculate remaining minutes
    return f"{hours:02d}:{mins:02d}"  # Return time in HH:MM format

# Function to fetch data from MySQL database with filters applied
def fetch_filtered_data(db_name, table_name, bus_route=None, bus_type=None, max_rating=None, min_price=None, max_price=None, start_time=None, end_time=None):
    try:
        conn = mysql.connector.connect(  # Establish connection to MySQL database
            host="127.0.0.1",
            user="root",
            password="Abdul@1973",
            database=db_name
        )
        cursor = conn.cursor(dictionary=True)  # Create a cursor object for executing queries

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
            logging.info(f"Filtering by Bus Type: {bus_type}")  # Log the Bus Type being filtered
        
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

        # Log the constructed query and parameters
        logging.debug(f"Constructed Query: {query}")
        logging.debug(f"Parameters: {params}")

        cursor.execute(query, params)  # Execute the query with parameters
        result = cursor.fetchall()  # Fetch all the results
        df = pd.DataFrame(result)  # Convert the results into a DataFrame

        # Log the number of results returned
        logging.info(f"Number of rows returned: {len(df)}")

        cursor.close()  # Close the cursor
        conn.close()  # Close the database connection

        return df  # Return the filtered DataFrame
    except mysql.connector.Error as err:  # Handle MySQL errors
        st.error(f"Error: {err}")
        return pd.DataFrame()  # Return an empty DataFrame in case of an error

# Function to fetch maximum price from the database
def get_max_price(db_name, table_name):
    try:
        conn = mysql.connector.connect(  # Establish connection to MySQL database
            host="127.0.0.1",
            user="root",
            password="Abdul@1973",
            database=db_name
        )
        query = f"SELECT MAX(CAST(REPLACE(REPLACE(`Price`, 'INR ', ''), ',', '') AS DECIMAL(10,2))) AS max_price FROM {table_name}"  # Query to fetch the maximum price
        df = pd.read_sql(query, conn)  # Execute the query and store the result in a DataFrame
        conn.close()  # Close the database connection
        return df['max_price'].values[0] if not df.empty else 0.0  # Return the maximum price or 0.0 if no data
    except mysql.connector.Error as err:  # Handle MySQL errors
        st.error(f"Error: {err}")
        return 0.0  # Return 0.0 if there's an error

# Main function to render the Streamlit application
def main():
    st.title('Bus Data Filtering Application')  # Set the title of the application
    st.subheader('Choose the State')  # Set the subheader for state selection

    states = ["Kerala", "Kadamba", "Southbengal", "Bihar", "Telengana", 
              "Rajasthan", "Northbengal", "Chandigarh", "Punjab", "Assam"]  # List of states to select from

    selected_state = st.selectbox('Select State', [''] + states)  # Dropdown to select a state

    if selected_state:  # If a state is selected
        db_name = "redbus"  # Database name
        table_name = selected_state.lower().replace(' ', '')  # Format table name based on selected state

        st.sidebar.header('Filters')  # Set the sidebar header for filters

        try:
            conn = mysql.connector.connect(  # Establish connection to MySQL database
                host="127.0.0.1",
                user="root",
                password="Abdul@1973",
                database=db_name
            )
            cursor = conn.cursor(dictionary=True)  # Create a cursor object

            cursor.execute(f"SELECT DISTINCT `Bus Route Name` FROM {table_name}")  # Fetch distinct bus routes
            bus_routes = [row['Bus Route Name'] for row in cursor.fetchall()]  # Store bus routes in a list

            cursor.execute(f"SELECT DISTINCT `Bus Type` FROM {table_name}")  # Fetch distinct bus types
            bus_types = [row['Bus Type'] for row in cursor.fetchall()]  # Store bus types in a list
            
            # Log all distinct bus types retrieved
            logging.debug(f"Bus Types Retrieved: {bus_types}")

            max_price_value = get_max_price(db_name, table_name)  # Fetch the maximum price from the database

            cursor.close()  # Close the cursor
            conn.close()  # Close the database connection
        except Exception as e:  # Handle exceptions during database access
            st.error(f"Error accessing database: {e}")
            return

        selected_route = st.sidebar.selectbox('Select Bus Route', [''] + bus_routes)  # Dropdown to select bus route
        selected_type = st.sidebar.selectbox('Select Bus Type', [''] + bus_types)  # Dropdown to select bus type

        max_rating = st.sidebar.slider('Maximum Rating', min_value=0.0, max_value=5.0, step=0.1, value=5.0)  # Slider for maximum rating
        min_price = st.sidebar.number_input('Minimum Price', min_value=0.0, step=1.0, value=0.0)  # Number input for minimum price
        max_price = st.sidebar.number_input('Maximum Price', min_value=0.0, max_value=max_price_value, step=1.0, value=max_price_value)  # Number input for maximum price

        start_time_min, end_time_min = st.sidebar.slider(
            'Select Departure Time Range',
            min_value=0, max_value=1439, value=(0, 1439), step=1,
            format="HH:MM"  # Slider for departure time range
        )

        start_time_hhmm = convert_minutes_to_hhmm(start_time_min)  # Convert start time to HH:MM format
        end_time_hhmm = convert_minutes_to_hhmm(end_time_min)  # Convert end time to HH:MM format

        st.sidebar.write(f"Departure Time Range: {start_time_hhmm} to {end_time_hhmm}")  # Display selected time range

        filtered_df = fetch_filtered_data(db_name, table_name, selected_route, selected_type, max_rating, min_price, max_price, start_time_min, end_time_min)  # Fetch filtered data

        st.subheader('Filtered Bus Details')  # Subheader for filtered bus details
        st.dataframe(filtered_df)  # Display the filtered data in a table

        st.write(f"Number of buses filtered: {len(filtered_df)}")  # Display the number of buses filtered

if __name__ == '__main__':  # Run the main function if the script is executed directly
    main()
