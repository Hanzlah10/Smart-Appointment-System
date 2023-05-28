from datetime import datetime

timeSlot = []

timeSlot_1 = []


def convert24(str1):
    if str1[-2:] == "AM" and str1[:2] == "12":
        return "00" + str1[2:-2]
    elif str1[-2:] == "AM":
        return str1[:-2]
    elif str1[-2:] == "PM" and str1[:2] == "12":
        return str1[:-2]
    else:
        return str(int(str1[:2]) + 12) + str1[2:8]


def convert12(time):
    if int(time[0:2]) >= 12:
        time = time[0:5]+" PM"
        print(time)
        return time
    else:
        return time
    # d = datetime.strptime(time[0:5], "%H:%M")
    # return d.strftime("%I:%M %p")


def getHour(hour):
    return int(hour[0:2])


def getHourDifference(start_hour, end_hour):
    try:
        sh = str(start_hour[0:2])
        eh = str(end_hour[0:2])

        if eh > sh:
            sm = str(start_hour[3:5])
            em = str(end_hour[3:5])
            total_time = int(sm) + int(em)
            if total_time == 60:
                return abs(int(sh) - int(eh)) + 1
            else:
                return abs(int(sh) - int(eh))
        else:
            return 0
    except:
        print("Enter Valid input!")
        return 0


def convertToUseAbleTime(time):
    if time.index(":") == 1:
        return "0" + str(time[0]) + ":" + time[2:]
    else:
        return time


def init_slot_maker(start, end):
    start = convertToUseAbleTime(start)
    hour = start[0:2]
    minute = start[3:]

    end = convertToUseAbleTime(end)
    diff = getHourDifference(convert24(start), convert24(end))
    clearSlots()

    for i in range(0, diff + 1):
        if diff == i:
            timeSlot.append(end)
        else:
            final_time = str(int(hour) + i) + ":" + minute
            final_time = convertToUseAbleTime(final_time)
            timeSlot.append(convert12(final_time))


def init_slot_maker_1(start, end):
    start = convertToUseAbleTime(start)
    hour = start[0:2]
    minute = start[3:]

    end = convertToUseAbleTime(end)
    diff = getHourDifference(convert24(start), convert24(end))
    clearSlots_1()

    for i in range(0, diff + 1):
        if diff == i:
            timeSlot_1.append(end)
        else:
            final_time = str(int(hour) + i) + ":" + minute
            final_time = convertToUseAbleTime(final_time)
            timeSlot_1.append(convert12(final_time))



def getSlot():
    timeSlot.append("break")
    timeSlot.append("break")
    return timeSlot+timeSlot_1


def clearSlots():
    timeSlot.clear()

def clearSlots_1():
    timeSlot_1.clear()


def getHourDifferenceNumber(start, end):
    start = convertToUseAbleTime(start)
    end = convertToUseAbleTime(end)
    diff = getHourDifference(convert24(start), convert24(end)) - 1

    diffNumber = 0

    for i in range(0, diff + 1):
        diffNumber += 1

    return diffNumber
