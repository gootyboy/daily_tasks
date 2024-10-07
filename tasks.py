import os
import pygame
import tkinter
import datetime
from pymongo import MongoClient
from pgzero.rect import Rect

pygame.init()
info = pygame.display.Info()
window_x = (info.current_w - (798)) // 2
window_y = (info.current_h - (700)) // 2
os.environ["SDL_VIDEO_WINDOW_POS"] = f"{window_x},{window_y}"

client = MongoClient("mongodb://localhost:27017/")
database = client.get_database("my_tasks_db")
task_colection = database.get_collection("my_tasks")

ORG_WIDTH = 798
ORG_HEIGHT = 600
WIDTH = ORG_WIDTH
HEIGHT = ORG_HEIGHT + 100
TITLE = "Calendar App"

days = ["Sun", "    Mon", "        Tues", "           Wed", "                Thurs", "                    Fri", "                      Sat"]
screen_clicked = False

tasks=[]
rects = {"day_rect": [Rect((ORG_WIDTH / 7) * i - 1, 124 + 100 * j, ORG_WIDTH / 7 + 1, HEIGHT / 7 + 1) for j in range(5) for i in range(7)],
         "today_rect": Rect(ORG_HEIGHT + 50, ORG_WIDTH - 100, 75, 30),
         "add_task_rect": Rect(ORG_WIDTH + 40, ORG_HEIGHT + 15, 125, 30)
         }
rect_clicked = None
rect_hover = None
hover_color = (200, 200, 200)
today_color = (150, 150, 255)

def screeninput(title, prompt, width, height):
    root = tkinter.Tk()
    root.geometry(f"{width}x{height}")
    root.title(title)
    label = tkinter.Label(root, text=prompt)
    label.pack(pady=20)
    entry = tkinter.Entry(root, width=50)
    entry.pack(pady=20)
    user_input = []
    ok_button = tkinter.Button(root, text="OK", command=lambda: (user_input.append(entry.get()), root.destroy()))
    ok_button.pack(pady=20)
    root.mainloop()
    return user_input[0] if user_input else None

def order_tasks():
    global tasks
    n = len(tasks)
    for i in range(n):
        for j in range(0, n-i-1):
            time_j = int(tasks[j]["start_time"].split(":")[0])
            time_j1 = int(tasks[j+1]["start_time"].split(":")[0])
            if not tasks[j]["morning"]:
                time_j += 12
            if not tasks[j+1]["morning"]:
                time_j1 += 12
            if time_j > time_j1:
                tasks[j], tasks[j+1] = tasks[j+1], tasks[j]

def get_first_day(year, month):
    day_of_week = datetime.datetime(year, month, 1).strftime("%A")
    days_to_dates = {
        "sunday": 0,
        "monday": 1,
        "tuesday": 2,
        "wednesday": 3,
        "thursday": 4,
        "friday": 5,
        "saturday": 6
    }
    for day, num in days_to_dates.items():
        if day_of_week.lower() == day:
            return num

def draw_lines():
    # Veritcal Lines (top to bottom)
    for i in range(1, 8):
        screen.draw.line((i * ORG_WIDTH / 7, 85 if i != 7 else 0), (i * ORG_WIDTH / 7, ORG_HEIGHT + 25 if i != 7 else HEIGHT + 25), (0, 0, 0))
        if i == 7:
            screen.draw.line(((i * ORG_WIDTH / 7) + 1, 0), ((i * ORG_WIDTH / 7) + 1, HEIGHT), (0, 0, 0))
    # Horizontial Lines (left to right)
    for i in range(-1, 6):
        screen.draw.line((0, (125 if i != -1 else 185) + i * (ORG_HEIGHT - 100) / 5), ((ORG_WIDTH if i != -1 and i != 0 else WIDTH), (125 if i != -1 else 185) + i * (ORG_HEIGHT - 100) / 5), (0, 0, 0))
        if i == -1:
            screen.draw.line((0, 226 + i * (ORG_HEIGHT - 100) / 5), (WIDTH, 226 + i * (ORG_HEIGHT - 100) / 5), (0, 0, 0))
            screen.draw.line((0, 186 + i * (ORG_HEIGHT - 100) / 5), (WIDTH, 186 + i * (ORG_HEIGHT - 100) / 5), (0, 0, 0))

def draw_days_of_week():
    global days
    for i in range(len(days)):
        screen.draw.text(days[i], color=(0, 0, 0), fontsize=45, midtop=(i * 100 + 50, 90))

