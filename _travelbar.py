__author__ = "NullScript"
__version__ = "1.0.0" 


# Script to create a persistent gump with all runes in a Runic Atlas

# SETTINGS
setX = 260
setY = 1180 
maxRows = 5
atlasSerialID = Misc.ReadSharedValue('mainRunicAtlas')
if atlasSerialID == None:
    atlasSerialID = Target.PromptTarget( 'Select Runic Atlas')


# SCRIPT
from math import trunc
from Scripts.utilities.runic_atlas import RunicAtlas
gumpid = 989898

def GenTravelBarGump(atlas): 
    gd = Gumps.CreateGump(movable=False,closable=False)
    Gumps.AddPage(gd, 0); 
   
    bWidth = 128
    bHeight = 27
    
    for i, entry in enumerate(atlas.runeList):
        currRow, currCol = i % maxRows, trunc(i / maxRows)
        Gumps.AddButton(gd,currCol*bWidth, currRow*bHeight, 105556, 105557, i, 1, 0)
        Gumps.AddLabelCropped(gd, 15 + currCol*bWidth, 4 + currRow*bHeight, bWidth, bHeight, 1096, entry.Name)
    
    return gd
        
    
def buttonChecker(atlas): 
    Gumps.WaitForGump(gumpid, 60000) 
    gd = Gumps.GetGumpData(gumpid) 
    Gumps.CloseGump(gumpid) 
    
    if gd.buttonid != -1:
        Player.SetWarMode(False)
        atlas.teleportToRuneIndex(gd.buttonid)
        
        
Gumps.CloseGump(gumpid) 
atlas = RunicAtlas(atlasSerialID)
travelBar = GenTravelBarGump(atlas)

while True:
    Gumps.SendGump(gumpid, Player.Serial, setX, setY, travelBar.gumpDefinition, travelBar.gumpStrings) 
    buttonChecker(atlas)
    Misc.Pause(100)

    