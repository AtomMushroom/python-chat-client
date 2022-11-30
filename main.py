from kivy.app import App
from kivy.uix.button import Button
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivymd.app import MDApp

Config.set("graphics", "resizeable", "0")
Config.set("graphics", "width", "480")
Config.set("graphics", "height", "853")

class AuthScreen(GridLayout):
    pass

class MainScreen(GridLayout):
    pass

class ClientApp(MDApp):
    def build(self):
        return AuthScreen()

if __name__ == "__main__":
    ClientApp().run()