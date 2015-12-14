import math

# UNITS CONVERSION

def millisToString(millis):
	hours, x = divmod(int(millis), 3600000)
	mins, x  = divmod(x, 60000)
	secs, x  = divmod(x, 1000)
	return "%d.%03d" % (secs, x) if mins == 0 else "%d:%02d.%03d" % (mins, secs, x)


def C_to_F(C):
	return 9 / 5 * C + 32


def L_to_Gal(val, type = "US"):
	if type == "US":
		return val * 0.264172
	elif type == "UK":
		return val * 0.219969


def PSI_to(val, to = "BAR"):
	if to == "BAR":
		return val * (6.8948 * 10**-2)
	elif to == "KPA":
		return val * 6.89475729
	else:
		return val
	

#-#####################################################################################################################################-#


# COLOR CONVERSION

def rgb(color, a = 1, bg = False):
	r = color[0] / 255
	g = color[1] / 255
	b = color[2] / 255
	if bg == False:
		return r, g, b, a
	else:
		return r, g, b


def hsv2rgb(h, s, v):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return r, g, b


def rgb2hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df/mx
    v = mx
    return h, s, v