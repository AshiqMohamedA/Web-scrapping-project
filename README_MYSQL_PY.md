## Bus Data Importer to MySQL
This Python script imports bus route details from a CSV file into a MySQL database. It is designed to be flexible and can be used for various regions, not just Kerala.

## Prerequisites
Ensure you have the following installed:

Python 3.x
MySQL Server: Set up and running on your machine.
MySQL Connector/Python: For connecting to the MySQL database.
Pandas: For handling CSV data.
## Install Required Python Packages
pip install mysql-connector-python pandas
## Script Overview
## 1. Load CSV Data
The script loads bus route details from a CSV file using Pandas:

data_df = pd.read_csv('Kerala.csv')  # Adjust the file name as needed
## 2. Connect to MySQL Database
The script connects to a MySQL database using the credentials provided:

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Abdul@1973',
    database='redbus'  # Use your database name
)
## 3. Create the Table
The script creates a new table in the database to store the bus data. It drops the table if it already exists to avoid conflicts:

cursor.execute("DROP TABLE IF EXISTS Kerala")
create_table_query = '''
CREATE TABLE Kerala(
    `Bus Route Name` VARCHAR(255),
    `Bus Name` VARCHAR(255),
    `Bus Type` VARCHAR(100),
    `Departing Time` VARCHAR(50),
    `Duration` VARCHAR(50),
    `Reaching Time` VARCHAR(50),
    `Star Rating` VARCHAR(10),
    `Price` VARCHAR(50),
    `Seat Availability` VARCHAR(50),
    `Route Link` TEXT
);
'''
cursor.execute(create_table_query)
## 4. Insert Data into MySQL Table
The script iterates over each row in the DataFrame and inserts the data into the MySQL table:

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
## 5. Commit and Close the Connection
After inserting the data, the script commits the transaction and closes the database connection:

conn.commit()
cursor.close()
conn.close()
## 6. Adjustments for Other Regions
To use this script for a different region, simply change the CSV file name and ensure the column names in your CSV match those in the script. The table name can also be changed to reflect the region.

## Running the Script
Prepare Your Data: Ensure your CSV file is correctly formatted and located in the same directory as the script.

Modify the Script: Adjust the file name, database details, and table name as needed.

## Run the Script: Execute the script using Python:

python your_script_name.py
The data will be imported into the specified MySQL database and table.
## Notes
Data Types: The script stores price as VARCHAR to retain any currency symbols or prefixes.

Database Credentials: Ensure your MySQL credentials are secure, especially if deploying this script in a production environment.

Table Naming: The table name in the script (Kerala) should be updated based on the region or dataset you are importing.
## License
This project is licensed under the MIT License.

