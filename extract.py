import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import pandas as pd
import time

#initialize the chrome driver
driver = webdriver.Chrome()

#webpage to scrap
url = "https://www.redbus.in/online-booking/west-bengal-transport-corporation?utm_source=rtchometile"
driver.get(url)
time.sleep(5) # wait for page to load 

#defining the function to scroll down
def scroll_to_load():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# defining the function to extract the route links for the current page
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

# defining the function to navigate the next page of route links
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

# defining the function to extract the bus details from a specific route link
def extract_bus_details(route_link, route_name):
    try:
        driver.get(route_link)
        time.sleep(3)  # Here it will wait for the page to load

        #  Here it Scroll down the page to load all bus details

        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3) 
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        #
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'bus-item-details'))
        )
        
        buses_loaded = driver.find_elements(By.CLASS_NAME, 'bus-item-details')
        bus_details_list = []
        
        for bus in buses_loaded:
            try:

                # it will extract the details of each bus
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
                

                # it will store the details in a dictionary
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
        
# Here it start scrapping process
all_route_links = []

scroll_to_load() # it load all content on the first page
current_page_links = extract_route_links() # it Get route links from the first page
all_route_links.extend(current_page_links)  # it Add links to the list

 # Here it Navigate through all pages and collect route links
page_num = 2
while navigate_to_next_page(page_num):
    time.sleep(5)  # wait for the next page to load
    scroll_to_load() # it load all the content of the next page
    current_page_links = extract_route_links() # next page  for to get route link
    all_route_links.extend(current_page_links) # and add links to a list
    page_num += 1

# it Extract bus details for each route
all_bus_details = []

for link, name in all_route_links:
    bus_details = extract_bus_details(link, name)
    all_bus_details.extend(bus_details) # add bus details into list

driver.quit() # it will close the browser

#saving the bus details into as a cvs file and sql database
if all_bus_details:
    bus_details_df = pd.DataFrame(all_bus_details)
else:
    print("No bus details were extracted.")
    bus_details_df = pd.DataFrame()

# Here it Connect to SQLite database and create table if it does not exist
conn = sqlite3.connect('westbengal.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS westbengal (
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

# Here it Insert bus details into the database
for _, row in bus_details_df.iterrows():
    cursor.execute('''
        INSERT INTO westbengal (
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

# Here it Save bus details to a CSV file if data is available
if not bus_details_df.empty:
    bus_details_df.to_csv('bus_details.csv', index=False)
    print("Data saved to CSV file 'bus_details.csv'.")
else:
    print("No bus details were saved to CSV.")

print(bus_details_df)
 
