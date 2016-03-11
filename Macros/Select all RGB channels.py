#===============================================================
# DMXIS Macro (c) 2010 db audioware limited
#===============================================================

found=False
for ch in range(1,511):
    nm = GetChName(ch).lower()
    if nm in ["r", "g", "b"]:
        SelectCh(ch, 1)
        found=True
    else:
        SelectCh(ch, 0)
        
if not found: Message("No RGB channels found!")