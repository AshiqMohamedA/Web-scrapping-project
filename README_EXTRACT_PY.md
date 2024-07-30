## Transport Bus Details Scraper
This project scrapes bus details for the Kerala Transport Corporation from the Redbus website. It uses Selenium for web scraping and stores the extracted data in a SQLite database and a CSV file. This data includes bus names, types, departure and arrival times, duration, star ratings, prices, and seat availability.

## Table of Contents
Prerequisites
Project Structure
Explanation
Database Schema
Output
## Prerequisites
Before running the script, ensure you have the following installed:

Python 3.x
Google Chrome browser
Streamlit
Pandas
SQLite3
Selenium
Project Structure
The project includes the following components:

scraper.py: The main script that performs web scraping and data storage.
Kerala.db: The SQLite database where the scraped data is stored.
Kerala.csv: The CSV file containing the scraped data.
Explanation
Imports and Setup
The script imports necessary libraries like Selenium for web scraping, SQLite3 for database operations, Pandas for data manipulation, and time for managing delays.

WebDriver Initialization
The Selenium WebDriver is initialized using Chrome, navigating to the Redbus URL for Kerala Transport Corporation. The browser window is maximized, and a delay is added to ensure the page fully loads.

Scrolling Function
The scroll_to_load function scrolls to the bottom of the page to load all dynamic content. It repeatedly performs this action until no new content is detected.

Extracting Route Links
The extract_route_links function collects the links and titles of bus routes. It waits for the route elements to be present and gathers their href attributes (links) and title attributes (route names) into a list.

Navigating Through Pages
The navigate_to_next_page function handles pagination by clicking the next page button. It handles exceptions for missing elements, timeouts, or elements blocked by overlays.

Extracting Bus Details
The extract_bus_details function gathers detailed information about buses from a specific route page. It navigates to the route link, attempts to click the "View Buses" button if present, scrolls to load all bus details, and waits for elements to be present. It collects details such as bus name, type, departure and arrival times, duration, rating, price, and seat availability.

Collecting All Route Links
The script initially collects all route links by scrolling through the page. It iterates through subsequent pages using pagination, accumulating all route links into a list.

Extracting All Bus Details
The script iterates over each collected route link, extracts bus details for each route, and accumulates the information into a list. It then closes the WebDriver.

Creating DataFrame and Database
The script checks if any bus details were collected and creates a Pandas DataFrame to hold the data. It connects to a SQLite database, creating a table to store the bus details if it doesn't already exist.

Inserting Data into Database
The script inserts the bus details from the DataFrame into the SQLite database, iterating over each row and executing an SQL insert statement. It commits the transaction and closes the database connection.

Saving Data to CSV
Finally, the script saves the bus details to a CSV file if the DataFrame is not empty. It notifies the user if the data was saved successfully or if no data was available. The DataFrame is also printed for review.

## Database Schema
The SQLite table Kerala is created with the following schema:

id INTEGER PRIMARY KEY AUTOINCREMENT
bus_route_name TEXT
route_link TEXT
bus_name TEXT
bus_type TEXT
departing_time DATETIME
reaching_time DATETIME
duration TEXT
star_rating FLOAT
price DECIMAL
seat_availability INTEGER
## Output
The scraped data is stored in a SQLite database Kerala.db.
The data is also saved in a CSV file Kerala.csv.
The script prints the DataFrame containing the scraped data.
