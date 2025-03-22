from fastapi import FastAPI, HTTPException
import psycopg2
import redis
import time

app = FastAPI()

# PostgreSQL connection
POSTGRES_CONFIG = {
    "dbname": "experiment",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432,
}

# Redis connection
REDIS_CONFIG = {
    "host": "localhost",
    "port": 6379,
    "db": 0,
    "password": "9941cc15f59e41cb7be6c52", 
}

# Connect to PostgreSQL
def get_postgres_connection():
    return psycopg2.connect(**POSTGRES_CONFIG)

# Connect to Redis
redis_client = redis.Redis(**REDIS_CONFIG)

# Endpoint to fetch data from PostgreSQL
@app.get("/postgres")
def fetch_from_postgres():
    start_time = time.time()
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM large_data LIMIT 1000;")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        end_time = time.time()
        return {
            "data": data,
            "response_time_seconds": end_time - start_time,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to fetch data from Redis
@app.get("/redis")
def fetch_from_redis():
    start_time = time.time()
    try:
        # Check if data is cached in Redis
        cached_data = redis_client.get("large_data")
        if cached_data:
            end_time = time.time()
            return {
                "data": cached_data.decode("utf-8"),
                "response_time_seconds": end_time - start_time,
            }
        else:
            # Fetch data from PostgreSQL and cache it in Redis
            conn = get_postgres_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM large_data LIMIT 1000;")
            data = cursor.fetchall()
            cursor.close()
            conn.close()
            # Cache data in Redis
            redis_client.set("large_data", str(data))
            end_time = time.time()
            return {
                "data": data,
                "response_time_seconds": end_time - start_time,
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)