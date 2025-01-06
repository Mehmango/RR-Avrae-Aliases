"""
Default Monster AI for AI Monsters with Battlemaps by @Mehmango and @.steamed

This module contains the basic behavior functions for general use and some monster functions. This is far from a comprehensive list, just a starting point!
Use this module as a template when creating your own monster AI.

* THINGS YOUR MODULE WILL NEED TO BE COMPATIBLE:
* - Your monster functions should have the same required parameters as the goblin function below, as well as **kwargs.
* - Your module needs to implement the FUNCTION constant dictionary and getFunction() function at the bottom of the file, as seen below
*   - The function names in FUNCTION are case sensitive

"""

CURRENT = combat().current
TILE_SIZE = 5
    
def goblin(mapInfo, combatantInfo, mapGrid, convertCoordinates, getDistance, scale=1, speed=30, meleeRange=5, rangedRange=80, **kwargs):
    """
    * Examples of the structures of attributes below may not be accurate. They are my best guesses from reading the !map alias code and other documentation.
    * Let me know if corrections are needed
    mapInfo: Dictionary containing map info, including:
        - size (eg: "10x10")
        - walls ([f"-c{wallColor}{wall}]", eg: [f"-crB3-oD3", f"-cD12E12"])
        - objects ([{objectLocation}{objectColor}{objectId}], eg: ["A1b$la", "B2r$ow"])
        - fow ([coordinate[:coordinate]], eg: ["A1:B3", "C4"])
        
    combatantInfo: Dictionary containing information on all combatants on the map. Each key is the combatant's name. Each item is also a dictionary, including:
        - location (eg: "A1")
        - effect#, eg: effect, effect2 ({effectName} / {effectTargetName}, eg: "Call Lightning / GO1")
        - overlay#, eg: overlay, overlay2 ({shape}{size}{colour (optional)}{target}, eg: "c30bI4", "co20~ffc1fa{aim}", "s20r{targ}")
        
    mapGrid: An X:Y grid representing the current map (eg: Coordinate B4 will be represented by mapGrid[1][5])
    
    convertCoordinates: Converts a set of coordinates from letter number representation to (x, y) representation, or vice versa. Takes a set of coordinates as an argument:
        - coordinates: A set of coordinates represented like "A1" or like (0,0)
        
    getDistance: A function that returns the distance between two coordinates or two combatants or between a coordinate and combatant in ft. Takes two arguments:
        - a: The first coordinate or combatant (eg: "A1" or (0,0) or "Goblin1")
        - b: The second coordinate or combatant (eg: "A1" or (0,0) or "Goblin1")
        
    scale: The scale that will be applied to the values calculated for each coordinate by this function. Useful for adjusting the function's sensitivity to sub-functions
    
    **kwargs: For future support
    
    Returns an X:Y grid representing the current map. Each element in the grid should contain an integer representing the calculated value of the position
    """ 
    mapGrid = basic(mapInfo, combatantInfo, mapGrid, convertCoordinates, getDistance, speed=speed)
    mapGrid = rangedAttacker(mapInfo, combatantInfo, mapGrid, convertCoordinates, getDistance, scale=100, speed=speed, meleeRange=meleeRange, rangedRange=rangedRange)
    # mapGrid = meleeAttacker(mapInfo, combatantInfo, mapGrid, convertCoordinates, getDistance, scale=100, meleeRange=meleeRange)
    
    # monsterCoordinates = combatantInfo[CURRENT.name]['location']
    # allPlayerNames = []
    # for combatant in combat().combatants:
    #     if not combatant.monster_name and 'location' in combatantInfo[combatant.name]:  # Combatant is a player
    #         allPlayerNames.append(combatant.name)
    # for x in range(len(mapGrid)):
    #     for y in range(len(mapGrid[0])):
    #         if getDistance(monsterCoordinates, (x,y)) > speed:
    #             mapGrid[x][y] = float('-inf')
    #         if mapGrid[x][y] != float('-inf'):
    #             selfSize = combatantInfo[CURRENT.name].get('size', 'M')[0].upper()
    #             selfSizeMultiplier = 1 + (1 if selfSize == 'L' else 2 if selfSize == 'H' else 3 if selfSize == 'G' else 0)
    #             for name, info in combatantInfo.items():
    #                 if name != CURRENT.name and 'location' in info:
    #                     x, y = convertCoordinates(info['location'])
    #                     otherCombatantSize = info.get('size', 'M')[0].upper()
    #                     otherSizeMultiplier = 1 + (1 if otherCombatantSize == 'L' else 2 if otherCombatantSize == 'H' else 3 if otherCombatantSize == 'G' else 0)   # Account for extra space other Large or larger combatants take up 
    #                     for ax in range(x - selfSizeMultiplier + 1, x + otherSizeMultiplier):
    #                         for ay in range(y - selfSizeMultiplier + 1, y + otherSizeMultiplier):
    #                             if ax >= 0 and ax < len(mapGrid) and ay >= 0 and ay < len(mapGrid[0]):
    #                                 mapGrid[ax][ay] = float('-inf')
    #         if mapGrid[x][y] != float('-inf'):
    #             mapGrid[x][y] -= getDistance((x, y), combatantInfo[CURRENT.name]['location'])*scale/TILE_SIZE
    #         if mapGrid[x][y] != float('-inf'):
    #             totalValue = 0
    #             for playerName in allPlayerNames:
    #                 distance = getDistance((x, y), playerName)
    #                 totalValue += distance/TILE_SIZE if distance <= rangedRange else 0
    #             mapGrid[x][y] += totalValue/len(allPlayerNames)*scale
    
    return mapGrid

