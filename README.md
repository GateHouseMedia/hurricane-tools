# Hurricane Tools
This is a collection of simple tools for tracking and reporting on 
hurricanes, released by GateHouse Media LLC. The **getspaghetti** 
program is intended to be run as a cron job/scheduled task long before 
you think you might need it.
## Installation
Clone or download the repo. With a functioning Python 3, use *pip 
install -r requirements.txt* or whatever your toolchain requires. No 
specific versions are required, and dependencies are quite limited.
## Files
**getspaghetti.py** -- Fetch and save KML and GIF versions of hurricane 
spaghetti model plots from the [South Florida Water Management 
District](https://apps.sfwmd.gov/sfwmd/common/images/weather/plots.html). 
Some configuration may be required at the top of the file. 
**getspaghetti.sh** is a sample program that makes it easier to call 
from a cron job; you'll want to configure the path to these program 
files and possibly the path to your Python 3 installation, particularly 
for Mac users. **windprobabilitynames.py** is just a way to prettify the 
names the National Weather Service kicks out in its wind probability 
forecasts. Setting the prettified name to "badstuff" will drop the entry 
entirely. When new locations are added to the forecasts, you'll want to 
add them to this file. Pull requests gratefully accepted, as this is 
missing all entries for Gulf of Mexico and Pacific storms. 
**windprobabilities.py** is a stupidly simple tool to scrape National 
Weather Service wind probability forecasts and turn them into something 
vaguely English. Configure at the top of the file to set your current 
storm's wind probability forecast URL and the output filename. What does 
it do? It generates stuff like this:
> West Palm Beach, Fla.: 95% chance of 39+ mph; 74% chance of 57+ mph; 
> 53% chance of 74+ mph
from this ungodly mess, with all-caps fractional location names, wind 
speeds in knots, and the most important number at the very end a large 
set of numbers:
> W PALM BEACH 34 X X( X) 1( 1) 5( 6) 62(68) 22(90) 5(95) W PALM BEACH 
> 50 X X( X) X( X) X( X) 32(32) 33(65) 9(74) W PALM BEACH 64 X X( X) X( 
> X) X( X) 13(13) 30(43) 10(53)
**animatedorian.sh* -- Another simple example that stacks GIFs saved by *getspaghetti* into an animated GIF. You'd need the common tool [ImageMagick](https://imagemagick.org/) for the actual processing. See the code for examples on how to build your own.
