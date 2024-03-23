__version__ = "1.2.0" 

# Zodiac Aries (Mar 21 - April 19)
#
# Script to "harvest" narby animals for Aries quest. 
# Automatically sheer nearby sheeps and attack nearby bears and deers.

# SCRIPT NOTES:
# 1) You need to walk around yourself (or create a script to route relevant areas)
# 2) It tries to patchfind to the animal. 
#   (Simple but imperfect patchfinding, but it will not freeze or hinder manual movement)
# 3) It stops for ~2s after killing a bear/deer before going to the next animal (if one is nearby)
#   (I use a melee weapon, so it gives me time kill and autolooter to loot the Fat)


# SCRIPT CONFIG
MODES = {
    'HarvestNearbyAnimals', # Quest Steps 1-3 
    'MakeFineWool',         # Quest Steps 6-10
    'MakeFineBolt',         # Quest Steps 11
}
MODE = 'HarvestNearbyAnimals'


# QUEST STEPS:
# * Craft 1x 'Wool Washing Station': Carpentry > Tailoring & Cooking > (page 2)
# * Craft 1x 'Scouring Through': Carpentry > Tailoring & Cooking > (page 3)
# * Craft 1x 'Wool Roller': Carpentry > Other > (page 4)
# * Craft ?x 'Sheep Shearing Scissors': Tinkering > Tools > (page 6)
#
# 1) Sheer 300 sheeps to get 300x'Fresh Fleece'
# 2) Kill deers until 300x'Deer Fat'
# 3) Kill bears until 300x'Bear Fat'   
#
# 4) Craft 300 x 'potash': Alchemy > Ingredients > (page 1)
# 5) Craft 300 x 'detergent': Alchemy > Ingredients > (page 1)
# 6) Use 'Wool Washing Station' (to convert 'Fresh Fleece' into 'Washed Fleece')
# 7) Use 'detergent' and target 'Scouring Through'
# 8) Use 'Scouring Through' (to convert 'Washed Fleece' into 'Clean Fleece')
# 9) Use 'Rolled Wool' (to convert 'Clean Fleece' into 'Rolled Wool')
# 10) Use 'Rolled Wool' and target a 'Spinning Wool' station (to make 'Ball of Fine Wool')
# 11) Use 'Ball of Fine Wool' and target a '(Colored) Loom' (to make 'Bolt of Fine Wool')
# 12) Craft 100x 'Woolly Jumper': Tailoring > Shirts and Pants > (page 5)



#### Animal Harvesting Scripts ###

from System.Collections.Generic import List
from System import Int32

sheeps = [0x00CF]
bears = [0x00D3, 0x00D4, 0x00D5, 0x00A7]
deers = [0x00EA, 0x00ED]
relevantAnimals = sheeps + bears + deers

def FindRelevantAnimal():
    animalFilter = Mobiles.Filter()
    animalFilter.Enabled = True
    animalFilter.Bodies = List[Int32](relevantAnimals)
    animalFilter.RangeMin = 0
    animalFilter.RangeMax = 22
    animalFilter.IsHuman = 0
    animalFilter.IsGhost = 0
    mobiles = Mobiles.ApplyFilter( animalFilter )
    
    # Aggro all bears and deers and return nearest animal
    for m in mobiles:
        if 'bear' in m.Name or m.Name in {'a great hart', 'a hind'}:  
            Player.Attack(m)      
            Misc.Pause(50)
    return Mobiles.Select(mobiles, 'Nearest') if len(mobiles)>0 else None
        
    
def WalkDirection( direction ):
    playerPosition = Player.Position
    if Player.Direction != direction:
        Player.Walk( direction )
    Player.Walk( direction )
    
    
def WalkToMobile( mobile, maxDistanceToMobile = 1, startPlayerStuckTimer = False ): 
    Mobiles.Message(mobile,(Player.DistanceTo( mobile ) * 10) % 255,'meep!',False)
    mobilePosition = mobile.Position
    playerPosition = Player.Position
    directionToWalk = ''
    if mobilePosition.X > playerPosition.X and mobilePosition.Y > playerPosition.Y: directionToWalk = 'Down'
    if mobilePosition.X < playerPosition.X and mobilePosition.Y > playerPosition.Y: directionToWalk = 'Left'
    if mobilePosition.X > playerPosition.X and mobilePosition.Y < playerPosition.Y: directionToWalk = 'Right'
    if mobilePosition.X < playerPosition.X and mobilePosition.Y < playerPosition.Y: directionToWalk = 'Up'
    if mobilePosition.X > playerPosition.X and mobilePosition.Y == playerPosition.Y: directionToWalk = 'East'
    if mobilePosition.X < playerPosition.X and mobilePosition.Y == playerPosition.Y: directionToWalk = 'West'
    if mobilePosition.X == playerPosition.X and mobilePosition.Y > playerPosition.Y: directionToWalk = 'South'
    if mobilePosition.X == playerPosition.X and mobilePosition.Y < playerPosition.Y: directionToWalk = 'North'

    if startPlayerStuckTimer:
        Timer.Create( 'playerStuckTimer', playerStuckTimerMilliseconds )
        
    playerPosition = Player.Position
    WalkDirection( directionToWalk )

    newPlayerPosition = Player.Position
    if playerPosition == newPlayerPosition and not Timer.Check( 'playerStuckTimer' ):
        if Player.Direction == 'Up':
            (Player.Walk( 'Down' ) for i in range (5))
        elif Player.Direction == 'Down':
            (Player.Walk( 'Up' ) for i in range(5))
        elif Player.Direction == 'Right':
            (Player.Walk( 'Left' ) for i in range(5))
        elif Player.Direction == 'Left':
            (Player.Walk( 'Right' ) for i in range(5))
        Timer.Create( 'playerStuckTimer', 5000 )
    elif playerPosition != newPlayerPosition:
        Timer.Create( 'playerStuckTimer', 5000 )
        
    if Player.DistanceTo( mobile ) > 25: # Moved too far away
        return False

    if Player.DistanceTo( mobile ) > maxDistanceToMobile:
        Misc.Pause( 100 )
        WalkToMobile( mobile, maxDistanceToMobile )

    return True


