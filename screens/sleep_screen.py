from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Canvas, Line, Rectangle, Ellipse, Color, Triangle
from kivy.core.window import Window


class SleepScreen(Screen):
    lb = Label(text='Mirage - Sleep')

    def __init__(self, **kwargs):  # commented out the clock
        super(Screen, self).__init__(**kwargs)
        self.setup()

    def setup(self):
        with self.canvas.before:
            self.add_widget(self.lb)

    def update(self):
        pass
