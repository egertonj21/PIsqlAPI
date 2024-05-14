import mysql.connector

# MariaDB Settings
DB_HOST = "localhost"
DB_USER = "new_user"
DB_PASSWORD = "user_password"
DB_NAME = "mydatabase"

try:
    # Connect to the MariaDB database
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    # Check if the connection was successful
    if conn.is_connected():
        print("Connected to MariaDB")
    
    # Close the connection
    conn.close()

except mysql.connector.Error as err:
    print("Error:", err)


