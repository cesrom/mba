print('Start Test')

import mysql.connector

# Establish the connection
cnx = mysql.connector.connect(
    user='python',
    password='Bootcamp!',
    host='127.0.0.1',
    database='mes_core'
)

try:
    # Create a cursor
    cursor = cnx.cursor()
    
    # Execute a simple SELECT query
    cursor.execute("SELECT * FROM enterprise")
    
    # Fetch all the rows from the query result
    result = cursor.fetchall()
    
    # Print the result
    print(result)

finally:
    # Close the connection
    cnx.close()
