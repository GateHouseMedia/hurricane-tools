# Removes older hurricane tracks

import datetime
from glob import glob
import os

datemargin = 21    # Leave at least 21 days behind on server
datadir = "data/"

earliestdate = (datetime.datetime.now() - datetime.timedelta(days=datemargin + 1))
print(f"Will purge files from before {earliestdate.strftime('%Y%m%d')}")

filenames = glob(datadir + "*")
filestopurge = []
for filename in filenames:
    if os.path.isfile(filename):     # Exclude any directories
        fileepochtime = os.path.getmtime(filename)
        filedatetime = datetime.fromtimestamp(fileepochtime)
        if filedatetime < earliestdate:
            filestopurge.append(filename)
print(f"{len(filestopurge):,} files to be purged")

for filetopurge in filestopurge:
    try:
        os.remove(filetopurge)
    except:
        print(f"Failed to remove {filetopurge}")

