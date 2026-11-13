from flask import Flask
import os
import redis

app = Flask(__name__)

@app.route("/")
def home():
    version = os.getenv("APP_VERSION", "2.0")
    return f"""
    <h1>Lab 2 - Kubernetes Deployment</h1>
    <h2>Welcome to DevOps Lab - Version 2!</h2>
    <p>Application Version: {version}</p>
    <p>Rolling update completed successfully.</p>
    """

@app.route("/health")
def health():
    return {"status": "healthy"}

@app.route("/cache")
def cache():
    try:
        r = redis.Redis(
            host=os.getenv("REDIS_HOST", "redis"),
            port=6379,
            decode_responses=True
        )
        count = r.incr("visits")
        return {"message": "Redis connected", "visits": count}
    except redis.RedisError:
        return {"message": "Redis is not available"}, 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
