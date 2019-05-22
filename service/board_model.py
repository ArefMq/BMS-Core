# House Config
NUM_OF_KEYPADS = 2
NUM_OF_HVACS = 3

# Data Config
NUM_OF_MODE_DATA_BYET = 1
NUM_OF_KEY_DATA_BYET = 14
NUM_OF_HVAC_DATA_BYET = 14


class BoardModel:
    def __init__(self):
        self.keys = [0 for _ in range(NUM_OF_KEYPADS)] # these are either 0 or 1
        self.hvacs = [0 for _ in range(NUM_OF_HVACS)] # these are degree of celcius
        self.previous_state = None
    
    def load_from_byte_array(data):
        for in range(NUM_OF_KEY_DATA_BYET):
            self.keys
    
    def to_byte_array():
        pass


