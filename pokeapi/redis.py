import redis
from pokeapi.config import settings

redis_client = redis.Redis(host='localhost', port=6379, db=0)
