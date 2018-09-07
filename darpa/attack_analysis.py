#!/usr/bin/env python
# THIS SCRIPT IS A PIECE OF SHIT

import sys
from datetime import datetime
from datetime import timedelta
import csv
import os

week = str
day = str 
csvfile = object
writer = object

def main():
    if len(sys.argv) != 2:
        print "Usage : %s <tcpdumplist>" % sys.argv[0]
        sys.exit(1)

    filename = sys.argv[1]
    global day 
    day = os.path.basename(filename[:-5])
    global week 
    week = os.path.basename(os.path.dirname(filename))[5:]

    global f
    csvfile = open("attacklog.csv", 'a+')
    global writer
    writer = csv.writer(csvfile)

    file2 = []
    with open(filename) as f:
        file = f.read().splitlines()

    i = 0
    while i < len(file):
        line_element = file[i].split()
        if (line_element[10] == "back"):
            file2.append(" ".join(str(item) for item in line_element))

        if (line_element[10] == "land"):
            file2.append(" ".join(str(item) for item in line_element))

        if (line_element[10] == "neptune"):
            file2.append(" ".join(str(item) for item in line_element))

        if (line_element[10] == "pod"):
            file2.append(" ".join(str(item) for item in line_element))

        if (line_element[10] == "smurf"):
            file2.append(" ".join(str(item) for item in line_element))

        if (line_element[10] == "syslog"):
            file2.append(" ".join(str(item) for item in line_element))

        if (line_element[10] == "teardrop"):
            file2.append(" ".join(str(item) for item in line_element))
                
        i = i + 1


    # print(file2)
    file2.append("0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0")
    i = 0
    while i < len(file2):
        if (i == len(file2)-1):
            line_element = file2[i].split()
            # print(line_element)
        else:
            line_element = file2[i].split()
            if (line_element[10] == "back"):
                    # print(line_element)
                    duration = datetime.strptime(line_element[3], "%H:%M:%S")
                    delta = timedelta(
                        hours=duration.hour, minutes=duration.minute, seconds=duration.second)
                    start_time = datetime.strptime(line_element[2], "%H:%M:%S")
                    end_time = start_time + delta
                    # print(start_time)
                    first_line_element = line_element
                    i = i + 1
                    line_element = file2[i].split()
                    while (line_element[10] == "back"):
                        # print("find")
                        duration_new = datetime.strptime(
                            line_element[3], "%H:%M:%S")
                        delta_new = timedelta(
                            hours=duration_new.hour, minutes=duration_new.minute, seconds=duration_new.second)
                        start_time_new = datetime.strptime(
                            line_element[2], "%H:%M:%S")
                        end_time_new = start_time_new + delta_new
                        
                        

                        if (end_time_new > end_time):
                            end_time = end_time_new

                        # print(end_time_new)

                        i = i + 1
                        line_element = file2[i].split()

                    first_line_element.insert(0, week)
                    first_line_element.insert(1, day)
                    end_time_str = (end_time.strftime("%H:%M:%S"))
                    first_line_element.insert(5, end_time_str)
                    del first_line_element[2]
                    del first_line_element[5:12]
                    i = i - 1
                    writer.writerow(first_line_element)

            if (line_element[10] == "land"):
                    duration = datetime.strptime(line_element[3], "%H:%M:%S")
                    delta = timedelta(
                        hours=duration.hour, minutes=duration.minute, seconds=duration.second)
                    start_time = datetime.strptime(line_element[2], "%H:%M:%S")
                    end_time = start_time + delta
                    first_line_element = line_element
                    i = i + 1
                    line_element = file2[i].split()
                    while (line_element[10] == "land"):
                        duration_new = datetime.strptime(
                            line_element[3], "%H:%M:%S")
                        delta_new = timedelta(
                            hours=duration_new.hour, minutes=duration_new.minute, seconds=duration_new.second)
                        start_time_new = datetime.strptime(
                            line_element[2], "%H:%M:%S")
                        end_time_new = start_time_new + delta_new
                        # print(end_time_new)

                        if (end_time_new > end_time):
                            end_time = end_time_new

                        i = i + 1
                        line_element = file2[i].split()

                    first_line_element.insert(0, week)
                    first_line_element.insert(1, day)
                    end_time_str = (end_time.strftime("%H:%M:%S"))
                    first_line_element.insert(5, end_time_str)
                    del first_line_element[2]
                    del first_line_element[5:12]
                    i = i - 1
                    writer.writerow(first_line_element)

            if (line_element[10] == "neptune"):
                    duration = datetime.strptime(line_element[3], "%H:%M:%S")
                    delta = timedelta(
                        hours=duration.hour, minutes=duration.minute, seconds=duration.second)
                    start_time = datetime.strptime(line_element[2], "%H:%M:%S")
                    end_time = start_time + delta

                    first_line_element = line_element
                    i = i + 1
                    line_element = file2[i].split()
                    while (line_element[10] == "neptune"):
                        duration_new = datetime.strptime(
                            line_element[3], "%H:%M:%S")
                        delta_new = timedelta(
                            hours=duration_new.hour, minutes=duration_new.minute, seconds=duration_new.second)
                        start_time_new = datetime.strptime(
                            line_element[2], "%H:%M:%S")
                        end_time_new = start_time_new + delta_new
                        # print(end_time_new)

                        if (end_time_new > end_time):
                            end_time = end_time_new

                        i = i + 1
                        line_element = file2[i].split()

                    first_line_element.insert(0, week)
                    first_line_element.insert(1, day)
                    end_time_str = (end_time.strftime("%H:%M:%S"))
                    first_line_element.insert(5, end_time_str)
                    del first_line_element[2]
                    del first_line_element[5:12]
                    i = i - 1
                    writer.writerow(first_line_element)

            if (line_element[10] == "pod"):
                    duration = datetime.strptime(line_element[3], "%H:%M:%S")
                    delta = timedelta(
                        hours=duration.hour, minutes=duration.minute, seconds=duration.second)
                    start_time = datetime.strptime(line_element[2], "%H:%M:%S")
                    end_time = start_time + delta

                    first_line_element = line_element
                    i = i + 1
                    line_element = file2[i].split()
                    while (line_element[10] == "pod"):
                        duration_new = datetime.strptime(
                            line_element[3], "%H:%M:%S")
                        delta_new = timedelta(
                            hours=duration_new.hour, minutes=duration_new.minute, seconds=duration_new.second)
                        start_time_new = datetime.strptime(
                            line_element[2], "%H:%M:%S")
                        end_time_new = start_time_new + delta_new
                        # print(end_time_new)

                        if (end_time_new > end_time):
                            end_time = end_time_new

                        i = i + 1
                        line_element = file2[i].split()

                    first_line_element.insert(0, week)
                    first_line_element.insert(1, day)
                    end_time_str = (end_time.strftime("%H:%M:%S"))
                    first_line_element.insert(5, end_time_str)
                    del first_line_element[2]
                    del first_line_element[5:12]
                    i = i - 1
                    writer.writerow(first_line_element)

            if (line_element[10] == "smurf"):
                    duration = datetime.strptime(line_element[3], "%H:%M:%S")
                    delta = timedelta(
                        hours=duration.hour, minutes=duration.minute, seconds=duration.second)
                    start_time = datetime.strptime(line_element[2], "%H:%M:%S")
                    end_time = start_time + delta

                    first_line_element = line_element
                    i = i + 1
                    line_element = file2[i].split()
                    while (line_element[10] == "smurf"):
                        duration_new = datetime.strptime(
                            line_element[3], "%H:%M:%S")
                        delta_new = timedelta(
                            hours=duration_new.hour, minutes=duration_new.minute, seconds=duration_new.second)
                        start_time_new = datetime.strptime(
                            line_element[2], "%H:%M:%S")
                        end_time_new = start_time_new + delta_new
                        # print(end_time_new)

                        if (end_time_new > end_time):
                            end_time = end_time_new

                        i = i + 1
                        line_element = file2[i].split()

                    first_line_element.insert(0, week)
                    first_line_element.insert(1, day)
                    end_time_str = (end_time.strftime("%H:%M:%S"))
                    first_line_element.insert(5, end_time_str)
                    del first_line_element[2]
                    del first_line_element[5:12]
                    i = i - 1
                    writer.writerow(first_line_element)

            if (line_element[10] == "syslog"):
                    duration = datetime.strptime(line_element[3], "%H:%M:%S")
                    delta = timedelta(
                        hours=duration.hour, minutes=duration.minute, seconds=duration.second)
                    start_time = datetime.strptime(line_element[2], "%H:%M:%S")
                    end_time = start_time + delta

                    first_line_element = line_element
                    i = i + 1
                    line_element = file2[i].split()
                    while (line_element[10] == "syslog"):
                        duration_new = datetime.strptime(
                            line_element[3], "%H:%M:%S")
                        delta_new = timedelta(
                            hours=duration_new.hour, minutes=duration_new.minute, seconds=duration_new.second)
                        start_time_new = datetime.strptime(
                            line_element[2], "%H:%M:%S")
                        end_time_new = start_time_new + delta_new
                        # print(end_time_new)

                        if (end_time_new > end_time):
                            end_time = end_time_new

                        i = i + 1
                        line_element = file2[i].split()

                    first_line_element.insert(0, week)
                    first_line_element.insert(1, day)
                    end_time_str = (end_time.strftime("%H:%M:%S"))
                    first_line_element.insert(5, end_time_str)
                    del first_line_element[2]
                    del first_line_element[5:12]
                    i = i - 1
                    writer.writerow(first_line_element)

            if (line_element[10] == "teardrop"):
                    duration = datetime.strptime(line_element[3], "%H:%M:%S")
                    delta = timedelta(
                        hours=duration.hour, minutes=duration.minute, seconds=duration.second)
                    start_time = datetime.strptime(line_element[2], "%H:%M:%S")
                    end_time = start_time + delta

                    first_line_element = line_element
                    i = i + 1
                    line_element = file2[i].split()
                    while (line_element[10] == "teardrop"):
                        duration_new = datetime.strptime(
                            line_element[3], "%H:%M:%S")
                        delta_new = timedelta(
                            hours=duration_new.hour, minutes=duration_new.minute, seconds=duration_new.second)
                        start_time_new = datetime.strptime(
                            line_element[2], "%H:%M:%S")
                        end_time_new = start_time_new + delta_new
                        # print(end_time_new)

                        if (end_time_new > end_time):
                            end_time = end_time_new

                        i = i + 1
                        line_element = file2[i].split()

                    first_line_element.insert(0, week)
                    first_line_element.insert(1, day)
                    end_time_str = (end_time.strftime("%H:%M:%S"))
                    first_line_element.insert(5, end_time_str)
                    del first_line_element[2]
                    del first_line_element[5:12]
                    i = i - 1
                    writer.writerow(first_line_element)

        # writer.writerow(first_line_element)

            # print(line_element[2])
        i = i + 1

if __name__ == "__main__":
    main()
