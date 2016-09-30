##########
# settings:
##########

# size of that thing
width = 250
height = 250
arrowWidth = 3

# speedometer params
speedMaximum = 200
startingPoint = 30 # degress
limited = True

##########
# script:
##########

import ac, acsys
import math

halfWidth = width / 2
halfHeight = height / 2
halfArrowWidth = arrowWidth / 2

degRange = 360.0 - startingPoint * 2.0
radRange = degRange * math.pi / 180.0
radStartingPoint = startingPoint * math.pi / 180.0

appWindow = 0

def acMain(ac_version):
    global appWindow
    
    appWindow = ac.newApp("Analog Speedometer")
    ac.setTitle(appWindow, "")
    ac.setIconPosition(appWindow, 0, -10000)
    ac.setSize(appWindow, width, height)
    ac.drawBorder(appWindow, 0)

    ac.addRenderCallback(appWindow, drawNeedle)

def acUpdate(delta_t):
    ac.setBackgroundOpacity(appWindow, 0)

def drawNeedle(delta_t):
    speed = ac.getCarState(0, acsys.CS.SpeedKMH)
    if limited and speed > speedMaximum: speed = speedMaximum
    radValue = speed / speedMaximum * radRange + radStartingPoint

    dx = math.sin(radValue)
    dy = math.cos(radValue)
    tx = halfWidth - dx * halfWidth
    ty = halfHeight + dy * halfHeight
    ax = dx * halfArrowWidth
    ay = dy * halfArrowWidth

    ac.glColor4f(1.0, 0.2, 0.2, 0.8) # color
    ac.glBegin(acsys.GL.Quads)
    ac.glVertex2f(halfWidth + ay, halfHeight + ax)
    ac.glVertex2f(halfWidth - ay, halfHeight - ax)
    ac.glVertex2f(tx - ay, ty - ax)
    ac.glVertex2f(tx + ay, ty + ax)
    ac.glEnd()
