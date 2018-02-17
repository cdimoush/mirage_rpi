from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Canvas, Line, Rectangle, Ellipse, Color, Triangle
from kivy.core.window import Window
import math

from functions.function import grid_function


class MenuScreen(Screen):
    menu_pos = 0
    old_menu_pos = 0
    total_icons = 5
    bg_count = math.pi
    lb = Label(text='text')

    def __init__(self, **kwargs):  # commented out the clock
        super(Screen, self).__init__(**kwargs)
        self.setup()

    def setup(self):
        x, y, col_sp, row_sp, x_list, y_list = grid_function(1, 1)
        with self.canvas.before:
            Rectangle(pos=(0, 0), source='images/BG_1.png', size=(x, y))

    def bg_draw(self):
        cols = 10
        rows = 10
        x, y, col_sp, row_sp, x_list, y_list = grid_function(cols, rows)
        with self.canvas:
            for i in range(1, cols):
                for j in range(1, rows):
                    Ellipse(pos=(x_list[i] + math.sin(self.bg_count + i*math.pi/4)*col_sp/16, y_list[j] + math.sin(self.bg_count + i*math.pi/4)*row_sp/16), size=(2, 2))
        self.bg_count += math.pi/256

    def draw(self, new_input, input_list):
        if new_input:
            if input_list[0] != 0:  # checks if there is a new x input
                self.menu_pos += input_list[0]
                if self.menu_pos < 0:
                    self.menu_pos = 0
                if self.menu_pos > self.total_icons - 1:
                    self.menu_pos = self.total_icons - 1
                if self.menu_pos != self.old_menu_pos:
                    self.old_menu_pos = self.menu_pos

        self.static_draw(self.menu_pos)
        return self.menu_pos

    def static_draw(self, p):
        label_list = ['Relay', 'Weather', 'NA', 'NA', 'NA']
        x, y, col_sp, row_sp, x_list, y_list = grid_function(7, 7)  # pass requested collums and rows

        self.lb.text = label_list[p]
        self.canvas.clear()
        with self.canvas:
            self.bg_draw()
            Rectangle(pos=(x_list[3] + col_sp/2 - self.lb.texture.size[0]/2, y_list[4] - 1.25*col_sp), texture=self.lb.texture,
                      size=list(self.lb.texture.size))
            Rectangle(pos=(x_list[3], y_list[4] - col_sp), source='images/' + label_list[p] + '1.png', size=(col_sp, col_sp))
            for i in range(0, p):
                Rectangle(pos=(x_list[3] - .75*col_sp - .75*(p-i)*col_sp, y_list[4] - col_sp), source='images/' + label_list[i] + '.png', size=(.6*col_sp, .6*col_sp))
            for i in range(p+1, self.total_icons):
                Rectangle(pos=(x_list[3] + .75*col_sp + .75*(i-p)*col_sp, y_list[4] - col_sp), source='images/' + label_list[i] + '.png', size=(.6*col_sp, .6*col_sp))

            for i in range(0, 5):
                    if i == p:
                        Line(close=True, ellipse=(Window.size[0]/2 + 20*i - 48, 10, 16, 16))
                    if i != p:
                        Ellipse(pos=(Window.size[0]/2 + 20*i - 48, 10), size=(16, 16))  # -48,-28,-8,3,8

    def update(self, new_input, input_list):
        screen_list = ['relay', 'weather', 'Label 3', 'Label 4', 'Label 5']
        # p is the name of the current icon, passed to main if selected

        p = self.draw(new_input, input_list)

        if new_input:
            if input_list[2] == 1:
                return [1, screen_list[p]]
            if input_list[3] == 1:
                return [1, 'start']

        return [0, 'menu']



