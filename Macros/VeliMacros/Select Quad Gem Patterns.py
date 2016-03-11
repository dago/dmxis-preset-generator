#===============================================================
# DMXIS Macro (c) 2010 db audioware limited
#===============================================================

found=False
for ch in range(1,511):
	SelectCh(ch, 0)
for ch in range(1,5):
    nm = GetChName(ch).lower()
    if nm in ["pattern"]:
        SelectCh(ch, 1)
