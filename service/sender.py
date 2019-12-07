#!/usr/bin/env python
import socket
import sqlite3
from time import sleep
from board_model import BoardModel
from socket_errors import error_list

DB_PATH = '/home/pi/BMS-Core/bms/db.sqlite3'
DEBUG = False
SENDING_DELAY = 0.1 if not DEBUG else 1.2


class Sender:
    def __init__(self, host='192.168.1.90', port=2223):
        self.HOST = host # Symbolic name meaning all available interfaces
        self.PORT = port # Arbitrary non-privileged port

        # Datagram (udp) socket
        try :
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print('Socket created')
        except socket.error as exp:
            print('Failed to create socket. Because: %s', str(exp))
            raise

        # Bind socket to local host and port
        try:
            self.socket.bind(('', self.PORT))
            print('Socket bind complete')
        except socket.error as exp:
            print('Failed to bind the socket. Because: %s', str(exp))
            raise

        try:
            self.db_connection = sqlite3.connect(DB_PATH)
            self.db_cursor_connection = self.db_connection.cursor()
            print('Data base connected.')
        except Exception as exp:
            print('Failed to connect to the database. Because: %s', str(exp))
            raise
        
        self.board_model = BoardModel(self.get_all_device_list())

    def destruct(self):
        self.socket.close()
        self.db_connection.close()
    
    def get_all_device_list(self):
        res = self.db_connection.execute("SELECT id,channel,pos,isAnalog FROM backend_accessories")
        res = [{'id': x[0], 'channel': x[1], 'pos': x[2], 'isAnalog': x[3]} for x in res]
        return res
    
    def get_device_status(self):
        res = self.db_connection.execute("SELECT id,status,analogValue FROM backend_accessories")
        res = [{'id': x[0], 'status': x[1], 'analogValue': x[2]} for x in res]
        return res
        
    def print_changes(self):
        changes = self.board_model.get_changed_keys()
        if changes:
            for _, d in changes.items():
                if d.type == 'hvac':
                    print('%d) change hvac to %d (status=%d)' % (d.id, d.value, d.status))
                elif d.type == 'key':
                    print('%d) change key to %d' % (d.id, d.status))

    def send_payload(self):
        if DEBUG:
            print('sending: ', [r for r in self.board_model.to_byte_array()])
        res = self.socket.sendto(self.board_model.to_byte_array() , (self.HOST, self.PORT))
        if res and res != 14 and DEBUG:
            res_text = ('  (%s)' % error_list[res]) if res in error_list else ''
            print('send-to function fail: %d%s' % (res, res_text))

    def send(self):
        status_list = self.get_device_status()
        self.board_model.load_status(status_list)
        self.print_changes()
        self.send_payload()


if __name__ == "__main__":
    sender = Sender()
    
    if DEBUG:
        excepted = KeyboardInterrupt
    else:
        excepted = Exception
        
    try:
        while 1:
            sender.send()
            sleep(SENDING_DELAY)
    except excepted:
        pass
    finally:
        sender.destruct()
