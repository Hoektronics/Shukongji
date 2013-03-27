import math
import argparse

def main():
  parser = argparse.ArgumentParser(description='Surfacing Script')
  parser.add_argument('-x','--xmax', help='Maximum available X area in millimeters', required=False, default=180)
  parser.add_argument('-y','--ymax', help='Maximum available Y area in millimeters', required=False, default=190)
  parser.add_argument('-t','--toolsize', help='Diameter of the tool in millimeters', required=False, default=4)
  parser.add_argument('-m','--millrate', help='Milling feedrate in mm/min', required=False, default=800)
  parser.add_argument('-p','--plungerate', help='Plunge feedreate in mm/min', required=False, default=500)
  parser.add_argument('-r','--rpm', help='Milling tool RPM', required=False, default=5000)
  parser.add_argument('-d','--depth', help='Depth in millimeters', required=False, default=0.25)
  parser.add_argument('-i','--increment', help='Increment in millimeters', required=False, default=0.25)
  parser.add_argument('--home', help='Home or not home', required=False, default=False)
  parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')

  results = parser.parse_args()
  
  #configuration
  xmin = 0
  xmax = float(results.xmax)
  ymin = 0
  ymax = float(results.ymax)
  toolsize = float(results.toolsize)
  rpm = float(results.rpm)
  pathsize = toolsize - 1.0
  millFeedrate = float(results.millrate)
  plungeFeedrate = float(results.plungerate)
  surfaceDepth = math.fabs(float(results.depth))
  increment = math.fabs(float(results.increment))
  
  #initialize
  cnc = CNCMachine()
  cnc.start()
  if results.home:
    cnc.home(z=True)
    cnc.home(x=True, y=True)
    cnc.setPosition(xmax+0.5, -0.5, 55.5) #we home to xmax, ymin, zmax w/ 0.5mm of clearance.
    cnc.goto(x=0, y=0, feedrate=0) #max speed move
  else:
    cnc.setPosition(0,0,0) #start at 0,0,0
    
  cnc.motorsOff()
  cnc.confirm("Adjust bit to +6mm")
  cnc.setPosition(0, 0, 6)
  cnc.spindleOn(rpm)


  #do it multiple times
  for z in range(int(math.floor(surfaceDepth / increment))):
    #how deep this pass?
    depth = -increment * (z+1)

    #mill a big square
    cnc.goto(x=0, y=0, z=depth, feedrate=plungeFeedrate)
    cnc.goto(x=0, y=ymax, feedrate=millFeedrate)
    cnc.goto(x=xmax, y=ymax, feedrate=millFeedrate)
    cnc.goto(x=xmax, y=0, feedrate=millFeedrate)

    #surface milling
    for y in range(0, int(math.ceil(ymax/pathsize))):
      ypos = y * pathsize
      cnc.goto(y=ypos, feedrate=millFeedrate)
      if cnc.x == xmin:
        cnc.goto(x = xmax, y = ypos, feedrate=millFeedrate)
      else:
        cnc.goto(x = xmin, y = ypos, feedrate=millFeedrate)

    #back to our origin, safely
    cnc.goto(z=6, feedrate=0)
    cnc.goto(x=0, y=0, feedrate=0)
  
  #we're done!
  cnc.end()

class Endmill():
  def __init__(self, width):
    self.width = width

class Machine():
  
  def __init__(self):
    self.x = 0;
    self.y = 0;
    self.z = 0;
    self.feedrate = 0;
    
  def goto(self, x=None, y=None, z=None, feedrate=None):
    if feedrate is not None:
      self.feedrate = feedrate;
    if x is not None:
      self.x = x
    if y is not None:
      self.y = y
    if z is not None:
      self.z = z

    if feedrate <= 0:
      str = "G0 X%0.4f Y%0.4f Z%0.4f" % (self.x, self.y, self.z)
    else:
      str = "G1 X%0.4f Y%0.4f Z%0.4f F%0.4f" % (self.x, self.y, self.z, self.feedrate)

    self.output(str);
  
  def wait(self, time):
    str = "G4 S%0.4f" % time
    self.output(str);
  
  def home(self, x=None, y=None, z=None):
    str = "G28 "
    if x is not None:
      str += "X"
    if y is not None:
      str += "Y"
    if z is not None:
      str += "Z"
    
    self.output(str)
  
  def setPosition(self, x=None, y=None, z=None):
    if x is not None:
      self.x = x;
    if y is not None:
      self.y = y;
    if z is not None:
      self.z = z;
      
    str = "G92 X%0.4f Y%0.4f Z%0.4f" % (self.x, self.y, self.z)
    self.output(str)
    
  def confirm(self, message):
    str = "M1 (%s)" % message
    self.output(str)

  def motorsOn(self):
    self.output("M17 (Motors On)")

  def motorsOff(self):
    self.output("M18 (Motors Off)")

  def beep(self, frequency, duration):
    self.output("M300 S%d P%d" % (frequency, duration))

  def ledColor(self, red, green, blue):
    self.output("M420 R%d E%d B%d" % (red, green, blue))
    
  def output(self, str):
    print str;
    
class CNCMachine(Machine):
  def start(self):
    self.ledColor(255, 255, 255)

  def end(self):
    self.spindleOff()
    self.vacuumOff()
    self.coolantOff()
    self.ledColor(0, 0, 255)
    self.beep(600, 1000)
    self.motorsOff()

  def spindleOn(self, rpm):
    self.output("M3 S%s (Spindle On)" % rpm)

  def spindleOff(self):
    self.output("M5 (Spindle Off)")

  def coolantOn(self):
    self.output("M7 (Coolant On)")

  def coolantOff(self):
    self.output("M9 (Coolant Off)")

  def vacuumOn(self):
    self.output("M10 (Vacuum On)")

  def vacuumOff(self):
    self.output("M11 (Vacuum Off)")
        
if __name__ == '__main__':
  main()