from aTubeControl.imports.TubeUtil import *


def getOscDelta():
    """ Return the delta between the next channel with osc enabled"""
    tmp_channels = GetAllSelCh(True)
    delta_store = {}
    for ch in tmp_channels:
        if isTubeChannel(ch) and GetOscType(ch):
            name = GetChName(ch).lower()
            color_name = getChannelColor(name)
            osc_chase = GetOscChase(ch)

            if osc_chase and color_name not in delta_store:
                for x in range(ch + 1, 512):
                    if isTubeChannel(x) and GetOscType(x):
                        namex = GetChName(x).lower()
                        color_name = getChannelColor(namex)
                        osc_chasex = GetOscChase(x)
                        chase_value = abs(osc_chase - osc_chasex)
                        delta_store[color_name] = chase_value
                        if "first" not in delta_store:
                            delta_store["first"] = chase_value
                        break

            if len(delta_store) == 4:
                break
    return delta_store

# Get all selected channels
channels = GetAllSelCh(False)

# if no channels are selected, get first RGB tube channels
if len(channels) == 0:
    # Message("Select some RGB channels first!")
    tmp_channels = GetAllSelCh(True)
    for ch in tmp_channels:
        if isTubeChannel(ch):
            channels.append(ch)
        if len(channels) == 3:
            break

printit = True


pr_channels = 0

delta_store = getOscDelta()
print delta_store

print
print 
print "------- Channel Values ---------"

for ch in channels:
    name = GetChName(ch).lower()
    color_name = getChannelColor(name)

    r = 0
    g = 0
    b = 0

    osc_type = 0
    osc_amount = 0
    osc_chase = 0
    osc_speed = 0
    osc_shape = 0

    if printit and False:
        print "Channel settings!"
        print "Name: %s" % name
        print "Color: %s" % color_name
        print "Value: %s" % GetChVal(ch)
        print "enabled: %s" % GetChEnabled(ch)
        print "Oscillator:"
        print " type - %s" % GetOscType(ch)
        print " amount - %s" % GetOscAmount(ch)
        print " chase - %s" % GetOscChase(ch)
        print " speed - %s" % GetOscSpeed(ch)
        print " shape - %s" % GetOscShape(ch)

    # grab at least one rgb value
    if color_name == "r":
        r = GetChVal(ch)
        pr_channels += 1
    elif color_name == "g":
        g = GetChVal(ch)
        pr_channels += 1
    elif color_name == "b":
        b = GetChVal(ch)
        pr_channels += 1

    if GetOscType(ch):
        osc_type = GetOscType(ch)
        osc_amount = float("{0:.4f}".format(GetOscAmount(ch)))
        osc_chase = float("{0:.4f}".format(delta_store.get(color_name) or GetOscChase(ch)))
        osc_speed = GetOscSpeed(ch)
        osc_shape = float("{0:.4f}".format(GetOscShape(ch)))

    print "Color: " + color_name
    print "-------------"
    osc_values = "(%s, %s, %s, %s, %s)" % (osc_type, osc_amount, osc_chase, osc_speed, osc_shape)


    print "(%s, %s)" % ((r, g, b), osc_values)
    if r or g or b:
        print "(%s, %s)" % (r or g or b, osc_values)
    else:
        print "(%s, %s)" % (0, osc_values)
    print
    print
    if pr_channels == 3:
        break

