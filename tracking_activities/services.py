import time

def import_data(obj_id):
    print('start import', obj_id)
    from .models import RegisterUploaded
    obj = RegisterUploaded.objects.get(id=obj_id)
    # import ipdb; ipdb.set_trace()
    obj.status = 'processing'
    obj.save()
    time.sleep(35)
    obj.status = 'success'
    obj.save()
    print('end import')