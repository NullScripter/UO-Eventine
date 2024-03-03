__author__ = "NullScripter"
__version__ = "0.9.0" 

# TODOs:
# 1) test other spells. Only tested with 'Sacred Journey' (default option)

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
