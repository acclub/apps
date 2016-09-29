try:
    import ac
    import acsys
except ImportError:
    pass

# stdlib, SimInfo
import sys
import os
import os.path
import platform
if platform.architecture()[0] == "64bit":
    sysdir=os.path.dirname(__file__)+'/stdlib64'
else:
    sysdir=os.path.dirname(__file__)+'/stdlib'
sys.path.insert(0, sysdir)
os.environ['PATH'] = os.environ['PATH'] + ";."
from third_party.sim_info import SimInfo

rpm_app = 0
toe_app = 0
rpm_label = 0
toe_label = 0
simInfo = SimInfo()

def createApp(label):
    app = ac.newApp(label)
    ac.setTitle(app, "")
    ac.setIconPosition(app, 0, -10000)
    ac.setSize(app, 100, 50)
    ac.drawBorder(app, 0)

    label = ac.addLabel(app, "")
    ac.setPosition(label, 10, 5)
    return app, label

def acMain(ac_version):
    global rpm_app, rpm_label, toe_app, toe_label
    rpm_app, rpm_label = createApp("RPM Viewer")
    toe_app, toe_label = createApp("Toe In")

# AccG, Aero,  BestLap, Brake, CamberDeg, CamberRad, Caster, CGHeight, Clutch, 
# CurrentTyresCoreTemp, DriftBestLap, DriftLastLap, DriftPoints, DriveTrainSpeed, 
# DY, DynamicPressure, Gas, Gear, InstantDrift, IsDriftInvalid, IsEngineLimiterOn, 
# LapCount, LapInvalidated, LapTime, LastFF, LastLap, LastTyresTemp, Load, 
# LocalAngularVelocity, LocalVelocity, Mz, NdSlip, NormalizedSplinePosition, 
# PerformanceMeter, RideHeight, RPM, SlipAngle, SlipAngleContactPatch, SlipRatio,
# SpeedKMH, SpeedMPH, SpeedMS, SpeedTotal, Steer, SuspensionTravel, ToeInDeg,
# TurboBoost, TyreContactNormal, TyreContactPoint, TyreDirtyLevel,
# TyreHeadingVector, TyreLoadedRadius, TyreRadius, TyreRightVector, TyreSlip,
# TyreSurfaceDef, TyreVelocity, Velocity, WheelAngularSpeed, WorldPosition

prev_fl = list()
prev_fr = list()
prev_rl = list()
prev_rr = list()

limit = 300

def toeP(l, v):
    l.append(v)
    if len(l) > limit: del l[0]

def toeSl(l, v):
    return str(round(v, 2)) + "\t(" + str(round(min(l), 2)) + ")"

def toeSr(l, v):
    return str(round(v, 2)) + "\t(" + str(round(max(l), 2)) + ")"

def acUpdate(delta_t):
    ac.setBackgroundOpacity(toe_app, 0)
    ac.setBackgroundOpacity(rpm_app, 0)

    rpm = ac.getCarState(0, acsys.CS.RPM)
    boost = ac.getCarState(0, acsys.CS.TurboBoost)
    fuel = simInfo.physics.fuel
    ac.setText(rpm_label, str(round(rpm)) + "\n" + str(round(boost, 3)) + "\n" + str(round(fuel, 1)))

    value_fl = ac.getCarState(0, acsys.CS.ToeInDeg, acsys.WHEELS.FL)
    value_fr = ac.getCarState(0, acsys.CS.ToeInDeg, acsys.WHEELS.FR)
    value_rl = ac.getCarState(0, acsys.CS.ToeInDeg, acsys.WHEELS.RL)
    value_rr = ac.getCarState(0, acsys.CS.ToeInDeg, acsys.WHEELS.RR)

    toeP(prev_fl, value_fl)
    toeP(prev_fr, value_fr)
    toeP(prev_rl, value_rl)
    toeP(prev_rr, value_rr)

    ac.setText(toe_label, toeSl(prev_fl, value_fl) + "\t" + toeSr(prev_fr, value_fr) + "\n" + toeSl(prev_rl, value_rl) + "\t" + toeSr(prev_rr, value_rr))
