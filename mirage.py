from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.graphics import Line, Rectangle, Ellipse, Color, Triangle
from kivy.clock import Clock
from kivy.core.window import Window

from screens.menu_screen import MenuScreen
from screens.relay_screen import RelayScreen
from screens.start_screen import StartScreen
from screens.weather_screen import WeatherScreen

import os
os.environ['KIVY_WINDOW'] = 'egl_rpi'

#uncomment for cursor
# Window.show_cursor = True


def input_decode(read_x, read_y, read_c, read_z):
    # use the working code on the raspberry pi
    # make sure to import the bluetooth library, and add socket and bluetooth information in the app build function
    global in_x
    global in_y
    global in_a
    global in_b

    input_list = [0, 0, 0, 0]  # Used to inform other function of what readings changed

    if in_x != read_x:
        input_list[0] = read_x
    if in_y != read_y:
        input_list[1] = read_y
    if in_a != read_c:
        input_list[2] = read_c
    if in_b != read_z:
        input_list[3] = read_z
    if input_list == [0, 0, 0, 0]:
        in_x = read_x
        in_y = read_y
        in_a = read_c
        in_b = read_z

        return False, input_list

    in_x = read_x
    in_y = read_y
    in_a = read_c
    in_b = read_z

    return True, input_list #add relay controller below this

class Mirage_RelayController:
    tv_pin = ''
    pin_list = [tv_pin]
    relay_state_list = ['ON']

    ON = 0
    OFF = 1  # for some reason relay is backwards, ON or 1 means OFF

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.tv_pin, GPIO.OUT)

    def toggle(self):
        if self.relay_state_list[0] == 'OFF':
            self.relay_state_list[0] = 'ON'
            GPIO.output(self.pin_list[0], self.ON)
            print('TV ON')
            return 'ON'
        if self.relay_state_list[0] == 'ON':
            self.relay_state_list[0] = 'OFF'
            GPIO.output(self.pin_list[0], self.OFF)
            print('TV OFF')
            return 'OFF'

class MirageClass(Widget):

    read_x = 0 # change var names
    read_y = 0
    read_a = 0
    read_b = 0

    post_update_data = []
    transition = False
    next_screen = ''

    sleep = False
    sleep_timer = 0

    rc = Mirage_RelayController()
    ###################################################################################################################

    # Keyboard Reader code, used to test screen development
    # REMOVE before upload

    def __init__(self, **kwargs):
        super(MirageClass, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'w':
            self.read_y = 1
        elif keycode[1] == 's':
            self.read_y = -1
        elif keycode[1] == 'd':
            self.read_x = 1
        elif keycode[1] == 'a':
            self.read_x = -1
        elif keycode[1] == 'f':
            self.read_a = 1
        elif keycode[1] == 'g':
            self.read_b = 1
        return True

    def read_input(self):
        f = open('input.txt','r+')
        r = str(f.read())
        if r != '':
            data = r[0]
            if data == 'w':
                self.read_y = 1
            if data == 's':
                 self.read_y = -1
            if data == 'd':
                self.read_x = 1
            if data == 'a':
                self.read_x = -1
            if data == 'f':
                self.read_a = 1
            if data == 'g':
                self.read_b = 1
        f.close()
        open('input.txt', 'w').close()

###################################################################################################################

    def mirage_update(self, dt):
        # The mirage_update function is the main loop of the entire GUI
        #
        # This function has three critical responsibilities
        # 1) Receive input from the custom controller or keyboard (used for testing purposes)
        # 2) Call and send inputs to the update function of the current screen
        # 3) Transition to other screens

        self.read_input()
        new_input, input_list = input_decode(self.read_x, self.read_y, self.read_a, self.read_b)

        if new_input:
            self.sleep_timer = 0
            if self.sleep:
                self.rc.toggle()
            self.sleep = False
        if self.sleep_timer > 100:
            if not self.sleep:
                self.rc.toggle()
            self.sleep = True
            # print('sleep')

        else:
            # Call current screens update function // new_input = True / False, input_list = [0, 0, 0, 0]
            # post_update_data = [boolean for transition, desired screen(same screen if first arg is false]
            self.post_update_data = sm.current_screen.update(new_input, input_list)

            if self.transition:  # Changes the current screen, prep is required for transition to be True
                sm.current = self.next_screen
                self.transition = False
            elif self.post_update_data[0] == 1:  # if new screen was selected in current_screen update
                self.transition = True
                self.next_screen = self.post_update_data[1]
                i = sm.screen_names.index(self.next_screen)  # gets index of new screen from screen manager list
                print('call next screen load')
                sm.screens[i].update(False, [0, 0, 0, 0])  # preps/updates new screen without setting it to current, 'Loading'

            self.sleep_timer += 1

        self.read_x = 0
        self.read_y = 0
        self.read_a = 0
        self.read_b = 0


sm = ScreenManager(transition=NoTransition())
sm.add_widget(StartScreen(name='start'))
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(RelayScreen(name='relay'))
sm.add_widget(WeatherScreen(name='weather'))
screen_list = ['start', 'menu', 'relay', 'weather']


class DisplayApp(App):
    def build(self):
        # Window.fullscreen = True
        main_class = MirageClass()
        Clock.schedule_interval(main_class.mirage_update, 1.0/60.0)
        # Defines the what screen the App show first
        sm.current = 'start'
        # Defaults to control of the screen manager
        # make the clock and general update, then remove the updates from the screens <-----------------------
        return sm

in_x = 0  # global nunchuk variables
in_y = 0
in_a = 0
in_b = 0
read_x = 0
read_y = 0
read_a = 0
read_b = 0

if __name__ == '__main__':
    DisplayApp().run()
