# #######################################################
#
#    OV1 Racing - Info app (OV1info)
#  	 version 4.1
#
#    Brought to you by [Rivali]
#    http://rivalitempo-softgrip.rhcloud.com
#
#    Author:
#	 GooglePlus: http://google.com/+OvidiuBarabula
#    OV1 Racing GooglePlus: http://goo.gl/thWc9c
#    OV1 Racing YouTube: http://goo.gl/o6Zsge
#
#    ---
#
#    Thanks to @Rombik for his "SimInfo" wonder class!
#    Thanks to @softgrip for his guidance!
#
# #######################################################


# imports
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

from app.app import App
import ac


ov1_info = 0

#-#####################################################################################################################################-#


def acMain(ac_version):
	try:
		global ov1_info
		# initialize the app
		ov1_info = App()
		# create the app objects
		ov1_info.start_up()
		# add render callback
		ov1_info.window.onRenderCallback(onFormRender)
		# return the app's ID
		return "OV1Info"
	
	except Exception as e:
		ac.console("OV1: Error in function acMain(): %s" % e)
		ac.log("OV1: Error in function acMain(): %s" % e)


#-#####################################################################################################################################-#


def acUpdate(deltaT):
	try:
		global ov1_info
		# init the app updates
		ov1_info.on_update(deltaT)
		
	except Exception as e:
		ac.console("OV1: Error in function acUpate(): %s" % e)
		ac.log("OV1: Error in function acUpate(): %s" % e)


#-#####################################################################################################################################-#


def onFormRender(deltaT):
	try:
		global ov1_info
		# init on_render function
		ov1_info.on_render()

	except Exception as e:
		ac.console("OV1: Error in function onFormRender(): %s" % e)
		ac.log("OV1: Error in function onFormRender(): %s" % e)


#-#####################################################################################################################################-#


def acShutdown():
	try:
		global ov1_info
		# init on_render function
		ov1_info.on_shutdown()

	except Exception as e:
		ac.console("OV1: Error in function acShutdown(): %s" % e)
		ac.log("OV1: Error in function acShutdown(): %s" % e)

