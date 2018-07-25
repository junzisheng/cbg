import xadmin
import uuid
from .models import CbgConvertCode


class CbgConvertCodeAdmin(object):
    list_display = ['id', 'obj_type', 'obj_id', 'obj_quantity', 'convert_code', 'quantity_limit', 'total_limit',
                    'receive_total', 'start_time', 'end_time', 'create_time']
    readonly_fields = ['convert_code', 'receive_total']

    def save_models(self):
        obj = self.new_obj
        if obj:
            obj.convert_code = str(uuid.uuid1())
            obj.save()

xadmin.site.register(CbgConvertCode, CbgConvertCodeAdmin)
