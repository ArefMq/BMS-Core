# Data Config
NUM_OF_MODE_DATA_BYET = 1
NUM_OF_KEY_DATA_BYET = 7
NUM_OF_HVAC_DATA_BYET = 6


class BoardModel:
    def __init__(self):
        self.mode = 1
        self.keys = [0 for _ in range(NUM_OF_KEY_DATA_BYET * 8)] # these are either 0 or 1
        self.hvacs = [0 for _ in range(NUM_OF_HVAC_DATA_BYET)] # these are degree of celcius
        self.previous_key_state = None
        self.previous_hvac_state = None
    
    def load_from_byte_array(self, data):
        self.previous_key_state = [i for i in self.keys]
        self.previous_hvac_state = [i for i in self.hvacs]

        self.keys = []
        for i in range(NUM_OF_KEY_DATA_BYET):
            self.keys.extend([i for i in '{0:08b}'.format(data[i])])
        for i in range(NUM_OF_HVAC_DATA_BYET):
            self.hvacs[i] = data[i+NUM_OF_KEY_DATA_BYET]
    
    def to_byte_array(self):
        b = bytearray()
        b.append(self.mode)

        data_string = ''.join([str(int(bool(k))) for k in self.keys])
        for i in range(NUM_OF_KEY_DATA_BYET):
            try:
                b.append(int(data_string[i*8:i*8+8], 2))
            except ValueError:
                b.append(0)
        b.extend([h for h in self.hvacs])
        return b

    def update_data(self, keys=None, hvacs=None):
        if keys:
            self.previous_key_state = [i for i in self.keys]
            self.keys = keys

        if hvacs:
            self.previous_hvac_state = [i for i in self.hvacs]
            self.hvacs = hvacs

    def get_changed_keys(self):
        if self.previous_key_state:
            return [(i, self.keys[i]) for i in range(len(self.keys)) if self.keys[i] != self.previous_key_state[i]]


