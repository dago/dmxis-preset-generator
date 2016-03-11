
import sys
import os
from os import walk
from os import path
from shutil import copyfile

BASE_PATH = "/Library/Application Support/ENTTEC/DMXIS/Presets"
PRESET_FOLDER = "ZZZ Preset Library"
SOURCE_PATH = "%s/%s" % (BASE_PATH, PRESET_FOLDER)
PRESET_EXTENSION = ".prt"


original_files = []

# Read all filenames from the /ZZZ_PReset folder
for (dirpath, dirnames, filenames) in walk(SOURCE_PATH):
    original_files = filenames
    break

# temp dict so we don't have to loop too many times
preset_files = {}
for f in original_files:
    preset_files[f] = True


# loop through all other folders and REPLACE any
# files that have the same name
ALL_PRESET_DIRECTORIES = [] 
for (dirpath, dirnames, filenames) in walk(BASE_PATH):
    ALL_PRESET_DIRECTORIES = dirnames
    break

for dirname in dirnames:
    # skip the original folder
    if dirname == PRESET_FOLDER:
        continue

    d = "%s/%s" % (BASE_PATH, dirname)
    print "Handling folder - %s" % d
    print "--------------------------"

    files = [f for f in os.listdir(d)]
    for f in files:
        if f in preset_files and f.endswith(PRESET_EXTENSION):
            src = "%s/%s" % (SOURCE_PATH, f)
            dst = "%s/%s" % (d, f)
            print "------- copy ----------"
            print "from %s" % src
            print "to %s" % dst
            print "-------- end -------------"
            copyfile(src, dst)
