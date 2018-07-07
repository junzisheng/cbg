import json
import datetime
from unit.utility import dtlib
from django.db import models


class BaseModel(models.Model):
    """ajax增量刷新的基类， 排序， 增量， 过滤， 排除， 还有限制用户可以看到的字段"""
    @classmethod
    def json_queryset(cls, order_by='-id', offset=0, limit=15, filter_={}, exclude={}, support_json=True, return_json=False):
        queryset = cls.objects.filter(**filter_).order_by(*order_by).exclude(**exclude) \
                       .values(*cls.out_params)[offset:offset+limit]
        queryset = list(queryset)
        if support_json:
            for obj in queryset:
                for k, v in obj.items():
                    if type(v) == datetime.date:
                        obj[k] = dtlib.FDD2(v)
                    elif type(v) == datetime.datetime:
                        obj[k] = dtlib.FDT2(v)
        return json.dumps(queryset) if return_json else queryset

    class Meta:
        abstract = True


