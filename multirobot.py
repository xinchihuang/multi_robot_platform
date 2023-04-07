#!/usr/bin/env python3
# coding=utf-8

import sys
import time
import threading
import socket

# IP_LIST = ['172.20.10.6','172.20.10.7','172.20.10.8']
IP_LIST = ['172.20.10.6']
EP_DICT = {}

class EP:
        def __init__(self, ip):
                self._IP = ip
                self.__socket_ctrl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.__socket_isRelease = True
                self.__socket_isConnect = False
                self.__thread_ctrl_recv = threading.Thread(target=self.__ctrl_recv)
                self.__seq = 0
                self.__ack_list = []
                self.__ack_buf = 'ok'

        def __ctrl_recv(self):
                while self.__socket_isConnect and not self.__socket_isRelease:
                        try:
                                buf = self.__socket_ctrl.recv(1024).decode('utf-8')
                                print('%s:%s' % (self._IP, buf))
                                buf_list = buf.split(' ')
                                if 'seq' in buf_list:
                                        self.__ack_list.append(int(float(buf_list[buf_list.index('seq') + 1])))
                                self.__ack_buf = buf
                        except socket.error as msg:
                                print('ctrl %s: %s' % (self._IP, msg))

        def start(self):
                try:
                        self.__socket_ctrl.connect((self._IP, 40923))
                        self.__socket_isConnect = True
                        self.__socket_isRelease = False
                        self.__thread_ctrl_recv.start()
                        self.command('command')
                        self.command('robot mode free')
                except socket.error as msg:
                        print('%s: %s' % (self._IP, msg))

        def exit(self):
                if self.__socket_isConnect and not self.__socket_isRelease:
                        self.command('quit')
                self.__socket_isRelease = True
                try:
                        self.__socket_ctrl.shutdown(socket.SHUT_RDWR)
                        self.__socket_ctrl.close()
                        self.__thread_ctrl_recv.join()
                except socket.error as msg:
                        print('%s: %s' % (self._IP, msg))

        def command(self, cmd):
                self.__seq += 1
                cmd = cmd + ' seq %d;' % self.__seq
                print('%s:%s' % (self._IP, cmd))
                self.__socket_ctrl.send(cmd.encode('utf-8'))
                timeout = 2
                while self.__seq not in self.__ack_list and timeout > 0:
                        time.sleep(0.01)
                        timeout -= 0.01
                if self.__seq in self.__ack_list:
                        self.__ack_list.remove(self.__seq)
                return self.__ack_buf

if __name__ == "__main__":
        #实例化机器人
        for ip in IP_LIST:
                print('%s connecting...' % ip)
                EP_DICT[ip] = EP(ip)
                EP_DICT[ip].start()

        for ip in IP_LIST:
                EP_DICT[ip].command("chassis speed x 0.1 y 0.1 z 1")
        time.sleep(3)

        while True:
                for ip in IP_LIST:
                        EP_DICT[ip].command('chassis speed x 0.1 y 0.1 z 1')
                time.sleep(3)
                for ip in IP_LIST:
                        EP_DICT[ip].command('chassis speed x 0.1 y 0.1 z 1')
                time.sleep(3)
        for ip in IP_LIST:
                EP_DICT[ip].exit()