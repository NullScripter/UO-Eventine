__author__ = "NullScript"
__version__ = "1.0.0" 


# Script to create a persistent gump with all runes in a Runic Atlas

# SETTINGS
setX = 260
setY = 1180 
maxRows = 6
atlasSerialID = Misc.ReadSharedValue('mainRunicAtlas')
if atlasSerialID == 0:
    atlasSerialID = Target.PromptTarget( 'Select Runic Atlas')

    
# RUNIC ATLAS CLASS    
runicAtlasSpellOptions = {
    'Recall (Spell)': 4,
    'Recall (Charge)': 5,
    'Gate Travel': 6,
    'Sacred Journey': 7,
}

class AtlasEntry:
    def __init__(self, name, gumpPath):
        self.Name = name
        self.gumpPath = gumpPath
        
        
class RunicAtlas:
    def __init__(self, atlasSerialID, spellOption='Sacred Journey'):
        self.SerialID = atlasSerialID
        self.spellGumpID = runicAtlasSpellOptions[spellOption]
        
        self.runeList = self.scanRunicAtlas()
        self.runeDict = {r.Name: r.gumpPath for r in self.runeList} 
        
    def teleportToRuneName(self, runename, maxAttempts=2, attemptDelay=2000):
        px,py = Player.Position.X, Player.Position.Y
        for i in range(0, maxAttempts):           
            Items.UseItem(self.SerialID)
            for path in self.runeDict[runename]:
                Gumps.WaitForGump(878763590, 10000)
                Gumps.SendAction(878763590, path)   
            Misc.Pause(attemptDelay)
            
            if px != Player.Position.X and py != Player.Position.Y: 
                break          
            
    def teleportToRuneIndex(self, runeIndex, maxAttempts=2, attemptDelay=2000):
        px,py = Player.Position.X, Player.Position.Y
        for i in range(0, maxAttempts):
            Items.UseItem(self.SerialID)
            for path in self.runeList[runeIndex].gumpPath:
                Gumps.WaitForGump(878763590, 10000)
                Gumps.SendAction(878763590, path)  
            Misc.Pause(attemptDelay)
            
            if px != Player.Position.X and py != Player.Position.Y: 
                break
            
    def scanRunicAtlas(self):
        Items.UseItem(self.SerialID)
        gumpLines = Gumps.LastGumpGetLineList()
        runeList = []
        for pageNum in range(0,3): # 3 pages per atlas
            Gumps.WaitForGump(878763590, 5000)
            
            for lineNum in range(8,24): # 16 entries per page
                if gumpLines[lineNum] != 'Empty':
                    # path => gump buttons order to turn required pages followed by the correct rune to use 
                    runeList.append(AtlasEntry(
                        gumpLines[lineNum], [1150 for i in range(0, pageNum)] + [92 + lineNum + 16 * pageNum , self.spellGumpID]))
                        
            if pageNum < 2:
                Gumps.SendAction(878763590, 1150) # next page
                
        Gumps.WaitForGump(878763590, 5000)
        Gumps.CloseGump(878763590) 
        return runeList        
    
    
# SCRIPT
from math import trunc
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

    