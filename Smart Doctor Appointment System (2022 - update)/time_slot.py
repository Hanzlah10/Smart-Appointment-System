timeSlot = []


def setSlot(start_hour, end_minute, end_hour, end_hour_minute):
    # odd numbers are start time
    # even numbers are end time

    if start_hour > 12:
        start_hour -= 12
        timeSlot.append([start_hour, int(end_minute)])
    else:
        timeSlot.append([start_hour, int(end_minute)])

    if end_hour > 12:
        end_hour -= 12
        timeSlot.append([end_hour, int(end_hour_minute)])
    else:
        timeSlot.append([end_hour, int(end_hour_minute)])


def calculateSlot(hour, count, i, start, end, diff):
    if count == 0:
        if diff - count == 1:
            setSlot(hour + count, start[3:5], hour + i, end[3:5])
        else:
            setSlot(hour, start[3:5], hour + i, end[3:5])
    else:
        if diff - count == 1:
            setSlot(hour, start[3:5], hour, end[3:5])
        else:
            setSlot(hour + count, start[3:5], hour + i, end[3:5])


def init_time_slot(start, end):
    if start is None and end is None:
        return 0

    if start[-2:] == "PM":
        start_convert_to_int = int(start[:2]) + 12
    else:
        start_convert_to_int = int(start[:2])

    if end[-2:] == "PM":
        end_convert_to_int = int(end[:2]) + 12 + 1
    else:
        end_convert_to_int = int(end[:2]) + 1

    # add_minute = int(start[3:5]) + int(end[3:5])
    diff = end_convert_to_int - start_convert_to_int

    # if add_minute >= 60:
    #     diff += 1

    count = 0

    for i in range(1, diff):
        calculateSlot(start_convert_to_int, count, i, start, end, diff)
        count += 1


def getSlot():
    return timeSlot


init_time_slot("12:00 PM", "01:00 PM")
print(getSlot())
