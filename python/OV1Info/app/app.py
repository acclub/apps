from app.util import millisToString, C_to_F, L_to_Gal, PSI_to, rgb, hsv2rgb, rgb2hsv
from app.classes import Window, Label, Button, Config
from third_party.sim_info import SimInfo
import ac
import acsys

# general global variables
main_window  = 0
app_size     = { "w" : 212, "h" : 212 }
sim_info     = SimInfo()
tick_counter = 0

# additional window apps
laps_window = 0
race_window = 0
tyre_window = 0
fuel_window = 0
settings_window = 0

# app path and config file names
appPATH      = "apps/python/OV1Info/"
ini_carsInfo = "userdata/cars_info.ini"
ini_bestLap  = "userdata/best_lap.ini"
ini_userconf = "cfg/user_config.ini"

# configParser objects
cfg_carsInfo = 0
cfg_bestLap  = 0
cfg_userConf = 0

# car specific information
gear              = 0
speed             = 0
tachometer        = {"bg" : 0, "base" : 0, "steps" : 0, "shift" : 0}
rpms              = -1
max_rpms          = 0
signal_abs        = 0
signal_fuel       = 0
signal_limiter    = 0
driver_name       = 0
personalBest      = 0
my_race_position  = 0
prev_lap_count    = 0
units             = { "speed" : "kmh", "temp" : "C", "pressure" : "psi", "volume" : "L" }
car_name          = ac.getCarName(0)
track_name        = ac.getTrackName(0)
speed_units_label = 0


# lap time information
v_lastLap      = 0
v_bestLap      = 0
v_currLap      = 0
v_lapDelta     = 0
v_personalBest = 0
v_position     = 0
l_currLap      = 0
ac_bestLap     = 0

# car info
fuel_gauge       = 0
low_fuel         = 0
v_fuel           = 0
v_fuelEstimate   = 0
v_fuel_per_lap   = 0
ac_fuel          = 0
average_lap_fuel = 0
start_line_fuel  = -1
fuel_per_laps    = []
skipLap          = True
start_of_lap     = False

# wheel info
WHEELS = {
	"BG" : 0, 
	"FL" : {
		"dirt" : 0,
		"slip" : 0,
		"temp" : { "cold"  : 0, "value" : 0, "graph" : 0 },
		"pres" : { "label" : 0, "value" : 0	},
		"wear" : { "label" : 0, "value" : 0, "graph" : 0 }
	},
	"FR" : {
		"dirt" : 0,
		"slip" : 0,
		"temp" : { "cold"  : 0, "value" : 0, "graph" : 0 },
		"pres" : { "label" : 0, "value" : 0	},
		"wear" : { "label" : 0, "value" : 0, "graph" : 0 }
	},
	"RL" : {
		"dirt" : 0,
		"slip" : 0,
		"temp" : { "cold"  : 0, "value" : 0, "graph" : 0 },
		"pres" : { "label" : 0, "value" : 0	},
		"wear" : { "label" : 0, "value" : 0, "graph" : 0 }
	},
	"RR" : {
		"dirt" : 0,
		"slip" : 0,
		"temp" : { "cold"  : 0, "value" : 0, "graph" : 0 },
		"pres" : { "label" : 0, "value" : 0	},
		"wear" : { "label" : 0, "value" : 0, "graph" : 0 }
	},
	"coldRead" : False
}

# race info
drivers_list_labels = []
drivers_list_pos_labels = []
lap_count_label = { "label" : 0, "value" : 0 }
last_lap_label  = { "label" : 0, "value" : 0 }
race_flag = 0

# groups of labels
panels = { "left" : [], "right" : [], "fuel_info" : [], "laps_info" : [], "tyre_info" : [], "race_info" : [], "delta_meter" : [] }
colored_labels = []

# label position x, y
label_pos = { "x1" :  20, "x2" : 340, "x3" : 449, "y1" :  42, "y2" : 87, "y3" : 132, "y_offest" : 15 }

# delta meter
delta_meter     = 0
delta_meter_bg  = 0
delta_meter_max = -1
delta_meter_status = "on"
is_delta_meter_visible = True

# colors
label_color = 0
colors = {
	"white"      : [255, 255, 255],
	"yellow"     : [247, 183,   9],
	"green"      : [151, 229,  68],
	"red"        : [252,  35,  35]
}
bg_colors = {
	"white"      : [255, 255, 255],
	"green"      : [104, 217,  43],
	"yellow"     : [250, 242,  21],
	"red"        : [254,   4,   2],
	"cold_green" : [155, 194,   5]
}

#skin colors
user_skin = "red"
skins = {
	"red"    : [255,  80,  76],
	"orange" : [253, 139,  38],
	"green"  : [106, 206, 101],
	"cyan"   : [52 , 239, 228],
	"blue"   : [75 , 175, 239],
	"dark"   : [115, 115, 115]
}

# textures
textures_bg = {
	"left"   : appPATH + "images/background/base-left.png",
	"mid"    : appPATH + "images/background/base-middle.png",
	"right"  : appPATH + "images/background/base-right.png",
	"full"   : appPATH + "images/background/base-full.png",
	"wheels" : appPATH + "images/background/wheels-bg.png"
}

textures_tach = {
	"bg"    : "", # to be set after user settings are read
	"steps" : "", # to be set after car specs are available
	"shift" : appPATH + "images/tachometer/tachometer-shiftlight.png"
}

textures_gear = [
	appPATH + "images/gears/gear_r.png", #0
	appPATH + "images/gears/gear_n.png", #1
	appPATH + "images/gears/gear_1.png", #2
	appPATH + "images/gears/gear_2.png", #3
	appPATH + "images/gears/gear_3.png", #4
	appPATH + "images/gears/gear_4.png", #5
	appPATH + "images/gears/gear_5.png", #6
	appPATH + "images/gears/gear_6.png", #7
	appPATH + "images/gears/gear_7.png", #8
	appPATH + "images/gears/gear_8.png"  #9
]

textures_signals = [
	appPATH + "images/signal_lights/abs-on.png",     #0
	appPATH + "images/signal_lights/fuel-low.png",   #1
	appPATH + "images/signal_lights/fuel-empty.png", #2
	appPATH + "images/signal_lights/limiter-on.png"  #3
]

textures_delta_meter = [
	appPATH + "images/delta_meter/delta_meter_bg.png"
]

log = 0

