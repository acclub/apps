try:
    import ac
    import acsys
except ImportError:
    pass

appWindow = 0
someLabel = 0

def acMain(ac_version):
    global appWindow, someLabel
    appWindow = ac.newApp("Rpm Viewer")
    ac.setSize(appWindow, 300, 60)
    ac.drawBorder(appWindow, 0)
    ac.setBackgroundOpacity(appWindow, 0)

    someLabel = ac.addLabel(appWindow, "")
    ac.setPosition(someLabel, 15, 20)

def acUpdate(delta_t):
    global someLabel
    rpm = ac.getCarState(0, acsys.CS.RPM)
    ac.setText(someLabel, str(rpm))

