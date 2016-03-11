#===============================================================
# DMXIS Macro (c) 2010 db audioware limited
#===============================================================

found=False
for ch in range(1,511):
	SelectCh(ch, 0)
for ch in range(16,48):
    SelectCh(ch, 1)
