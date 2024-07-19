import streamlit as st
import pandas as pd
import sqlite3
def fetch_data(db_name, table_name):
    conn = sqlite3.connect(db_name)
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, conn)
    conn.close()
    return df
def filter_data(df, bus_route=None, bus_type=None, min_rating=None, max_price=None):
    filtered_df = df.copy()

    if bus_route:
        filtered_df = filtered_df[filtered_df['bus_route_name'] == bus_route]

    if bus_type:
        filtered_df = filtered_df[filtered_df['bus_type'] == bus_type]

    if min_rating:
        filtered_df = filtered_df[filtered_df['star_rating'] >= min_rating]

    if max_price:
        filtered_df = filtered_df[filtered_df['price'] <= max_price]

    return filtered_df

def main():
    st.title('Data Filtering Application')
    st.subheader('Choose the State')

    states = ["Kerala", "Kadamba", "West Bengal", "Jammu_Kashmir", "Telangana", 
              "Rajasthan", "North Bengal", "Chandigarh", "Punjab", "Assam"]

    selected_state = st.selectbox('Select State', [''] + states)

    if selected_state:
        if st.button('Continue'):
            st.write(f"Filtering data for {selected_state}")

            db_name = f"{selected_state.lower().replace(' ', '_')}.db"
            table_name = selected_state.lower().replace(' ', '_')
            
            df = fetch_data(db_name, table_name)

            st.sidebar.header('Filters')

            bus_routes = df['bus_route_name'].unique()
            selected_route = st.sidebar.selectbox('Select Bus Route', [''] + list(bus_routes))

            bus_types = df['bus_type'].unique()
            selected_type = st.sidebar.selectbox('Select Bus Type', [''] + list(bus_types))

            min_rating = st.sidebar.slider('Minimum Rating', min_value=0.0, max_value=5.0, step=0.1)

            max_price = st.sidebar.number_input('Maximum Price', min_value=0.0)

            filtered_df = filter_data(df, selected_route, selected_type, min_rating, max_price)

            st.subheader('Filtered Bus Details')
            st.dataframe(filtered_df)

if __name__ == '__main__':
    main()
