from kivy.app import App
from kivy.uix.button import Button
from kivy.config import Config
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout

Config.set("graphics", "resizeable", "0")
Config.set("graphics", "width", "480")
Config.set("graphics", "height", "853")

class AuthScreen(GridLayout):
    pass

class ClientApp(App):
    def build(self):
        return AuthScreen()

if __name__ == "__main__":
    ClientApp().run()