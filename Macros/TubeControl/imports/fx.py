from aTubeControl.imports.TubeUtil import *
from aTubeControl.imports.fx_table import FX_TABLE
from aTubeControl.imports.fx_table import FX_TABLE_MULTI
from aTubeControl.imports.fx_table import COLOR_TABLE
from aTubeControl.imports.fx_table import OSCILLATOR_OFF


RGB_INDEX = {
    "r": 0,
    "g": 1,
    "b": 2,
    "red": 0,
    "green": 1,
    "blue": 2,
}

def setColor(color_name):
    # Grab the values from the fx table
    color_data = COLOR_TABLE.get(color_name)

    if not color_data:
        Message("Check the preset name! %s not found!" % color_name)
        return

    _setFX(color_data, OSCILLATOR_OFF, True)


def is_same_delta_value(fx_data):
    return fx_data.get("r")[1][2] == fx_data.get("g")[1][2] == fx_data.get("b")[1][2]


def setFX(fx_name, force_all = False):
    # Grab the values from the fx table
    fx_data = FX_TABLE.get(fx_name)
    if fx_data:
        rgb_tuple, o_tuple = fx_data

        _setFX(rgb_tuple, o_tuple)
        return
    # or from the multi table
    fx_data = FX_TABLE_MULTI.get(fx_name)
    if fx_data:
        print "Going to set up this shiid"
        print fx_data
        # Get all selected channels or all TUBE channels
        channels = GetAllTubeCh(True, force_all)
        chase_values = {
            "r": 0,
            "g": 0,
            "b": 0,
            "all": 0
        }
        for ch in channels:
            name = GetChName(ch).lower()
            color_name = getChannelColor(name)
            fxd = fx_data.get(color_name)
            is_same_delta = is_same_delta_value(fx_data)
            if fxd:
                _setFXtoChannel(color_name, ch, fxd[0], fxd[1], chase_values, is_same_delta)
        return
    if not fx_data:
        Message("Check the preset name! %s not found!" % fx_name)
        return


def _setFX(rgb_tuple, o_tuple, force_all = False):
    if not rgb_tuple or not o_tuple:
        Message("Check the preset data!")
        return

    print "Setting up some FX!"
    print "Color: %s, %s, %s" % rgb_tuple
    # print "Channel:"
    # print " - enabled %s" % bool(ch_tuple[0])
    # print " - inverted %s" % bool(ch_tuple[1])
    print "Oscillator:"
    print " type - %s" % o_tuple[0]
    print " amount - %s" % o_tuple[1]
    print " chase - %s" % o_tuple[2]
    print " speed - %s" % o_tuple[3]
    print " shape - %s" % o_tuple[4]
    print "-------------"

    # Get all selected channels or all TUBE channels
    channels = GetAllTubeCh(True, force_all)
    print " got channels "
    print channels
    chase_value = 0
    for i, ch in enumerate(channels):
        # skip channels that are not tube fixtures
        if not isTubeChannel(ch):
            continue
        SetChEnabled(ch, 1)
        # set the colour for the given channel
        # and check if the value is 0
        channel_on = setColour(ch, rgb_tuple)

        # if the channel value is 0
        # disable the channel and don't apply
        # the oscillator values
        if not o_tuple[0]:
            # SetChEnabled(ch, 0)
            SetOscType(ch, 0)
            SetOscAmount(ch, 0)
            SetOscChase(ch, 0)
            SetOscSpeed(ch, 0)
            SetOscShape(ch, 0)
            continue
        # using this only for colours for now
        continue
        getOscChaseValue(chase_value, o_tuple[2])

        # print "The osc value is %s " % delta
        # Set the channel settings
        
        SetChInvert(ch, False)
        # and the oscillator settings
        SetOscType(ch, o_tuple[0])
        SetOscAmount(ch, o_tuple[1])
        SetOscChase(ch, getOscChaseValue(chase_value, o_tuple[2]))
        SetOscSpeed(ch, o_tuple[3])
        SetOscShape(ch, o_tuple[4])

        chase_value += o_tuple[2]


def _setFXtoChannel(color_name, ch, channel_value, o_tuple, chase_values, is_same_delta):
    # skip channels that are not tube fixtures
    if not isTubeChannel(ch):
        return
    SetChEnabled(ch, 1)

    # set the colour for the given channel
    # and check if the value is 0
    SetChVal(ch, channel_value)

    # if the channel value is 0
    # disable the channel and don't apply
    # the oscillator values
    if not o_tuple[0]:
        #SetChEnabled(ch, 0)
        SetOscType(ch, 0)
        SetOscAmount(ch, 0)
        SetOscChase(ch, 0)
        SetOscSpeed(ch, 0)
        SetOscShape(ch, 0)
        return
    # print "The osc value is %s " % delta
    new_value = getOscChaseValue(color_name, chase_values, o_tuple, is_same_delta)

    # Set the channel settings
    SetChEnabled(ch, 1)
    SetChInvert(ch, False)
    # and the oscillator settings
    SetOscType(ch, o_tuple[0])
    SetOscAmount(ch, o_tuple[1])
    SetOscChase(ch, new_value)
    SetOscSpeed(ch, o_tuple[3])
    SetOscShape(ch, o_tuple[4])


def getOscChaseValue(color_name, chase_values, o_tuple, is_same_delta):
    if is_same_delta:
        current_chase_value = chase_values["all"]
    else:
        current_chase_value = chase_values[color_name]
    delta_value = o_tuple[2]
    new_value = current_chase_value + delta_value
    # keep the value below 1.0, because 1.0 is the max value
    if new_value > 1:
        new_value = new_value - 1

    if is_same_delta:
        chase_values["all"] += delta_value
    else:
        chase_values[color_name] += delta_value
    return current_chase_value


def setColour(ch, rgb_tuple):
    """ Sets the correct rgb value for the given channels
        the incoming tuple must have the color values in this order
        (R, G, B)
     """
    name = GetChName(ch).lower()
    # adjust the value only if this selected
    # channel looks like the tube fixture channel
    if name and name.startswith("tube"):
        color = getChannelColor(name)
        value = rgb_tuple[RGB_INDEX.get(color)]
        if value is None:
            SetChEnabled(ch, 0)
            return False
        SetChEnabled(ch, 1)
        SetChVal(ch, value)

        if not value:
            return False
        return True
    return False


def getChannelColor(channel_name):
    return channel_name[6:].lower()


def isTubeChannel(ch, cmp_name="Tube"):
    name = GetChName(ch)
    if name and name.startswith(cmp_name):
        return True
    return False

