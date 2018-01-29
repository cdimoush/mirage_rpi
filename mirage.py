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

Window.show_cursor = True

def chuck_decode():
    # use the working code on the raspberry pi
    # make sure to import the bluetooth library, and add socket and bluetooth information in the app build function
    global chuk_x
    global chuk_y
    global chuk_c
    global chuk_z
    global chuk_read_x
    global chuk_read_y
    global chuk_read_c
    global chuk_read_z

    input_list = [0, 0, 0, 0]  # Used to inform other function of what readings changed

    chuk_read_x = 0
    chuk_read_y = 0
    chuk_read_c = 0
    chuk_read_z = 0

    if chuk_x != chuk_read_x:
        input_list[0] = chuk_read_x
    if chuk_y != chuk_read_y:
        input_list[1] = chuk_read_y
    if chuk_c != chuk_read_c:
        input_list[2] = chuk_read_c
    if chuk_z != chuk_read_z:
        input_list[3] = chuk_read_z
    if input_list == [0, 0, 0, 0]:
        chuk_x = chuk_read_x
        chuk_y = chuk_read_y
        chuk_c = chuk_read_c
        chuk_z = chuk_read_z

        return False, input_list

    chuk_x = chuk_read_x
    chuk_y = chuk_read_y
    chuk_c = chuk_read_c
    chuk_z = chuk_read_z

    return True, input_list


def dev_chuck_decode(read_x, read_y, read_c, read_z):
    # use the working code on the raspberry pi
    # make sure to import the bluetooth library, and add socket and bluetooth information in the app build function
    global chuk_x
    global chuk_y
    global chuk_c
    global chuk_z

    input_list = [0, 0, 0, 0]  # Used to inform other function of what readings changed

    if chuk_x != read_x:
        input_list[0] = read_x
    if chuk_y != read_y:
        input_list[1] = read_y
    if chuk_c != read_c:
        input_list[2] = read_c
    if chuk_z != read_z:
        input_list[3] = read_z
    if input_list == [0, 0, 0, 0]:
        chuk_x = read_x
        chuk_y = read_y
        chuk_c = read_c
        chuk_z = read_z

        return False, input_list

    chuk_x = read_x
    chuk_y = read_y
    chuk_c = read_c
    chuk_z = read_z

    return True, input_list


class MirageClass(Widget):

    chuk_read_x = 0
    chuk_read_y = 0
    chuk_read_c = 0
    chuk_read_z = 0

    post_update_data = []

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
            self.chuk_read_y = 1
        elif keycode[1] == 's':
            self.chuk_read_y = -1
        elif keycode[1] == 'd':
            self.chuk_read_x = 1
        elif keycode[1] == 'a':
            self.chuk_read_x = -1
        elif keycode[1] == 'f':
            self.chuk_read_c = 1
        elif keycode[1] == 'g':
            self.chuk_read_z = 1
        return True

    def read_input(self):
        f = open('input.txt','r+')
        r = str(f.read())
        if r != '':
	   data = r[0]
	   if data == 'w':
	      self.chuk_read_y = 1
	   if data == 's':
	      self.chuk_read_y = -1
	   if data == 'd':
	      self.chuk_read_x = 1
	   if data == 'a':
	      self.chuk_read_x = -1
           if data == 'f':
	      self.chuk_read_c = 1
	   if data == 'g':
	      self.chuk_read_z = 1
	f.close()
	open('input.txt', 'w').close()
    ###################################################################################################################

    def mirage_update(self, dt):
        # real chuk_decode function uncomment for final program
        # new_input, input_list = chuck_decode()

        # dev chuck decode works with the keyboard reader
        self.read_input()
        new_input, input_list = dev_chuck_decode(self.chuk_read_x, self.chuk_read_y, self.chuk_read_c, self.chuk_read_z)
        self.post_update_data = sm.current_screen.update(new_input, input_list)

        # print(self.post_update_data)
        if self.post_update_data[0] == 1:
            print(self.post_update_data[1])
            sm.current = self.post_update_data[1]

        self.chuk_read_x = 0
        self.chuk_read_y = 0
        self.chuk_read_c = 0
        self.chuk_read_z = 0


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

chuk_x = 0  # global nunchuk variables
chuk_y = 0
chuk_c = 0
chuk_z = 0
chuk_read_x = 0
chuk_read_y = 0
chuk_read_c = 0
chuk_read_z = 0

if __name__ == '__main__':
    DisplayApp().run()
