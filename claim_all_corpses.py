__author__ = "NullScript"
__version__ = "1.0.0" 

from AutoComplete import *

IGNORE_LIST = {0x0ECD, 0x0ECF}

def ClaimAllCorpses():
    corpseFilter = Items.Filter()
    corpseFilter.Enabled = True
    corpseFilter.IsCorpse = True
    corpseFilter.OnGround = True
    corpseFilter.Movable = False
    corpseFilter.RangeMin = -1
    corpseFilter.RangeMax = 8
    corpses = Items.ApplyFilter(corpseFilter)
    corpses = [c for c in corpses if c.ItemID not in IGNORE_LIST]
    
    if len(corpses) == 0:
        Player.HeadMessage(89, 'No corpses nearby.')
        return
    Player.HeadMessage(89, 'Claiming {} corpses.'.format(len(corpses)))
    
    Player.ChatSay(690, "[claim")
    for c in corpses:
        Journal.Clear( )
        Target.WaitForTarget(200, True)
        Target.TargetExecute(c)
        
        if Journal.Search('Target cannot be seen') or Journal.Search('Nothing happens') or Journal.Search('You did not earn'):
            Player.ChatSay(690, "[claim")
            Target.WaitForTarget(200, True)
        
        Misc.Pause(5)

    Target.WaitForTarget(200, True)
    if Target.HasTarget():    
        Target.Cancel()


ClaimAllCorpses()  