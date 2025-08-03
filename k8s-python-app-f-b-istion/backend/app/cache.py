import redis
import os

def get_redis_connection():
    try:
        r = redis.Redis(
            host=os.environ.get("REDIS_HOST"),
            port=int(os.environ.get("REDIS_PORT")),
            password=os.environ.get("REDIS_PASSWORD"),
            db=0,
            socket_connect_timeout=5,
            decode_responses=True
        )
        r.ping()
        return r
    except redis.exceptions.RedisError as e:
        print(f"Error connecting to Redis: {e}")
        return None

def get_redis_data(r_conn):
    if not r_conn:
        return {"redis_status": "Error: Not connected to Redis"}
        
    try:
        info = r_conn.info()
        return {"redis_version": info.get("redis_version"), "uptime_in_seconds": info.get("uptime_in_seconds")}
    except redis.exceptions.RedisError as e:
        return {"redis_status": f"Error querying Redis: {e}"}