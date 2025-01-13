# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

print('Zack')
print('')

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('mes_core')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
# Start of Test Query Code -- retrieve record from enterprise table in mes_core schema
# Connect to MySQL db

print("Start Test")

import mysql.connector

# Establishing the connection
cnx = mysql.connector.connect(
    user='Root',
    password='MySQLadmin42',
    host='127.0.0.1',
    database='mes_core'
)

try:
    # Creating a cursor to execute queries
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM enterprise")
    
    # Fetching all results from the query
    result = cursor.fetchall()
    print(result)
    
finally:
    # Closing the connection
    cnx.close()
