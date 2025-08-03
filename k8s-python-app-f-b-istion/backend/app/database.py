import pymysql
import os

def get_db_connection():
    try:
        connection = pymysql.connect(
            host=os.environ.get("MYSQL_HOST"),
            user=os.environ.get("MYSQL_USER"),
            password=os.environ.get("MYSQL_PASSWORD"),
            database=os.environ.get("MYSQL_DB"),
            connect_timeout=5
        )
        return connection
    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL Database: {e}")
        return None

def get_db_data(connection):
    if not connection:
        return {"db_status": "Error: Not connected to database"}
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION() as version;")
            result = cursor.fetchone()
            return {"mysql_version": result[0]}
    except pymysql.MySQLError as e:
        return {"db_status": f"Error querying database: {e}"}
    finally:
        if connection:
            connection.close()