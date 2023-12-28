import mysql.connector

# Replace these with your actual MySQL database credentials
host = 'sql12.freesqldatabase.com'
user = 'sql12671860'
password = '9J6YkYHHUw'
database = 'sql12671860'

try:
    # Connect to the MySQL database
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Now you can execute SQL queries using the cursor
    # For example, let's create a simple table
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL
    )
    '''
    cursor.execute(create_table_query)

    # Commit the changes to the database
    conn.commit()

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    # Close the cursor and connection when you're done
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()