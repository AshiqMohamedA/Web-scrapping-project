## Bus Data Filtering Application
This is a Streamlit-based web application that allows users to filter and view bus details from a MySQL database. The application provides multiple filtering options, including bus route, bus type, star rating, price range, and departure time.

## Prerequisites
Before running the application, ensure you have the following installed:

Python 3.x
Streamlit: For the web interface.
MySQL Connector: For connecting to the MySQL database.
## You can install the required Python packages using:
pip install streamlit mysql-connector-python pandas
## MySQL Setup
Make sure you have MySQL installed and running, with a database named redbus. The database should contain tables for different states, each table storing bus data. The table structure should match the following columns:

Bus Route Name
Bus Name
Bus Type
Departing Time
Duration
Reaching Time
Star Rating
Price
Seat Availability
Route Link
## Application Structure
bus_filter_app.py: The main script containing the Streamlit app code.
README.md: This documentation file.
## Running the Application
Ensure MySQL is running on your local machine with the database and tables correctly set up.

Update Database Connection:

Ensure that the database connection details in the script match your local setup. Specifically, check the host, user, password, and database parameters in the MySQL connection calls.
Run the Streamlit App:

## Navigate to the directory containing the script and run the following command:

streamlit run bus_filter_app.py
The application should open in your default web browser.
## Features
## 1. State Selection:
Select from a list of Indian states to view the bus details specific to that region.
## 2. Filtering Options:
Bus Route: Select a specific bus route.
Bus Type: Filter by the type of bus (e.g., Sleeper, AC, etc.).
Maximum Rating: Set a maximum star rating to filter out lower-rated buses.
Price Range: Specify minimum and maximum prices to narrow down your search.
Departure Time Range: Select a departure time range using a slider to filter buses by their departure time.
## 3. Data Display:
Filtered bus details are displayed in a table with columns for each relevant attribute.
The number of buses that match the filters is displayed.
## Logging
The application logs key events and errors to the console using Python's built-in logging module.
Debugging: The application logs details such as SQL queries and the distinct values retrieved for bus routes and bus types.
## Limitations
Database Connection: Ensure the MySQL database is accessible from your local machine.
SQL Injection: The application uses parameterized queries to prevent SQL injection attacks.
Time Format: The departure time filtering assumes that the time is stored in HH:MM format in the database.
## License
This project is licensed under the MIT License.

## Acknowledgments
Streamlit Documentation

MySQL Connector Python Documentation

Pandas Documentation
