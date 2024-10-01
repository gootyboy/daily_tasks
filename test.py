with open(r"C:\Projects\daily_tasks\tasks.txt", "r") as file:
    lines = file.readlines()

for line in lines:
    line_data = line.split("|")
    line_month = line_data[0]
    line_year = line_data[1]
    line_day = line_data[2]
    line_tasks = line_data[3].split(";")
    for line_task in line_tasks:
        one_task = line_task.split(":")
        print(f"{line_month} {line_day}, {line_year}:")
        print(f"Activity: {one_task[0]}, Time: {one_task[1]}")