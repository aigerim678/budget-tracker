import redis
from app.settings import cache

redis_client = redis.Redis(host=cache.host, port=cache.port, db=cache.db, password=cache.password, decode_responses=True)
