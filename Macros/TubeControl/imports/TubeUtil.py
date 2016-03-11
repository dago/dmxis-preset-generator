import _DmxApi
from _DmxApi import *
import System.Helpers
from System.Helpers import *


#---------------------------------------------------
# Redirect stdout/stderr to DMXIS extension module
#    def write(self, s): dmxis.write(s)
#---------------------------------------------------
import sys


class Redirect:

    def write(self, s): _DmxApi.DmxisWrite(s)
sys.stdout = Redirect()
sys.stderr = Redirect()

print "Initialising DMXIS Python engine..."

#---------------------------------------------------
# Import DMXIS RGB utility methods
#---------------------------------------------------
import System.RGB
from System.RGB import *

#---------------------------------------------------
# Import general helper methods
#---------------------------------------------------
import System.Helpers
from System.Helpers import *


TUBES_PREFIX = "Tube"
PIXEL_COUNT_PER_TUBE = 16
CHANNELS_PER_PIXEL = 3

# Browns
BROWN = (165, 42, 42)

# Blues
TURQUOISE = (64, 244, 208)
BLUE = (0, 0, 255)

# Oranges
ORANGE = (255, 27, 0)

# Pinks
HOT_PINK = (255, 105, 180)

# Purples
PURPLE = (128, 0, 128)

# Whites
WHITE = (255, 255, 255)

# Yellows
YELLOW = (255, 255, 0)

# Reds
RED = (255, 0, 0)

# Greens
GREEN = (0, 255, 0)


FX_OSC = {
    "red_rain": {
        1: {
            "channel_value": 0,
            "osc": {
                "type": 2,
                "amount": 1,
                "chase": 0.5,
                "speed": 7,
                "shape": 0.1
            }
        }
    }
}


def getChannelColor(ch):
    return ch[6:].lower()


def isTubeChannel(ch, cmp_name="Tube"):
    name = GetChName(ch)
    if name:
        if name.startswith(cmp_name):
            return True
    return False


def isTubeNumber(ch, nr):
    return isTubeChannel(ch, cmp_name="Tube%s" % nr)


def isInTubeChannels(ch, channels):
    isit = False
    for poop in channels:
        isit = isTubeChannel(ch, cmp_name="Tube%s" % poop)
        if isit:
            return isit
    return isit


def deselectChannels():
    # Deselect other channels
    for ch in range(0, 511):
        SelectCh(ch, 0)


def selectChannels():
    for ch in range(0, 511):
        if isTubeChannel(ch):
            SelectCh(ch, 1)
        else:
            SelectCh(ch, 0)


def selectTube(nr, unselect=True):
    for ch in range(0, 511):
        if isTubeNumber(ch, nr):
            SelectCh(ch, 1)
        elif unselect:
            SelectCh(ch, 0)


def selectTubes(ch_names):
    for ch in range(0, 511):
        if isInTubeChannels(ch, ch_names):
            SelectCh(ch, 1)
        else:
            SelectCh(ch, 0)


def setTubesRGB(rgb_tuple):
    """ Sets the LED tubes to specific RGB value """
    r, g, b = rgb_tuple
    print "Setting tubes to RGB values (%s, %s, %s)" % (r, g, b)
    RgbColour(r, g, b)


def selectPixelsByColor(color=None, deselect=True, ch_selected=True):
    """ Selects the given channel in the pixel
     - RGB """
    for ch in range(0, 511):
        if isTubeChannel(ch):
            name = GetChName(ch).lower()
            if name:
                cn = getChannelColor(name)
                if cn == color:
                    SelectCh(ch, ch_selected)
                elif deselect:
                    SelectCh(ch, not ch_selected)


def selectWithOffset(offset=2, pixel_index=None, deselect=True):
    """ """
    print "Selecting pixel channel with index %s" % (pixel_index)
    if deselect:
        deselectChannels()
    for i in PIXEL_INDEXES[0::offset]:
        if pixel_index is None:
            SelectCh(i - 1, 1)
            SelectCh(i, 1)
            SelectCh(i + 1, 1)
        else:
            SelectCh(i + pixel_index - 1, 1)


def deselectTubeChannels(pixel_index=0):
    """ Deselects the given channel in the pixel
        G = 0
        R = 1
        B = 2
     - RGB """

    for ch in range(0, 511):
        if isTubeChannel(ch):
            SetChVal(ch, 0)


def setFXOld(fx_type):
    fx_data = FX_OSC.get(fx_type)
    print fx_data
    # set the FX for each pixel
    for ch in range(0, 511):
        # loop each channel and set it to value or 0
        for n in [0, 1, 2]:
            ch = i - 1 + n
            # set the new values or reset all to 0
            if n in (fx_data or []):
                fx = fx_data.get(n)
                SetChVal(ch, fx.get("channel_value") or 0)
                # the FX data has the channel value and the
                # oscillator values
                osc = fx.get("osc")
                setOscillatorForPixel(
                    i - 1 + n,
                    osc.get("type"),
                    osc.get("amount"),
                    osc.get("chase"),
                    osc.get("speed"),
                    osc.get("shape"),
                )
            else:
                SetChVal(ch, 0)
                SetOscType(ch, 0)


def setOscillatorForPixel(ch, osc_type,
                          osc_amount, osc_chase, osc_speed, osc_shape):
    """ Set the oscillator for given pixel offset """
    # loop through the pixels and set the oscillator
    # values
    if ch <= 511:
        # Square
        SetOscType(ch, osc_type)
        SetOscAmount(ch, osc_amount)
        # chase
        SetOscChase(ch, osc_chase)
        SetOscSpeed(ch, osc_speed)
        # shape
        SetOscShape(ch, osc_shape)


def RgbColour(r, g, b):
    sel = GetAllSelCh(False)
    if len(sel) == 0:
        Message("Select some RGB channels first!")

    for ch in sel:
        name = GetChName(ch).lower()
        if name:
            color = getChannelColor(name)
            if color == "r" or color == "red":
                SetChVal(ch, r)
            elif color == "g" or color == "green":
                SetChVal(ch, g)
            elif color == "b" or color == "blue":
                SetChVal(ch, b)


def GetAllTubeCh(doAll, force_all):
    sc = []
    ns = GetNumSelCh()

    if (ns == 0 and doAll) or force_all:
        ns = 512
        for i in range(ns):
            if isTubeChannel(i):
                sc.append(i)
        return sc

    for i in range(ns):
        if isTubeChannel(i):
            sc.append(GetSelCh(i))
    return sc
