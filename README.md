# Transport Bus Details Scraper

This project is designed to scrape bus details for the  Transport Corporation from the Redbus website. The script uses Selenium for web scraping and SQLite for storing the extracted data. Additionally, it saves the data in a CSV file for easy access and manipulation.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Explanation](#explanation)
- [Database Schema](#database-schema)
- [Output](#output)

## Prerequisites

Before running the script, ensure you have the following installed:

- Python 3.x
- Google Chrome browser
- Streamlit
- Pandas
- SQLite3
- Selenium

## Explanation

1. Imports and Setup
This section imports the necessary libraries, such as selenium for web scraping, sqlite3 for database operations, pandas for data manipulation, and time for managing delays.

2. WebDriver Initialization
The Selenium WebDriver is initialized using Chrome, and the script navigates to the Redbus URL for the West Bengal Transport Corporation. The browser window is maximized, and a delay is added to ensure the page loads completely.

3. Scrolling Function
The scroll_to_load function scrolls the webpage to ensure all dynamic content is loaded. It repeatedly scrolls to the bottom of the page and waits for new content to load until no new content is detected.

4. Extracting Route Links
The extract_route_links function extracts the links and titles of bus routes listed on the page. It waits for the route elements to be present and collects their href attributes (links) and title attributes (route names) into a list.

5. Navigating Through Pages
The navigate_to_next_page function handles pagination by clicking the next page button. It waits for the button to be clickable, scrolls to it, and clicks it. It also manages exceptions for missing elements, timeouts, or elements blocked by other overlays.

6. Extracting Bus Details
The extract_bus_details function extracts detailed information about buses from a specific route page. It navigates to the route link, scrolls to load all bus details, and waits for the elements to be present. It collects details such as bus name, type, departure and arrival times, duration, rating, price, and seat availability.

7. Collecting All Route Links
This section collects all route links by scrolling through the initial page to load all content and then iterating through subsequent pages using pagination. It accumulates all route links into a list.

8. Extracting All Bus Details
This part iterates over each collected route link, calls the function to extract bus details for each route, and accumulates all bus details into a list. It then closes the WebDriver.

9. Creating DataFrame and Database
This section checks if any bus details were collected and creates a pandas DataFrame to hold the data. It connects to a SQLite database and creates a table to store the bus details if it doesn't already exist.

10. Inserting Data into Database
This part inserts the bus details from the DataFrame into the SQLite database. It iterates over each row of the DataFrame and executes an SQL insert statement to add the data to the database table. Finally, it commits the transaction and closes the database connection.

11. Saving Data to CSV
This final section checks if the DataFrame is not empty and saves the bus details to a CSV file. It notifies the user if the data was successfully saved or if no data was available to save. It also prints the DataFrame for review.

## Database schema
The SQLite table westbengal(example) is created with the following schema:

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

The scraped data is stored in a SQLite database westbengal.db
The data is also saved in a CSV file westbengal.csv
The script prints the DataFrame containing the scraped data



