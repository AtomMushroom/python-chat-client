from kivymd.app import MDApp
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
import socket, threading
from time import sleep

Config.set("graphics", "resizeable", "0")
#Config.set("graphics", "width", "480") WTF
#Config.set("graphics", "height", "853") WTF
Window.size = (480, 853)

host = socket.gethostbyname(socket.gethostname())
port = 0

class connect_manipulation():
    def __init__(self, ip=0, nickname=""):
        self._ip = ip
        self._nickname = nickname
    def get_ip(self):
        return self._ip
    def set_ip(self, x):
        self._ip = x
    def get_nickname(self):
        return self._nickname
    def set_nickname(self, x):
        self._nickname = x
conn_man = connect_manipulation()
def listen():
    quit = False
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((socket.gethostbyname(socket.gethostname()), 2222))
    print(f'Слушаю на {socket.gethostbyname(socket.gethostname())}:2222')
    clients = []

    while not quit:
        try:
            data, addr = s.recvfrom(1024)

            if addr not in clients:
                clients.append(addr)
            if "KILLED" in data.decode("utf-8"):
                clients.remove(addr)

            #print(addr[0] + "=" + str(addr[1]), end="")
            print(data.decode("utf-8"))

            for client in clients:
                if addr != client:
                    s.sendto(data, client)
        except:
            print("\n[ Чтука сломалась ]")
            quit = True
            break

class AuthScreen(Screen):
    def switch(self):
        conn_man.set_ip(str(self.ids.ip.text))
        conn_man.set_nickname(str(self.ids.nickname.text))
        self.manager.current = "menu"

class MainScreen(Screen):
    def auth(self):
        shutdown = False
        join = False
        server = (conn_man.get_ip(), 2222)

        def receving(name, sock):
            while not shutdown:
                try:
                    while True:
                        data, addr = sock.recvfrom(1024)
                        print(data.decode("utf-8"))
                        # time.sleep(0.2)
                except:
                    pass
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((host, port))
        s.setblocking(0)
        alias = conn_man.get_nickname()
        rT = threading.Thread(target=receving, args=("RecvThread", s))
        rT.start()
        while not shutdown:
            if not join:
                s.sendto(("Поц " + alias +" Таки законектился").encode("utf-8"), server)
                join = True
            else:
                try:
                    message = str(self.ids.message.text)

                    if message != "":
                        s.sendto(("Поц " + alias + ": " + message).encode("utf-8"), server)

                    sleep(0.2)
                except:
                    s.sendto(("Поц " + alias + " Таки пошел помолиться Господу").encode("utf-8"), server)
                    s.sendto("KILLED".encode("utf-8"), server)
                    shutdown = True

        rT.join()
        s.close()


class ClientApp(MDApp):
    def build(self):
        self.title = 'Python Chat'
        self.sm = ScreenManager()

        self.sm.add_widget(AuthScreen(name='auth'))
        self.sm.add_widget(MainScreen(name='menu'))

        return self.sm

if __name__ == "__main__":
    ClientApp().run()