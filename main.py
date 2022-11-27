from kivy.app import App
from kivy.uix.button import Button
from kivy.config import Config

Config.set("graphics", "resizeable", "0")
Config.set("graphics", "width", "1080")
Config.set("graphics", "height", "600")

class ClientApp(App):
    pass

if __name__ == "__main__":
    ClientApp().run()