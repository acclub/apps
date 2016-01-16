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

appWindow = 0
someLabel = 0
simInfo = SimInfo()

def acMain(ac_version):
    global appWindow, someLabel
    appWindow = ac.newApp("Rpm Viewer")
    ac.setTitle(appWindow, "")
    ac.setIconPosition(appWindow, 0, -10000)
    ac.setSize(appWindow, 100, 50)
    ac.drawBorder(appWindow, 0)

    someLabel = ac.addLabel(appWindow, "")
    ac.setPosition(someLabel, 10, 5)

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

def acUpdate(delta_t):
    global someLabel, simInfo
    ac.setBackgroundOpacity(appWindow, 0)
    rpm = ac.getCarState(0, acsys.CS.RPM)
    fuel = simInfo.physics.fuel
    ac.setText(someLabel, str(round(rpm)) + "\n" + str(round(fuel, 1)))



