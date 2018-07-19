# -*- coding: utf8 -*-
"""
 *  jct.cache 的升级版本：
 *     >>  对django.cache的封装，保持原有(jct.cache.py)接口不变
 *     >>  使用django.cache中的version概念来管理key的失效，更简单易懂，更容易使缓存手动或者自动失效
 *
 * Create by Truan Wang on 2018/04/12
 *
 * Copyright ? 2014-2020 . 上海进馨网络科技有限公司 . All Rights Reserved
"""
from cbg_backup import settings
import os
from multiprocessing import Lock



def key_func(key, key_prefix, version):
    """ django默认的key_func将version放在key前面，与我们想达到的效果不一样
    """
    return u'%s:%s:%s' % (key_prefix, key, version)


class CacheManagerBase(object):
    # local_memory_cache = get_cache("local")          # 将从redis中取出的缓存在内存中保留本风，后续再查找缓存时候有限从内存中取

    # @classmethod
    # def clear_memory_cache(cls):
    #     """ 清除在内存中的缓存备份
    #     """
    #     cls.local_memory_cache.clear()

    def __init__(self,
                 key_prefix,
                 log_obj=None,
                 should_lock_update=True):
        """
        :param key_prefix:  必须，避免多个CacheManager实例使用的key命名冲突, 初始化一个CacheManager对象时候必须设定一个唯一的
        key_prefix，这个key_prefix会作为在redis存储每个缓存对象的键的一部分。
        :param timeout: 缓存失效时间，单位秒; 最小值0，当设置为0时候不缓存
        :param should_lock_update: 是否锁定更新，避免多进程同时调用缓存函数
        """
        # self._timeout = max(0, timeout)
        self._lock = should_lock_update
        self._lock_key_suffix = "LOCK"
        self._lock_key_timeout = 3.0
        self._key_prefix = key_prefix
        self._log = log_obj

    def _get_locker(self, key, version):
        """ 避免其它进程同时进行创建或者更新缓存操作，只有在初始化参数lock为true时候才启用
        """
        from django.core.cache import cache         # 延迟加载, 等django初始化好默认的cache backend之后再加载
            #  使用redis锁定修改缓存，避免多进程重复产生缓存数据
        lock_key = cache.make_key("{key}:{suffix}".format(key=cache.make_key(self._wrap_key(key), version),
                                                          suffix=self._lock_key_suffix))
        if hasattr(cache, "client") and hasattr(cache.client, "get_client"):
            client = cache.client.get_client(write=True)
            if hasattr(client, "lock"):
                return client.lock(lock_key, self._lock_key_timeout)
        # 不是用redis做缓存，或者后端的redis客户端没有实现lock方法，采用进程锁
        return Lock()

    def _wrap_key(self, key):
        """ 在不同的CacheManager中同一个key必须指向不同的redis键; 每个CacheManager实例需要设置独有的key_prefix或key_suffix
        """
        return u"{prefix}:{key}".format(prefix=self._key_prefix, key=key)

    def __getitem__(self, key_version):
        """ 兼容jct.cahce里的接口， 获取指定（key, version)里缓存的对象
        :param key_version: key or (key, version) tuple
        :return: 缓存的对象，或者None（当该对象没有被缓存，且没有实现get_value_of_key方法)
        """
        if isinstance(key_version, tuple):
            key = key_version[0]
            version = key_version[1]
        else:
            key = key_version
            version = None
        return self.get(key, version=version)

    def get(self, key, version=None, timeout=60):
        """ 获取缓存对象，建议新代码采用这个方法获取；或者直接使用 cache.get方法
        :param key:
        :param version: 该对象的版本，同一key的不同version可能会返回不同的内容
        :return: 缓存的对象，或者None（当该对象没有被缓存，且没有实现get_value_of_key方法)
        """
        from django.core.cache import cache         # 延迟加载, 等django初始化好默认的cache backend之后再加载
        if timeout <= 0:      # self._timeout <= 0 时候不使用缓存
            self._log.debug(u"NOT CACHE key [{key}]".format(key=self._wrap_key(key), version=version))
            value = None
        else:       # 先尝试从缓存中获取数据
            if version is None:
                version = self.get_version_of_key(key)
            # value = self.__class__.local_memory_cache.get(self._wrap_key(key), default=None, version=version)
            # if value is None:
            value = cache.get(self._wrap_key(key), version=version)

        if value is None:  # 缓存失效或者还没建立, 或者不缓存（timeout<=0
            if self._lock:
                with self._get_locker(key, version):
                    value = self.get_value_of_key(key, version)
            else:
                value = self.get_value_of_key(key, version)
            if value is not None and timeout > 0:  # 创建了对象且timeout > 0，存入缓存
                cache.set(self._wrap_key(key), value, timeout=timeout, version=version)

        # self.__class__.local_memory_cache.set(self._wrap_key(key), value, version=version, timeout=self._timeout)
        return value

    def set(self, key, value, version=None, timeout=60):
        """ 设置指定key,指定版本的值；
        如果没有重载get_value_of_key方法，所有的缓存必须通过set来设置之后才能被使用
        :return: None
        """
        from django.core.cache import cache         # 延迟加载, 等django初始化好默认的cache backend之后再加载
        if timeout:
            return cache.set(self._wrap_key(key), value, timeout=timeout, version=version)

    def get_version_of_key(self, key):
        """ 返回指定key的当前版本，在获取一个key的缓存对象时候，如果没有指定版本，会通过该函数来设置它的当前版本
        """
        return None

    def get_value_of_key(self, key, version=None):
        """  各子类可以实现这个方法来返回key对应的内容，或者自己set缓存值
        :param key:     缓存的键，在同一个CacheManager实例下，相同的key指向相同的缓存内容
        """
        return None


