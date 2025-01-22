import mysql.connector  # For MySQL
# import psycopg2  # For PostgreSQL

def connect_to_mysql():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="your_database"
    )
    return conn

# Uncomment this function if you're using PostgreSQL
# def connect_to_postgresql():
#     conn = psycopg2.connect(
#         dbname="your_database",
#         user="your_user",
#         password="your_password",
#         host="localhost"
#     )
#     return conn

def fetch_supplier_data(conn):
    cursor = conn.cursor()
    query = "SELECT supplier_name, supplier_info FROM suppliers"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result
