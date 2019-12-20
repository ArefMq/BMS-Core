# Data Config
NUM_OF_MODE_DATA_BYTE = 1
NUM_OF_KEY_DATA_BYTES = 7
NUM_OF_HVAC_DATA_BYTES = 6


class Key:
    def __init__(self, id, channel=0, pos=0, status=0):
        self.id = id
        self.channel = channel
        self.pos = pos
        self.status = status
        self.has_changed = False
        self.type = 'key'
        self.toggle_command = None

    def set_cmd(self, cmd):
        if cmd != self.status:
            self.status = cmd
            self.has_changed = True

    def toggle(self, value):
        if self.toggle_command is None:
            self.toggle_command = value

        if self.toggle_command == value:
            return

        self.status = not self.status
        self.has_changed = True
        self.toggle_command = value


class HVAC:
    def __init__(self, id, channel=0, status=0, value=0):
        # FIXME : the naming is crap, change it
        self.id = id
        self.channel = channel
        self.status = status
        self.value = value
        self.has_changed = False
        self.isActive = True
        self.type = 'hvac'
    
    def set_cmd(self, cmd, is_active):
        if cmd == self.value and is_active == self.isActive:
            return
        self.value = cmd
        self.isActive = is_active
        self.has_changed = True

    def set_status(self, status):
        if self.status == status:
            return
        self.status = status
        self.has_changed = True


class HVACMode:
    def __init__(self, id, status=1, value=1):
        # FIXME : the naming is crap, change it
        self.id = id
        self.status = status
        self.has_changed = False
        self.type = 'hvac_mode'

    def set_status(self, status):
        if self.status == status:
            return
        self.status = status
        self.has_changed = True


class BoardModel:
    def __init__(self, device_list):
        self.mode = None
        self.keys = {}
        self.hvacs = {}

        for dev in device_list:
            id = dev['id']
            if dev['channel'] == 0:
                if self.mode is None:
                    self.mode = HVACMode(id)
                else:
                    raise Exception('Multiple HVAC mode found...')
            elif dev['isAnalog']:
                self.hvacs[id] = HVAC(id, dev['channel'])
            else:
                self.keys[id] = Key(id, dev['channel'], dev['pos'])
        
        self.key_channel_pos_map = {}
        for _, k in self.keys.items():
            self.key_channel_pos_map[(k.channel, k.pos)] = k

        self.hvac_channel_map = {}
        for _, hv in self.hvacs.items():
            self.hvac_channel_map[hv.channel] = hv
    
    def load_status(self, status_list):
        for status in status_list:
            id = status['id']
            if id in self.keys:
                self.keys[id].set_cmd(status['status'])
            elif id in self.hvacs:
                self.hvacs[id].set_cmd(status['analogValue'], status['isActive'])
            elif id == self.mode.id:
                self.mode.set_status(status['status'])

    @staticmethod
    def set_bit(b, ith, value):
        if value:
            return b | (1 << ith)
        else:
            return b & ~(1 << ith)

    def to_byte_array(self):
        b = bytearray()
        mode = self.mode.status+1
        i = 0
        for _, h in self.hvacs.items():
            mode |= h.isActive << (i+2)
            i += 1

        b.append(mode)

        for _ in range(NUM_OF_KEY_DATA_BYTES + NUM_OF_HVAC_DATA_BYTES):
            b.append(0)

        for id in self.keys:
            channel = self.keys[id].channel
            pos = self.keys[id].pos
            value = self.keys[id].status
            b[channel] = self.set_bit(b[channel], pos, value)

        for id in self.hvacs:
            channel = self.hvacs[id].channel
            b[channel] = self.hvacs[id].value

        return b

    def get_changed_keys(self):
        changes = {}
        if self.mode.has_changed:
            changes[self.mode.id] = self.mode
            self.mode.has_changed = False
        for i in self.keys:
            if self.keys[i].has_changed:
                changes[i] = self.keys[i]
                self.keys[i].has_changed = False
        for i in self.hvacs:
            if self.hvacs[i].has_changed:
                changes[i] = self.hvacs[i]
                self.hvacs[i].has_changed = False
        return changes

    def set_key_by_channel_pos(self, channel_pos, value):
        self.key_channel_pos_map[channel_pos].toggle(value)

    def set_hvac_by_channel(self, channel, value):
        self.hvac_channel_map[channel].set_status(value)

    def set_hvac_mode(self, value):
        self.mode.set_status(value)

    def reset_changes(self):
        for _, k in self.keys.items():
            k.has_changed = False
        for _, hv in self.hvacs.items():
            hv.has_changed = False

        self.mode.has_changed = False
