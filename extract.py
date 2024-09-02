from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import pandas as pd
import time

# Initialize the WebDriver
driver = webdriver.Chrome()

# Define the URL to be accessed
url = "https://www.redbus.in/online-booking/ksrtc-kerala/?utm_source=rtchometile"

# Load the web page
driver.get(url)

# Wait for the page to load
time.sleep(5)

# Maximize the browser window
driver.maximize_window()

# Function to scroll the page to load all content dynamically
def scroll_to_load():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Wait for content to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:  # Break if no new content is loaded
            break
        last_height = new_height

# Function to extract route links from the page
def extract_route_links():
    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'route'))
    )
    route_elements = driver.find_elements(By.CLASS_NAME, 'route')
    route_links = []
    for route in route_elements:
        href = route.get_attribute('href')  # Get the link
        title = route.get_attribute('title')  # Get the route title
        route_links.append((href, title))
    return route_links

# Function to navigate to the next page of search results
def navigate_to_next_page(page_num):
    try:
        next_page_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[@class='DC_117_paginationTable']//div[@class='DC_117_pageTabs ' and text()='{page_num}']"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", next_page_button)  # Scroll to the next page button
        driver.execute_script("arguments[0].click();", next_page_button)  # Click the next page button
        return True
    except NoSuchElementException:
        print("Next page button not found or end of pagination reached.")
        return False
    except TimeoutException:
        print("Timeout waiting for next page button to be clickable.")
        return False
    except ElementClickInterceptedException:
        print("Element click intercepted, handling overlay or pop-up.")
        return False

# Function to extract bus details from a specific route page
def extract_bus_details(route_link, route_name):
    try:
        driver.get(route_link)  # Navigate to the route page
        time.sleep(3)  # Wait for the page to load

        # Attempt to click the "View Buses" button, if present
        try:
            view_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'button'))
            )
            view_button.click()
            time.sleep(2)  # Wait for the details to load
        except NoSuchElementException:
            print("View button not found. Attempting to extract bus details directly.")
        except ElementClickInterceptedException:
            print("View button click intercepted.")

        # Scroll to load all buses on the page
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Wait until bus details are fully loaded
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'bus-item-details'))
        )

        buses_loaded = driver.find_elements(By.CLASS_NAME, 'bus-item-details')
        bus_details_list = []
        for bus in buses_loaded:
            try:
                bus_name = bus.find_element(By.CLASS_NAME, 'travels').text.strip()
                bus_type = bus.find_element(By.CLASS_NAME, 'bus-type').text.strip()
                departing_time = bus.find_element(By.CLASS_NAME, 'dp-time').text.strip()
                duration = bus.find_element(By.CLASS_NAME, 'dur').text.strip()
                reaching_time = bus.find_element(By.CLASS_NAME, 'bp-time').text.strip()
                try:
                    star_rating = bus.find_element(By.CLASS_NAME, 'rating').text.strip()
                except NoSuchElementException:
                    star_rating = 'N/A'
                price = bus.find_element(By.CLASS_NAME, 'fare').text.strip()
                seat_availability = bus.find_element(By.CLASS_NAME, 'seat-left').text.strip()

                # Store extracted bus details in a dictionary
                bus_details = {
                    'Bus Route Name': route_name,
                    'Bus Name': bus_name,
                    'Bus Type': bus_type,
                    'Departing Time': departing_time,
                    'Duration': duration,
                    'Reaching Time': reaching_time,
                    'Star Rating': star_rating,
                    'Price': price,
                    'Seat Availability': seat_availability,
                    'Route Link': route_link
                }
                bus_details_list.append(bus_details)
            except NoSuchElementException as e:
                print(f"Error processing bus details: {e}")

        return bus_details_list

    except TimeoutException:
        print(f"Timed out waiting for buses to load on route: {route_link}")
        return []
    except NoSuchElementException as e:
        print(f"Element not found while extracting bus details: {e}")
        return []

# Extract all route links by scrolling through the page
all_route_links = []
scroll_to_load()
current_page_links = extract_route_links()
all_route_links.extend(current_page_links)

# Navigate through pages and collect route links
page_num = 2
while navigate_to_next_page(page_num):
    time.sleep(5)  # Wait for the next page to load
    scroll_to_load()
    current_page_links = extract_route_links()
    all_route_links.extend(current_page_links)
    page_num += 1

# Extract bus details from all route links collected
all_bus_details = []
for link, name in all_route_links:
    bus_details = extract_bus_details(link, name)
    all_bus_details.extend(bus_details)

# Quit the WebDriver after completing the extraction
driver.quit()

# Save the extracted data into a DataFrame
if all_bus_details:
    bus_details_df = pd.DataFrame(all_bus_details)
    bus_details_df.to_csv('Kerala.csv', index=False)  # Save DataFrame to CSV
    print("Bus details extracted and saved to 'Kerala.csv' successfully.")
else:
    print("No bus details were extracted.")
