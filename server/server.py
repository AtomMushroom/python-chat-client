import threading

from kivymd.app import MDApp
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
import socket

Config.set("graphics", "resizeable", "0")
#Config.set("graphics", "width", "480") WTF
#Config.set("graphics", "height", "853") WTF
Window.size = (480, 853)


def listen():  # МЕТОД ДЛЯ ЕГОРА. МОЖНО НЕ СМОТРЕТЬ, НИГДЕ НЕ ИСПОЛЬЗУЕТСЯ.
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

            # print(addr[0] + "=" + str(addr[1]), end="")
            print(data.decode("utf-8"))

            for client in clients:
                if addr != client:
                    s.sendto(data, client)
        except:
            print("\n[ Чтука сломалась ]")
            quit = True
            break
mainT = threading.Thread(target=listen, daemon=True)
mainT.start()
class Main(Screen):
    def start(self):
        self.ids.lb.text = f"IP: {socket.gethostbyname(socket.gethostname())}"
class ServerApp(MDApp):
    def build(self):
        self.title = 'Python Server'
        self.sm = ScreenManager()

        self.sm.add_widget(Main(name='main'))

        return self.sm

if __name__ == "__main__":
    ServerApp().run()