class App:

	# INITIALIZATION
	
	def __init__(self):
		global appPATH, app_size, main_window, laps_window, race_window, tyre_window, fuel_window, settings_window
		# loading config files settings and data
		self.load_config()
		# creating the main app window
		main_window = Window(name="OV1Info", icon=False, width=app_size["w"], height=app_size["h"], texture=textures_bg["mid"])
		# extending the scope of the window variable
		# used to be able to access it from the main file
		self.window = main_window
		# adding the lap info window app
		laps_window = Window(name="OV1LapsInfo", icon=False, width=242, height=186, texture=appPATH+"images/background/panel-bg.png")
		# adding the tyre info window app
		tyre_window = Window(name="OV1TyreInfo", icon=False, width=242, height=186, texture=appPATH+"images/background/panel-bg.png")
		# adding the race window app
		race_window = Window(name="OV1RaceInfo", icon=False, width=242, height=186, texture=appPATH+"images/background/panel-bg.png")
		# adding the fuel window app
		fuel_window = Window(name="OV1FuelInfo", icon=False, width=121, height=186, texture=appPATH+"images/background/small-panel-bg.png")
		# adding the settings window app
		settings_window = Window(name="OV1InfoSettings", title="OV1 info - Settings", width=242, height=266, texture=appPATH+"images/background/settings-panel-bg.png")
	
	
	# PUBLIC METHODS
	
	#-#####################################################################################################################################-#
	
	def start_up(self):
		global appPATH, app_size, main_window, race_window, tyre_window, settings_window, laps_window
		global textures_bg, textures_tach, textures_delta_meter
		global tachometer, gear, speed, speed_units_label, signal_abs, signal_fuel, signal_limiter
		global is_delta_meter_visible, delta_meter, delta_meter_bg, delta_meter_status
		global personalBest, v_lastLap, v_bestLap, v_currLap, v_lapDelta, l_currLap, v_personalBest, v_position
		global panels, label_pos, colored_labels, bg_colors, label_color
		global units, v_fuel, v_fuelEstimate, v_fuel_per_lap, fuel_gauge
		global WHEELS, drivers_list_labels, lap_count_label, last_lap_label, race_flag
		global log
	
		# -- LABEL CUSTOMIZATION -- #########################################################################################################
		
		delta_meter         = Label(main_window.app)              .setSize(101, 16)
		delta_meter_bg      = Label(main_window.app)              .setSize(206, 18).setBgTexture(textures_delta_meter[0])
		tachometer["bg"]    = Label(main_window.app)              .setSize(212,212).setPos(0,    0).setBgTexture(textures_tach["bg"])
		tachometer["steps"] = Label(main_window.app)              .setSize(212,212).setPos(0,    0)
		tachometer["shift"] = Label(main_window.app)              .setSize(212,212).setPos(0,    0).setBgTexture(textures_tach["shift"])
		tachometer["base"]  = Label(main_window.app)              .setSize(174,174).setPos(19,  19)
		gear                = Label(main_window.app)              .setSize(46,  46).setPos(83,  59)
		speed               = Label(main_window.app, "---")       .setSize(60,  14).setPos(76, 107).setFontSize(18).setAlign("center")
		speed_units_label   = Label(main_window.app, "KM/H")      .setSize(60,  14).setPos(76, 129).setFontSize( 7).setAlign("center")
		signal_abs          = Label(main_window.app, "")          .setSize(38,  38).setPos(151,106).setBgTexture(textures_signals[0])
		signal_fuel         = Label(main_window.app, "")          .setSize(38,  38).setPos(135,134).setBgTexture(textures_signals[1])
		signal_limiter      = Label(main_window.app, "")          .setSize(38,  38).setPos(106,150).setBgTexture(textures_signals[3])
		
		
		# -- LAP INFO PANEL -- ###############################################################################################################
		
		l_position     = Label(laps_window.app, "Position:")      .setSize(95,  20).setPos(20, label_pos["y1"]).setFontSize(12).setAlign("left" ).setColor(label_color)
		l_personalBest = Label(laps_window.app, "Personal best:") .setSize(95,  20).setPos(20, label_pos["y2"]).setFontSize(12).setAlign("left" ).setColor(label_color)
		l_bestLap      = Label(laps_window.app, "Session best:")  .setSize(95,  20).setPos(20, label_pos["y3"]).setFontSize(12).setAlign("left" ).setColor(label_color)
		v_position     = Label(laps_window.app, "- / -")          .setSize(95,  32).setPos(20, label_pos["y1"] + label_pos["y_offest"]).setFontSize(17).setAlign("left" )
		v_personalBest = Label(laps_window.app, "--:--.---")      .setSize(95,  32).setPos(20, label_pos["y2"] + label_pos["y_offest"]).setFontSize(17).setAlign("left" )
		v_bestLap      = Label(laps_window.app, "--:--.---")      .setSize(95,  32).setPos(20, label_pos["y3"] + label_pos["y_offest"]).setFontSize(17).setAlign("left" )
		
		l_currLap      = Label(laps_window.app, "Current lap:")   .setSize(95,  20).setPos(128, label_pos["y1"]).setFontSize(12).setAlign("right").setColor(label_color)
		l_lapDelta     = Label(laps_window.app, "Session delta:") .setSize(95,  20).setPos(128, label_pos["y2"]).setFontSize(12).setAlign("right").setColor(label_color)
		l_lastLap      = Label(laps_window.app, "Last lap:")      .setSize(95,  20).setPos(128, label_pos["y3"]).setFontSize(12).setAlign("right").setColor(label_color)
		v_currLap      = Label(laps_window.app, "--:--.---")      .setSize(95,  32).setPos(128, label_pos["y1"] + label_pos["y_offest"]).setFontSize(17).setAlign("right")
		v_lapDelta     = Label(laps_window.app, "--.---")         .setSize(95,  32).setPos(128, label_pos["y2"] + label_pos["y_offest"]).setFontSize(17).setAlign("right")
		v_lastLap      = Label(laps_window.app, "--:--.---")      .setSize(95,  32).setPos(128, label_pos["y3"] + label_pos["y_offest"]).setFontSize(17).setAlign("right")
		
		fuel_gauge_bg  = Label(main_window.app)                   .setSize(174, 46).setPos(19,-20).setBgTexture(appPATH+"images/fuel/fuel_gauge_base.png")
		fuel_gauge     = Label(main_window.app)                   .setSize(174, 46).setPos(19,-20)
		l_fuel         = Label(fuel_window.app, "Fuel:")          .setSize(65,  20).setPos(label_pos["x1"], label_pos["y1"]).setFontSize(12).setColor(label_color)
		l_fuelEstimate = Label(fuel_window.app, "Laps left:")     .setSize(65,  20).setPos(label_pos["x1"], label_pos["y2"]).setFontSize(12).setColor(label_color)
		l_fuel_per_lap = Label(fuel_window.app, "Fuel/lap:")      .setSize(65,  20).setPos(label_pos["x1"], label_pos["y3"]).setFontSize(12).setColor(label_color)
		v_fuel         = Label(fuel_window.app, "-- L")           .setSize(65,  32).setPos(label_pos["x1"], label_pos["y1"] + label_pos["y_offest"]).setFontSize(14)
		v_fuelEstimate = Label(fuel_window.app, "-- laps")        .setSize(65,  32).setPos(label_pos["x1"], label_pos["y2"] + label_pos["y_offest"]).setFontSize(14)
		v_fuel_per_lap = Label(fuel_window.app, "-- L/lap")       .setSize(65,  32).setPos(label_pos["x1"], label_pos["y3"] + label_pos["y_offest"]).setFontSize(14)
		
		
		# -- TYRE INFO PANEL -- ##############################################################################################################
		
		# adding the tyre info labels
		
		WHEELS["BG"]                  = Label(tyre_window.app)       .setSize(222, 160).setPos(21,  26)      .setBgTexture(textures_bg["wheels"])
		WHEELS["FL"]["temp"]["value"] = Label(tyre_window.app, "--C").setSize( 26,  14).setPos(20, 43)       .setFontSize(12).setAlign("left")
		WHEELS["FR"]["temp"]["value"] = Label(tyre_window.app, "--C").setSize( 26,  14).setPos(20 + 176, 43) .setFontSize(12).setAlign("right")
		WHEELS["RL"]["temp"]["value"] = Label(tyre_window.app, "--C").setSize( 26,  14).setPos(20, 152)      .setFontSize(12).setAlign("left")
		WHEELS["RR"]["temp"]["value"] = Label(tyre_window.app, "--C").setSize( 26,  14).setPos(20 + 176, 152).setFontSize(12).setAlign("right")
		
		WHEELS["FL"]["wear"]["value"] = Label(tyre_window.app, "100%").setSize( 26,  14).setPos(20, 71)       .setFontSize(12).setAlign("left")
		WHEELS["FR"]["wear"]["value"] = Label(tyre_window.app, "100%").setSize( 26,  14).setPos(20 + 176, 71) .setFontSize(12).setAlign("right")
		WHEELS["RL"]["wear"]["value"] = Label(tyre_window.app, "100%").setSize( 26,  14).setPos(20, 112)      .setFontSize(12).setAlign("left")
		WHEELS["RR"]["wear"]["value"] = Label(tyre_window.app, "100%").setSize( 26,  14).setPos(20 + 176, 112).setFontSize(12).setAlign("right")
		
		WHEELS["FL"]["wear"]["label"] = Label(tyre_window.app, "LEFT").setSize( 26,  14).setPos(20, 86)      .setFontSize(8).setAlign("left") .setColor(label_color)
		WHEELS["FR"]["wear"]["label"] = Label(tyre_window.app, "LEFT").setSize( 26,  14).setPos(20 + 176, 86).setFontSize(8).setAlign("right").setColor(label_color)
		WHEELS["RL"]["wear"]["label"] = Label(tyre_window.app, "LEFT").setSize( 26,  14).setPos(20, 127)      .setFontSize(8).setAlign("left") .setColor(label_color)
		WHEELS["RR"]["wear"]["label"] = Label(tyre_window.app, "LEFT").setSize( 26,  14).setPos(20 + 176, 127).setFontSize(8).setAlign("right").setColor(label_color)
		
		WHEELS["FL"]["pres"]["value"] = Label(tyre_window.app, "--")  .setSize( 25,  14).setPos(20 +  72,  58).setFontSize(12).setAlign("center")
		WHEELS["FR"]["pres"]["value"] = Label(tyre_window.app, "--")  .setSize( 25,  14).setPos(20 + 106,  58).setFontSize(12).setAlign("center")
		WHEELS["RL"]["pres"]["value"] = Label(tyre_window.app, "--")  .setSize( 25,  14).setPos(20 +  72, 128).setFontSize(12).setAlign("center")
		WHEELS["RR"]["pres"]["value"] = Label(tyre_window.app, "--")  .setSize( 25,  14).setPos(20 + 106, 128).setFontSize(12).setAlign("center")
		
		WHEELS["FL"]["pres"]["label"] = Label(tyre_window.app, "PSI") .setSize( 25,  14).setPos(20 +  72,  72).setFontSize(8).setAlign("center").setColor(label_color)
		WHEELS["FR"]["pres"]["label"] = Label(tyre_window.app, "PSI") .setSize( 25,  14).setPos(20 + 106,  72).setFontSize(8).setAlign("center").setColor(label_color)
		WHEELS["RL"]["pres"]["label"] = Label(tyre_window.app, "PSI") .setSize( 25,  14).setPos(20 +  72, 142).setFontSize(8).setAlign("center").setColor(label_color)
		WHEELS["RR"]["pres"]["label"] = Label(tyre_window.app, "PSI") .setSize( 25,  14).setPos(20 + 106, 142).setFontSize(8).setAlign("center").setColor(label_color)
		
		# wheel visual info
		
		WHEELS["FL"]["dirt"] = Label(tyre_window.app).setSize(25, 4).setPos(20 +  45,  48).setBgColor(rgb(bg_colors["white"], bg = True)).setBgOpacity(1)
		WHEELS["FR"]["dirt"] = Label(tyre_window.app).setSize(25, 4).setPos(20 + 134,  48).setBgColor(rgb(bg_colors["white"], bg = True)).setBgOpacity(1)
		WHEELS["RL"]["dirt"] = Label(tyre_window.app).setSize(25, 4).setPos(20 +  45, 118).setBgColor(rgb(bg_colors["white"], bg = True)).setBgOpacity(1)
		WHEELS["RR"]["dirt"] = Label(tyre_window.app).setSize(25, 4).setPos(20 + 134, 118).setBgColor(rgb(bg_colors["white"], bg = True)).setBgOpacity(1)
		
		WHEELS["FL"]["slip"] = Label(tyre_window.app).setSize(25, 4).setPos(20 +  45, 90).setBgColor(rgb(bg_colors["yellow"], bg = True)).setBgOpacity(1)
		WHEELS["FR"]["slip"] = Label(tyre_window.app).setSize(25, 4).setPos(20 + 134, 90).setBgColor(rgb(bg_colors["yellow"], bg = True)).setBgOpacity(1)
		WHEELS["RL"]["slip"] = Label(tyre_window.app).setSize(25, 4).setPos(20 +  45, 160).setBgColor(rgb(bg_colors["yellow"], bg = True)).setBgOpacity(1)
		WHEELS["RR"]["slip"] = Label(tyre_window.app).setSize(25, 4).setPos(20 + 134, 160).setBgColor(rgb(bg_colors["yellow"], bg = True)).setBgOpacity(1)
		
		WHEELS["FL"]["temp"]["graph"] = Label(tyre_window.app).setSize(25, 36).setPos(20 +  45,  53).setBgColor(rgb(bg_colors["cold_green"], bg = True)).setBgOpacity(1)
		WHEELS["FR"]["temp"]["graph"] = Label(tyre_window.app).setSize(25, 36).setPos(20 + 134,  53).setBgColor(rgb(bg_colors["cold_green"], bg = True)).setBgOpacity(1)
		WHEELS["RL"]["temp"]["graph"] = Label(tyre_window.app).setSize(25, 36).setPos(20 +  45, 123).setBgColor(rgb(bg_colors["cold_green"], bg = True)).setBgOpacity(1)
		WHEELS["RR"]["temp"]["graph"] = Label(tyre_window.app).setSize(25, 36).setPos(20 + 134, 123).setBgColor(rgb(bg_colors["cold_green"], bg = True)).setBgOpacity(1)
		
		WHEELS["FL"]["wear"]["graph"] = Label(tyre_window.app).setSize(3, 46).setPos(20 +  35,  48).setBgColor(rgb(bg_colors["green"], bg = True)).setBgOpacity(1)
		WHEELS["FR"]["wear"]["graph"] = Label(tyre_window.app).setSize(3, 46).setPos(20 + 166,  48).setBgColor(rgb(bg_colors["green"], bg = True)).setBgOpacity(1)
		WHEELS["RL"]["wear"]["graph"] = Label(tyre_window.app).setSize(3, 46).setPos(20 +  35, 118).setBgColor(rgb(bg_colors["green"], bg = True)).setBgOpacity(1)
		WHEELS["RR"]["wear"]["graph"] = Label(tyre_window.app).setSize(3, 46).setPos(20 + 166, 118).setBgColor(rgb(bg_colors["green"], bg = True)).setBgOpacity(1)
		
		
		# -- RACE PANEL -- ##############################################################################################################
		
		# adding the race window app static labels
		lap_count_label["label"] = Label(race_window.app, "Lap:")     .setSize(28, 20).setPos(20, 40).setFontSize(12).setColor(label_color)
		lap_count_label["value"] = Label(race_window.app, "- / -")    .setSize(74, 20).setPos(lap_count_label["label"].pos["x"] + lap_count_label["label"].size["w"], 40).setFontSize(12)
		last_lap_label["label"]  = Label(race_window.app, "Last lap:").setSize(50, 20).setPos(20 + 100, 40).setFontSize(12).setColor(label_color)
		last_lap_label["value"]  = Label(race_window.app, "--:--.---").setSize(50, 20).setPos(last_lap_label["label"].pos["x"] + last_lap_label["label"].size["w"], 40).setFontSize(12).setAlign("right")
		race_flag                = Label(race_window.app)             .setSize(34, 22).setPos(20, 195)
		
		# adding the race dynamic position labels
		for i in range(5):
			# creating the labels for race listing (position and name)
			drivers_list_labels.append(Label(race_window.app).setSize(175, 20).setPos(20 + 28, i * 20 + 66 ).setFontSize(14))
			drivers_list_pos_labels.append(Label(race_window.app).setSize(28, 20).setPos(20, i * 20 + 66 ).setFontSize(14))
			# grouping the new labels inside the "race_info" panel
			panels["race_info"].extend([drivers_list_labels[i], drivers_list_pos_labels[i]])
		
		
		# -- SETTINGS PANEL -- ##############################################################################################################
		
		# adding the settings buttons
		button_delta       = Button(settings_window.app, button_func_delta, width=202, height=30, x=20, y=66, texture=appPATH+"images/buttons/button_toggle_delta_meter.png")
		button_color       = Button(settings_window.app, button_func_color, width=202, height=30, x=20, y=button_delta.y+(button_delta.height), texture=appPATH+"images/buttons/button_color_scheme.png")
		button_speed_units = Button(settings_window.app, button_func_speed, width=202, height=30, x=20, y=button_delta.y+(button_delta.height*2), texture=appPATH+"images/buttons/button_speed_units.png")		
		button_temp_units  = Button(settings_window.app, button_func_temperature, width=202, height=30, x=20, y=button_delta.y+(button_delta.height*3), texture=appPATH+"images/buttons/button_temp_units.png")
		button_press_units = Button(settings_window.app, button_func_pressure, width=202, height=30, x=20, y=button_delta.y+(button_delta.height*4), texture=appPATH+"images/buttons/button_pressure_units.png")
		button_fuel_units  = Button(settings_window.app, button_func_fuel, width=202, height=30, x=20, y=button_delta.y+(button_delta.height*5), texture=appPATH+"images/buttons/button_fuel_units.png")
		
		#-#####################################################################################################################################-#
		
		
		# grouping labels into panels
		panels["delta_meter"] = [delta_meter, delta_meter_bg]
		panels["fuel_info"]   = [l_fuel, l_fuelEstimate, l_fuel_per_lap, v_fuel, v_fuelEstimate, v_fuel_per_lap]
		panels["laps_info"]   = [l_position, l_personalBest, l_bestLap, v_position, v_personalBest, v_bestLap, l_currLap, l_lapDelta, l_lastLap, v_currLap, v_lapDelta, v_lastLap]
		panels["tyre_info"]   = [WHEELS["BG"], WHEELS["FL"]["temp"]["value"], WHEELS["FR"]["temp"]["value"], WHEELS["RL"]["temp"]["value"], WHEELS["RR"]["temp"]["value"], WHEELS["FL"]["wear"]["value"], WHEELS["FR"]["wear"]["value"], WHEELS["RL"]["wear"]["value"], WHEELS["RR"]["wear"]["value"], WHEELS["FL"]["wear"]["label"], WHEELS["FR"]["wear"]["label"], WHEELS["RL"]["wear"]["label"], WHEELS["RR"]["wear"]["label"], WHEELS["FL"]["pres"]["value"], WHEELS["FR"]["pres"]["value"], WHEELS["RL"]["pres"]["value"], WHEELS["RR"]["pres"]["value"], WHEELS["FL"]["pres"]["label"], WHEELS["FR"]["pres"]["label"], WHEELS["RL"]["pres"]["label"], WHEELS["RR"]["pres"]["label"], WHEELS["FL"]["dirt"], WHEELS["FR"]["dirt"], WHEELS["RL"]["dirt"], WHEELS["RR"]["dirt"], WHEELS["FL"]["slip"], WHEELS["FR"]["slip"], WHEELS["RL"]["slip"], WHEELS["RR"]["slip"], WHEELS["FL"]["temp"]["graph"], WHEELS["FR"]["temp"]["graph"], WHEELS["RL"]["temp"]["graph"], WHEELS["RR"]["temp"]["graph"], WHEELS["FL"]["wear"]["graph"], WHEELS["FR"]["wear"]["graph"], WHEELS["RL"]["wear"]["graph"], WHEELS["RR"]["wear"]["graph"]]
		panels["race_info"].extend([lap_count_label["label"], lap_count_label["value"], last_lap_label["label"], last_lap_label["value"]])
			
		colored_labels  = [l_position, l_personalBest, l_bestLap, l_currLap, l_lapDelta, l_lastLap, l_fuel, l_fuelEstimate, l_fuel_per_lap, WHEELS["FL"]["wear"]["label"], WHEELS["FR"]["wear"]["label"], WHEELS["RL"]["wear"]["label"], WHEELS["RR"]["wear"]["label"], WHEELS["FL"]["pres"]["label"], WHEELS["FR"]["pres"]["label"], WHEELS["RL"]["pres"]["label"], WHEELS["RR"]["pres"]["label"], lap_count_label["label"], last_lap_label["label"]]
		panels["left"]  = panels["fuel_info"]
		panels["right"] = panels["laps_info"]
		
				
		#-#####################################################################################################################################-#
		
		# check config for delta meter status
		# hide/show it recording to the user config file
		if delta_meter_status == "off":
			hide_labels(panels["delta_meter"])
			is_delta_meter_visible = False
		elif delta_meter_status == "on":
			hide_labels(panels["delta_meter"], False)
			is_delta_meter_visible = True
		
		# centering the delta meter gauge
		delta_meter   .setPos(main_window.width/2-delta_meter.size["w"]   /2, main_window.height + 10)
		delta_meter_bg.setPos(main_window.width/2-delta_meter_bg.size["w"]/2, main_window.height + 10)
		
		#-#####################################################################################################################################-#
		
		# SETTING UNITS LABELS
		if units["speed"] == "MPH":
			speed_units_label.setText("MPH")
		
		for wheel in ["FL", "FR", "RL", "RR"]:
			if units["pressure"] == "BAR":
				WHEELS[wheel]["pres"]["label"].setText("bar")
			elif units["pressure"] == "KPA":
				WHEELS[wheel]["pres"]["label"].setText("kPa")
		
		# temporary label
		log = Label(main_window.app, "").setSize(420, 20).setPos(-200, -60).setFontSize(14)


	#-#####################################################################################################################################-#
	
	
	def load_config(self):
		global appPATH, cfg_carsInfo, cfg_bestLap, cfg_userConf, ini_carsInfo, ini_bestLap, ini_userconf
		global personalBest, units, average_lap_fuel, low_fuel
		global delta_meter_max, delta_meter_status, textures_tach
		global skins, user_skin, label_color
		
		try:
			# init config files
			cfg_carsInfo = Config(appPATH, ini_carsInfo)
			cfg_bestLap  = Config(appPATH, ini_bestLap)
			cfg_userConf = Config(appPATH, ini_userconf)
			
			# getting values from config files
			average_lap_fuel   = cfg_carsInfo.get(track_name + "_average_fuel", car_name, "float")
			personalBest       = cfg_bestLap.get(track_name, car_name, "int")
			units["pressure"]  = cfg_userConf.get("UNITS", "pressure").upper()
			units["volume"]    = cfg_userConf.get("UNITS", "volume").upper()
			units["speed"]     = cfg_userConf.get("UNITS", "speed").upper()
			units["temp"]      = cfg_userConf.get("UNITS", "temperature").upper()
			low_fuel           = cfg_userConf.get("SETTINGS", "low_fuel_warning", "float")
			delta_meter_max    = cfg_userConf.get("SETTINGS", "delta_meter_max", "float")
			delta_meter_status = cfg_userConf.get("SETTINGS", "delta_meter_status")
			user_skin          = cfg_userConf.get("SETTINGS", "skin")
			
			# make sure the skin name from the config file is valid
			# if not valid set default skin to "red"
			user_skin = user_skin if user_skin in skins else "red" 
			
			# applying the skin setting
			textures_tach["bg"] = appPATH + "images/tachometer/tach-base-" + user_skin + ".png"
			label_color = rgb(skins[user_skin])			
			
		except Exception as e:
			ac.console("OV1: Error in function load_config(): %s" % e)
			ac.log("OV1: Error in function load_config(): %s" % e)
		
		
	#-#####################################################################################################################################-#

	
	def on_update(self, deltaT):
		global appPATH, main_window, tick_counter, sim_info, driver_name, gear, speed, rpms, ac_bestLap, v_position, tachometer, textures_tach
		global cfg_bestLap, cfg_carsInfo, cfg_userConf, units, max_rpms
		global laps_window, race_window, tyre_window, settings_window
		
		# updating deltaT
		self.deltaT = deltaT
		
		# always set the background opacity to 0
		# always hide the app's border; happens when the pin is clicked
		
		main_window.setBgOpacity(0).border(0)
		race_window.setBgOpacity(0).border(0)
		tyre_window.setBgOpacity(0).border(0)
		laps_window.setBgOpacity(0).border(0)
		fuel_window.setBgOpacity(0).border(0)
		settings_window.setBgOpacity(0).border(0)
		
		# AC variables
		ac_gear     = ac.getCarState(0, acsys.CS.Gear)
		ac_speed    = ac.getCarState(0, acsys.CS.SpeedKMH) if units["speed"] == "KMH" else ac.getCarState(0, acsys.CS.SpeedMPH)
		# lap info
		ac_currLap  = ac.getCarState(0, acsys.CS.LapTime)
		ac_bestLap  = ac.getCarState(0, acsys.CS.BestLap)
		# commented until acsys.CS.LastLap is fixed
		ac_lastLap  = ac.getCarState(0, acsys.CS.LastLap)
		# lap delta
		ac_lapDelta = ac.getCarState(0, acsys.CS.PerformanceMeter)
		# number of cars on track
		ac_num_of_cars = sim_info.static.numCars if sim_info.static.numCars > 1 else "-"
		
		# reducing the refresh rate of certain elements
		# e.g. speed indicator, position, fuel info, etc.
		if tick_counter == 16:
			# updating speed indicator
			speed.setText("%d" % round(ac_speed))
			
			# if sim is Live
			if sim_info.graphics.status == 2:
				# calculating the fuel estimate
				self.estimate_fuel()
				# display fuel level with the fuel gauge
				self.fuel_gauge()
				
			# updating position
			v_position.setText("%s / %s" % (my_race_position, ac_num_of_cars))
			
			# update race info
			self.update_race_info()
			
			# reseting the tick counter
			tick_counter = 0
			
		# rpms
		rpms = ac.getCarState(0, acsys.CS.RPM)
		max_rpms = sim_info.static.maxRpm if max_rpms == 0 else max_rpms
		
		# applying the tachometer steps texture
		if textures_tach["steps"] == "":
			if max_rpms >= 6000 and max_rpms < 7000:
				textures_tach["steps"] = appPATH + "images/tachometer/tach-steps-7000.png"
			if max_rpms >= 7000 and max_rpms < 8000:
				textures_tach["steps"] = appPATH + "images/tachometer/tach-steps-8000.png"
			elif max_rpms >= 8000 and max_rpms < 9000:
				textures_tach["steps"] = appPATH + "images/tachometer/tach-steps-9000.png"
			elif max_rpms >= 9000 and max_rpms <= 10000:
				textures_tach["steps"] = appPATH + "images/tachometer/tach-steps-10000.png"
			elif max_rpms > 10000 and max_rpms <= 14000:
				textures_tach["steps"] = appPATH + "images/tachometer/tach-steps-14000.png"
			elif max_rpms >= 17000:
				textures_tach["steps"] = appPATH + "images/tachometer/tach-steps-18000.png"
			tachometer["steps"].setBgTexture(textures_tach["steps"])
		
		# updating gear indicator
		self.display_gear(ac_gear)
		
		# updating lap info
		self.update_lap_info(ac_currLap, ac_bestLap, ac_lastLap, ac_lapDelta)
		
		# update tyre info
		self.update_tyre_info()
		
		# check panel proximity
		self.check_panel_proximity()
		
		# finally incrementing the counter
		tick_counter += 1


	#-#####################################################################################################################################-#

	
	def on_render(self):
		global rpms, max_rpms
		
		# tachometer animation
		self.tach_animate(rpms)
		# shift light
		self.shift_light()
		# signal lights
		self.signal_lights()
		# delta meter
		self.delta_meter()


	#-#####################################################################################################################################-#

	
	def on_shutdown(self):
		global cfg_carsInfo, average_lap_fuel, car_name, track_name
		
		# adding suffix to the section ID
		section = track_name + "_average_fuel"
		# saving fuel consumption per lap
		if average_lap_fuel > 0:
			cfg = cfg_carsInfo
			#add section if not found
			if not cfg.has(section):	
				cfg.set(section)
				cfg.set(section, car_name, average_lap_fuel)
			else:
				cfg.set(section, car_name, average_lap_fuel)


	#-#####################################################################################################################################-#
	
	
	def check_panel_proximity(self):
		global main_window, laps_window, race_window, tyre_window, fuel_window
		global appPATH, textures_bg, delta_meter, delta_meter_bg
		global log
		# local variables
		pos_threshold   = 30 # position threshold
		panels_attached =  0 # number of panels attached
		
		# local functions
		def move_delta_meter(y):
			delta_meter.setPos(delta_meter.pos["x"], y)
			delta_meter_bg.setPos(delta_meter_bg.pos["x"], y)
			
		# getting main window position
		main_window.getPos()
		# calculating the target sweet spot for attachment on the right side
		target_x1, target_y = main_window.x + main_window.width, main_window.y
		
		# going through each panel window
		for panel in [laps_window, race_window, tyre_window, fuel_window]:
			# calculating the target sweet spot for attachment on the left size
			target_x2 = main_window.x - panel.width
			# updating panel window position coords
			panel.getPos()
			# conditions of proximity for both sides
			near_right = target_x1 - pos_threshold < panel.x < target_x1 + pos_threshold and target_y - pos_threshold < panel.y < target_y + pos_threshold
			near_left  = target_x2 - pos_threshold < panel.x < target_x2 + pos_threshold and target_y - pos_threshold < panel.y < target_y + pos_threshold
				
			# checking if panel is in main app window proximity
			# on the right hand side
			if near_right:
				# raising flag
				main_window.attached_r = panel
				# set the panel background to accomodate the attachment
				panel.setBgTexture(appPATH+"images/background/panel-bg-right.png") if panel != fuel_window else panel.setBgTexture(appPATH+"images/background/small-panel-bg-right.png")
				# move the panel to the target position
				panel.setPos(target_x1, target_y)
				# if panel is attached increment counter
				panels_attached += 1
			# checking if panel is in main ap window proximity
			# on the left hand side
			elif near_left:
				# raising flag
				main_window.attached_l = panel
				# set the panel background to accomodate the attachment
				panel.setBgTexture(appPATH+"images/background/panel-bg-left.png") if panel != fuel_window else panel.setBgTexture(appPATH+"images/background/small-panel-bg-left.png")
				# move the panel to the target position
				panel.setPos(target_x2, target_y)
				# if panel is attached increment counter
				panels_attached += 1
			else:
				if panel == main_window.attached_l:
					main_window.attached_l = -1
				if panel == main_window.attached_r:
					main_window.attached_r = -1
				# resetting the panel's background texture
				panel.setBgTexture(appPATH+"images/background/panel-bg.png") if panel != fuel_window else panel.setBgTexture(appPATH+"images/background/small-panel-bg.png")
			
		# temporary log output
		# log.setText("%s, %s" % (main_window.attached_l, main_window.attached_r))	
		
		# if no panels are attached
		if panels_attached == 0:
			# lowering the flag
			main_window.is_attached = False
			main_window.attached_l  = -1
			main_window.attached_r  = -1
			# resetting main window's background texture
			main_window.setBgTexture(textures_bg["mid"])
			# change delta meter's position
			#move_delta_meter(94)
		
		# if at least 1 panel is attached
		if panels_attached > 0:
			# raising flag
			main_window.is_attached = True
		
		# if panel attached on the left hand side
		if main_window.attached_l != -1 and main_window.attached_r == -1:
			# resetting main window's background texture
			main_window.setBgTexture(textures_bg["left"])
		
		# if panel attached on the right hand side		
		if main_window.attached_r != -1 and main_window.attached_l == -1:
			# change delta meter's position
			#move_delta_meter(-10)
			# resetting main window's background texture
			main_window.setBgTexture(textures_bg["right"])
		
		# if panels are attached on both sides
		if main_window.attached_l != -1 and main_window.attached_r != -1:
			# change main window background texture
			main_window.setBgTexture(textures_bg["full"])
			
	
	#-#####################################################################################################################################-#


	def update_lap_info(self, ac_currLap, ac_bestLap, ac_lastLap, ac_lapDelta):
		global sim_info, personalBest, v_lastLap, v_bestLap, v_currLap, v_lapDelta, l_currLap, v_personalBest, colors
		
		# updating the current lap label
		v_currLap.setText(millisToString(ac_currLap))
		
		if personalBest <= 0:
			v_personalBest.setText("--:--.---")
			personalBest = ac_bestLap
		else:
			if ac_bestLap > 0 and personalBest > ac_bestLap:
				personalBest = ac_bestLap
				v_bestLap.setColor(rgb(colors["yellow"]))
				v_personalBest.setColor(rgb(colors["yellow"]))
				#write personal best to file
				if sim_info.graphics.status == 2:
					self.save_best_lap(ac_bestLap)
			if ac_bestLap > 0 and ac_bestLap > personalBest:
				v_bestLap.setColor(rgb(colors["white"]))
			v_personalBest.setText("%s" % millisToString(personalBest))
			
		# updating the best lap label
		if ac_bestLap > 0:
			v_bestLap.setText(millisToString(ac_bestLap))
		else:
			v_bestLap.setText("--:--.---")
			v_bestLap.setColor(rgb(colors["white"]))

		# updating the last lap label
		# temporary solution
		lastLap = 0
		if ac_lastLap > 0:
			v_lastLap.setText(millisToString(ac_lastLap))
		else:
			lastSplits = ac.getLastSplits(0)
			for split in lastSplits:
				lastLap += split
			if lastLap > 0:
				v_lastLap.setText(millisToString(lastLap))
		
		# updating the lap delta label
		if ac_lapDelta != 0.0:
			if ac_lapDelta >= 0:
				v_lapDelta.setColor(rgb(colors["red"]))
			else:
				v_lapDelta.setColor(rgb(colors["green"]))
			v_lapDelta.setText("%+07.3f" % ac_lapDelta)

		# updating current lap count
		lapCount = ac.getCarState(0, acsys.CS.LapCount)
		if lapCount >= 0:
			l_currLap.setText("Current lap: %s / %s" % (lapCount + 1, sim_info.graphics.numberOfLaps if sim_info.graphics.numberOfLaps > 0 else "-"))
		
	
	#-#####################################################################################################################################-#


	def update_tyre_info(self):
		global sim_info, WHEELS, bg_colors, units
		
		# local variables
		maxHue     = 100  # maximum hue, coldest graph color (degrees on color wheel)
		hotTemp    = 125  # tyre temperature at which the graph displays red
		saturation = 0.95 # saturation of tyre temperature graph
		brightness = 0.92 # brightness of tyre temperature graph
		
		wheels  = ["FL", "FR", "RL", "RR"]
		ac_temp = { "FL" : 0, "FR" : 0, "RL" : 0, "RR" : 0 }
		ac_wear = { "FL" : 0, "FR" : 0, "RL" : 0, "RR" : 0 }
		ac_pres = { "FL" : 0, "FR" : 0, "RL" : 0, "RR" : 0 }
		ac_slip = { "FL" : 0, "FR" : 0, "RL" : 0, "RR" : 0 }
		ac_dirt = { "FL" : 0, "FR" : 0, "RL" : 0, "RR" : 0 }
		
		# AC variables
		ac_temp["FL"], ac_temp["FR"], ac_temp["RL"], ac_temp["RR"] = ac.getCarState(0, acsys.CS.CurrentTyresCoreTemp)
		ac_wear["FL"], ac_wear["FR"], ac_wear["RL"], ac_wear["RR"] = sim_info.physics.tyreWear
		ac_pres["FL"], ac_pres["FR"], ac_pres["RL"], ac_pres["RR"] = sim_info.physics.wheelsPressure
		ac_slip["FL"], ac_slip["FR"], ac_slip["RL"], ac_slip["RR"] = sim_info.physics.wheelSlip
		ac_dirt["FL"], ac_dirt["FR"], ac_dirt["RL"], ac_dirt["RR"] = sim_info.physics.tyreDirtyLevel
		
		# getting the cold temperatures read
		if WHEELS["coldRead"] is False:
			WHEELS["FL"]["temp"]["cold"] = ac_temp["FL"]
			WHEELS["FR"]["temp"]["cold"] = ac_temp["FR"]
			WHEELS["RL"]["temp"]["cold"] = ac_temp["RL"]
			WHEELS["RR"]["temp"]["cold"] = ac_temp["RR"]
			# stop this from running again
			WHEELS["coldRead"] = True
		
		# going through each wheel
		for wheel in wheels:
			# updating TEMP level graph
			hue = maxHue - (maxHue / hotTemp * ac_temp[wheel])
			if hue > maxHue: hue = maxHue
			if hue < 0 : hue = 0
			hue = hsv2rgb(hue, saturation, brightness)
			WHEELS[wheel]["temp"]["graph"].setBgColor(rgb(hue, bg = True)).setBgOpacity(1)
			
			# updating the tyre TEMPERATURES
			temperature = "%dC" % ac_temp[wheel] if units["temp"] == "C" else "%dF" % C_to_F(ac_temp[wheel])
			WHEELS[wheel]["temp"]["value"].setText(temperature)
			
			# updating tyre WEAR
			WHEELS[wheel]["wear"]["value"].setText("%d%%" % ac_wear[wheel])
			
			# updating tyre PRESSURE
			if units["pressure"] == "BAR": pressure = "%.1f" % PSI_to(ac_pres[wheel])
			elif units["pressure"] == "KPA": pressure = "%d" % PSI_to(ac_pres[wheel], to = "KPA")
			else: pressure = "%d" % ac_pres[wheel] # PSI
			WHEELS[wheel]["pres"]["value"].setText(pressure)
			
			# updating the tyre DIRT level graph
			max_dirt = 5 # maximum dirt level value (from AC testing)
			dirt_level = int(25 * ac_dirt[wheel] / max_dirt)
			dirt_level = dirt_level if dirt_level <= 25 else 25 # making sure width doesn't exceed the maximum value
			WHEELS[wheel]["dirt"].setSize(dirt_level, 4)
			
			# updating WEAR level graph
			wear_level = int(46 * ac_wear[wheel] / 100)
			if wheel == "RL" or wheel == "RR": wear_level_y = 118
			else: wear_level_y = 48
			WHEELS[wheel]["wear"]["graph"].setSize(3, wear_level).setPos(WHEELS[wheel]["wear"]["graph"].pos["x"], wear_level_y + (46 - wear_level))
			
			# updating SLIP level graph
			slip_level = int(25 * ac_slip[wheel]) if ac_slip[wheel] <= 1 else 25
			slip_level_color = rgb(bg_colors["yellow"], bg = True) if slip_level < 25 else rgb(bg_colors["red"], bg = True)
			WHEELS[wheel]["slip"].setSize(slip_level, 4).setBgColor(slip_level_color).setBgOpacity(1)


	#-#####################################################################################################################################-#


	def update_race_info(self):
		global appPATH, sim_info, drivers_list_labels, my_race_position, lap_count_label, last_lap_label, v_lastLap, colors, race_flag
		
		# local variables
		drivers     = []
		final_list  = []
		
		# AC variables
		ac_numCars = sim_info.static.numCars   # number of cars on the track
		number_of_laps = sim_info.graphics.numberOfLaps
		
		# this is here so we get proper scope to it later (we assign it in the loop)
		my_driver = None
		
		# going through each car on the track
		for i in range(ac_numCars):
			# getting information about each driver's car
			driver = {
				"driver_name" : ac.getDriverName(i),
				"lap_count"   : ac.getCarState(i, acsys.CS.LapCount),
				"spline_pos"  : ac.getCarState(i, acsys.CS.NormalizedSplinePosition)
			}
			# tyring to solve the first lap position problem:
			# once the leader crosses the finish line into lap 1, cars before the finish line
			# are positioned at the top of the list, which is not what we want :-)
			driver["lap_count"] = -1 if driver["lap_count"] <= 0 and 0.8 < driver["spline_pos"] < 1 else driver["lap_count"]
			
			# set our own driver record
			if i == 0:
				my_driver = driver
			
			# add the driver in the drivers list
			drivers.append(driver)
		
		# sorting the drivers by lap count and position on the track
		# keeping the previous syntax:
		# drivers = sorted(drivers, key=operator.itemgetter("lap_count", "spline_pos"), reverse = True)
		drivers = sorted(drivers, key = lambda i: (-i["lap_count"], -i["spline_pos"]))
		
		# what position are we?
		my_position = drivers.index(my_driver)
		# saving the player's position inside a variable
		my_race_position = my_position + 1

		# checking if there are more drivers on the track
		# if number of drivers is between 1 and 5
		if 1 < len(drivers) <= 5:
			first_driver_in_list = 0
		# if number of drivers is more than 5
		elif len(drivers) > 5:
			# calculating the first driver name in the list
			first_driver_in_list = my_position - 2 if my_position > 2 else 0
			first_driver_in_list = ac_numCars - 5 if my_position > ac_numCars - 3 else first_driver_in_list
		# if you're alone! :-)
		else:
			first_driver_in_list = 0
		
		# when player finishes the race, stop refreshing the list
		# when in practice or when replaying a saved race
		# --
		# unfortunately this will cause the positioning to go crazy...
		if (my_driver["lap_count"] < number_of_laps and 0.1 < my_driver["spline_pos"] > 0) or number_of_laps == 0:
			
			# going through each label, setting the position and driver name
			# the label that contains the player' name will be highlighted
			for i, label in enumerate(drivers_list_labels):
				# making sure we don't get an error if drivers' index is exceeded
				try:
					# current driver we're working with
					driver = drivers[first_driver_in_list + i]
					# adding text to labels
					label.setText("%s" % driver["driver_name"])
					drivers_list_pos_labels[i].setText("%s." % (drivers.index(driver) + 1))
					
					# highlighting the player's name and position
					if drivers[first_driver_in_list + i] == my_driver and len(drivers) > 1:
						label.setColor(rgb(colors["yellow"])).setBgColor(rgb(colors["white"], bg = True)).setBgOpacity(0.03)
						drivers_list_pos_labels[i].setColor(rgb(colors["yellow"])).setBgColor(rgb(colors["white"], bg = True)).setBgOpacity(0.03)
					# removing highlighting for other drivers
					else:
						label.setColor(rgb(colors["white"])).setBgOpacity(0)
						drivers_list_pos_labels[i].setColor(rgb(colors["white"])).setBgOpacity(0)
				except:
					pass
		
		# settings the lap count and last lap labels
		current_lap_count = ac.getCarState(0, acsys.CS.LapCount) + 1
		lap_count_label["value"].setText("%s / %s" % (current_lap_count, number_of_laps if number_of_laps > 0 else "-"))
		last_lap_label["value"].setText("%s" % v_lastLap.text)
		
		# raising the flags
		if number_of_laps > 0:
			# green flag: race start
			if current_lap_count == 1 and 0 < ac.getCarState(0, acsys.CS.LapTime) < 10 * 1000: # 10 seconds
				race_flag.setBgTexture(appPATH + "images/flags/flags_green.png")
				hide_labels([race_flag], False)
			# white flag: last lap
			elif current_lap_count == number_of_laps:
				race_flag.setBgTexture(appPATH + "images/flags/flags_white.png")
				hide_labels([race_flag], False)
			# checkered flag: race is over
			elif current_lap_count > number_of_laps:
				race_flag.setBgTexture(appPATH + "images/flags/flags_checkered.png")
				hide_labels([race_flag], False)
			# hide the flags if no condition is met
			else:
				hide_labels([race_flag])
	

	#-#####################################################################################################################################-#


	def display_gear(self, i):
		global textures_gear, gear
		if i == 0:
			gear.setBgTexture(textures_gear[0])
		if i == 1:
			gear.setBgTexture(textures_gear[1])
		if i > 1:
			gear.setBgTexture(textures_gear[i])


	#-#####################################################################################################################################-#


	def tach_animate(self, rpms):
		global appPATH, tachometer, max_rpms
		
		# sometimes the rpm value is negative
		# making sure this doesn't break the code
		if rpms >= 0:
			# getting the number of steps in relation to the car's max rpm value
			tachSteps = round(max_rpms / 33.3333333333333) # 1 tach step = 100 rpms (90 steps total)
			# calculating the tachometer value
			tachValue = round((rpms / 1000) * tachSteps / (max_rpms / 1000))
			# custom cases
			# more than 17K RPMs
			if max_rpms >= 17000:
				if rpms >= 10000:
					tachValue -= 270
				else:
					tachSteps = 30
					tachValue = round((rpms / 1000) * tachSteps / 10)
			# between 10K and 14K RPMs
			if 10000 < max_rpms <= 14000:
				if rpms >= 6000:
					tachValue -= 150
				else:
					tachSteps = 30
					tachValue = round((rpms / 1000) * tachSteps / 6)
			# between 9K and 10K
			if 9000 <= max_rpms <= 10000:
				if rpms >= 2000:
					tachValue -= 30
				else:
					tachSteps = 30
					tachValue = round((rpms / 1000) * tachSteps / 2)
			# if tach value is less then 10, add the leading 00s
			if tachValue < 10:
				tachValue = "00" + str(tachValue)
			# if it's less than 100 add one leading 0
			elif tachValue >= 10 and tachValue < 100:
				tachValue = "0" + str(tachValue)
			# do nothing :)
			else:
				tachValue = str(tachValue)
		# if the rpm value is negative use the first tach step
		else:
			tachValue = "000"
		
		# create the image path
		tachTexture = appPATH + "images/tach_needle/needle_" + tachValue + ".png"
		# apply the texture
		tachometer["base"].setBgTexture(tachTexture)
	
	
	#-#####################################################################################################################################-#


	def fuel_gauge(self):
		global appPATH, fuel_gauge, sim_info, low_fuel
		gauge_steps  = 10 # number of fuel gauge step images (temporary solution...)
		# getting car info
		current_fuel = sim_info.physics.fuel
		max_fuel     = sim_info.static.maxFuel
		# calculating the gauge level
		if current_fuel > low_fuel or current_fuel == 0:
			gauge_value  = round(current_fuel * gauge_steps / max_fuel)
		elif current_fuel <= low_fuel:
			gauge_value = 1
		# create the image path
		gauge_texture = appPATH + "images/fuel/fuel_gauge_" + str(gauge_value) + ".png"
		# apply the texture
		fuel_gauge.setBgTexture(gauge_texture)
	
	
	#-#####################################################################################################################################-#


	def save_best_lap(self, bestLap):
		global cfg_bestLap, track_name, car_name
		cfg = cfg_bestLap
		
		# add section if not found
		if not cfg.has(track_name):
			cfg.set(track_name)
			cfg.set(track_name, car_name, bestLap)
		else:
			if not cfg.has(track_name, car_name) and bestLap > 0:
				cfg.set(track_name, car_name, bestLap)
			else:
				if bestLap > 0 and cfg.get(track_name, car_name, "int") > bestLap:
					cfg.set(track_name, car_name, bestLap)


	#-#####################################################################################################################################-#


	def shift_light(self):
		global main_window, appPATH, rpms, max_rpms, tachometer
		if rpms >= max_rpms - 400:
			tachometer["shift"].setVisible(1)
		else:
			tachometer["shift"].setVisible(0)


	#-#####################################################################################################################################-#


	def delta_meter(self):
		global delta_meter, textures_delta_meter, delta_meter_max, colors
		# local variables
		max_value = delta_meter_max # seconds until meter reaches the max value
		width     = 202             # total width of the meter + and -
		height    = 16              # height of the meter
		value     = 0               # the new meter's width
		half      = width / 2       # meter's middle
		# AC values
		delta     = ac.getCarState(0, acsys.CS.PerformanceMeter)
		# assign value from config file
		max_value = 2 if delta_meter_max == -1 else delta_meter_max
		# calculate meter value
		value     = abs(delta) * half / max_value
		# making sure the meter doesn't exceed its boundaries
		if value > half:
			value = half
		# apply meter value and style
		
		# calculating x coord. offset
		x_offset = delta_meter_bg.pos["x"] + delta_meter_bg.size["w"]/2
		
		if delta <= 0:
			delta_meter.setPos(x_offset, delta_meter.pos["y"]).setSize(value, height).setBgColor(rgb(colors["green"], bg = True)).setBgOpacity(0.8)
		else:
			delta_meter.setPos(x_offset - value, delta_meter.pos["y"]).setSize(value, height).setBgColor(rgb(colors["red"], bg = True)).setBgOpacity(0.8)
	
		
	#-#####################################################################################################################################-#


	def signal_lights(self):
		global sim_info, signal_abs, signal_fuel, signal_limiter, textures_signals, low_fuel
		
		# turn off all signals
		signal_abs.setVisible(0)
		signal_fuel.setVisible(0)
		signal_limiter.setVisible(0)
		
		if sim_info.graphics.status == 2:
			# local variables
			ac_limiter = sim_info.physics.pitLimiterOn
			ac_fuel    = sim_info.physics.fuel
			
			# PIT LIMITER
			if ac_limiter == 1:
				signal_limiter.setVisible(1)
			elif ac_limiter == 0:
				signal_limiter.setVisible(0)

			# FUEL
			# empty
			if ac_fuel == 0.0:
				signal_fuel.setBgTexture(textures_signals[2]).setVisible(1)
			# low
			elif ac_fuel <= low_fuel:
				signal_fuel.setBgTexture(textures_signals[1]).setVisible(1)
			# enough
			elif ac_fuel > low_fuel:
				signal_fuel.setVisible(0)


	#-#####################################################################################################################################-#


	def estimate_fuel(self):
		global sim_info, low_fuel, v_fuel, v_fuelEstimate, ac_fuel, start_line_fuel, prev_lap_count, start_of_lap, fuel_per_laps, average_lap_fuel, skipLap, units, colors
		
		# local variables
		estimated_laps  = 0
		string          = ""
		inPit           = sim_info.graphics.isInPit
		ac_current_fuel = sim_info.physics.fuel
		ac_lap_count    = sim_info.graphics.completedLaps
		average_per_lap = 0
		
		if inPit == 1 or start_line_fuel == -1:
			# skip the lap
			skipLap = True
			
		if start_of_lap == True:
			if ac_lap_count > 1 and start_line_fuel > ac_current_fuel and skipLap == False:
				# add each amount of fuel burnt for every lap inside a list
				fuel_per_laps.append(start_line_fuel - ac_current_fuel)
				# sum up the fuel burnt for each lap
				for fuel_amount in fuel_per_laps:
					average_per_lap += fuel_amount
				# divide the fuel by the number of laps
				average_lap_fuel = average_per_lap = average_per_lap / len(fuel_per_laps)
			# store the curent fuel level
			start_line_fuel = ac_current_fuel
			# lower flag when car is passed the finish line	
			start_of_lap = False
			# skip the lap
			skipLap = False
			
		# raise a flag each time the finish line is crossed
		if prev_lap_count != ac_lap_count:
			start_of_lap = True
			# store the current fuel level at start of the first lap
			prev_lap_count = ac_lap_count
		
		if average_lap_fuel > 0:
			# calculating the number of estimated laps until tank is empty
			estimated_laps = ac_current_fuel / average_lap_fuel
			# string variants
			string = "%.01f lap" if estimated_laps == 1 else "%.01f laps"
			# write the final result
			v_fuelEstimate.setText(string % estimated_laps)
		
		# display the values
		if units["volume"] == "L":
			v_fuel.setText("%.01f L" % ac_current_fuel)
			if average_lap_fuel > 0:
				v_fuel_per_lap.setText("%.02f L/lap" % average_lap_fuel)
		elif units["volume"] == "USGAL":
			v_fuel.setText("%.01f US gal" % L_to_Gal(ac_current_fuel))
			if average_lap_fuel > 0:
				v_fuel_per_lap.setText("%.02f gal/lap" %  L_to_Gal(average_lap_fuel))
			else:
				v_fuel_per_lap.setText("- gal/lap")
		elif units["volume"] == "UKGAL":
			v_fuel.setText("%.01f UK gal" % L_to_Gal(ac_current_fuel, type = "UK"))
			if average_lap_fuel > 0:
				v_fuel_per_lap.setText("%.02f gal/lap" %  L_to_Gal(average_lap_fuel, type = "UK"))
			else:
				v_fuel_per_lap.setText("- gal/lap")
		
		# color highlight for low fuel and empty tank warning
		if 0 < ac_current_fuel <= low_fuel:
			v_fuel.setColor(rgb(colors["yellow"]))
		elif ac_current_fuel == 0:
			v_fuel.setColor(rgb(colors["red"]))
		else:
			v_fuel.setColor(rgb(colors["white"]))
	

