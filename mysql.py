import mysql.connector
import pandas as pd

# Load data (adjust the file path and name as needed)
data_df = pd.read_csv('Kerala.csv')  # Assuming the file is saved as 'Kerala.csv'

# MySQL connection details
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Abdul@1973',
    database='redbus'  # Use the correct database name
)
cursor = conn.cursor()

# Drop the table if it exists to avoid any conflicts
cursor.execute("DROP TABLE IF EXISTS Kerala")

# Create the table with backticks for column names with spaces
create_table_query = '''
CREATE TABLE Kerala(
    `Bus Route Name` VARCHAR(255),
    `Bus Name` VARCHAR(255),
    `Bus Type` VARCHAR(100),
    `Departing Time` VARCHAR(50),
    `Duration` VARCHAR(50),
    `Reaching Time` VARCHAR(50),
    `Star Rating` VARCHAR(10),
    `Price` VARCHAR(50),  -- Store Price as VARCHAR to keep the INR prefix
    `Seat Availability` VARCHAR(50),
    `Route Link` TEXT
);
'''
cursor.execute(create_table_query)

# Insert data from DataFrame into the table
for index, row in data_df.iterrows():
    cursor.execute(
        '''
        INSERT INTO Kerala (`Bus Route Name`, `Bus Name`, `Bus Type`, `Departing Time`, 
                            `Duration`, `Reaching Time`, `Star Rating`, `Price`, 
                            `Seat Availability`, `Route Link`) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''',
        (row['Bus Route Name'], row['Bus Name'], row['Bus Type'], row['Departing Time'], 
         row['Duration'], row['Reaching Time'], row['Star Rating'], row['Price'], 
         row['Seat Availability'], row['Route Link'])
    )

# Commit the transaction
conn.commit()

# Close the connection
cursor.close()
conn.close()

print("Data inserted into the MySQL database successfully.")
