"""
author: Nishaoshan
email:790016602@qq.com
time:2020-6-22
env:python3.6
socket,Process,signal,sys,time,C负责逻辑处理
"""
from socket import *
from multiprocessing import Process
import signal, sys, time

from month02.day19.dict_db import Database


class Server:
    def __init__(self, host="0.0.0.0", port=9999):
        self.host = host
        self.port = port
        self.sock = socket()
        self.sock.bind((self.host, self.port))
        signal.signal(signal.SIGCHLD, signal.SIG_IGN)
        self.db = Database()

    def start(self):
        self.sock.listen(5)
        while True:
            try:
                print("等待链接......")
                connfd, addr = self.sock.accept()
                print("connect from", addr)
            except KeyboardInterrupt:
                self.sock.close()
                sys.exit("服务端退出")
            p = Process(target=self.handle, args=(connfd,))
            p.daemon = True
            p.start()

    def handle(self, connfd):
        self.db.cursor()
        while True:
            request = connfd.recv(1024).decode()
            if request:
                print("接收到", request)
            if not request:
                connfd.close()
                return
            if request.split(" ", 2)[0] == "R":
                name = request.split(" ")[1]
                passwd = request.split(" ")[2]
                res = self.db.r(name, passwd)
                print(res)
                if res:
                    connfd.send(b"fail")
                else:
                    connfd.send(b"ok")
            elif request.split(" ", 2)[0] == "L":
                name = request.split(" ")[1]
                passwd = request.split(" ")[2]
                res = self.db.l(name, passwd)
                if res is True:
                    connfd.send(b"ok")
                else:
                    connfd.send(res.encode())
            elif request.split(" ", 2)[0] == "Q":
                name = request.split(" ")[1]
                word = request.split(" ")[2]
                self.db.insert_h(name, word)
                mean = self.db.query(word)
                if mean:
                    data = "%s : %s" % (word, mean)
                    print(data)
                else:
                    data = "没有找到"
                connfd.send(data.encode())
            elif request.split(" ", 2)[0] == "H":
                name = request.split(" ")[1]
                msg = self.db.hist(name)
                if not msg:
                    connfd.send(b"no info")
                else:
                    connfd.send(b"ok")
                    time.sleep(0.1)
                    for item in msg:
                        msg = "%-10s   %-10s   %-s" % item
                        connfd.send(msg.encode())
                        time.sleep(0.1)
                    connfd.send(b'##')

            elif request == "E":
                connfd.close()
                sys.exit("子进程已退出")


if __name__ == '__main__':
    Server().start()
