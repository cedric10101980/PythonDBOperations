from flask import Flask, jsonify
import redis
import os

app = Flask(__name__)

# Function to connect to Redis
def connect_to_redis():
    try:
        cache = redis.Redis(host=os.getenv('REDIS_HOST', 'redis'), port=6379)
        cache.ping()  # Test the connection
        return cache
    except redis.ConnectionError as e:
        print(f"Redis connection error: {e}")
        return None

# Function to increment visit counter
def increment_visit_counter(cache):
    try:
        visits = cache.incr('counter')
        return f'This page has been visited {visits} times'
    except redis.ConnectionError as e:
        return jsonify({"error": "Redis connection error", "details": str(e)}), 500


# Initial connection attempt
cache = connect_to_redis()

@app.route('/')
def page_view():
    global cache
    if cache:
        result = increment_visit_counter(cache)
        if isinstance(result, str):
            return result
        else:
            cache = None
            return result
    else:
         # Attempt to reconnect
        cache = connect_to_redis()
        if cache:
            result = increment_visit_counter(cache)
            if isinstance(result, str):
                return result
            else:
                cache = None
                return result
        else:
            return jsonify({"error": "Redis connection not established"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5100)
