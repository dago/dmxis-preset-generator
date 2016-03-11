""" Generate random pixel colors """
from aTubeControl.imports.TubeUtil import *

channels = GetAllSelCh(True)
delta_store = {}
for ch in channels:
    if isTubeChannel(ch):
        SetOscType(ch, 0)
        name = GetChName(ch).lower()
        color_name = getChannelColor(name)

        if color_name == "g" and not ch % 4:
            SetChVal(ch, 255)
        else:
            SetChVal(ch, 0)


