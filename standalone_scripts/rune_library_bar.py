__author__ = "NullScript"
__version__ = "1.3.0" 


###### Personal Settings (change them to yours) ######
RUNIC_ATLAS_SERIALS = [
    0x4028B889, # Main Atlas
    0x4034820D, # Monsters 1
    0x40362F9C, # Monsters 2
    0x40348243, # Animals
    0x4024CA6E, # Quests
]
POOF_BAAL = None # (Optional) Put a Puffball Serial here

POSITION_X = 150 # Gump position 
POSITION_Y = 1158 # Gump position 
ROWS = 6 # Number of rune per rows 


TRAVEL_METHOD = 'Sacred Journey'
MAX_TRIES = 2 # In recall/sacred journey fail


###### Script ######
from AutoComplete import *

GUMPID = 979797
TAB_BUTTONID_OFFSET = 100


class AtlasEntry:
    def __init__(self, name, gumpPath):
        self.Name = name
        self.gumpPath = gumpPath
                

class RunicAtlas:
    def __init__(self, atlasSerialID, spellOption=TRAVEL_METHOD):
        runicAtlasSpellOptions = {
            'Recall (Spell)': 4,
            'Recall (Charge)': 5,
            'Gate Travel': 6,
            'Sacred Journey': 7,
        }
        self.SerialID = atlasSerialID
        self.spellGumpID = runicAtlasSpellOptions[spellOption]
        
        self.runeList = self.scanRunicAtlas()
        self.runeDict = {r.Name: r.gumpPath for r in self.runeList} 
    

    def openRunicAtlas(self):
        Gumps.CloseGump(878763590)
        Items.UseItem(self.SerialID)
        Gumps.WaitForGump(878763590, 2000)

        while not Gumps.HasGump(878763590): # to solve 'too fast' to use
            Gumps.CloseGump(878763590)
            Items.UseItem(self.SerialID)
            Gumps.WaitForGump(878763590, 1000)
            

    def teleportToRuneName(self, runename, maxAttempts=MAX_TRIES, attemptDelay=500):
        if POOF_BAAL: Items.UseItem(POOF_BAAL)
        px,py = Player.Position.X, Player.Position.Y
        for i in range(0, maxAttempts):           
            self.openRunicAtlas()
            for path in self.runeDict[runename]:
                Gumps.WaitForGump(878763590, 6000)
                Gumps.SendAction(878763590, path) 
            Gumps.CloseGump(878763590) 

            if px != Player.Position.X or py != Player.Position.Y or Journal.Search('blocked'): 
                break
            Misc.Pause(attemptDelay) 
        Gumps.CloseGump(878763590) 


    def teleportToRuneIndex(self, runeIndex, maxAttempts=MAX_TRIES, attemptDelay=500):
        if POOF_BAAL: Items.UseItem(POOF_BAAL)
        px,py = Player.Position.X, Player.Position.Y
        for i in range(0, maxAttempts):
            self.openRunicAtlas()
            for path in self.runeList[runeIndex].gumpPath:
                Gumps.WaitForGump(878763590, 6000)
                Gumps.SendAction(878763590, path) 
            Gumps.CloseGump(878763590) 

            if px != Player.Position.X or py != Player.Position.Y or Journal.Search('blocked'): 
                break
            Misc.Pause(attemptDelay)
        Gumps.CloseGump(878763590) 
    

    def scanRunicAtlas(self):
        self.openRunicAtlas()
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


class RunicLibraryEntry():
    def __init__(self, atlas):
        self.Serial = atlas.Serial
        self.Name = list(atlas.Properties)[-1].ToString()
        if 'Crafted' in self.Name or 'Exceptional' in self.Name or 'Weight' in self.Name:
            self.Name = 'Unnamed Atlas'

        self.LoadedAtlas = None

    def GetRunicAtlas(self):
        if self.LoadedAtlas: return self.LoadedAtlas
        self.LoadedAtlas = RunicAtlas(self.Serial)
        return self.LoadedAtlas


def GenRuneLibraryGump(runic_library, active_atlas_idx): 
    atlas = runic_library[active_atlas_idx].GetRunicAtlas()

    gd = Gumps.CreateGump(movable=False,closable=False)
    bWidth = 128
    bHeight = 27

    for i, entry in enumerate(runic_library):
        currRow, currCol = i % 1, i // 1
        Gumps.AddButton(gd,currCol*bWidth, currRow*bHeight, 105557, 105556, TAB_BUTTONID_OFFSET + i, 1, 0)
        color = 45 if i == active_atlas_idx else 0x448
        Gumps.AddLabelCropped(gd, 15 + currCol*bWidth, 4 + currRow*bHeight, bWidth-25, bHeight, color, entry.Name)

    rowsOffset = len(runic_library) // ROWS +  (1 if len(runic_library) % ROWS else 0)
    for i, entry in enumerate(atlas.runeList):
        currRow, currCol = rowsOffset + i % ROWS, i // ROWS
        Gumps.AddButton(gd,currCol*bWidth, 5 + currRow*bHeight, 105556, 105557, i, 1, 0)
        Gumps.AddLabelCropped(gd, 15 + currCol*bWidth, 9 + currRow*bHeight, bWidth-25, bHeight, 1096, entry.Name)
    
    return gd
  

active_atlas_idx = 0
def ButtonChecker(runic_library): 
    global active_atlas_idx
    Gumps.WaitForGump(GUMPID, 60000) 
    gd = Gumps.GetGumpData(GUMPID) 
    Gumps.CloseGump(GUMPID) 
    
    if gd.buttonid >= TAB_BUTTONID_OFFSET:
        active_atlas_idx = gd.buttonid - TAB_BUTTONID_OFFSET
    elif gd.buttonid >= 0:
        Player.SetWarMode(False)
        atlas = runic_library[active_atlas_idx].GetRunicAtlas()
        atlas.teleportToRuneIndex(gd.buttonid)


def ManageRuneLibraryBar():
    runic_library = []
    for serial in RUNIC_ATLAS_SERIALS:
        atlas = Items.FindBySerial(serial)
        if atlas is None:
            Misc.SendMessage(f'Runic Atlas {serial} not found!', 0x21)
            continue
        runic_library.append(RunicLibraryEntry(atlas))
        
    if len(runic_library) == 0:
        return Misc.SendMessage('No Runic Atlas available! Please check the settings!', 0x21)

    while True:
        if Player.IsGhost:
            Misc.Pause(1000)
            continue

        gump = GenRuneLibraryGump(runic_library, active_atlas_idx)
        Gumps.SendGump(GUMPID, Player.Serial, POSITION_X, POSITION_Y, gump.gumpDefinition, gump.gumpStrings) 
        ButtonChecker(runic_library)
        Misc.Pause(10)


ManageRuneLibraryBar()
