from environs import Env
import customtkinter as ctk
import pyowm
from pyowm.utils.config import get_default_config
from pyowm.utils import timestamps

env = Env()
env.read_env()
API_TOKEN = env('API_TOKEN')

config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = pyowm.OWM(API_TOKEN, config_dict)
mgr = owm.weather_manager()

ctk.set_default_color_theme("dark-blue")
ctk.set_appearance_mode('dark')
window = ctk.CTk()
window.minsize(640, 480)
window.resizable(False, False)
window.title("Погода")
window.iconbitmap('icon.ico')
content = ''

def get_weather_now():
    
    city =  entry.get()

    observation = mgr.weather_at_place(city)
    w = observation.weather

    temp = w.temperature('celsius')['temp']
    hum = w.humidity
    det = w.detailed_status
    return f'В городе {city} сейчас {int(temp)} °C\nВлажность {hum} %\n{det.capitalize()}'

def show_weather_now():
    global content
    if content:
        content.destroy()
    content = ctk.CTkLabel(master=window, text=get_weather_now(), font=('Roboto', 26))
    content.pack(pady=10)

def get_weather_tomorrow():
    
    city =  entry.get()

    forecast = mgr.forecast_at_place(city, '3h')
    tomorrow = timestamps.tomorrow()
    weather = forecast.get_weather_at(tomorrow)

    temp = weather.temperature('celsius')['temp']
    hum = weather.humidity
    det = weather.detailed_status
    return f'В городе {city} завтра будет {int(temp)} °C\nВлажность {hum} %\n{det.capitalize()}'

def show_weather_tomorrow():
    global content
    if content:
        content.destroy()
    content = ctk.CTkLabel(master=window, text=get_weather_tomorrow(), font=('Roboto', 26))
    content.pack(pady=10)

def change_theme():
    if ctk.AppearanceModeTracker.get_mode():
        return ctk.set_appearance_mode("light")
    else:
        return ctk.set_appearance_mode("dark")


switch_frame = ctk.CTkFrame(master=window)
switch_frame.pack(fill="x")

switch = ctk.CTkSwitch(master=switch_frame, command=change_theme, text=None)
switch.pack(side='right')


entry = ctk.CTkEntry(master=window, placeholder_text="Укажите город", width=640, height=40, font=('Moon Dance', 18, 'italic'))
entry.pack(padx=20, pady=20)

button_frame = ctk.CTkFrame(master=window)
button_frame.pack()

button = ctk.CTkButton(master=button_frame , text="Погода сейчас", command=show_weather_now, font=('Roboto', 18), height=40)
button.pack(side='left', padx=20, pady=20)

button = ctk.CTkButton(master=button_frame , text="Погода на завтра", command=show_weather_tomorrow, font=('Roboto', 18), height=40)
button.pack(side='right', padx=20, pady=20)

window.mainloop()
