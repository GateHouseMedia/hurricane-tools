import requests
from pyquery import PyQuery as pq

import subprocess
import datetime
import os

hosturl = "https://my.sfwmd.gov/sfwmd/common/images/weather/plots.html"
urlpre = "https://my.sfwmd.gov/sfwmd/common/images/weather/"
datadir = "data/"

os.makedirs(datadir, exist_ok=True)

now = datetime.datetime.now()
stamp = datetime.datetime.strftime(now, "%Y%m%d_%H%M")

r = requests.get(hosturl)

html = pq(r.content)

links = pq(html)("a")

for link in links:
    target = pq(link).attr("href")
    if target[-3:] in ("kml", "gif") and "autoupdate" not in target:
        filename = target.replace("plots/storm_", "plots/storm")
        filename = filename.replace("plots/", "")
        parts = filename.split(".")
        filename = f"{datadir}{parts[0]}_{stamp}.{parts[1]}"
        target = urlpre + target
        with open(filename, "wb") as f:
            try:
                print(f"Saving {target} to {filename}")
                f.write(requests.get(target).content)
            except:
                print(f"Failed to fetch {target} to {filename}")
# subprocess.check_call(["animate.bat"])
