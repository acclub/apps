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
    ac.setTitle(appWindow, "")
    ac.setIconPosition(appWindow, 0, -10000)
    ac.setSize(appWindow, 100, 50)
    ac.drawBorder(appWindow, 0)

    someLabel = ac.addLabel(appWindow, "")
    ac.setPosition(someLabel, 10, 5)

def acUpdate(delta_t):
    global someLabel
    ac.setBackgroundOpacity(appWindow, 0)
    rpm = ac.getCarState(0, acsys.CS.RPM)
    ac.setText(someLabel, str(round(rpm)))