#-#####################################################################################################################################-#
	

def hide_labels(labels, hide=True):
	for label in labels:
		if hide == True:
			label.setVisible(0)
		else:
			label.setVisible(1)


#-#####################################################################################################################################-#


def button_func_color(dummy, variables):
	global cfg_userConf, user_skin, textures_tach, appPATH, label_color, skins, tachometer, colored_labels
	
	# going from one skin to another
	if user_skin == "red": user_skin = "orange"
	elif user_skin == "orange": user_skin = "green"
	elif user_skin == "green": user_skin = "cyan"
	elif user_skin == "cyan": user_skin = "blue"
	elif user_skin == "blue": user_skin = "dark"
	elif user_skin == "dark": user_skin = "red"
	
	# applying the skin settings
	textures_tach["bg"] = appPATH + "images/tachometer/tach-base-" + user_skin + ".png"
	tachometer["bg"].setBgTexture(textures_tach["bg"])
	label_color = rgb(skins[user_skin])
	
	# going through each colored label and applying the color
	for label in colored_labels:
		label.setColor(label_color)
	
	# saving the setting in config file
	cfg_userConf.set("SETTINGS", "skin", user_skin)


#-#####################################################################################################################################-#


def button_func_temperature(dummy, variables):
	global cfg_userConf, units
	
	# switching between temperature units
	if units["temp"] == "C":
		units["temp"] = "F"
	elif units["temp"] == "F":
		units["temp"] = "C"
	
	# saving the setting in config file
	cfg_userConf.set("UNITS", "temperature", units["temp"])


