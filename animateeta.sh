# This requires ImageMagick.
# Storms can have multiple names.
# There can be several versions of the files.
# So Dorian started off as Invest99L, which was recorded as storm99.
# Then Dorian got recorded as storm05, with ensemble components and without.
# So to filter out the ensemble components, storm05_201* covers everything.
# But Dorian took forever to show up. Compositing at first just
# the every-hour files (*00.gif) cut the frame count and file size in half.
# And at some point we dropped the Invest99L stuff to focus only on the 
# stronger parts of the storm.

# A result: https://irma.palmbeachpost.com/misc/dorian/dorian-animated.gif


# So, the sample code to get you started: 

cd ~stucka/hurricane-tools
# /usr/bin/convert data/storm99_*00.gif data/storm05_201*00.gif /var/www/html/misc/dorian/dorian-animated.gif
#/usr/bin/convert -loop 0 data/storm98_201*00.gif data/storm19_201*00.gif /var/www/html/misc/20200914-sally/sally-animated.gif
# /usr/bin/convert -delay 15 -loop 0 data/storm29_202011*00.gif /var/www/html/misc/20201102-eta/eta-animated.gif
cp data/storm29_202011*00.gif staging-eta
rm staging-eta/storm29_20201101*
rm staging-eta/storm29_20201102*
rm staging-eta/storm29_20201103_0*
/usr/bin/convert -delay 15 -loop 0 staging-eta/*.gif /var/www/html/misc/20201102-eta/eta-animated.gif

