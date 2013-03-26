#!/usr/bin/env python

import argparse
import re
import math

def main():
  parser = argparse.ArgumentParser(description='GCode Tiler')
  parser.add_argument('-i','--input', help='GCode file to tile', required=True)
  parser.add_argument('-o','--output', help='Output GCode file', required=True)
  parser.add_argument('-x','--xmax', help='Maximum available X area in millimeters', required=True)
  parser.add_argument('-y','--ymax', help='Maximum available Y area in millimeters', required=True)
  parser.add_argument('--xgap', help='X axis gap between tiles in millimeters', required=False, default=5)
  parser.add_argument('--ygap', help='Y axis gap between tiles in millimeters', required=False, default=5)
  parser.add_argument('-r', '--rows', help='Number of rows (Y dimension) to make. Default = max', required=False, default=0)
  parser.add_argument('-c', '--cols', help='Number of columns (X dimension) to make.  Default = max', required=False, default=0)
  #parser.add_argument('-q', '--qty', help='Quantity of parts to tile.', default=0)
  parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')

  results = parser.parse_args()

  infile = open(results.input, 'r')
  outfile = open(results.output, 'w')
  
  xgap = float(results.xgap)
  ygap = float(results.ygap)
  bounds = find_minmax(infile)

  print "Part Min: %s" % bounds.min
  print "Part Max: %s" % bounds.max
  print "Part Delta: %s" % bounds.delta
  print "X Gap: %smm" % xgap
  print "Y Gap: %smm" % ygap
  print
  
  maxCols = math.floor(float(results.xmax) / (bounds.delta[0]+xgap))
  maxRows = math.floor(float(results.ymax) / (bounds.delta[1]+ygap))
  maxParts = maxCols * maxRows
  
  #how many rows?
  if (results.rows):
    rows = int(results.rows)
  else:
    rows = maxRows
  if (rows > maxRows):
    print "Rows is too big, defaulting to maxRows instead"
    rows = maxRows

  #how many cols?
  if (results.cols):
    cols = int(results.cols)
  else:
    cols = maxCols
  if (cols > maxCols):
    print "Cols is too big, defaulting to maxCols instead"
    cols = maxCols
  
  parts = rows * cols
    
  print "X Bed Size: %smm" % results.xmax
  print "Y Bed Size: %smm" % results.ymax
  print "Max Columns: %d" % maxCols
  print "Max Rows: %d" % maxRows 
  print "Max Parts: %d" % maxParts
  print "Actual Columns: %d" % cols
  print "Actual Rows: %d" % rows 
  print "Actual Parts: %d" % parts
  print    

  delta = bounds.delta
  delta[0] = delta[0]+xgap
  delta[1] = delta[1]+ygap
  
  if (rows > 0 and cols > 0):
    tile_files(infile, outfile, rows, cols, delta)
  else:
    print "Nothing to do!"

def tile_files(infile, outfile, rows, cols, delta):
  rows = int(rows)
  cols = int(cols)
  for y in range(rows):
    for x in range(cols):
      col = x+1
      row = y+1
      xoffset = delta[0]*x
      yoffset = delta[1]*y
      print "Writing Row %d, Column %d" % (row, col)

      outfile.write("(Tiler.py - Start Row %d, Col %d)\n" % (row, col))
      infile.seek(0)
      for line in infile:
        # if re.match('G(0|1)', line):        
        #   m = re.search("X([-+]?\d*\.\d+|\d+)", line)
        #   if m:
        #     oldVal = float(m.group(1))
        #     newVal = oldVal + xoffset
        #     line = re.sub("X([-+]?\d*\.\d+|\d+)", "X" + str(newVal), line)
        #   m = re.search("Y([-+]?\d*\.\d+|\d+)", line)
        #   if m:
        #     oldVal = float(m.group(1))
        #     newVal = oldVal + yoffset
        #     line = re.sub("Y([-+]?\d*\.\d+|\d+)", "Y" + str(newVal), line)
        outfile.write(line)
      outfile.write("(Tiler.py - End Row %d, Col %d)\n" % (row, col))
      
      #don't offset the last one.
      if not (col == cols and row == rows):
        outfile.write("G0 Z6 (Tiler - safe Z)\n")
        if x+1 == cols:
          outfile.write("G0 X%.4f Y%0.4f (Tiler - X return to 0)\n" % (-(delta[0]*(cols-1)), delta[1]))
        else:
          outfile.write("G0 X%.4f (Tiler - Increment X)\n" % delta[0])
        outfile.write("G0 Z0 (Tiler - Z=0)\n")
        outfile.write("G92 X0 Y0 Z0 (Tiler - Reset Origin)\n")

def find_minmax(source_file):
  
  bounds = Bounds()
  point = [0,0,0]
  
  move = re.compile('Processing input file')
  for line in source_file:
    if re.match("G[01]+", line):
      m = re.search("X([-+]?\d*\.\d+|\d+)", line)
      if m:
        point[0] = float(m.group(1))
      m = re.search("Y([-+]?\d*\.\d+|\d+)", line)
      if m:
        point[1] = float(m.group(1))
      m = re.search("Z([-+]?\d*\.\d+|\d+)", line)
      if m:
        point[2] = float(m.group(1))
      bounds.add(point)
  
  return bounds
      
class Bounds(object):

  def __init__(self):
    self.min = [0,0,0]
    self.max = [0,0,0]
    self.delta = [0,0,0]

  def add(self, point):
    for idx, val in enumerate(point):
      self.min[idx] = min(val, self.min[idx])
      self.max[idx] = max(val, self.max[idx])
      self.delta[idx] = self.max[idx] - self.min[idx]
      
if __name__ == '__main__':
  main()