def HarvestNearbyAnimals():
    animal = FindRelevantAnimal()
    if animal is None:
        return Misc.Pause(3000)
    
    if 'sheep' in animal.Name:
        Player.HeadMessage(60,'Sheep with wool found')
        if WalkToMobile(animal):
            sheers = Items.FindByName('Sheep Shearing Scissors',-1,Player.Backpack.Serial,3,True)
            if sheers is None: return Player.HeadMessage(40,'Sheep Shearing Scissors not found')          
            Items.UseItem(sheers)
            Target.WaitForTarget(10000, False)
            Target.TargetExecute(animal)
    elif 'bear' in animal.Name or animal.Name in {'a great hart', 'a hind'}:  
        Player.HeadMessage(60,'Attacking ' + animal.Name)
        Player.Attack(animal)
        if WalkToMobile(animal):
            Misc.Pause(2000)
    
    Misc.Pause(500)

    
#### Crafring Scripts ###
    
def MakeFineWool():
    # (Quest steps 6 to 10) Use all crafting stations in order. 
    # From 'Fresh Fleece' to 'Ball of Fine Wool' 
    # Using stations at Numem`s house [TODO: update Serials or use ItemFilter to locate]
    
    Items.UseItem(0x40490B88) # Rinsing Trough Serial
    detergent = Items.FindByID(0xA3E8,-1,Player.Backpack.Serial,1,True)
    Items.UseItem(detergent)
    Target.WaitForTarget(1000, False)
    Target.TargetExecute(0x40490C91) # Scouring Rrough water Serial
    Items.UseItem(0x40490C88) # Scouring Rrough Serial
    Items.UseItem(0x40490BD4) # Wool roller Serial
    rolledWool = Items.FindByID(0xACF8,0,Player.Backpack.Serial,1,True)
    Items.UseItem(rolledWool)
    Target.WaitForTarget(1000, False)
    Target.TargetExecute(0x408E1B86)
    Misc.Pause(5500)

    
def FindLoom():
    filter = Items.Filter()
    filter.RangeMax = 3
    filter.Name = 'upright loom'
    items = Items.ApplyFilter(filter)
    return items[0]
        
    
def MakeFineBolt():
    # (Quest step 11) 'Bolt of Fine Wool' using Colored Loom 
    # Using loom coordinates at Numem`s house [TODO: update (852, 1152 ,32 ,1231) floor position]
    # Retriving and re-placing the loom at every bolt (Colored Loom bug)
    
    # Retrive Loom
    hatchet = Items.FindByID(0x0F43,0,Player.Backpack.Serial,1,True)
    Items.UseItem(hatchet)
    Target.WaitForTarget(1000, False)
    Target.TargetExecute(FindLoom())
    Misc.Pause(500)
    
    # Put Loom back on the floor
    loomDeed = Items.FindByName('Colored Loom (east)',-1,Player.Backpack.Serial,1,True) 
    Items.UseItem(loomDeed)
    Target.WaitForTarget(1000, False)
    Target.TargetExecute(852, 1152 ,32 ,1231) # Coordinate (Static)
    Misc.Pause(500)
    
    
    # Create Bolt
    for i in range(3):
        ballWool = Items.FindByID(0x0E1D,0x0436,Player.Backpack.Serial,1,True)
        Items.UseItem(ballWool)
        Target.WaitForTarget(1000, False)
        Target.TargetExecute(FindLoom())
        
    Misc.Pause(1000)
    
    
#### Loop ###    
while True:
    if MODE not in MODES: break
    
    if MODE == 'HarvestNearbyAnimals':
        HarvestNearbyAnimals()
    elif MODE == 'MakeFineWool':
        MakeFineWool()
    elif MODE == 'MakeFineBolt':
        MakeFineBolt()
