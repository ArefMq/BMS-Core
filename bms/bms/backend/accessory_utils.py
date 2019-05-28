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


def get_hvac_detailed_status(acc_id):
    TEMP_COOLING_STATE_MODE = 2
    accessory = Accessories.objects.get(id=acc_id)

    result = {
        "targetHeatingCoolingState": TEMP_COOLING_STATE_MODE,
        "targetTemperature": accessory.analogValue,
        "currentHeatingCoolingState": TEMP_COOLING_STATE_MODE,
        "currentTemperature": accessory.status
    }
    return result


def set_hvac_detailed_status(acc_id, value):
    accessory = Accessories.objects.get(id=acc_id)
    accessory.analogValue = value
    accessory.save({'success': True, 'message': '', 'data': ''})


def set_hvac_cooling_state(acc_id, value):
    pass
