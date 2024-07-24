# Bus Details Filtering Application

## Overview
The Streamlit application is designed to filter and display bus details from a SQLite database. Users can select different filters, such as bus route, bus type, minimum rating, and maximum price, to narrow down the bus details they are interested in.

## Functionality Breakdown

### 1. Fetching Data
The application connects to a SQLite database to fetch the bus details. The database name is determined based on the user's selection from a list of states. Once connected, it queries the relevant table and retrieves the data, which is then loaded into a pandas DataFrame for further processing.

### 2. Filtering Data
The application provides several filtering options via the sidebar:
- **Bus Route**: Users can select a specific bus route from the available routes in the data.
- **Bus Type**: Users can choose a specific type of bus from the available types in the data.
- **Minimum Rating**: Users can set a slider to filter buses by their star rating, specifying a minimum rating threshold.
- **Maximum Price**: Users can input a maximum price value to filter out buses that exceed this price.

Based on the user’s input, the application filters the DataFrame to only include rows that meet the specified criteria.

### 3. User Interface
The user interface is built using Streamlit and consists of the following components:
- **Title and State Selection**: The main part of the application displays a title and a dropdown menu where users can select a state. This selection determines which database file will be accessed.
- **Sidebar Filters**: The sidebar contains several filtering options. Users can set these filters to narrow down the bus details displayed.
- **Filtered Data Display**: The filtered bus details are displayed in a table format. Additionally, the application shows the total number of buses that match the filter criteria.

## Step-by-Step Process

### Title and State Selection
When users open the application, they see the main title and a dropdown menu for state selection. They can choose from a list of predefined states.

### Database Connection
Once a state is selected, the application constructs the database name based on the state and connects to the corresponding SQLite database. It then queries the database to fetch all bus details and loads this data into a pandas DataFrame.

### Sidebar Filters
The sidebar provides options for users to filter the data:
- **Bus Route**: A dropdown menu lists all unique bus routes in the data.
- **Bus Type**: Another dropdown menu lists all unique bus types.
- **Minimum Rating**: A slider allows users to set a minimum star rating for the buses.
- **Maximum Price**: An input field where users can specify a maximum price.

### Data Filtering
The application filters the DataFrame based on the user-selected criteria. Each filter (bus route, bus type, minimum rating, and maximum price) is applied sequentially to refine the data.

### Displaying Results
The filtered bus details are displayed in the main part of the application. The DataFrame is shown in a table format, and the application also displays the number of buses that match the filter criteria.

## Conclusion
This Streamlit application provides a user-friendly interface for filtering and viewing bus details from a SQLite database. It allows users to easily narrow down their search using multiple filter options and presents the filtered data in an organized manner. The use of pandas for data manipulation and Streamlit for the interactive interface makes it a powerful tool for users to explore bus details efficiently.
