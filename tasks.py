import os
import datetime
import pygame

pygame.init()
info = pygame.display.Info()
window_x = (info.current_w - (798)) // 2
window_y = (info.current_h - (700)) // 2
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{window_x},{window_y}"

ORG_WIDTH = 798
ORG_HEIGHT = 600

WIDTH = ORG_WIDTH
HEIGHT = ORG_HEIGHT + 100
TITLE = "Calendar App"

current_time = {
    "second": datetime.datetime.now().second,
    "minute": datetime.datetime.now().minute,
    "hour": datetime.datetime.now().hour,
    "day": datetime.datetime.now().day,
    "month": datetime.datetime.now().strftime("%B"),
    "month(int)": datetime.datetime.now().month,
    "year": datetime.datetime.now().year
}

days = ["Sun", "    Mon", "        Tues", "           Wed", "                Thurs", "                    Fri", "                      Sat"]

def get_first_day(year, month):
    day_of_week = datetime.datetime(year, month, 1).strftime('%A')
    days_to_dates = {
        "sunday": 1,
        "monday": 2,
        "tuesday": 3,
        "wednesday": 4,
        "thursday": 5,
        "friday": 6,
        "saturday": 7
    }
    for day, num in days_to_dates.items():
        if day_of_week.lower() == day:
            return num

def draw_lines():
    for i in range(1, 8):
        screen.draw.line((i * ORG_WIDTH / 7, 85 if i != 7 else 0), (i * ORG_WIDTH / 7, ORG_HEIGHT + 25 if i != 7 else HEIGHT + 25), (0, 0, 0))
        if i == 7:
            screen.draw.line(((i * ORG_WIDTH / 7) + 1, 0), ((i * ORG_WIDTH / 7) + 1, HEIGHT), (0, 0, 0))
    for i in range(-1, 6):
        screen.draw.line((0, (125 if i != -1 else 185) + i * (ORG_HEIGHT - 100) / 5), (ORG_WIDTH, (125 if i != -1 else 185) + i * (ORG_HEIGHT - 100) / 5), (0, 0, 0))
        if i == -1:
            screen.draw.line((0, 226 + i * (ORG_HEIGHT - 100) / 5), (ORG_WIDTH, 226 + i * (ORG_HEIGHT - 100) / 5), (0, 0, 0))

def draw_days_of_week():
    global days
    for i in range(len(days)):
        screen.draw.text(days[i], color=(0, 0, 0), fontsize=45, midtop=(i * 100 + 50, 90))

def draw_dates_of_month():
    global current_time
    for i in range(1, 8):
        screen.draw.text(str(i), color=(0, 0, 0), fontsize=35, center=((100 * get_first_day(int(current_time["year"]), int(8))) + (110 * (i - 1)) + ((i - 1) * 5) - i, 140))

def draw():
    screen.fill((255, 255, 255))
    screen.draw.text(f"{current_time['month']}  {current_time['year']}", color=(0, 0, 0), fontsize=75, center=(400, 55))
    draw_lines()
    draw_days_of_week()
    draw_dates_of_month()

def update():
    global current_time
    current_time = {
        "second": datetime.datetime.now().second,
        "minute": datetime.datetime.now().minute,
        "hour": datetime.datetime.now().hour,
        "day": datetime.datetime.now().day,
        "month": datetime.datetime.now().strftime("%B"),
        "month(int)": datetime.datetime.now().month,
        "year": datetime.datetime.now().year,
    }

def on_mouse_down(pos, button):
    global WIDTH
    if button == 1:
        WIDTH = ORG_WIDTH + 350

def on_mouse_up():
    pass

import pgzrun
pgzrun.go()