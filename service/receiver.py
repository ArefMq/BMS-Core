#!/usr/bin/env python
import socket
import sqlite3

from board_model import BoardModel


DB_PATH = '/home/pi/BMS-Core/bms/db.sqlite3'
DEBUG = False


class Receiver:
    def __init__(self, host='', port=2222):
        self.host = host    # Symbolic name meaning all available interfaces
        self.port = port    # Arbitrary non-privileged port
        self.network_data = None

        # Datagram (udp) socket
        try :
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print('Socket created')
        except socket.error as exp :
            print('Failed to create socket. Because: %s', str(exp))
            raise

        # Bind socket to local host and port
        try:
            self.socket.bind((self.host, self.port))
            print('Socket bind complete.')
        except socket.error as exp:
            print('Failed to bind the socket. Because: %s', str(exp))
            raise
            
        try:
            self.db_connection = sqlite3.connect(DB_PATH)
            self.db_connection_cursor = self.db_connection.cursor()
            print('Data base connected.')
        except Exception as exp:
            print('Failed to connect to the database. Because: %s', str(exp))
            raise
        
        self.board_model = BoardModel(self.get_all_device_list())

    def get_all_device_list(self):
        res = self.db_connection.execute("SELECT id,channel,pos,isAnalog FROM backend_accessories")
        res = [{'id': x[0], 'channel': x[1], 'pos': x[2], 'isAnalog': x[3]} for x in res]
        return res

    def get_device_status(self):
        res = self.db_connection.execute("SELECT id,status,analogValue FROM backend_accessories")
        res = [{'id': x[0], 'status': x[1], 'analogValue': x[2]} for x in res]
        # FIXME: make digital status only boolean
        return res

    def destruct(self):
        self.socket.close()
        self.db_connection.close()

    def update_data_from_network(self):
        data, addr = self.socket.recvfrom(1024)
        if not data: 
            raise Exception('invalid data recieved.')
        self.network_data = bytearray(data.strip())

    def apply_changes(self):
        changed_keys = self.board_model.get_changed_keys()
        if changed_keys:
            for _, k in changed_keys.items():
                if k.type == 'key':
                    self.set_key_on_db(k.id, k.status)
                elif k.type == 'hvac':
                    self.set_hvac_on_db(k.id, k.status)
            self.db_connection.commit()

    def process_key_channel(self, channel_id, channel_payload):
        for pos in range(8):
            val = channel_payload & (1 << pos)
            try:
                self.board_model.set_key_by_channel_pos((channel_id, pos), val)
            except KeyError:
                pass

    def process_net_data(self):
        # process keys
        for i in range(1, 8):
            self.process_key_channel(i, self.network_data[i])
        
        # process hvacs
        for i in range(8, 14):
            try:
                self.board_model.set_hvac_by_channel(i, self.network_data[i])
            except KeyError:
                pass

    def cycle(self):
        status_list = self.get_device_status()
        self.board_model.load_status(status_list)
        self.board_model.reset_changes()

        self.update_data_from_network()
        self.process_net_data()
        self.apply_changes()
    
    def set_key_on_db(self, id, value):
        print('toggeling %d to %d' % (id, value))
        self.db_connection.execute('UPDATE backend_accessories SET status=%d WHERE id=%d' % (value, id))

    def set_hvac_on_db(self, id, value):
        self.db_connection.execute('UPDATE backend_accessories SET status=%d WHERE id=%d' % (value, id))


if __name__ == "__main__":
    receiver = Receiver()

    if DEBUG:
        excepted = KeyboardInterrupt
    else:
        excepted = Exception
        
    try:
        while 1:
            receiver.cycle()
    except excepted:
        pass
    finally:
        receiver.destruct()
