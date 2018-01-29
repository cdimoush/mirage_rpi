from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Line, Rectangle, Ellipse, Color, Triangle
import RPi.GPIO as GPIO
from functions.function import grid_function

class RelayController:
    amp_pin = 5  # figure out the pins on the rpi, change the comments in the init function, somethings probably wrong with the green pin
    lamp_pin = 6
    fan_pin = 13
    red_pin = 19
    green_pin = 26
    # blue_pin = fill this in

    pin_list = [amp_pin, lamp_pin, fan_pin, red_pin, green_pin, 'blue_pin']  # add blue pin
    relay_state_list = ['OFF', 'OFF', 'OFF', 'OFF', 'OFF', 'OFF']

    ON = 0
    OFF = 1  # for some reason relay is backwards, ON or 1 means OFF

    def __init__(self):
        # super(class, self).__init__()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.amp_pin, GPIO.OUT)  # controls 1st relay
        GPIO.setup(self.lamp_pin, GPIO.OUT)  # controls 4th relay (second relay appears broken)
        GPIO.setup(self.fan_pin, GPIO.OUT)  # controls 3rd relay
        GPIO.setup(self.red_pin, GPIO.OUT)  # controls 5th relay
        GPIO.setup(self.green_pin, GPIO.OUT)  # controls 6th relay
        #GPIO.setup(self.blue_pin, GPIO.OUT)  # controls 7th relay
        

    def toggle(self, channel):
        GPIO.output(red_pin, OFF)

    def toggle(self, pin):
        if self.relay_state_list[pin] == 'OFF':
            self.relay_state_list[pin] = 'ON'
            GPIO.output(self.pin_list[pin], self.ON)
            return 'ON'
        if self.relay_state_list[pin] == 'ON':
            self.relay_state_list[pin] = 'OFF'
            GPIO.output(self.pin_list[pin], self.OFF)
            return 'OFF'


class RelayScreen(Screen):

    cols = 6
    rows = 6
    cursor_x = 0

    label_list = ['Amplifier', 'Lamp', 'Fan', 'Red', 'Green', 'Blue']
    relay_state_list = ['OFF', 'OFF', 'OFF', 'OFF', 'OFF', 'OFF']

    rc = RelayController()

    def __init__(self, **kwargs):  # commented out the clock
        super(Screen, self).__init__(**kwargs)
        self.setup()

    def setup(self):
        x, y, col_sp, row_sp, x_list, y_list = grid_function(self.cols, self.rows)

        with self.canvas.before:

            Rectangle(pos=(0, 0), source='images/BG_1.png', size=(x, y))
            # Rectangle(pos=(0, 0), source='images/BG_1.png', size=(x - col_sp/25, y_list[5] - row_sp/2))
            self.add_widget(Label(text='Relay Controller', pos=(-x/2 + col_sp/2, y/2 - row_sp/4)))
            Color(0,0,0)
            Line(points=(col_sp/50, y_list[1], x - col_sp/50, y_list[1], x - col_sp/50, y_list[5] + row_sp/2, col_sp/50, y_list[5] + row_sp/2, col_sp/50, y_list[1], x - col_sp/50), width=1)
            Line(points=(col_sp/50, y_list[2] - row_sp/2, x - col_sp/50, y_list[2] - row_sp/2))
            for i in range(0, 6):
                Color(.4,.4,.4)
                self.add_widget(Label(text=self.label_list[i], pos=(x_list[i] - x/2 + col_sp/2, y_list[1] - y/2 + 25)))

    def draw(self, new_input, input_list):
        x, y, col_sp, row_sp, x_list, y_list = grid_function(self.cols, self.rows)

        self.cursor_x += input_list[0]
        if self.cursor_x < 0:
            self.cursor_x = 0
        if self.cursor_x > 5:
            self.cursor_x = 5

        if new_input:
            if input_list[2] == 1:  # tests if the c button is pressed
                self.relay_state_list[self.cursor_x] = self.rc.toggle(self.cursor_x)
        self.canvas.clear()

        with self.canvas:
            Color(.4, .4, .4)
            Rectangle(pos=(x_list[self.cursor_x] + 10, y_list[0] + 25), size=(col_sp - 20, row_sp - 50))
            # Triangle(points=()) add triangles left and right of the cursor

            for i in range(0, 6):
                if self.relay_state_list[i] == 'ON':
                    Color(.2, .9, .2)
                    Line(points=(x_list[i] + col_sp/2, y_list[2], x_list[i] + col_sp/2, y_list[5]), width=3)
                    Ellipse(pos=(x_list[i] + col_sp / 2 - 25, y_list[5] - 25), size=(50, 50))
                else:
                    Color(.9, .2, .2)
                    Line(points=(x_list[i] + col_sp/2, y_list[2], x_list[i] + col_sp/2, y_list[5]), width=3)
                    Ellipse(pos=(x_list[i] + col_sp / 2 - 25, y_list[2] - 25), size=(50, 50))

            Color(1, 1, 1)  # RESET COlOR, in case this is the last time the draw function is called

    def update(self, new_input, input_list):

        self.draw(new_input, input_list)
        if new_input:
            if input_list[3] == 1:
                return [1, 'menu']
        return [0, 'relay']