def movementLimiter(mapInfo, combatantInfo, mapGrid, convertCoordinates, getDistance, scale=1, speed=30, **kwargs):
    monsterCoordinates = combatantInfo[CURRENT.name]['location']
    for x in range(len(mapGrid)):
        for y in range(len(mapGrid[0])):
            if getDistance(monsterCoordinates, (x,y)) > speed:
                mapGrid[x][y] = float('-inf')
    
    return mapGrid
                
def avoidStandingInSpaceWithCombatants(mapInfo, combatantInfo, mapGrid, convertCoordinates, getDistance, scale=1, **kwargs):
    selfSize = combatantInfo[CURRENT.name].get('size', 'M')[0].upper()
    selfSizeMultiplier = 1 + (1 if selfSize == 'L' else 2 if selfSize == 'H' else 3 if selfSize == 'G' else 0)
    for name, info in combatantInfo.items():
        if name != CURRENT.name and 'location' in info:
            x, y = convertCoordinates(info['location'])
            otherCombatantSize = info.get('size', 'M')[0].upper()
            otherSizeMultiplier = 1 + (1 if otherCombatantSize == 'L' else 2 if otherCombatantSize == 'H' else 3 if otherCombatantSize == 'G' else 0)   # Account for extra space other Large or larger combatants take up 
            for ax in range(x - selfSizeMultiplier + 1, x + otherSizeMultiplier):
                for ay in range(y - selfSizeMultiplier + 1, y + otherSizeMultiplier):
                    if ax >= 0 and ax < len(mapGrid) and ay >= 0 and ay < len(mapGrid[0]):
                        mapGrid[ax][ay] = float('-inf')
    
    return mapGrid

def prioritiseLeastMovement(mapInfo, combatantInfo, mapGrid, convertCoordinates, getDistance, scale=1, **kwargs):
    for x in range(len(mapGrid)):
        for y in range(len(mapGrid[0])):
            if mapGrid[x][y] != float('-inf'):
                mapGrid[x][y] -= getDistance((x, y), combatantInfo[CURRENT.name]['location'])*scale/TILE_SIZE
                
    return mapGrid
    
def meleeAttacker(mapInfo, combatantInfo, mapGrid, convertCoordinates, getDistance, scale=1, meleeRange=5, **kwargs):
    for combatant in combat().combatants:
        if not combatant.monster_name and 'location' in combatantInfo[combatant.name]:  # Combatant is a player
            playerX, playerY = convertCoordinates(combatantInfo[combatant.name]['location'])
            monsterSize = combatantInfo[CURRENT.name].get('size', 'M')[0].upper()
            monsterSizeMultiplier = 1 + (1 if monsterSize == 'L' else 2 if monsterSize == 'H' else 3 if monsterSize == 'G' else 0)
            playerSize = combatantInfo[combatant.name].get('size', 'M')[0].upper()
            playerSizeMultiplier = 1 + (1 if playerSize == 'L' else 2 if playerSize == 'H' else 3 if playerSize == 'G' else 0)
            for ax in range(playerX - monsterSizeMultiplier, playerX + 1 + playerSizeMultiplier):
                for ay in range(playerY - monsterSizeMultiplier + 1, playerY + 1 + playerSizeMultiplier):
                    if ax >= 0 and ax < len(mapGrid) and ay >= 0 and ay < len(mapGrid[0]):
                        mapGrid[ax][ay] += 1*scale
                    
    return mapGrid

def rangedAttacker(mapInfo, combatantInfo, mapGrid, convertCoordinates, getDistance, scale=1, rangedRange=30, **kwargs):
    allPlayerNames = []
    for combatant in combat().combatants:
        if not combatant.monster_name and 'location' in combatantInfo[combatant.name]:  # Combatant is a player
            allPlayerNames.append(combatant.name)
    for x in range(len(mapGrid)):
        for y in range(len(mapGrid[0])):
            if mapGrid[x][y] != float('-inf'):
                totalValue = 0
                for playerName in allPlayerNames:
                    distance = getDistance((x, y), playerName)
                    totalValue += distance/TILE_SIZE if distance <= rangedRange else 0
                mapGrid[x][y] += totalValue/len(allPlayerNames)*scale
    
    return mapGrid

def basic(mapInfo, combatantInfo, mapGrid, convertCoordinates, getDistance, scale=1, speed=30, **kwargs):
    mapGrid = movementLimiter(mapInfo, combatantInfo, mapGrid, convertCoordinates, getDistance, speed)
    mapGrid = avoidStandingInSpaceWithCombatants(mapInfo, combatantInfo, mapGrid, convertCoordinates, getDistance)
    mapGrid = prioritiseLeastMovement(mapInfo, combatantInfo, mapGrid, convertCoordinates, getDistance)
    
    return mapGrid
    
FUNCTIONS = {
    'movementLimiter': movementLimiter,
    'meleeAttacker': meleeAttacker,
    'basic': basic,
    'goblin': goblin,
}

def getFunction(functionName):
    return FUNCTIONS[functionName]