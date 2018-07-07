# 对一些使用的模块打一些补丁
import pymysql
import types
import traceback
import time
pymysql.install_as_MySQLdb()
import redis

"""对redis打补丁"""
class RedisMthodHookInstance(object):
    """拦截类的所有函数调用方法，输出调用信息"""
    id_call = 0

    def __init__(self , classname , method , logname):
        self.classname  = classname
        self.method     = method
        # self.object_logging = logging.getLogger(logname) if logname else None

    def __call__(self , *args , **kwargs):
        assert self.classname
        assert isinstance(self.method , types.MethodType)

        RedisMthodHookInstance.id_call += 1
        current_id = RedisMthodHookInstance.id_call

        key_hook = (self.classname , self.method.__name__)

        ts_now = time.time()
        retval = self.method(*args , **kwargs)
        ts_now = time.time() - ts_now

        if key_hook in HookClassMthod.dict_hook_class_method:
            try:
                args_str   = u''.join(u'%s, ' % (u"'" + arg + u"'" if isinstance(arg , types.StringTypes) else arg) for arg in args) if args else ''
                kwargs_str = u','.join(u'%s=%s' % (_k , u"'" + _v + u"'" if isinstance(_v , types.StringTypes) else _v) for _k , _v in kwargs.items()) if kwargs else ''
                retval_str = smart_decode(retval)

                debug_info = u'<--[%d] Hook %.3fs - %s.%s(%s%s) = %s' % (current_id , ts_now , self.classname , self.method.__name__ ,
                                                  args_str, kwargs, retval_str)

                val_track = {   'timestamp' :   time.time() ,
                                'duartion'  :   ts_now ,
                                'classname' :   key_hook[0] ,
                                'methodname':   key_hook[1] ,
                                'args'      :   args ,
                                'kwargs'    :   kwargs ,
                                'retval'    :   retval
                            }

                # >>> self.method.im_self.connection_pool.connection_kwargs
                # {'encoding': 'utf-8', 'encoding_errors': 'strict', 'socket_timeout': None, 'decode_responses': False, 'db': 3, 'host': '127.0.0.1', 'password': 'Xj3.14164', 'port': 6379}
                # >>> self.method.im_class
                # <class 'redis.client.StrictRedis'>
                # >>> self.method.im_class == redis.StrictRedis
                # True
                if self.method.im_class in (redis.StrictRedis , redis.client.StrictPipeline):
                    redis_kwars = self.method.im_self.connection_pool.connection_kwargs
                    val_track['host']   = redis_kwars['host']
                    val_track['port']   = redis_kwars['port']
                    val_track['db']     = redis_kwars['db']
                    val_track['type']   = 'redis'

                HookClassMthod.list_hook_class_result.append(val_track)

                # if self.object_logging:
                #     self.object_logging.info(debug_info)
            except UnicodeDecodeError:
                pass
            except:
                print(traceback.format_exc())

        return retval



