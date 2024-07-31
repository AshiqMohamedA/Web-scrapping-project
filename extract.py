import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import pandas as pd
import time

driver = webdriver.Chrome()
url = "https://www.redbus.in/online-booking/ksrtc-kerala/?utm_source=rtchometile"
driver.get(url)
time.sleep(5)  # Wait for the page to load
driver.maximize_window()

def scroll_to_load():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def extract_route_links():
    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'route'))
    )
    route_elements = driver.find_elements(By.CLASS_NAME, 'route')
    route_links = []
    for route in route_elements:
        href = route.get_attribute('href')
        title = route.get_attribute('title')
        route_links.append((href, title))
    return route_links

def navigate_to_next_page(page_num):
    try:
        next_page_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[@class='DC_117_paginationTable']//div[@class='DC_117_pageTabs ' and text()='{page_num}']"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", next_page_button)
        driver.execute_script("arguments[0].click();", next_page_button)
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

def extract_bus_details(route_link, route_name):
    try:
        driver.get(route_link)
        time.sleep(3)  # Wait for the page to load

        # Attempt to click the "View Buses" button, if present
        try:
            view_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'button'))  #  class name of the view button
            )
            view_button.click()
            time.sleep(2)  # Wait for the details to load
        except NoSuchElementException:
            print("View button not found. Attempting to extract bus details directly.")
        except ElementClickInterceptedException:
            print("View button click intercepted.")

        # Scroll to load all buses
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

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

# Extract route links
all_route_links = []
scroll_to_load()
current_page_links = extract_route_links()
all_route_links.extend(current_page_links)

# Navigate through pages and collect route links
page_num = 2
while navigate_to_next_page(page_num):
    time.sleep(5)
    scroll_to_load()
    current_page_links = extract_route_links()
    all_route_links.extend(current_page_links)
    page_num += 1

# Extract bus details from all route links
all_bus_details = []
for link, name in all_route_links:
    bus_details = extract_bus_details(link, name)
    all_bus_details.extend(bus_details)

# Quit the WebDriver
driver.quit()

# Save extracted data to SQLite and CSV
if all_bus_details:
    bus_details_df = pd.DataFrame(all_bus_details)
else:
    print("No bus details were extracted.")
    bus_details_df = pd.DataFrame()

conn = sqlite3.connect('Kerala.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Kerala (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bus_route_name TEXT,
        route_link TEXT,
        bus_name TEXT,
        bus_type TEXT,
        departing_time DATETIME,
        reaching_time DATETIME,
        duration TEXT,
        star_rating FLOAT,
        price DECIMAL,
        seat_availability INTEGER
    )
''')

conn.commit()

for _, row in bus_details_df.iterrows():
    cursor.execute('''
        INSERT INTO Kerala (
            bus_route_name, route_link, bus_name, bus_type,
            departing_time, reaching_time, duration, star_rating,
            price, seat_availability
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        row['Bus Route Name'], row['Route Link'], row['Bus Name'], row['Bus Type'],
        row['Departing Time'], row['Reaching Time'], row['Duration'], row['Star Rating'],
        row['Price'], row['Seat Availability']
    ))

conn.commit()
conn.close()

if not bus_details_df.empty:
    bus_details_df.to_csv('Kerala.csv', index=False)
    print("Data saved to CSV file 'Kerala.csv'.")
else:
    print("No bus details were saved to CSV.")
print(bus_details_df)
