import sys

BASE_PATH = "/Volumes/bootdrive/Library/Application Support/ENTTEC/DMXIS/Macros/aTubeControl"
FX_PATH = "%s/imports" % BASE_PATH
PRESET_PATH = "%s/2_FX" % BASE_PATH
COLOR_PATH = "%s/1_Colours" % BASE_PATH
SELECT_PATH = "%s/SelectTubes" % BASE_PATH
ADD_PATH = "%s/5_AddToSelection" % BASE_PATH



# import the FX  file path
if FX_PATH not in sys.path:
    sys.path.insert(0, FX_PATH)

from fx_table import FX_TABLE
from fx_table import FX_TABLE_MULTI
from fx_table import COLOR_TABLE
from fx_table import TUBE_AMOUNT
from fx_table import TUBE_GROUP_COUNT


# loop through the FX map and create python files
for fx in FX_TABLE:
    fname = "%s/%s.py" % (PRESET_PATH, fx)

    f = open(fname, 'w+')
    f.write('from aTubeControl.imports.fx import setFX\n')
    f.write('\n')
    f.write('setFX("%s")' % fx)
    f.write('\n')
    f.close()

# loop through the FX MULTI map and create python files
for fx in FX_TABLE_MULTI:
    fname = "%s/%s.py" % (PRESET_PATH, fx)

    f = open(fname, 'w+')
    f.write('from aTubeControl.imports.fx import setFX\n')
    f.write('\n')
    f.write('setFX("%s")' % fx)
    f.write('\n')
    f.close()

# loop through the FX map and create python files
for fx in COLOR_TABLE:
    fname = "%s/%s.py" % (COLOR_PATH, fx)

    f = open(fname, 'w+')
    f.write('from aTubeControl.imports.fx import setColor\n')
    f.write('\n')
    f.write('setColor("%s")' % fx)
    f.write('\n')
    f.close()

fname = "%s/AllTubes.py" % (SELECT_PATH)
f = open(fname, 'w+')
f.write('from aTubeControl.imports.TubeUtil import *\n')
f.write('\n')
f.write('selectChannels()')
f.write('\n')
f.close()


for i in range(1, TUBE_AMOUNT + 1):
    fname = "%s/Tube%s.py" % (SELECT_PATH, i)
    f = open(fname, 'w+')
    f.write('from aTubeControl.imports.TubeUtil import *\n')
    f.write('\n')
    f.write('selectTube(%s)' % i)
    f.write('\n')
    f.close()

for i in range(1, TUBE_AMOUNT + 1):
    fname = "%s/Tube%s.py" % (ADD_PATH, i)
    f = open(fname, 'w+')
    f.write('from aTubeControl.imports.TubeUtil import *\n')
    f.write('\n')
    f.write('selectTube(%s,unselect=False)' % i)
    f.write('\n')
    f.close()

c = 1
for i in range(1, TUBE_AMOUNT + 1):
    fname = "%s/FullTube%s.py" % (SELECT_PATH, i)
    f = open(fname, 'w+')
    f.write('from aTubeControl.imports.TubeUtil import *\n')
    f.write('\n')
    f.write('selectTubes([%s, %s])' % (c, c + TUBE_GROUP_COUNT - 1))
    f.write('\n')
    f.close()
    if c >= TUBE_AMOUNT:
        break
    c = c + TUBE_GROUP_COUNT
    print c
