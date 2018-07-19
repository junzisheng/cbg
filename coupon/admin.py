import xadmin
from coupon.models import CbgCoupon
# from service.models import CbgCouponServiceRelation


class CbgCouponAdmin(object):
    list_display = ['coupon_name' ,'style', 'service_range', 'service', 'fill', 'discount', 'reduction', 'total_limit', 'assign_limit',
                    'acquire_count', 'usage_count', 'received',  'acquire_start_time', 'acquire_end_time', 'create_time']
    readonly_fields = ['acquire_count', 'usage_count']


xadmin.site.register(CbgCoupon, CbgCouponAdmin)