def draw_dates_of_month():
    global current_time, days_in_month
    first_day = get_first_day(current_time["year"], current_time["month(int)"])
    days_in_month = (datetime.datetime(current_time["year"], current_time["month(int)"] + 1, 1) - datetime.datetime(current_time["year"], current_time["month(int)"], 1)).days
    for i in range(days_in_month):
        x = (((i + first_day) % 7) * ORG_WIDTH / 7) + 7.5
        y = 132.5 + (((i + first_day) // 7) * (ORG_HEIGHT - 100) / 5)
        screen.draw.text(str(i + 1), color= (0, 0, 0), topleft= (x, y), fontsize= 30)

def draw_tasks(tasks):
    global rect_clicked
    screen.draw.text("Tasks", color=(0, 0, 0), fontsize=75, center=(950, 55))
    for i in range(len(tasks)):
        if int(tasks[i]["end_time"].removesuffix(":00")) > current_time["hour"]["int"] >= int(tasks[i]["start_time"].removesuffix(":00")):
            if current_time["hour"]["morning"] == tasks[i]["morning"] and rect_clicked == current_time["day"]:
                screen.draw.text(f"{tasks[i]["name"]}: {tasks[i]["start_time"]} to {tasks[i]["end_time"]}", color=(255, 0, 0), fontsize=35, midleft=(810, 145 + (i * 35)))
                continue
        screen.draw.text(f"{tasks[i]["name"]}: {tasks[i]["start_time"]} to {tasks[i]["end_time"]}", color=(0, 0, 0), fontsize=35, midleft=(810, 145 + (i * 35)))
    screen.draw.text(f"{current_time["month"]} {rect_clicked}", color = (0, 0, 0), fontsize = 45, center=(950, 110))

def draw():
    global screen_clicked, rect_hover
    screen.fill((255, 255, 255))
    screen.draw.text(f"{current_time["month"]}  {current_time["year"]}", color=(0, 0, 0), fontsize=75, center=(400, 55))
    screen.draw.text(f"Current Date: {current_time["month"]} {current_time["day"]}", color=(0, 0, 0), fontsize=35, midleft=(0, ORG_HEIGHT + 50))
    screen.draw.text(f"Current Time: {current_time["time(AM/PM)"]}", color=(0, 0, 0), fontsize=35, midleft=(0, ORG_HEIGHT + 85))
    screen.draw.filled_rect(rects["day_rect"][current_time["day"] + get_first_day(current_time["year"], current_time["month(int)"]) - 1], color=today_color)
    if rect_hover != None:
        screen.draw.filled_rect(rects["day_rect"][rect_hover], color= hover_color)
    if screen_clicked:
        draw_tasks(tasks)
        screen.draw.filled_rect(Rect(810, ORG_HEIGHT + 60, 40, 20), color=(255, 0, 0))
        screen.draw.text("= Current Task", color=(0, 0, 0), fontsize=30, topleft=(855, ORG_HEIGHT + 60))
        # screen.draw.rect(rects["today_rect"], color= (0, 0, 0))
        screen.draw.filled_rect(rects["add_task_rect"], color= (150, 255, 175))
        screen.draw.textbox("Add Task", rects["add_task_rect"], color= (0, 0, 0))
    draw_lines()
    draw_days_of_week()
    draw_dates_of_month()

def update():
    global current_time
    current_hour = datetime.datetime.now().strftime("%I %p")
    if current_hour.startswith("0"):
        current_hour = current_hour.removeprefix("0")
    if current_hour.endswith(" AM"):
        current_hour = int(current_hour.removesuffix(" AM"))
        morning = True
    elif current_hour.endswith(" PM"):
        current_hour = int(current_hour.removesuffix(" PM"))
        morning = False
    current_time = {
        "time(AM/PM)": datetime.datetime.now().strftime("%I:%M:%S %p"),
        "hour": {"int": current_hour, "morning": morning},
        "day": datetime.datetime.now().day,
        "month": datetime.datetime.now().strftime("%B"),
        "month(int)": datetime.datetime.now().month,
        "year": datetime.datetime.now().year,
    }
    order_tasks()

def get_tasks(day, month, year):
    global tasks,task_colection
    query = {"day": day, "month": month, "year": year}
    task_data = task_colection.find_one(query)
    if task_data != None:
        tasks = task_data["tasks"]
    else:
        tasks = []

def ask_for_time(start_time):
    title = f"{"Start" if start_time else "End"} Time"
    time = screeninput(title, f"Enter {title.lower()}:", 255, 175)
    while True:
        if time.endswith(":00"):
            if time.removesuffix(":00").isnumeric():
                if 0 < int(time.removesuffix(":00")) < 13:
                    break
                else:
                    time = screeninput(title, "Time must be in 12 hour format (without the \"am\"/\"pm\")\n(You will determine if the time is in the \nmorning or evening later)", 310, 175)
            else:
                time = screeninput(title, "All digits must be numeric (except for \":\")", 255, 175)
        else:
            if time.lower().endswith("am") or time.lower().endswith("pm"):
                time = screeninput(title, "Time must not end with \"AM\" or \"PM\"", 255, 175)
            else:
                time = screeninput(title, "Time must end in \":00\"", 255, 175)
    return time

def add_task():
    task_name = screeninput("Task Name", "Enter task name:", 255, 175)
    start_time = ask_for_time(True)
    end_time = ask_for_time(False)
    print(task_name, start_time, end_time)

def on_mouse_down(pos, button):
    global rects, WIDTH, screen_clicked, rect_clicked, days_in_month
    for i in range(len(rects["day_rect"])):
        if rects["day_rect"][i].collidepoint(pos) and button == 1:
            rect_clicked = i + 1 - int(get_first_day(current_time["year"], current_time["month(int)"]))
            if rect_clicked > 0 and rect_clicked <= days_in_month:
                WIDTH = ORG_WIDTH + 350
                screen_clicked = True
                get_tasks(rect_clicked, current_time["month(int)"], current_time["year"])
            else:
                WIDTH = ORG_WIDTH
                screen_clicked = False
    if rects["add_task_rect"].collidepoint(pos) and button == 1:
        add_task()

def on_mouse_move(pos):
    global rect_hover
    if 0 < pos[0] < ORG_WIDTH - 1 and 125 < pos[1] < ORG_HEIGHT:
        for i in range(len(rects["day_rect"])):
            if rects["day_rect"][i].collidepoint(pos):
                rect_hover = i
    else:
        rect_hover = None

import pgzrun
pgzrun.go()