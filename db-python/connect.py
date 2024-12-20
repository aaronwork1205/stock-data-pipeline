import mysql.connector
from mysql.connector import Error
import config



def check_and_create_database():
    credentials = config.MysqlCredentials()
    try:
        # Connect to MySQL server (not specific to any database)
        connection = mysql.connector.connect(
            host=credentials.get_host(),
            user=credentials.get_user(),
            password=credentials.get_password()
        )
        
        if connection.is_connected():
            print("Successfully connected to MySQL server")
            cursor = connection.cursor()
            
            # Check if the database exists
            cursor.execute("SHOW DATABASES")
            databases = [db[0] for db in cursor.fetchall()]
            db_name = credentials.get_name()
            if db_name not in databases:
                print(f"Database '{db_name}' not found. Creating the database...")
                cursor.execute(f"CREATE DATABASE {db_name}")
                print(f"Database '{db_name}' created successfully.")
            else:
                print(f"Database '{db_name}' already exists.")
            
            # Switch to the created or existing database
            cursor.execute(f"USE {db_name}")
            
            # Create the stock_data table if it does not exist
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
            
            # Insert sample stock data
            insert_query = """
            INSERT INTO stock_data (stock_symbol, date, price, volume)
            VALUES (%s, %s, %s, %s);
            """
            stock_data = [
                ('AAPL', '2024-12-18', 175.34, 150000),
                ('GOOGL', '2024-12-18', 2800.56, 120000),
                ('AMZN', '2024-12-18', 3350.76, 100000)
            ]
            cursor.executemany(insert_query, stock_data)
            connection.commit()
            print("Stock data inserted successfully.")
            
            cursor.close()
            connection.close()
    
    except Error as e:
        print("Error while connecting to MySQL:", e)

# Run the function
check_and_create_database()
