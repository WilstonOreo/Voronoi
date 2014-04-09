#!/usr/bin/env python

from __future__ import print_function

import os, sys

if len(sys.argv) != 5:
  print("Call: python stitch PATH/TO/IMAGES width height OUTPUT.png")
  exit()

path = sys.argv[1]
width = int(sys.argv[2])
height = int(sys.argv[3])
output = sys.argv[4]
directions = ["NORTH","WEST","SOUTH","EAST","UP","DOWN"]

images = dict()
count = dict()

for element in directions:
  images[element] = []
  count[element] = 0

files = os.listdir(path)
files.sort()
numbers = set()

for f in files:
  tokens = f.split("_")
  if len(tokens) != 2: continue
  direction = tokens[0]
  if not direction in images: continue

  images[direction].append(tokens[1])
  count[direction] += 1
  numbers.add(tokens[1])

for key1 in count:
  for key2 in count:
    if count[key1] != count[key2]: 
      print("File number is not matching!")
      exit()

numberList = list(numbers)
numberList.sort()

for number in numberList:
  print("Stitching file '%s'..." % (output+"_"+number))
  c = "montage "
  for direction in directions:
    c += os.path.join(path,direction + "_" + number) + " "
  c += " -tile 6x1 -geometry %dx%d " % (width,height)
  c += output + "_" + number
  os.system(c)

