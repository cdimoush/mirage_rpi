from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Canvas, Line, Rectangle, Ellipse, Color, Triangle
from kivy.core.window import Window


from functions.function import grid_function
import requests
import datetime

class WeatherScreen(Screen):
    new_screen = True
    call_draw = True
    logged_data = False
    error = False

    for_data = ''
    current_data = ''
    astro_data = ''

    current_time = ''

    rows = 6
    cols = 6

    lb_time = Label(text='text')

    a = Label(text='Weather')  # title
    b = Label(text='text: ', font_size='64sp')  # current temp
    c = Label(text='text')  # Daily high and low
    d = Label(text='text')  # Daily conditions with built in word wrap
    d1 = Label(text='text')
    d2 = Label(text='text')
    d3 = Label(text='text')
    e = Label(text='text')  # Daily pop and other info
    e1 = Label(text='text')
    e2 = Label(text='text')
    f = Label(text='text')  # Sun up
    g = Label(text='text')  # Sun Down
    h = Label(text='text')  # Moon up
    i = Label(text='text')  # Moon Down
    j = Label(text='Solar: ')
    k = Label(text='Lunar: ')
    l = Label(text='text')  # Length of Day
    m = Label(text='text')  # Phase of Moon
    n = Label(text='text', font_size='24sp')  # Date
    o = Label(text='text', font_size='48sp')  # Time

    date_rect = ''
    time_rect = ''

    i0 = ''
    i1 = ''

    lb_day0 = Label(text='text')  # Day of the week for forecast
    lb_day1 = Label(text='text', font_size='24sp')
    lb_day2 = Label(text='text', font_size='24sp')
    lb_day3 = Label(text='text', font_size='24sp')

    lb_high0 = Label(text='text')  # Daily Highs
    lb_high1 = Label(text='text')
    lb_high2 = Label(text='text')
    lb_high3 = Label(text='text')

    lb_low0 = Label(text='text')  # Daily Lows
    lb_low1 = Label(text='text')
    lb_low2 = Label(text='text')
    lb_low3 = Label(text='text')

    lb_pop0 = Label(text='text')  # Daily Percent Chance of Precipitation
    lb_pop1 = Label(text='text')
    lb_pop2 = Label(text='text')
    lb_pop3 = Label(text='text')

    day_list = [lb_day0, lb_day1, lb_day2, lb_day3]
    high_list = [lb_high0, lb_high1, lb_high2, lb_high3]
    low_list = [lb_low0, lb_low1, lb_low2, lb_low3]
    pop_list = [lb_pop0, lb_pop1, lb_pop2, lb_pop3]

    def __init__(self, **kwargs):  # commented out the clock
        super(Screen, self).__init__(**kwargs)
        self.setup()

    def setup(self):
        x, y, col_sp, row_sp, x_list, y_list = grid_function(self.cols, self.rows)

        with self.canvas.before:

            Rectangle(pos=(0, 0), source='images/BG_1.png', size=(x, y))
            Color(0,0,0)
            Line(points=(col_sp/50, y_list[0], x - col_sp/50, y_list[0], x - col_sp/50, y_list[5] + row_sp/2, col_sp/50, y_list[5] + row_sp/2, col_sp/50, y_list[0], x - col_sp/50), width=1)
            Line(points=(col_sp/50, y_list[2] - row_sp/2, x - col_sp/50, y_list[2] - row_sp/2))
            Line(points=(3*col_sp, y_list[2] - row_sp/2, 3*col_sp, 0))

            Color(.9, .2, .2)
            Line(points=(x_list[1], y_list[3] + row_sp/4, x_list[3], y_list[3] + row_sp/4), width=1.5)
            Ellipse(pos=(x_list[1] - 5, y_list[3] + row_sp/4 - 5), size=(10, 10))
            Ellipse(pos=(x_list[3] - 5, y_list[3] + row_sp/4 - 5), size=(10, 10))
            Color(.2, .2, .9)
            Line(points=(x_list[1], y_list[3] - row_sp/2, x_list[3], y_list[3] - row_sp/2), width=1.5)
            Ellipse(pos=(x_list[1] - 5, y_list[3] - row_sp/2 - 5), size=(10, 10))
            Ellipse(pos=(x_list[3] - 5, y_list[3] - row_sp/2 - 5), size=(10, 10))

            Color(1, 1, 1)

    def get_data(self):
        print('getting data')
        while True:
            try:
                #  get and save weather data
                #  data includes current, forecast, and astronomy
                c = requests.get("http://api.wunderground.com/api/1a6103aff95a0f09/conditions/q/TX/Austin.json")
                f = requests.get("http://api.wunderground.com/api/1a6103aff95a0f09/forecast/q/TX/Austin.json")
                a = requests.get("http://api.wunderground.com/api/1a6103aff95a0f09/astronomy/q/TX/Austin.json")
                self.current_data = c.json
                self.for_data = f.json
                self.astro_data = a.json
                self.logged_data = True

        #  ################################################################################################################### #

                #  Current Data Labels

                #  Current Temp
                self.b.text = str(self.current_data['current_observation']['temp_f']) + 'F'
                self.i0 = self.current_data['current_observation']['icon_url']
                with open('images/w_icon.png', 'wb') as f:
                    f.write(requests.get(self.i0).content)
                #  Current conditions description, if statements handel word wrap
                d_text = 'Conditions: ' + str(self.for_data['forecast']['txt_forecast']['forecastday'][0]['fcttext'])
                if len(d_text) > 180:
                    self.d.text = d_text[0:60]
                    self.d1.text = d_text[60:120]
                    self.d2.text = d_text[120:180]
                    self.d3.text = d_text[180:]
                elif len(d_text) > 120:
                    self.d.text = d_text[0:60]
                    self.d1.text = d_text[60:120]
                    self.d2.text = d_text[120:]
                elif len(d_text) > 60:
                    self.d.text = d_text[0:60]
                    self.d1.text = d_text[60:]
                else:
                    self.d.text = d_text


        # #################################################################################################################### #

                #  Forecast Data Labels

                i = 0
                for day in self.for_data['forecast']['simpleforecast']['forecastday']:
                    self.day_list[i].text = day['date']['weekday']
                    if i == 0:
                        self.high_list[i].text = day['high']['fahrenheit']
                        self.low_list[i].text = day['low']['fahrenheit']
                        self.pop_list[i].text = str(day['pop'])
                    else:
                        self.high_list[i].text = 'High: ' + str(day['high']['fahrenheit']) + 'F'
                        self.low_list[i].text = 'Low: ' + str(day['low']['fahrenheit']) + 'F'
                        self.pop_list[i].text = 'POP: ' + str(day['pop']) + '%'
                    i += 1

                self.c.text = self.high_list[0].text + 'F / ' + self.low_list[0].text + 'F'
                self.e.text = 'Chance of Precipitation: ' + self.pop_list[0].text + '%'
                self.e1.text = 'Avg Wind Speed: ' + str(self.for_data['forecast']['simpleforecast']['forecastday'][0]['avewind']['mph']) + 'mph'
                self.e2.text = 'Avg Humidity: ' + str(self.for_data['forecast']['simpleforecast']['forecastday'][0]['avehumidity'])

        # #################################################################################################################### #

                #  Astronomy Labels

                self.f.text = 'Rise: ' + str(self.astro_data['sun_phase']['sunrise']['hour']) + ':' + \
                                        str(self.astro_data['sun_phase']['sunrise']['minute'])
                self.g.text = 'Set: ' + str(self.astro_data['sun_phase']['sunset']['hour']) + ':' + \
                                        str(self.astro_data['sun_phase']['sunset']['minute'])
                self.h.text = 'Rise: ' + str(self.astro_data['moon_phase']['moonrise']['hour']) + ':' + \
                                        str(self.astro_data['moon_phase']['moonrise']['minute'])
                self.i.text = 'Set: ' + str(self.astro_data['moon_phase']['moonset']['hour']) + ':' + \
                                        str(self.astro_data['moon_phase']['moonset']['minute'])
                self.current_time = str(self.astro_data['moon_phase']['current_time']['hour']) + ':' + \
                                    str(self.astro_data['moon_phase']['current_time']['minute'])
                sun_range = abs(int(self.astro_data['sun_phase']['sunset']['hour']) +
                                    int(self.astro_data['sun_phase']['sunset']['minute']) / 60 -
                                    int(self.astro_data['sun_phase']['sunrise']['hour']) -
                                    int(self.astro_data['sun_phase']['sunrise']['minute']) / 60)
                self.l.text = 'Length of Day: ' + str(round(sun_range, 2)) + 'hrs'
                self.m.text = 'Phase of Moon: ' + str(self.astro_data['moon_phase']['phaseofMoon'])
                break
            except ConnectionError:
                self.error = True
                break

    def get_time_date(self):
        now = datetime.datetime.now()
        weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

        day = weekdays[now.weekday()]
        month = months[now.month]
        self.n.text = (day + ', ' + month + ' ' + str(now.day))
        minute = now.minute
        if minute < 10:
            minute = '0' + str(minute)
        else:
            minute = str(minute)
        sec = now.second
        if sec < 10:
            sec = '0' + str(sec)
        else:
            sec = str(sec)
        micro = str(now.microsecond)
        micro = micro[:2]
        self.o.text = ('%d' % now.hour + ':' + minute + ':' + sec + ':' + micro)

    def static_draw(self, new_input, input_list):
        x, y, col_sp, row_sp, x_list, y_list = grid_function(self.cols, self.rows)

        '''self.add_widget(Label(text=self.high_list[0].text,
                              pos=(-x/2, -y/2 + y_list[5] - row_sp/4),
                              font_size='64sp'))  # current temp
        self.add_widget(Label(text=self.high_list[0].text + ' / ' + self.low_list[0].text,
                              pos=(-x/2 + self.size[0]/2, -y/2 + y_list[4] + row_sp/3),
                              font_size='16sp'))  # current temp'''
        self.canvas.clear()
        with self.canvas:
            Rectangle(pos=(col_sp/32, y - row_sp/3), texture=self.a.texture, size=self.a.texture.size)
            Rectangle(pos=(col_sp/32, y_list[4] + 2*row_sp/3), texture=self.b.texture, size=self.b.texture.size)
            Rectangle(pos=(col_sp/32 + self.b.texture.size[0]/2 - self.c.texture.size[0]/2, y_list[4] + row_sp/2),
                      texture=self.c.texture,
                      size=self.c.texture.size)
            Rectangle(pos=(x_list[1] + col_sp/2, y_list[4] + 7*row_sp/12), source='images/w_icon.png', size=(75,75))

            if self.d3.text != 'text':
                Rectangle(pos=(x_list[2] + col_sp/2, y_list[5]), texture=self.d.texture, size=self.d.texture.size)
                Rectangle(pos=(x_list[2] + col_sp/2, y_list[5] - self.d.texture.size[1]),
                          texture=self.d1.texture,
                          size=self.d1.texture.size)
                Rectangle(pos=(x_list[2] + col_sp/2, y_list[5] - self.d1.texture.size[1]*2),
                          texture=self.d2.texture,
                          size=self.d2.texture.size)
                Rectangle(pos=(x_list[2] + col_sp/2, y_list[5] - self.d2.texture.size[1]*3),
                          texture=self.d3.texture,
                          size=self.d3.texture.size)
            elif self.d2.text != 'text':
                Rectangle(pos=(x_list[2] + col_sp/2, y_list[5]), texture=self.d.texture, size=self.d.texture.size)
                Rectangle(pos=(x_list[2] + col_sp/2, y_list[5] - self.d.texture.size[1]),
                          texture=self.d1.texture,
                          size=self.d1.texture.size)
                Rectangle(pos=(x_list[2] + col_sp/2, y_list[5] - self.d1.texture.size[1]*2),
                          texture=self.d2.texture,
                          size=self.d2.texture.size)
            elif self.d1.text != 'text':
                Rectangle(pos=(x_list[2] + col_sp/2, y_list[5]), texture=self.d.texture, size=self.d.texture.size)
                Rectangle(pos=(x_list[2] + col_sp/2, y_list[5] - self.d.texture.size[1]),
                          texture=self.d1.texture,
                          size=self.d1.texture.size)
            else:
                Rectangle(pos=(x_list[2] + col_sp/2, y_list[5]), texture=self.d.texture, size=self.d.texture.size)

            # Precipitation, Wind, and Humity
            Rectangle(pos=(col_sp/32, y_list[4]), texture=self.e.texture, size=self.e.texture.size)
            Rectangle(pos=(col_sp/32, y_list[4] - self.e.texture.size[1]), texture=self.e1.texture, size=self.e1.texture.size)
            Rectangle(pos=(col_sp/32, y_list[4] - self.e.texture.size[1]*2), texture=self.e2.texture, size=self.e2.texture.size)

            # ASTRONOMY TITLES, Solar Title(j) nad Lunar Title(k)
            Rectangle(pos=(col_sp/32, y_list[3] + row_sp/4 - 10), texture=self.j.texture, size=self.j.texture.size)
            Rectangle(pos=(col_sp/32, y_list[3] - row_sp/2 - 10), texture=self.k.texture, size=self.k.texture.size)
            # End segments of solar line (x_list[1], y_list[3] + row_sp/4) and (x_list[3], y_list[3] + row_sp/4)
            # End segments of lunar line (x_list[1], y_list[3] - row_sp/2) and (x_list[3], y_list[3] - row_sp/2)
            # Sun up(f) Sun down(g) Moon up(h) Moon down(i)
            Rectangle(pos=(x_list[1] - self.f.texture.size[0]/2, y_list[3]), texture=self.f.texture, size=self.f.texture.size)
            Rectangle(pos=(x_list[3] - self.g.texture.size[0]/2, y_list[3]), texture=self.g.texture, size=self.g.texture.size)
            Rectangle(pos=(x_list[1] - self.h.texture.size[0]/2, y_list[3] - .75*row_sp), texture=self.h.texture, size=self.h.texture.size)
            Rectangle(pos=(x_list[3] - self.i.texture.size[0]/2, y_list[3] - .75*row_sp), texture=self.i.texture, size=self.i.texture.size)
            # Show current sun and moon location
            sun_range = abs(int(self.astro_data['sun_phase']['sunset']['hour']) +
                            int(self.astro_data['sun_phase']['sunset']['minute']) / 60 -
                            int(self.astro_data['sun_phase']['sunrise']['hour']) -
                            int(self.astro_data['sun_phase']['sunrise']['minute']) / 60)
            moon_range = abs(int(self.astro_data['moon_phase']['moonset']['hour']) +
                             int(self.astro_data['moon_phase']['moonset']['minute']) / 60 -
                             int(self.astro_data['moon_phase']['moonrise']['hour']) -
                             int(self.astro_data['moon_phase']['moonrise']['minute']) / 60)
            s_calc_time = abs(int(self.astro_data['moon_phase']['current_time']['hour']) +
                            int(self.astro_data['moon_phase']['current_time']['minute']) / 60 -
                            int(self.astro_data['sun_phase']['sunrise']['hour']) -
                            int(self.astro_data['sun_phase']['sunrise']['minute']) / 60)
            m_calc_time = abs(int(self.astro_data['moon_phase']['current_time']['hour']) +
                            int(self.astro_data['moon_phase']['current_time']['minute']) / 60 -
                            int(self.astro_data['moon_phase']['moonrise']['hour']) -
                            int(self.astro_data['moon_phase']['moonrise']['minute']) / 60)
            sun_pct = s_calc_time / sun_range
            moon_pct = m_calc_time / moon_range
            if sun_pct < 1:
                Color(.9, .2, .2)
                Line(points=(3*col_sp*sun_pct, y_list[3] + row_sp/4 + row_sp/8, 3*col_sp*sun_pct, y_list[3] + row_sp/4 - row_sp/8), width=1.5)
            if moon_pct < 1:
                Color(.2, .2, .9)
                Line(points=(3*col_sp*moon_pct, y_list[3] - row_sp/2 + row_sp/8, 3*col_sp*moon_pct, y_list[3] - row_sp/2 - row_sp/8), width=1.5)
            Color(1, 1, 1)
            Rectangle(pos=(x_list[4] - col_sp/4, y_list[3] + row_sp/4 - 10), texture=self.l.texture, size=self.l.texture.size)
            Rectangle(pos=(x_list[4] - col_sp/4, y_list[3] - row_sp/2 - 10), texture=self.m.texture, size=self.m.texture.size)

            for i in range(1, len(self.day_list)):
                Rectangle(pos=(col_sp/32 + 1*col_sp*(i-1), y_list[1] + row_sp/6), texture=self.day_list[i].texture, size=self.day_list[i].texture.size)
                Rectangle(pos=(col_sp/32 + 1*col_sp*(i-1), y_list[1] - row_sp/4), texture=self.high_list[i].texture, size=self.high_list[i].texture.size)
                Rectangle(pos=(col_sp/32 + 1*col_sp*(i-1), y_list[1] - row_sp/4 - self.low_list[i].texture.size[1]), texture=self.low_list[i].texture, size=self.low_list[i].texture.size)
                Rectangle(pos=(col_sp/32 + 1*col_sp*(i-1), y_list[1] - row_sp/4 - self.low_list[i].texture.size[1]*2), texture=self.pop_list[i].texture, size=self.pop_list[i].texture.size)

            self.date_rect = Rectangle(pos=(x_list[3] + col_sp/2, y_list[1] + row_sp/6), texture=self.n.texture, size=self.n.texture.size)
            self.time_rect = Rectangle(pos=(self.date_rect.pos[0] + (self.n.texture.size[0] - self.o.texture.size[0])/2, y_list[1] - self.o.texture.size[1]), texture=self.o.texture, size=self.o.texture.size)

    def dynamic_draw(self):
        self.date_rect.texture = self.n.texture
        self.date_rect.size = self.n.texture.size
        self.time_rect.texture = self.o.texture
        self.time_rect.size = self.o.texture.size

    def update(self, new_input, input_list):
        if not self.error:
            self.get_time_date()
            print('A')
            if self.logged_data:
                if self.call_draw:
                    self.static_draw(new_input, input_list)
                    self.call_draw = False
                self.dynamic_draw()
            if self.new_screen:
                print('B')
                self.get_data()
                self.logged_data = True
                self.new_screen = False
        else:
            self.add_widget(Label(text='Failed to Fetch Data'))

        print('C')
        if new_input:
            if input_list[3] == 1:
                self.logged_data = False
                self.new_screen = True
                self.call_draw = True
                print('end weather update')
                return [1, 'menu']
        print('end weather update')
        return [0, 'weather']

