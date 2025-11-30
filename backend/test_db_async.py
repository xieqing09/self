import asyncio
import aiomysql
import sys

async def test_connection():
    host = '127.0.0.1'
    port = 3306
    user = 'root'
    password = 'xcqlife0918'
    
    print(f"Attempting to connect to MySQL (Async) at {host}:{port} with user '{user}'...")
    
    try:
        conn = await aiomysql.connect(
            host=host, 
            port=port,
            user=user, 
            password=password,
            connect_timeout=5
        )
        print("Successfully connected to MySQL (Async)!")
        conn.close()
        return True
    except Exception as e:
        print(f"\nAsync Connection failed: {e}")
        return False

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    success = asyncio.run(test_connection())
    sys.exit(0 if success else 1)
