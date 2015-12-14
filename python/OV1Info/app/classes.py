import ac
import math
import configparser


class Window:
	
	# INITIALIZATION
	
	def __init__(self, name="defaultAppWindow", title="", icon=True, width=100, height=100, scale=1, texture=""):
		# local variables
		self.name        = name
		self.title       = title
		self.width       = width
		self.height      = height
		self.x           = 0
		self.y           = 0
		self.is_attached = False
		self.attached_l  = -1
		self.attached_r  = -1
		
		# creating the app window
		self.app = ac.newApp(self.name)
		
		# default settings
		ac.drawBorder(self.app, 0)
		ac.setBackgroundOpacity(self.app, 0)
		if icon is False:
			ac.setIconPosition(self.app, 0, -10000)
		
		# applying settings
		ac.setTitle(self.app, self.title)
		ac.setBackgroundTexture(self.app, texture)
		ac.setSize(self.app, math.floor(self.width*scale), math.floor(self.height*scale))
		
	# PUBLIC METHODS
	
	def onRenderCallback(self, func):
		ac.addRenderCallback(self.app, func)
		return self
	
	def setBgOpacity(self, alpha):
		ac.setBackgroundOpacity(self.app, alpha)
		return self
		
	def border(self, value):
		ac.drawBorder(self.app, value)
		return self
	
	def setBgTexture(self, texture):
		ac.setBackgroundTexture(self.app, texture)
		return self
	
	def setPos(self, x, y):
		self.x = x
		self.y = y
		ac.setPosition(self.app, self.x, self.y)
		return self
	
	def getPos(self):
		self.x, self.y = ac.getPosition(self.app)
		return self
	

#-#####################################################################################################################################-#


class Label:

	# INITIALIZATION
	
	def __init__(self, window, text = ""):
		self.text      = text
		self.label     = ac.addLabel(window, self.text)
		self.size      = { "w" : 0, "h" : 0 }
		self.pos       = { "x" : 0, "y" : 0 }
		self.color     = (1, 1, 1, 1)
		self.bgColor   = (0, 0, 0, 1)
		self.fontSize  = 12
		self.align     = "left"
		self.bgTexture = ""
		self.opacity   = 1
		
	# PUBLIC METHODS
	
	def setText(self, text):
		self.text = text
		ac.setText(self.label, self.text)
		return self
	
	def setSize(self, w, h):
		self.size["w"] = w
		self.size["h"] = h
		ac.setSize(self.label, self.size["w"], self.size["h"])
		return self
	
	def setPos(self, x, y):
		self.pos["x"] = x
		self.pos["y"] = y
		ac.setPosition(self.label, self.pos["x"], self.pos["y"])
		return self
		
	def setColor(self, color):
		self.color = color
		ac.setFontColor(self.label, *self.color)
		return self
	
	def setFontSize(self, fontSize):
		self.fontSize = fontSize
		ac.setFontSize(self.label, self.fontSize)
		return self
	
	def setAlign(self, align = "left"):
		self.align = align
		ac.setFontAlignment(self.label, self.align)
		return self
	
	def setBgTexture(self, texture):
		self.bgTexture = texture
		ac.setBackgroundTexture(self.label, self.bgTexture)
		return self
	
	def setBgColor(self, color):
		ac.setBackgroundColor(self.label, *color)
		return self
	
	def setBgOpacity(self, opacity):
		ac.setBackgroundOpacity(self.label, opacity)
		return self
	
	def setVisible(self, value):
		ac.setVisible(self.label, value)
		return self

		
#-#####################################################################################################################################-#

	
class Button:

	# INITIALIZATION

	def __init__(self, window, clickFunc, width=60, height=20, x=0, y=0, text="", texture=""):
		self.width = width
		self.height = height
		self.x = x
		self.y = y
		self.button = ac.addButton(window, text)
		
		# adding default settings
		self.setSize(width, height)
		self.setPos(x, y)
		if texture != "":
			self.setBgTexture(texture)
		
		# default settings
		ac.drawBorder(self.button, 0)
		ac.setBackgroundOpacity(self.button, 0)
		
		# adding a click event
		ac.addOnClickedListener(self.button, clickFunc)
	
	# PUBLIC METHODS
	
	def setSize(self, width, height):
		self.width = width
		self.height = height
		ac.setSize(self.button, self.width, self.height)
		return self
	
	def setPos(self, x, y):
		self.x = x
		self.y = y
		ac.setPosition(self.button, self.x, self.y)
		return self
	
	def setBgTexture(self, texture):
		ac.setBackgroundTexture(self.button, texture)
		return self
		

#-#####################################################################################################################################-#


class Config:

	# INITIALIZATION
	
	def __init__(self, path, filename):
		self.file = path + filename
		self.parser = 0
		
		try:
			self.parser = configparser.RawConfigParser()
		except:
			ac.console("OV1: Config -- Failed to initialize ConfigParser.")
		
		# read the file
		self._read()
		
	# LOCAL METHODS
	
	def _read(self):
		self.parser.read(self.file)
	
	def _write(self):
		with open(self.file, "w") as cfgFile:
			self.parser.write(cfgFile)
	
	# PUBLIC METHODS
	
	def has(self, section=None, option=None):
		if section is not None:
			# if option is not specified, search only for the section
			if option is None:
				return self.parser.has_section(section)
			# else, search for the option within the specified section
			else:
				return self.parser.has_option(section, option)
		# if section is not specified
		else:
			ac.console("OV1: Config.has -- section must be specified.")
	
	def set(self, section=None, option=None, value=None):
		if section is not None:
			# if option is not specified, add the specified section
			if option is None:
				self.parser.add_section(section)
				self._write()
			# else, add the option within the specified section
			else:
				if not self.has(section, option) and value is None:
					ac.console("OV1: Config.set -- a value must be passed.")
				else:
					self.parser.set(section, option, value)
					self._write()
		# if sections is not specified
		else:
			ac.console("OV1: Config.set -- section must be specified.")
		
	
	def get(self, section, option, type = ""):
		if self.has(section) and self.has(section, option):
			# if option request is an integer
			if type == "int":
				return self.parser.getint(section, option)
			# if option request is a float
			elif type == "float":
				return self.parser.getfloat(section, option)
			# if option request is boolean
			elif type == "bool":
				return self.parser.getboolean(section, option)
			# it must be a string then!
			else:
				return self.parser.get(section, option)
		else:
			return -1
		
		
	def remSection(self, section):
		if self.has(section):
			self.parser.remove_section(section)
			self._write()
		else:
			ac.console("OV1: Config.remSection -- section not found.")
			
	def remOption(self, section, option):
		if self.has(section) and self.has(section, option):
			self.parser.remove_option(section, option)
			self._write()
		else:
			ac.console("OV1: Config.remOption -- option not found.")

