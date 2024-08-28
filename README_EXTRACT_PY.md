## Bus Details Scraper
This project is a Python script that automates the extraction of bus details from various regions using the Selenium web automation library. The script navigates through multiple pages of a website, extracts route links, and then scrapes detailed bus information for each route. The collected data is saved into a CSV file for each region.

## Prerequisites
Before running the script, ensure you have the following installed:

Python 3.x
Google Chrome Browser
ChromeDriver (compatible with your Chrome browser version)
Required Python libraries:
selenium
pandas
You can install the required Python libraries using the following command:

## bash
pip install selenium pandas

## Project Structure
bus_scraper.py: The main script that performs the web scraping for various regions, including Kerala.
Kerala.csv: The output CSV file containing the scraped bus details for Kerala (or other regions as specified in the script).
README.md: This documentation file.
## Usage
Set Up WebDriver:

Download and install ChromeDriver from here.
Ensure the path to chromedriver is added to your system's PATH, or modify the script to specify the path to chromedriver.
Run the Script:

Modify the script to specify the region you want to scrape and then execute the script using Python:

## bash
python bus_scraper.py

Extracted Data:

The script will save the extracted bus details into a CSV file named after the region being scraped, such as Kerala.csv.

## Script Details
Initialization:

The script initializes a Chrome WebDriver, navigates to the specified region's page, and maximizes the window.
Scrolling to Load All Routes:

The script scrolls the page to load all available route links for the specified region.
Route Links Extraction:

The script extracts all route links from the current page.
Pagination Handling:

The script navigates through multiple pages to collect all route links.
Bus Details Extraction:

For each route link, the script navigates to the corresponding page, loads all bus details, and extracts relevant information like bus name, type, departure time, duration, etc.
Error Handling:

The script includes error handling mechanisms to deal with common issues such as missing elements, timeouts, and click interceptions.
## Output
The script generates a CSV file named after the region being scraped (e.g., Kerala.csv), containing the following columns:
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
## Limitations
The script relies on the structure of the website; changes to the website's HTML structure may require adjustments to the script.
The script might not work correctly if dynamic content is loaded via JavaScript that Selenium cannot detect.
## License
This project is licensed under the MIT License.

## Acknowledgments
Selenium Documentation
pandas Documentation