#-#####################################################################################################################################-#


def button_func_pressure(dummy, variables):
	global cfg_userConf, units, WHEELS
	
	# switching between pressure units
	if units["pressure"] == "PSI":
		units["pressure"] = "BAR"
	elif units["pressure"] == "BAR":
		units["pressure"] = "KPA"
	elif units["pressure"] == "KPA":
		units["pressure"] = "PSI"
	
	# changing the pressure labels to the selected unit
	for wheel in ["FL", "FR", "RL", "RR"]:
		if units["pressure"] == "PSI":
			WHEELS[wheel]["pres"]["label"].setText("PSI")
		elif units["pressure"] == "BAR":
			WHEELS[wheel]["pres"]["label"].setText("bar")
		elif units["pressure"] == "KPA":
			WHEELS[wheel]["pres"]["label"].setText("kPa")
	
	# saving the setting in config file
	cfg_userConf.set("UNITS", "pressure", units["pressure"])


#-#####################################################################################################################################-#


def button_func_speed(dummy, variables):
	global cfg_userConf, units, speed_units_label
	
	# switching between units
	# and changing the speed units label
	if units["speed"] == "MPH":
		units["speed"] = "KMH"
		speed_units_label.setText("KM/H")
	elif units["speed"] == "KMH":
		units["speed"] = "MPH"
		speed_units_label.setText("MPH")

	# saving the setting in config file
	cfg_userConf.set("UNITS", "speed", units["speed"])


#-#####################################################################################################################################-#


def button_func_fuel(dummy, variables):
	global cfg_userConf, units
	
	# switching between units
	if units["volume"] == "L":
		units["volume"] = "USGAL"
	elif units["volume"] == "USGAL":
		units["volume"] = "UKGAL"
	elif units["volume"] == "UKGAL":
		units["volume"] = "L"
	
	# saving the setting in config file
	cfg_userConf.set("UNITS", "volume", units["volume"])


#-#####################################################################################################################################-#


def button_func_delta(dummy, variables):
	global cfg_userConf, panels, is_delta_meter_visible
	
	if is_delta_meter_visible is True:
		hide_labels(panels["delta_meter"])
		is_delta_meter_visible = False
	else:
		hide_labels(panels["delta_meter"], False)
		is_delta_meter_visible = True
	
	# saving the setting in config file
	cfg_userConf.set("SETTINGS", "delta_meter_status", "on" if is_delta_meter_visible else "off")


#-#####################################################################################################################################-#