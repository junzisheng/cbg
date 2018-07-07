from django.test import TestCase

# Create your tests here.
import redis
s = redis.StrictRedis(host='127.0.0.1', password='Xj3.14164', db=3)
print(s.ttl('a'))
