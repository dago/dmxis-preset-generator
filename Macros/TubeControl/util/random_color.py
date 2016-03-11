""" Generate random pixel colors """
from aTubeControl.imports.TubeUtil import *
import random

channels = GetAllSelCh(True)
delta_store = {}
for ch in channels:
    if isTubeChannel(ch):
        SetChVal(ch, random.randint(0, 255))
        SetOscType(ch, 0)
