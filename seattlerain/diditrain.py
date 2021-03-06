#!/usr/bin/python3

##
## Print percent of days with recorded rainfall, using CSV file
## Author: Aiden Woodruff <aiden.woodruff@gmail.com>
##

import csv

total = 0
totalyes = 0
totalno = 0
totalna = 0

with open('seattleWeather_1948-2017.csv', 'r', newline='') as seattlefile:
  seattleread = csv.DictReader(seattlefile)
  for row in seattleread:
    total += 1
    if (row['RAIN'] == "TRUE"):
      totalyes += 1
    elif (row['RAIN'] == "NA"):
      totalna += 1
    else:
      totalno += 1
print("Rained " + str(totalyes) + " out of " + str(total) + " days. (" + format(totalyes/total*100, '.2f') + "% and " + str(totalna) + "NAs)")
