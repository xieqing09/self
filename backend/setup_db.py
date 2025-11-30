import mysql.connector
import sys

def setup_database():
    host = '127.0.0.1'
    port = 3306
    user = 'root'
    password = 'xcqlife0918'
    db_name = 'wechat_finetune'
    
    print(f"Connecting to MySQL to setup database '{db_name}'...")
    
    try:
        conn = mysql.connector.connect(
            host=host, 
            port=port,
            user=user, 
            password=password
        )
        cursor = conn.cursor()
        
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        print(f"Database '{db_name}' created or already exists.")
        
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as err:
        print(f"\nDatabase setup failed: {err}")
        return False

if __name__ == "__main__":
    success = setup_database()
    sys.exit(0 if success else 1)
