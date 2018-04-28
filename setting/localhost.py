from share.setting_share import *
import redis
RUN_LOCATION = 'LOCAL'

DATABASE = {'default':   {   'ENGINE'    :   'django_mysqlpool.backends.mysqlpool',
                                   'NAME'      :   'test',
                                   'USER'      :   'wordpress',
                                   'PASSWORD'  :   'Xj3.14164',
                                   'HOST'      :   HOST_TEST_SEREVER ,
                                   'PORT'      :   '3306',
                                   },
                }

redis2 = redis.StrictRedis(host='127.0.0.1', password='Xj3.14164', db=2)
redis3 = redis.StrictRedis(host='127.0.0.1', password='Xj3.14164', db=3)
