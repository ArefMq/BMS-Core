from bms.backend.serializers import AccessoriesSerializer
from bms.backend.models import Accessories


def set_command_view_data(acc_id, status, is_analog=False, analog_value=0):
    accessory = Accessories.objects.get(id=acc_id)
    if is_analog:
        accessory.analogValue = analog_value
    else:
        accessory.status = status
    accessory.save()


def get_accessory_view_data(acc_id):
    accessory = Accessories.objects.get(id=acc_id)
    serializer = AccessoriesSerializer(accessory)
    return accessory.status

