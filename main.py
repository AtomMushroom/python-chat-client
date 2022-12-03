from kivymd.app import MDApp
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
import socket, threading

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
'''
def listen(): # МЕТОД ДЛЯ ЕГОРА. МОЖНО НЕ СМОТРЕТЬ, НИГДЕ НЕ ИСПОЛЬЗУЕТСЯ.
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
'''
def receving(name, sock, shutdown): #Принимает пакеты от сервера и принтует в консоль (Пока не используется)
    while not shutdown:
        try:
            while True:
                data, addr = sock.recvfrom(1024)
                print(data.decode("utf-8"))
        except:
            pass
class AuthScreen(Screen): #Окно аворизации
    def switch(self):
        conn_man.set_ip(self.ids.IP.text)
        conn_man.set_nickname(str(self.ids.nickname.text))
        self.manager.current = "menu"

class MainScreen(Screen): #Основное окно
    def __init__(self, join=False, shutdown=False, **kw):
        super().__init__(**kw)
        self._join = join
        self._shutdown = join
    #join = False
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))
    s.setblocking(0)

    def do_the_trick(self, s): #Отправляет сообщение
        message = self.ids.message.text
        s.sendto(f"Поц {conn_man.get_nickname()}: {message}".encode("utf-8"), (conn_man.get_ip(), 2222))
        if message == "exit":
            s.sendto(bytearray("Поц + {str(conn_man.get_nickname())} Таки пошел помолиться Господу").encode("utf-8"), (conn_man.get_ip(), 2222))
            s.sendto("KILLED".encode("utf-8"), (conn_man.get_ip(), 2222))
            self._join = False
            self._shutdown = True
            self.manager.current = "menu"

    def sendm(self, s): #Костыль без которого не работает. Завтра уберу
        conn_man.set_msg(self.ids.message.text)
        self.do_the_trick(s)

    #rT = threading.Thread(target=receving, args=("RecvThread", s, shutdown))

    '''while not shutdown:
            if not join:
                s.sendto(("Поц " + alias +" Таки законектился").encode("utf-8"), server)
                join = True
            else:
                try:
                    print(1)
                    message = str(self.ids.message.text)

                    if message != "":
                        print(2)
                        s.sendto(("Поц " + alias + ": " + message).encode("utf-8"), server)

                    sleep(0.2)
                except:
                    s.sendto(("Поц " + alias + " Таки пошел помолиться Господу").encode("utf-8"), server)
                    s.sendto("KILLED".encode("utf-8"), server)
                    shutdown = True'''
    #rT.start()
    #rT.join()

class ClientApp(MDApp):
    def build(self):
        self.title = 'Python Chat'
        self.sm = ScreenManager()

        self.sm.add_widget(AuthScreen(name='auth'))
        self.sm.add_widget(MainScreen(name='menu'))

        return self.sm

if __name__ == "__main__":
    ClientApp().run()