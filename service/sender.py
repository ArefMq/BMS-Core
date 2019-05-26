#!/usr/bin/env python
import socket
import sys
import array
import sqlite3
from time import sleep
from board_model import BoardModel
from socket_errors import error_list

DB_PATH = '/home/pi/BMS-Core/bms/db.sqlite3'
DEBUG = False
SENDING_DELAY = 1.1


class Sender:
    def __init__(self, host='192.168.1.1', port=2223):
        self.HOST = host # Symbolic name meaning all available interfaces
        self.PORT = port # Arbitrary non-privileged port
        self.board_model = BoardModel()

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

    def destruct(self):
        self.socket.close()
        self.db_connection.close()
    
    def get_keys_from_db(self):
        res = self.db_connection.execute("SELECT id,status FROM backend_accessories WHERE isAnalog=0")
        byte_data = [x[1] for x in res]
        return byte_data
        
    def get_hvacs_from_db(self):
        res = self.db_connection.execute("SELECT id,analogValue FROM backend_accessories WHERE isAnalog=1")
        byte_data = [x[3] for x in res]
        return byte_data
        
    def send(self):
        byte_data_keys = self.get_keys_from_db()
        byte_data_hvacs = self.get_hvacs_from_db()
        self.board_model.update_data(keys=byte_data, hvacs=byte_data_hvacs)

        changes = self.board_model.get_changed_keys()
        if changes:
            for key, state in changes:
                print('change state of %d to %d' % (key, state))

        if DEBUG:
            print('sending: ', [r for r in self.board_model.to_byte_array()])
        res = self.socket.sendto(self.board_model.to_byte_array() , (self.HOST, self.PORT))
        if res and res != 14 and DEBUG:
            res_text = ('  (%s)' % error_list[res]) if res in error_list else ''
            print('send-to function fail: %d%s' % (res, res_text))


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
