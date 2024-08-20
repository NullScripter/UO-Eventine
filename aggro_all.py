__author__ = "NullScript"
__version__ = "1.0.0" 

from AutoComplete import *
from AutoComplete import *
from System.Collections.Generic import List
from System import Byte

def GetNearbyEnemies(maxRange=1, ignore_list={0x02D4}):
    # Notorieties
    # 1: 'innocent' ('blue')
    # 2: 'ally' ('green')
    # 3: 'attackable' ('gray')
    # 4: 'criminal' ('gray')
    # 5: 'enemy' ('orange')
    # 6: 'murderer' ('red')
    # 7: 'npc'

    # 0x02D4= Annoying Thing

    enemyFilter = Mobiles.Filter()
    enemyFilter.Enabled = True
    enemyFilter.RangeMax = maxRange
    enemyFilter.Notorieties = List[Byte](bytes([3,4,5,6]))
    mobiles = Mobiles.ApplyFilter( enemyFilter )
    return [m for m in mobiles if m.MobileID not in ignore_list]


def AggroAll():       
    enemies = GetNearbyEnemies(25)
    for enemy in enemies:
        Mobiles.Message(enemy,0x21,'!!!')
        if enemy != None:
            Player.Attack( enemy )
            Misc.Pause(10)
       
AggroAll()