# class ConfigIniCache(CacheManagerBase):
#     def get_version_of_key(self, key):
#         """ 以该文件的最后修改时间作为它的版本号
#         """
#         if os.path.exists(key):
#             return str(os.stat(key).st_mtime)
#         return None
#
#     def get_value_of_key(self, key, version=None):
#         """ 对于ini类型文件的缓存，返回的是configobj实例
#         """
#         import configobj
#         if os.path.exists(key):
#             return configobj.ConfigObj(key, encoding='utf8', file_error=True)
#         return None


class RedisKeyCache(CacheManagerBase):
    """以redis_key为version控制缓存"""

    def __init__(self, redis_obj=settings.redis1, key='', *args, **kwargs):
        super(RedisKeyCache, self).__init__(*args, **kwargs)
        self._version_key = self._wrap_key(key) + '_version'
        self._redis = redis_obj

    def get_version_of_key(self, key):
        return self._redis.get(self._version_key) or None

    def incr_version(self):
        return str(self._redis.incr(self._version_key)).encode()


class NamedVaryCache(CacheManagerBase):
    """ 兼容jct.cache.NamedVaryCache
        通过回调函数来初始化或者创建待缓存对象
    """

    def __init__(self,
                 callback=None,
                 callback_arg=None,
                 *args,
                 **kwargs):
        """
        :param callback: 调用该函数来创建缓存对象
        :param callback_arg: 传递给callback的参数
        :param args: 其它参数透传给CacheManagerBase
        :param kwargs: 其它参数透传给CacheManagerBase
        """
        assert callable(callback), u"参数callback必须可调用!"

        super(NamedVaryCache, self).__init__(*args, **kwargs)

        self._callback = callback
        self._callback_args = callback_arg or []

    def get_value_of_key(self, key, version=None):
        return self._callback(key, *self._callback_args)


class NamedVaryCacheByRedisCheck(NamedVaryCache):
    """ 兼容jct.cache.NamedVaryCacheByRedisCheck
        通过一个redis键的值来返回被缓存对象的版本信息
    """

    def __init__(self,
                 obj_redis,
                 key_monitor,
                 callback=None,
                 callback_arg=None,
                 *args,
                 **kwargs):
        super(NamedVaryCacheByRedisCheck, self).__init__(callback=callback,
                                                         callback_arg=callback_arg,
                                                         *args,
                                                         **kwargs)

        self._redis_client = obj_redis
        self._redis_key = key_monitor

    def get_version_of_key(self, key):
        return self._redis_client.get(self._redis_key) or None


class TapeDirectoryCache(CacheManagerBase):
    u"""  兼容 jct.cache.TapeDirectoryCache
      纳米盒磁带书籍目录的缓存器对象
    . 该类是为磁带目录缓存设计，监控基准是目录下time.txt文件和title.jpg文件的修改时间没有发生变化
    . 系统中只需要创建全局管理对象，如dircc = jct.utility.TapeDirectoryCache(log_obj = log_error , timeout = 300)
    . 后使用bookCache = dircc[book_dir]就可以管理缓存数据
    """
    def get_version_of_key(self, tape_dir_as_key):

        time_txt_file = os.path.join(tape_dir_as_key, "time.txt")
        if os.path.exists(time_txt_file):
            version = str(os.stat(time_txt_file).st_mtime)
            title_jpg_file = os.path.join(tape_dir_as_key, "title.jpg")
            if os.path.exists(title_jpg_file):
                version += str(os.stat(title_jpg_file).st_mtime)
        else:
            raise KeyError

        return version
