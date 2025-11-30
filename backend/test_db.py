import mysql.connector
import sys

def test_connection():
    host = '127.0.0.1'
    port = 3306
    user = 'root'
    password = 'xcqlife0918'
    
    print(f"Attempting to connect to MySQL at {host}:{port} with user '{user}'...")
    
    try:
        conn = mysql.connector.connect(
            host=host, 
            port=port,
            user=user, 
            password=password,
            connection_timeout=5
        )
        print("Successfully connected to MySQL!")
        
        # Check available databases
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES;")
        databases = cursor.fetchall()
        print("\nAvailable databases:")
        for db in databases:
            print(f"- {db[0]}")
            
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as err:
        print(f"\nConnection failed: {err}")
        return False
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
