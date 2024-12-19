import mysql.connector
from mysql.connector import Error
import config



# Function to check if the database exists, and create it if not
def check_and_create_database():
    credentials = config.MysqlCredentials()
    try:
        # Connect to MySQL server (not specific to any database)
        connection = mysql.connector.connect(
            host= credentials.get_host(),
            user=credentials.get_user(),
            password=credentials.get_password()
        )
        
        if connection.is_connected():
            print("Successfully connected to MySQL server")

            # Create a cursor object
            cursor = connection.cursor()
            
            # Check if the database exists
            # cursor.execute("SHOW DATABASES LIKE %s", (credentials.get_name()))
            # result = cursor.fetchone()
            
            # if result:
            #     print(f"Database '{credentials.get_name()}' already exists.")
            # else:
            #     print(f"Database '{credentials.get_name()}' not found. Creating the database...")
            #     cursor.execute(f"CREATE DATABASE {credentials.get_name}")
            #     print(f"Database '{credentials.get_name()}' created successfully.")
                
            # Switch to the created or existing database
            cursor.execute(f"USE {credentials.get_name()}")
            
            # Create the stock information table if it does not exist
            create_table_query = """
            CREATE TABLE IF NOT EXISTS stock_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                stock_symbol VARCHAR(10) NOT NULL,
                date DATE NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                volume INT NOT NULL
            );
            """
            cursor.execute(create_table_query)
            print("Table 'stock_data' is ready.")
            
            # Insert stock data
            insert_query = """
            INSERT INTO stock_data (stock_symbol, date, price, volume)
            VALUES (%s, %s, %s, %s);
            """
            # Example stock data to insert
            stock_data = [
                ('AAPL', '2024-12-18', 175.34, 150000),
                ('GOOGL', '2024-12-18', 2800.56, 120000),
                ('AMZN', '2024-12-18', 3350.76, 100000)
            ]
            cursor.executemany(insert_query, stock_data)
            connection.commit()
            print("Stock data inserted successfully.")
            
            # Close the cursor and connection
            cursor.close()
            connection.close()

    except Error as e:
        print("Error while connecting to MySQL:", e)

# Run the function to check, create database and insert stock data
check_and_create_database()
