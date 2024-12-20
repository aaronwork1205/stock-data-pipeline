import mysql.connector
from mysql.connector import Error
import os
import pandas as pd
import config
from tqdm import tqdm

def insert_stock_data(stock_data, connection, table_name):
    try:
        # print(stock_data)
        if connection.is_connected():
            cursor = connection.cursor()

            # Define the INSERT query
            insert_query = f"""
            INSERT INTO `{table_name}` (date, open_price, high_price, low_price, close_price, adj_close_price, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            """

            # Insert the data
            cursor.executemany(insert_query, stock_data)
            connection.commit()
            # print(f"Inserted {cursor.rowcount} rows into the stock_data table.")


    except Error as e:
        print("Error while inserting data into MySQL:", e)


# Function to check and create database
def table_creation(stock_data,table_name, connection):

    try:
            # Create the stock_data table if it does not exist
            create_table_query = f"""
                CREATE TABLE IF NOT EXISTS `{table_name}` (
                date DATE NOT NULL,
                open_price DECIMAL(10, 2),
                high_price DECIMAL(10, 2),
                low_price DECIMAL(10, 2),
                close_price DECIMAL(10, 2),
                adj_close_price DECIMAL(10, 2),
                volume INT NOT NULL
                );
            """

            cursor.execute(create_table_query)
            # print(f"Table '{table_name}' is ready.")
            
            insert_stock_data(stock_data, connection, table_name)
    
    except Error as e:
        print("Error while connecting to MySQL:", e)


# Function to load CSV files from the 'hist' folder and insert data into the database
def load_csv_files_to_db(connection):
    folder_path = 'hist'
    for filename in tqdm(os.listdir(folder_path), desc="Processing files"):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            # print(f"Loading file: {file_path}")
            
            # Read CSV file into a DataFrame
            df = pd.read_csv(file_path)

            # Ensure the DataFrame has the correct columns
            # print(f"Columns in {filename}: {df.columns.tolist()}")

            # Assuming your CSV has these columns: Date, Open, High, Low, Close, Adj Close, Volume
            df = df.rename(columns={
                'Date': 'date',
                'Open': 'open_price',
                'High': 'high_price',
                'Low': 'low_price',
                'Close': 'close_price',
                'Adj Close': 'adj_close_price',
                'Volume': 'volume'
            })

            # Convert the date column to datetime format if necessary
            df['date'] = pd.to_datetime(df['date']).dt.date

            # Debugging: Print out the first few rows of the DataFrame
            # print(df.head())  # This will show the data and help identify any issues

            # Prepare data for insertion (convert the dataframe to a list of tuples)
            stock_data = [tuple(row) for row in df.values]

            # Debugging: Print the number of columns in the data
            # print(f"Number of columns: {len(df.columns)}")  # Ensure there are exactly 8 columns

            # Insert the stock data into the MySQL database
            table_creation(stock_data, filename[:-4], connection)



credentials = config.MysqlCredentials()
connection = mysql.connector.connect(
    host=credentials.get_host(),
    user=credentials.get_user(),
    password=credentials.get_password()
)

if connection.is_connected():
    # print("Successfully connected to MySQL server")
    cursor = connection.cursor()


    cursor.execute("SHOW DATABASES")
    databases = [db[0] for db in cursor.fetchall()]

    cursor.execute(f"USE {credentials.get_name()}")
    db_name = credentials.get_name()
    if db_name not in databases:
        print(f"Database '{db_name}' not found. Creating the database...")
        cursor.execute(f"CREATE DATABASE {db_name}")
        print(f"Database '{db_name}' created successfully.")
    else:
        print(f"Database '{db_name}' already exists.")

load_csv_files_to_db(connection)

cursor.close()
connection.close()


