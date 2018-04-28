from share.setting_share import *
import redis
RUN_LOCATION = 'ESC'

DATABASE = {'default':   {   'ENGINE'    :   'django_mysqlpool.backends.mysqlpool',
                             'NAME'      :   'sql_test',
                             'USER'      :   'root',
                             'PASSWORD'  :   'guwenjiang',
                             'HOST'      :   HOST_TEST_SEREVER ,
                             'PORT'      :   '3306',
                             },
            }

redis2 = redis.StrictRedis(host='127.0.0.1', password='Xj3.14164', db=2)
redis3 = redis.StrictRedis(host='127.0.0.1', password='Xj3.14164', db=3)
