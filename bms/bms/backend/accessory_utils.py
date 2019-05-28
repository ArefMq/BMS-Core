from bms.backend.serializers import AccessoriesSerializer
from bms.backend.models import Accessories


def set_command_view_data(acc_id, status, is_analog=False, analog_value=0):
    accessory = Accessories.objects.get(id=acc_id)
    if is_analog:
        accessory.analogValue = analog_value
    else:
        accessory.status = int(str(status).lower() == 'true' or str(status) == '1')
    accessory.save()


def get_accessory_view_data(acc_id, is_command):
    accessory = Accessories.objects.get(id=acc_id)
    serializer = AccessoriesSerializer(accessory)
    if is_command:
        if not accessory.isAnalog:
            raise Exception('accessory id "%d" is not analog' % acc_id)
        return accessory.analogValue
    if accessory.isAnalog:
        return accessory.status
    return bool(accessory.status)
