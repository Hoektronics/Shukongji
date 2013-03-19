import math

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
    self.home(z=True)
    self.home(x=True, y=True)

  def end(self):
    self.spindleOff()
    self.vacuumOff()
    self.coolantOff()
    self.ledColor(0, 0, 255)
    self.beep(600, 1000)
    self.home(z=True)
    self.home(x=True, y=True)
    self.motorsOff()

  def spindleOn(self):
    self.output("M3 (Spindle On)")

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
  
  #configuration
  xmin = 0
  xmax = 160
  ymin = 0
  ymax = 180
  toolsize = 6
  pathsize = toolsize - 1.5
  moveFeedrate = 1000
  plungeFeedrate = 500
  millFeedrate = 1000
  surfaceDepth = -0.2
  
  #initialize
  cnc = CNCMachine()
  cnc.start()
  cnc.setPosition(xmax+0.5, -0.5, 55.5) #we home to xmax, ymin, zmax w/ 0.5mm of clearance.
  cnc.goto(x=0, y=0, feedrate=moveFeedrate)
  cnc.motorsOff()
  cnc.confirm("Adjust bit to +10mm")
  cnc.setPosition(0, 0, 10)
  cnc.spindleOn()
  cnc.goto(x=0, y=0, z=surfaceDepth, feedrate=plungeFeedrate)
  cnc.goto(x=0, y=ymax, z=surfaceDepth, feedrate=millFeedrate)
  cnc.goto(x=xmax, y=ymax, z=surfaceDepth, feedrate=millFeedrate)
  cnc.goto(x=xmax, y=0, z=surfaceDepth, feedrate=millFeedrate)

  #surface milling
  for y in range(0, int(math.ceil(ymax/pathsize))):
    ypos = y * pathsize
    cnc.goto(y=ypos, feedrate=millFeedrate)
    if cnc.x == xmin:
      cnc.goto(x = xmax, y = ypos, feedrate=millFeedrate)
    else:
      cnc.goto(x = xmin, y = ypos, feedrate=millFeedrate)
  
  #we're done!
  cnc.end()