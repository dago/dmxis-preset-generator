#===============================================================
# DMXIS Macro (c) 2010 db audioware limited
#===============================================================

#for ch in [36, 40, 44, 48, 52, 56, 60, 64]:
#    SelectCh(ch-1, 1)

found=False
for ch in range(1,511):
    nm = GetChName(ch).lower()
    if nm=="dim":
        SelectCh(ch, 1)
        found=True
    else:
        SelectCh(ch, 0)
        
if not found: Message("No RGB channels found!")