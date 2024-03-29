import requests
from pyquery import PyQuery as pq
import pytz

import windprobabilitynames   # Local file

import re
import datetime

# Configure these. hosturl is direct to the NHC wind probability page for
# your storm. targetfilename is where you want the output to go.

# hosturl = "https://www.nhc.noaa.gov/text/refresh/MIAPWSAT5+shtml/281506.shtml"
#hosturl = "https://www.nhc.noaa.gov/text/refresh/MIAPWSAT1+shtml/171457.shtml"
# hosturl = "https://www.nhc.noaa.gov/text/refresh/MIAPWSAT3+shtml/030844.shtml"
# hosturl = "https://www.nhc.noaa.gov/text/refresh/MIAPWSAT3+shtml/200900.shtml"
#hosturl = "https://www.nhc.noaa.gov/text/refresh/MIAPWSAT3+shtml/212050.shtml?"
# hosturl = "https://www.nhc.noaa.gov/text/refresh/MIAPWSAT4+shtml/141451.shtml?"
#hosturl = "https://www.nhc.noaa.gov/text/refresh/MIAPWSAT1+shtml/050849.shtml?"
#hosturl = "https://www.nhc.noaa.gov/text/refresh/MIAPWSAT1+shtml/051452.shtml?"
#hosturl = "https://www.nhc.noaa.gov/text/refresh/MIAPWSAT3+shtml/260852.shtml?" 
# hosturl = "https://www.nhc.noaa.gov/text/refresh/MIAPWSAT4+shtml/022050.shtml?"
#hosturl = "https://www.nhc.noaa.gov/text/refresh/MIAPWSAT5+shtml/011448.shtml"
# hosturl = "https://www.nhc.noaa.gov/text/refresh/MIAPWSAT3+shtml/200858.shtml?"
# hosturl = "https://www.nhc.noaa.gov/text/refresh/MIAPWSAT4+shtml/261445.shtml?"
# hosturl = "https://www.nhc.noaa.gov/text/refresh/MIAPWSAT4+shtml/230855.shtml?"
# hosturl = "https://www.nhc.noaa.gov/text/refresh/MIAPWSAT2+shtml/070900.shtml?"
hosturl = "https://www.nhc.noaa.gov/text/refresh/MIAPWSEP4+shtml/190847.shtml?" # Pacific Hilary

#targetfilename = "/var/www/html/misc/201910storm/windprobability.txt"
#targetfilename = "/var/www/html/misc/20200729-isaias/windprobability.txt"
#targetfilename = "/var/www/html/misc/20200914-sally/windprobability.txt"
#targetfilename = "/var/www/html/misc/20201005-delta/windprobability.txt"
#targetfilename = "/var/www/html/misc/20201026-zeta/windprobability.txt"
# targetfilename = "/var/www/html/misc/20210701-elsa/windprobability.txt"
# targetfilename = "/var/www/html/misc/20210820-henri/windprobability.txt"
#targetfilename = "/var/www/html/misc/20210826-ida/windprobability.txt"
#targetfilename = "/var/www/html/misc/20220923-al092022/windprobability.txt"
targetfilename = "test/20230819-hilary-windprobability.txt"


# targetfilename = "windprobability.txt"                # If you want to save the file locally

# You shouldn't need to mess with these:
separator = "\r\n"
tab = "    "
divider = "LOCATION       KT"
ender = "$$"
mysplitter = "----" + separator

namedict = windprobabilitynames.namedict

r = requests.get(hosturl)
html = r.content
holder = pq(html)("pre").html().split("\n")

mytime = datetime.datetime.now().strftime("%I:%M %p on %A, %b %d")
output = f"File checked at {mytime} Eastern at {hosturl}{separator}"
simpletimestamp = None



for row in holder:
    if " UTC " in row:
        try:
            row = row.strip()       # Lose whitespace
            utc = pytz.utc
            eastern = pytz.timezone('US/Eastern')
            sourcedate = utc.localize(datetime.datetime.strptime(row, "%H%M UTC %a %b %d %Y")).astimezone(eastern)
            simpletimestamp = sourcedate.strftime("%I %p").replace("AM", "a.m.").replace("PM", "p.m.")
            if simpletimestamp[0] == "0":
                simpletimestamp = simpletimestamp[1:]              # Strip off leading zeroes, as from 0500
            simpletimestamp += f" Eastern windspeed forecast{separator}"
        except:
            simpletimestamp = None
        if not simpletimestamp:
            timestamp = f"Forecast from {row.strip()}{separator}"

if not simpletimestamp:   # If we were able to unable to translate UTC
    for row in holder:
        if " Z TIME" in row:
            timestamp += f"{tab}{row.strip()}{separator}"
if simpletimestamp:   # If we have a local translation
    output += f"{separator}{simpletimestamp}{separator}{separator}"
else:
    output += f"{separator}{separator}{timestamp}{separator}{separator}"

output += "The National Hurricane Center is estimating the likelihood of powerful windspeeds at a number of locations. "
output += "Tropical storm speeds begin around 39 mph. 57 mph is an average tropical storm. 74 mph is a Category 1 hurricane."
output += separator
output += mysplitter


def sconvert(s):
    if s == "34":
        return("39")
    elif s == "50":
        return("57")
    elif s == "64":
        return("74")
    else:
        print(f"Something went weird with speed conversion on string {s}")


for i, row in enumerate(holder):
    if divider in row:
        break
rows = holder[i + 1:]    # Trim off header junk
for i, row in enumerate(rows):
    if ender in row:      # Trim off stuff after the end of the records
        break
rows = rows[:i]

running = ""
lastname = ""
unknowncities = []
for row in rows:
    if len(row.strip()) > 10:
        name = row[:14].strip()
        speed = row[14:17].strip()
        percentage = row[row.rfind("(")+1:].replace(")", "").strip()
        if name in namedict:
            name = namedict[name]
        else:
            # print(name)
            unknowncities.append(name)
        if name != "badstuff":
            if name != lastname:   # If we need to start a new row
                output += running + separator
                lastname = name
                running = f"{name}: {percentage}% chance of {sconvert(speed)}+ mph"
            else:
                running += f"; {percentage}% chance of {sconvert(speed)}+ mph"   # append to existing row
output += running + separator + separator    # Add the last line

with open(targetfilename, "w", encoding='utf-8', newline="") as f:
    f.write(output)

if len(unknowncities) > 0:
    print("\r\n".join(set(unknowncities)))

