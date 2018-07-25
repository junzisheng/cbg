from cbg_backup import settings
from unit.cache import RedisKeyCache
import xadmin
from .models import CbgBanner, CbgService, CbgServiceActivity


class CbgBannerAdmin(object):
    list_display = ['tag', 'href', 'render_img', 'create_time', 'start_time', 'deadline_time', 'weight', 'is_delete']
    search_fields = ['tag']
    list_filter = ['start_time', 'deadline_time', 'weight', 'is_delete']

    def save_models(self):
        obj = self.new_obj
        if obj:
            obj.save()
            redis_cache = RedisKeyCache(key_prefix='banner')
            redis_cache.incr_version()


class CbgServiceAdmin(object):
    list_display = ['name', 'subtitle', 'show_img', 'count_buy', 'count_price', 'price', 'points', 'activity']
    readonly_fields = ['count_buy', 'count_price']

    def save_models(self):
        obj = self.new_obj
        obj.save()
        redis_cache = RedisKeyCache(key_prefix='service')
        redis_cache.incr_version()


class CbgServiceActivityAdmin(object):
    list_display = ['title', 'style','subtitle', 'fill', 'discount', 'reduction', 'points', 'banner',
                    'start_time', 'end_time']



xadmin.site.register(CbgBanner, CbgBannerAdmin)
xadmin.site.register(CbgService, CbgServiceAdmin)
xadmin.site.register(CbgServiceActivity, CbgServiceActivityAdmin)
