from kivymd.app import MDApp
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen

Config.set("graphics", "resizeable", "0")
#Config.set("graphics", "width", "480") WTF
#Config.set("graphics", "height", "853") WTF
Window.size = (480, 853)

class AuthScreen(Screen):
    pass

class MainScreen(Screen):
    pass

class ClientApp(MDApp):
    def build(self):
        self.title = 'Python Chat'
        self.sm = ScreenManager()

        self.sm.add_widget(AuthScreen(name='auth'))
        self.sm.add_widget(MainScreen(name='menu'))

        return self.sm

if __name__ == "__main__":
    ClientApp().run()