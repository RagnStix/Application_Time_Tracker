import win32gui as w
import psutil as ps
from datetime import datetime
import json, time, atexit




i = 0                                                                               #Variable to iterate dictionary
iteration = 0                                                                       #Variable to iterate list of times
active_window_name = ""
first_time = True
activities = {0: {"Activity": [],"Time": [] }}
times = []

def time_difference(d1, d2):
    return abs((d2-d1))                                                             #Calculates time spent on window by subtracting the time the next window was opened from the time the first window was opened.


try:
    while True:

        window = w.GetForegroundWindow()
        new_window_name = w.GetWindowText(window)
        if active_window_name != new_window_name:  # If the active window is not the same as the the previous window, set the previous window to new window.
            active_window_name = new_window_name

            if not first_time:

                end_time = datetime.now()  # The time when application was closed.

                if (active_window_name != "") and (active_window_name != "AppTimer – main.py"):  # Removes empty activities from dictionary.
                    activities[i] = {"Activity": active_window_name}  # Adds activity entry to the dictionary.
                    times.append(end_time)  # Adds end time value to the list of times.
                    i += 1
                    iteration += 1

                    if iteration > 1:
                        d1 = times[i - 2]
                        d2 = times[i - 1]
                        time_spent = str(time_difference(d1, d2))
                        activities[i - 2]["Time"] = time_spent  # Appends time spent on activity to dictionary.



        first_time = False

except KeyboardInterrupt:
    j = json.dumps(activities)  # Writes activities into a json file.
    with open('data_file.json', 'a') as f:
        f.write("{\n")
        for k in activities.keys():
            f.write("{}:{}\n".format(k, activities[k]))
        f.write("}\n")
        f.close()

    for p_id, p_info in activities.items():
        print("\nActivities: ", p_id)

        for key in p_info:
            print(key + ":", p_info[key])