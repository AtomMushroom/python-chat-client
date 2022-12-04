from kivymd.app import MDApp
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
import socket, threading

from kivymd.uix.list import OneLineListItem

Config.set("graphics", "resizeable", "0")
#Config.set("graphics", "width", "480") WTF
#Config.set("graphics", "height", "853") WTF
Window.size = (480, 853)

host = socket.gethostbyname(socket.gethostname()) #Хост клиента
port = 0 #Порт клиента

class connect_manipulation(): #Геттеры и сеттеры для айпи сервака, никнейма и сообщения
    def __init__(self, ip="", nickname="", msg=""):
        self._ip = ip
        self._nickname = nickname
        self._msg = msg
    def get_ip(self):
        return self._ip
    def set_ip(self, x):
        self._ip = x
    def get_nickname(self):
        return self._nickname
    def set_nickname(self, x):
        self._nickname = x
    def set_msg(self, x):
        self._msg = x
    def get_msg(self):
        return self._msg
conn_man = connect_manipulation()

class AuthScreen(Screen): #Окно авторизации
    def switch(self):
        conn_man.set_ip(self.ids.IP.text)
        conn_man.set_nickname(str(self.ids.nickname.text))
        self.manager.current = "menu"
class MainScreen(Screen): #Основное окно
    def __init__(self, join=False, shutdown=False, **kw):
        super().__init__(**kw)
        self._join = join
        self._shutdown = join

    def receving(self, name, sock):  # Принимает пакеты от сервера и принтует в консоль
        try:
            data, addr = sock.recvfrom(1024)
            print(data.decode("utf-8"))
            self.ids.lst.add_widget(OneLineListItem(text="Single-line item"))
        except Exception as e:
            print(e)
    shutdown = False
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))
    s.setblocking(False)
    def do_the_trick(self, s): #Отправляет сообщение
        message = self.ids.message.text
        s.sendto(f"Поц {conn_man.get_nickname()}: {message}".encode("utf-8"), (conn_man.get_ip(), 2222))
        self.receving("kurwa", s)
        if message == "exit":
            s.sendto(f"Поц {str(conn_man.get_nickname())} Таки пошел помолиться Господу".encode("utf-8"), (conn_man.get_ip(), 2222))
            s.sendto("KILLED".encode("utf-8"), (conn_man.get_ip(), 2222))
            self._join = False
            self._shutdown = True
            self.manager.current = "menu"
class ClientApp(MDApp):
    def build(self):
        self.title = 'Python Chat'
        self.sm = ScreenManager()

        self.sm.add_widget(AuthScreen(name='auth'))
        self.sm.add_widget(MainScreen(name='menu'))

        return self.sm

if __name__ == "__main__":
    ClientApp().run()