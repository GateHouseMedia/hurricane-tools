import requests
from pyquery import PyQuery as pq

import windprobabilitynames   # Local file

import re
import datetime

# Configure these. hosturl is direct to the NHC wind probability page for
# your storm. targetfilename is where you want the output to go.

hosturl = "https://www.nhc.noaa.gov/text/refresh/MIAPWSAT5+shtml/281506.shtml"
# targetfilename = "/var/www/html/misc/dorian/windprobability.txt"
targetfilename = "windprobability.txt"

# You shouldn't need to mess with these:
separator = "\r\n"
tab = "    "
divider = "LOCATION       KT"
ender = "$$"

namedict = windprobabilitynames.namedict

r = requests.get(hosturl)
html = r.content
holder = pq(html)("pre").html().split("\n")

mytime = datetime.datetime.now().strftime("%I:%M %p on %A, %b %d")
output = f"File checked at {mytime} at {hosturl}{separator}"
simpletimestamp = None
for row in holder:
    if " UTC " in row:
        if "0900 UTC" in row or "1000 UTC" in row:
            simpletimestamp = f"5 a.m. windspeed forecast{separator}"
        if "1500 UTC" in row or "1600 UTC" in row:
            simpletimestamp = f"11 a.m. windspeed forecast{separator}"
        if "2100 UTC" in row or "2200 UTC" in row:
            simpletimestamp = f"5 p.m. windspeed forecast{separator}"
        if "0300 UTC" in row or "0400 UTC" in row:
            simpletimestamp = f"11 p.m. windspeed forecast{separator}"
        else:
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

with open(targetfilename, "w", newline="") as f:
    f.write(output)

if len(unknowncities) > 0:
    print("\r\n".join(set(unknowncities)))
