import streamlit as st
import pandas as pd
import sqlite3

# Function to convert total minutes to HH:MM format
def convert_minutes_to_hhmm(minutes):
    """Convert total minutes to HH:MM format."""
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours:02d}:{mins:02d}"

# Function to fetch data from SQLite database with filters applied
def fetch_filtered_data(db_name, table_name, bus_route=None, bus_type=None, min_rating=None, min_price=None, max_price=None, start_time=None, end_time=None):
    conn = sqlite3.connect(db_name)
    
    # Start building the SQL query
    query = f"SELECT * FROM {table_name} WHERE 1=1"  # Initial SQL query
    params = []  # List to store query parameters dynamically
    
    # Add conditions based on user inputs
    if bus_route:
        query += " AND bus_route_name = ?"
        params.append(bus_route)  # Append bus_route to parameters
    
    if bus_type:
        query += " AND bus_type = ?"
        params.append(bus_type)  # Append bus_type to parameters
    
    if min_rating is not None:
        query += " AND star_rating >= ?"
        params.append(min_rating)  # Append min_rating to parameters
    
    if min_price is not None:
        # Convert price format and add condition
        query += " AND CAST(REPLACE(REPLACE(price, 'INR ', ''), ',', '') AS REAL) >= ?"
        params.append(min_price)  # Append min_price to parameters
    
    if max_price is not None:
        # Convert price format and add condition
        query += " AND CAST(REPLACE(REPLACE(price, 'INR ', ''), ',', '') AS REAL) <= ?"
        params.append(max_price)  # Append max_price to parameters
    
    if start_time is not None and end_time is not None:
        # Add time range condition
        query += " AND (CAST(strftime('%H', departing_time) AS INTEGER) * 60 + CAST(strftime('%M', departing_time) AS INTEGER)) BETWEEN ? AND ?"
        params.extend([start_time, end_time])  # Extend params with start_time and end_time
    
    # Execute SQL query with parameters and fetch data into DataFrame
    df = pd.read_sql(query, conn, params=params)
    conn.close()  # Close database connection
    return df

# Function to fetch maximum price from the database
def get_max_price(db_name, table_name):
    conn = sqlite3.connect(db_name)  # Connect to SQLite database
    query = f"""
    SELECT MAX(CAST(REPLACE(REPLACE(price, 'INR ', ''), ',', '') AS REAL)) AS max_price
    FROM {table_name}
    """
    df = pd.read_sql(query, conn)  # Execute SQL query and fetch result into DataFrame
    conn.close()  # Close database connection
    return df['max_price'].values[0] if not df.empty else 0.0

def main():
    st.title('Bus Data Filtering Application')  # Application title
    st.subheader('Choose the State')  # Subheader for selecting state

    states = ["Kerala", "Kadamba", "westbengal", "Jammu_Kashmir", "Telengana", 
              "Rajasthan", "Northbengal", "Chandigarh", "Punjab", "Assam"]  # List of states

    selected_state = st.selectbox('Select State', [''] + states)  # Dropdown to select state

    if selected_state:
        db_name = f"{selected_state.lower().replace(' ', '_')}.db"  # Database name based on selected state
        table_name = selected_state.lower().replace(' ', '_')  # Table name based on selected state
        
        st.sidebar.header('Filters')  # Sidebar header for filters

        # Fetch unique values for bus routes and bus types from the database
        try:
            conn = sqlite3.connect(db_name)  # Connect to SQLite database
            # Fetch distinct bus routes and bus types
            bus_routes = pd.read_sql(f"SELECT DISTINCT bus_route_name FROM {table_name}", conn)['bus_route_name'].tolist()
            bus_types = pd.read_sql(f"SELECT DISTINCT bus_type FROM {table_name}", conn)['bus_type'].tolist()
            # Fetch the maximum price for setting the maximum value in the slider
            max_price_value = get_max_price(db_name, table_name)
            conn.close()  # Close database connection
        except Exception as e:
            st.error(f"Error accessing database: {e}")  # Display error message if database access fails
            return

        selected_route = st.sidebar.selectbox('Select Bus Route', [''] + bus_routes)  # Dropdown to select bus route
        selected_type = st.sidebar.selectbox('Select Bus Type', [''] + bus_types)  # Dropdown to select bus type

        min_rating = st.sidebar.slider('Minimum Rating', min_value=0.0, max_value=5.0, step=0.1, value=0.0)  # Slider for minimum rating
        min_price = st.sidebar.number_input('Minimum Price', min_value=0.0, step=1.0, value=0.0)  # Numeric input for minimum price
        max_price = st.sidebar.number_input('Maximum Price', min_value=0.0, max_value=max_price_value, step=1.0, value=max_price_value)  # Numeric input for maximum price

        # Time range slider in minutes
        start_time_min, end_time_min = st.sidebar.slider(
            'Select Departure Time Range',
            min_value=0, max_value=1439, value=(0, 1439), step=1,
            format="HH:MM"
        )

        # Convert minutes to HH:MM format for display
        start_time_hhmm = convert_minutes_to_hhmm(start_time_min)
        end_time_hhmm = convert_minutes_to_hhmm(end_time_min)

        st.sidebar.write(f"Departure Time Range: {start_time_hhmm} to {end_time_hhmm}")  # Display selected time range in HH:MM format

        # Fetch data with SQL filtering
        filtered_df = fetch_filtered_data(db_name, table_name, selected_route, selected_type, min_rating, min_price, max_price, start_time_min, end_time_min)

        st.subheader('Filtered Bus Details')  # Subheader for displaying filtered bus details
        st.dataframe(filtered_df)  # Display filtered bus details in DataFrame format

        st.write(f"Number of buses filtered: {len(filtered_df)}")  # Display number of buses filtered

if __name__ == '__main__':
    main()  # Call the main function when the script is executed
