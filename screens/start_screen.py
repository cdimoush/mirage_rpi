from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Canvas, Line, Rectangle, Ellipse, Color, Triangle
from kivy.core.window import Window

from functions.function import grid_function
import math
from random import randint


class StartScreen(Screen):
    bg_count = math.pi

    lb = Label(text='text')
    lb_ = Label(text=' ')
    lb0 = Label(text='0')
    lb1 = Label(text='1')
    lbt = Label(text='Mirage', font_size='120sp')

    lb_list = [lb_, lb_, lb_, lb0, lb1]

    def __init__(self, **kwargs):  # commented out the clock
        super(Screen, self).__init__(**kwargs)
        self.setup()

    def setup(self):

        with self.canvas.before:
            Rectangle(pos=(0, 0), source='images/BG_1.png', size=Window.size)

    def draw(self):
        cols = 10
        rows = 10
        x, y, col_sp, row_sp, x_list, y_list = grid_function(cols, rows)
        self.canvas.clear()
        self.row_labels = []
        with self.canvas:
            Rectangle(pos=(Window.size[0]/2 - self.lbt.texture_size[0]/2, Window.size[1]/2 - self.lbt.texture_size[1]/2),
                      texture=self.lbt.texture, size=list(self.lbt.texture_size))

            for i in range(1, cols):
                for j in range(1, rows):
                    Ellipse(pos=(x_list[i] + math.sin(self.bg_count + i*math.pi/4)*col_sp/8, y_list[j] + math.sin(self.bg_count + i*math.pi/4)*row_sp/8), size=(2, 2))
        self.bg_count += math.pi/32

    def update(self, new_input, input_list):

        self.draw()
        if new_input:
            if input_list[2] == 1:
                return [1, 'menu']
        return [0, 'start']
