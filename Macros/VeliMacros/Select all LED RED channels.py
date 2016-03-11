#===============================================================
# DMXIS Macro (c) 2010 db audioware limited
#===============================================================

found=False
for ch in range(1,511):
	SelectCh(ch, 0)
for ch in range(16,48):
    nm = GetChName(ch).lower()
    if nm in ["r"]:
        SelectCh(ch, 1)
