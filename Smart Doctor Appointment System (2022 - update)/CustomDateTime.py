# Python program to convert time
# from 12 hour to 24 hour format

from datetime import datetime


def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds)


# Function to convert the date format
def convert24(str1):
    str1 = str1[0:5]+":00 "+str1[6:8]
    # Checking if last two elements of time
    # is AM and first two elements are 12
    if str1[-2:] == "AM" and str1[:2] == "12":
        return "00" + str1[2:-2]

    # remove the AM
    elif str1[-2:] == "AM":
        return str1[:-2]

    # Checking if last two elements of time
    # is PM and first two elements are 12
    elif str1[-2:] == "PM" and str1[:2] == "12":
        return str1[:-2]

    else:

        # add 12 to hours and remove PM
        return str(int(str1[:2]) + 12) + str1[2:8]

    # Driver Code


#


def TimeDifference(start, end):
    fmt = '%H:%M:%S'
    tstamp1 = datetime.strptime(start, fmt)
    tstamp2 = datetime.strptime(end, fmt)

    td = tstamp2 - tstamp1

    return td


start_time = "01:00 PM"
end_time = "12:00 PM"

a = convert24(start_time)
