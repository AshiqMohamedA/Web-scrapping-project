import streamlit as st
import pandas as pd
import sqlite3

# Here the Function to fetch data from the SQLite database
def fetch_data(db_name, table_name):
    conn = sqlite3.connect(db_name)  # it Connecting to the SQLite database
    query = f"SELECT * FROM {table_name}"   # In here the SQL query to select all data from the specified table
    df = pd.read_sql(query, conn)   # Read SQL query into a DataFrame
    conn.close()  # Clossing the database connection
    return df   # return the dataframe

# Here the Function to filter the data based on user input
def filter_data(df, bus_route=None, bus_type=None, min_rating=None, max_price=None):
    filtered_df = df.copy()  # In here it Create a copy of the DataFrame to avoid modifying the original

    # In here it Filtering by bus details if specified
    if bus_route:
        filtered_df = filtered_df[filtered_df['bus_route_name'] == bus_route]

    if bus_type:
        filtered_df = filtered_df[filtered_df['bus_type'] == bus_type]

    if min_rating:
        filtered_df = filtered_df[filtered_df['star_rating'] >= min_rating]

    if max_price:
        filtered_df = filtered_df[filtered_df['price'] <= max_price]

    return filtered_df

# It is the Main function to create the streamlit app
def main():
    st.title('Data Filtering Application') # tittle
    st.subheader('Choose the State')# sub tittle for state selection

    # list of states available in here
    states = ["Kerala", "Kadamba", "westbengal", "Jammu_Kashmir", "Telengana", 
              "Rajasthan", "Northbengal", "Chandigarh", "Punjab", "Assam"]
    
    # It Dropdown menu for selecting the state
    selected_state = st.selectbox('Select State', [''] + states)

    # If a state is selected
    if selected_state:
        # Construct database name and table name based on the selected state
        db_name = f"{selected_state.lower().replace(' ', '_')}.db"
        table_name = selected_state.lower().replace(' ', '_')

        # It Fetch data from the selected state's database and table
        df = fetch_data(db_name, table_name)

        st.sidebar.header('Filters')   # Sidebar header for filters

        # Dropdown menu for selecting bus route
        bus_routes = df['bus_route_name'].unique()
        selected_route = st.sidebar.selectbox('Select Bus Route', [''] + list(bus_routes))

        # Dropdown menu for selecting bus type
        bus_types = df['bus_type'].unique()
        selected_type = st.sidebar.selectbox('Select Bus Type', [''] + list(bus_types))

        # Slider for selecting minimum rating
        min_rating = st.sidebar.slider('Minimum Rating', min_value=0.0, max_value=5.0, step=0.1)

        # Input field for selecting maximum price
        max_price = st.sidebar.number_input('Maximum Price', min_value=0.0)

        # Apply filters to the data based on user input
        filtered_df = filter_data(df, selected_route, selected_type, min_rating, max_price)

        st.subheader('Filtered Bus Details')   # Subtitle for displaying filtered data
        st.dataframe(filtered_df)    # Display the filtered DataFrame

        st.write(f"Number of buses filtered: {len(filtered_df)}")  # Display the number of filtered buses

# Here it Run the main function if this script is executed directly
if __name__ == '__main__':
    main()

