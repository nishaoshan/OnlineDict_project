"""
author: Nishaoshan
email:790016602@qq.com
time:2020-6-22
env:python3.6
socket,V负责界面显示
"""
from socket import *

class Client:
    def __init__(self, host="127.0.0.1", port=9999):
        self.host = host
        self.port = port
        self.sock = socket()
        self.name = ""

    def r(self):
        while True:
            try:
                name = input("请输入用户名：")
                if not name:
                    print("输入有误,请重新输入--------------")
                    continue
                while True:
                    passwd1 = input("请输入密码：")
                    if not passwd1:
                        print("输入有误,请重新输入--------------")
                        continue
                    passwd2 = input("请再次确认密码：")
                    if passwd1 != passwd2:
                        print("两次密码输入不一致,请重新出入-----------")
                        continue
                    break
                self.sock.send(f"R {name} {passwd1}".encode())
                response = self.sock.recv(1024).decode()
                if response == "ok":
                    print("注册成功")
                    self.name = name
                    return "ok"
                elif response == "fail":
                    print("注册失败，用户名有人用了，请更换")
                    continue
            except KeyboardInterrupt:
                return "back"

    def l(self):
        while True:
            name = input("请输入用户名：")
            passwd = input("请输入密码：")
            if not name:
                print("用户名输入有误请重新输入---------")
                continue
            if not passwd:
                print("用户名输入有误请重新输入---------")
            self.sock.send(f"L {name} {passwd}".encode())
            response = self.sock.recv(1024).decode()
            if response == "ok":
                print("登录成功")
                self.name = name
                return
            else:
                print("登录失败", response)

    def h(self):
        self.sock.send(f"H {self.name}".encode())
        msg=self.sock.recv(1024).decode()
        if msg=="ok":
            while True:
                data = self.sock.recv(1024).decode()
                if data == "##":
                    break
                print(data)
        else:
            print("没有记录，快去查询吧")

    def start(self):
        try:
            self.sock.connect((self.host, self.port))
        except:
            print("请检查网络后重试！")
            return
        while True:
            self.func1()
            cmd = input("请输入指令：")
            if cmd == "登录":
                self.l()
                while True:
                    self.func2()
                    break
            elif cmd == "注册":
                msg = self.r()
                if msg == "ok":
                    while True:
                        choose = input("是否直接登录？(y/n)")
                        if choose == "y":
                            while True:
                                self.func2()
                                break
                            break
                        elif choose == "n":
                            break
                        else:
                            print("输入有误，请重新输入-------")
                elif msg == "back":
                    continue
            elif cmd == "退出":
                self.sock.send(b"E")
                return
            else:
                print("输入有误,请重新输入")

    def func1(self):
        print("=========== 界面1 ==============")
        print("***登录       注册        退出***")
        print("===============================")

    def func2(self):
        while True:
            print("=========== 界面2 =============")
            print("***查单词    历史记录     注销***")
            print("===============================")
            cmd = input("请输入指令：")
            if cmd == "查单词":
                self.q()
            elif cmd == "历史记录":
                self.h()
            elif cmd == "注销":
                return

    def q(self):
        while True:
            word = input("请输入单词：")
            if word == "##":
                break
            self.sock.send(f"Q {self.name} {word}".encode())
            data = self.sock.recv(1024).decode()
            print(data)


if __name__ == '__main__':
    Client().start()
