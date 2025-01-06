"""
Default Monster AI for AI Monsters with Battlemaps by @mehmango

This module contains the basic behavior functions for general use and some monster functions. This is far from a comprehensive list, just a starting point!
Use this module as a template when creating your own monster AI.

* THINGS YOUR MODULE WILL NEED TO BE COMPATIBLE:
* - Your monster functions should have the same required parameters as the goblin function below, as well as **kwargs.
* - Your module needs to implement the FUNCTION constant dictionary and getFunction() function at the bottom of the file, as seen below
*   - The function names in FUNCTION are case sensitive

"""

using(
    monsters1="d2d76c97-b63a-4e8d-846a-461cdbf576a1",
    monsters2="0b8ea785-bdb9-4922-9dc6-a21777f891b6",
    monsters3="749ede56-0691-46fc-95ea-1425bb3bfff3",
    monsters4="1ff68e1c-1056-4d2c-88a3-d824d18eca2f",
    monsters5="6aff63da-0299-41c6-8d18-06d2e9eb3707",
    monsters6="8fa2026e-cdb2-48d0-8fbb-84008d4d4d31",
    monsters7="e5dd5352-90df-471f-b694-14fade6d6fc1",
    monsters8="02377edc-82e8-41b7-8d6f-12ba3d749de8",
    monsters9="269ca567-b58f-458f-895f-04b36768c742",
    monsters10="4ffcd016-c059-44ec-86c9-2fe95c2a6fc6"
)

GLOBALS = {}

def setupGlobals(currentCombatant, allCombatantInfo, mapX, mapY, alph, argList, tileSize=5):
    playersAndAllies = []
    if 'aoo' in argList:
        manualTarget = argparse(argList).last('t')
        target = combat().get_combatant(manualTarget)
        if target and target.type == 'combatant':
            playersAndAllies.append(target)
        elif combat().current.type == "combatant":
            playersAndAllies.append(combat().current)
        else:
            err("Current combatant is in a group. If you are trying to perform an attack of opportunity against a combatant in a group, use `-t` to specify the target.")
    else:
        manualTargets = argparse(argList).get('t')
        for combatant in combat().combatants:
            if combatant.name != currentCombatant.name and (not combatant.monster_name or 'ally' in allCombatantInfo[combatant.name]) and 'location' in allCombatantInfo[combatant.name] and (len(manualTargets) <= 0 or any(manualTarget.lower() in combatant.name.lower() for manualTarget in manualTargets)):  # Combatant is a player or ally. Only consider manual targets if provided with '-t'
                playersAndAllies.append(combatant)
        if len(playersAndAllies) < 1:
            err("No players or allies found. If you specified targets using '-t', make sure that they are valid targets.")
    GLOBALS.update({
        'CURRENT': currentCombatant,
        'COMBATANTS_INFO': allCombatantInfo,
        'MAP_X': mapX,
        'MAP_Y': mapY,
        'ALPH': alph,
        'ARGLIST': argList,
        'TILE_SIZE': tileSize,
        'MONSTER_INFO': None,
        'MONSTER_MULTIATTACKS': None,
        'PLAYERS_AND_ALLIES': playersAndAllies,
    })

def convertCoordinatesToIndexes(coordinates):
    # Convert coordinates from alphanumeric representation to a set of indexes 
    if typeof(coordinates) == 'str':
        x = ''.join(x for x in coordinates if x.isalpha())
        x = GLOBALS.ALPH.index(x)
        y = ''.join(y for y in coordinates if y.isdigit())
        return (int(x), int(y)-1)
      
def convertCoordinatesToAlphanumeric(coordinates):
  # Convert coordinates from alphanumeric representation to a set of indexes
  if typeof(coordinates) != 'str':
      return str(GLOBALS.ALPH[coordinates[0]]) + str(coordinates[1]+1)

def getSizeMultiplier(size): 
      return 1 + (1 if size == 'L' else 2 if size == 'H' else 3 if size == 'G' else 0)

def getCombatantCoordinates(name):
    coordinates = []
    info = GLOBALS.COMBATANTS_INFO[name]
    size = info.get('size', 'M')[0].upper()
    sizeMultiplier = getSizeMultiplier(size)
    x, y = convertCoordinatesToIndexes(info['location'])
    for ax in range(x, x + sizeMultiplier):
        for ay in range(y, y + sizeMultiplier):
            coordinates.append((ax, ay))

    return coordinates

def getDistance(a, b, aSize='M', bSize='M'):
    if typeof(a) == 'str':
        if a in GLOBALS.COMBATANTS_INFO:  # a is a combatant
            aSize = GLOBALS.COMBATANTS_INFO[a].get('size', 'M')[0].upper()
            a = convertCoordinatesToIndexes(GLOBALS.COMBATANTS_INFO[a]['location'])
        else:  # a is a coordinate is represented like: A1
            a = convertCoordinatesToIndexes(a)
    if typeof(b) == 'str':
        if b in GLOBALS.COMBATANTS_INFO:  # b is a combatant
            bSize = GLOBALS.COMBATANTS_INFO[b].get('size', 'M')[0].upper()
            b = convertCoordinatesToIndexes(GLOBALS.COMBATANTS_INFO[b]['location'])
        else:  # b is a coordinate is represented like: A1
            b = convertCoordinatesToIndexes(b)
    
    # Account for size
    a = list(a)
    b = list(b)
    if a[0] < b[0]:
        a[0] = min(GLOBALS.MAP_X, a[0] + getSizeMultiplier(aSize) - 1)
    else:
        b[0] = min(GLOBALS.MAP_X, b[0] + getSizeMultiplier(bSize) - 1)
    if a[1] < b[1]:
        a[1] = min(GLOBALS.MAP_Y, a[1] + getSizeMultiplier(aSize) - 1)
    else:
        b[1] = min(GLOBALS.MAP_Y, b[1] + getSizeMultiplier(bSize) - 1)

    # Calculate the delta for X and Y between the two
    deltaX, deltaY = abs(int(
        a[0])-int(b[0])), abs(int(a[1])-int(b[1]))
    # Doing 5ft diag's, the distance is just the higher delta
    distance = max(deltaX, deltaY)*5

    return distance

def getMonsterInfo(monsterName):
    monsterInfo = None
    if not monsterInfo:
        if monsterName in monsters1.monsters.keys():
            monsterInfo = monsters1.monsters[monsterName]
    if not monsterInfo:
        if monsterName in monsters2.monsters.keys():
            monsterInfo = monsters2.monsters[monsterName]
    if not monsterInfo:
        if monsterName in monsters3.monsters.keys():
            monsterInfo = monsters3.monsters[monsterName]
    if not monsterInfo:
        if monsterName in monsters4.monsters.keys():
            monsterInfo = monsters4.monsters[monsterName]
    if not monsterInfo:
        if monsterName in monsters5.monsters.keys():
            monsterInfo = monsters5.monsters[monsterName]
    if not monsterInfo:
        if monsterName in monsters6.monsters.keys():
            monsterInfo = monsters6.monsters[monsterName]
    if not monsterInfo:
        if monsterName in monsters7.monsters.keys():
            monsterInfo = monsters7.monsters[monsterName]
    if not monsterInfo:
        if monsterName in monsters8.monsters.keys():
            monsterInfo = monsters8.monsters[monsterName]
    if not monsterInfo:
        if monsterName in monsters9.monsters.keys():
            monsterInfo = monsters9.monsters[monsterName]
    if not monsterInfo:
        if monsterName in monsters10.monsters.keys():
            monsterInfo = monsters10.monsters[monsterName]
            
    return monsterInfo

def getMultiattackOptions(monsterInfo):
    numbers = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve']   # You should not be automating a monster with more than 12 attacks a turn, what are you Skynet?
    confirmedMultiattackOptions = []
    unconfirmedMultiattackOptions = []
    if monsterInfo and 'multiattack' in monsterInfo.Actions.lower():
        # Do not continue if you value your sanity
        attacks = []
        meleeAttacks = []
        rangedAttacks = []
        
        for attack in GLOBALS.CURRENT.attacks:
            for automation in attack.raw.automation:
                if automation.type == 'text' and ('Melee' in automation.text or 'Ranged' in automation.text):
                    if 'Melee' in automation.text and not '(1H)' in attack.name:
                        meleeAttacks.append(attack.name)
                    if 'Ranged' in automation.text:
                        rangedAttacks.append(attack.name)
                    break
                
        attacks = meleeAttacks + rangedAttacks
        
        joiners = {
            'afterAnd': False,
            'afterOr': True
        }
        def addMultiattackOptions(options, confirmedMultiattackOptions, unconfirmedMultiattackOptions, joiners):
            if joiners.afterAnd:
                newOptions = []
                for existingOption in unconfirmedMultiattackOptions:
                    for option in options:
                        existingOption.append(option)
                        newOptions.extend(existingOption)
                unconfirmedMultiattackOptions.clear()
                unconfirmedMultiattackOptions.append(newOptions)
            elif joiners.afterOr:
                confirmedMultiattackOptions.extend(unconfirmedMultiattackOptions)
                unconfirmedMultiattackOptions.clear()
                unconfirmedMultiattackOptions.append([option for option in options])
            joiners['afterAnd'] = False
            joiners['afterOr'] = False   
        
        def getAttack(word, attacks):
            foundAttack = None
            sanitisedAttacks = [attack.replace(' ', '').replace('.', '').replace(',', '').lower() for attack in attacks]
            for i in range(len(sanitisedAttacks)):
                sanitisedAttack = sanitisedAttacks[i]
                if '(' in sanitisedAttack:
                    sanitisedAttacks[i] = sanitisedAttack[:sanitisedAttack.find('(')]   # Remove stuff like "(1H)" or "(x form only)"
                    
            for i in range(len(sanitisedAttacks)):
                sanitisedAttack = sanitisedAttacks[i]
                if sanitisedAttack in word.lower():
                    foundAttack = attacks[i]
            
            return foundAttack
                
        words = monsterInfo.Actions[monsterInfo.Actions.find('/em>')+4:monsterInfo.Actions.find('</p')].replace('--', ' ').split()
        for i in range(len(attacks)):
            attack = attacks[i]
            attackWords = attack.split()
            if len(attackWords) > 1 and attackWords[0].lower() in [word.lower() for word in words]:
                combinedAttackName = "".join(attackWords)
                attackWordIndex = [word.lower() for word in words].index(attackWords[0].lower())
                words[attackWordIndex] = combinedAttackName
                words.pop(attackWordIndex+1)
        
        i = 0
        number = 1
        while i < len(words):
            word = words[i]
            i += 1
            
            if word.lower() in numbers:
                number = numbers.index(word.lower()) + 1
            elif word.lower() == 'or':
                joiners['afterOr'] = True
            elif word.lower() == 'and':
                joiners['afterAnd'] = True
            elif number > 0:
                if word.lower() == 'melee':
                    while i < len(words):
                        word = words[i]
                        i += 1
                        if word.lower() in ['or', 'and'] or i == len(words):    # Monster can make any combination of x melee attacks
                            for meleeAttack in meleeAttacks:    # We assume that the monster will always max x number of the same attack, never making two different melee attacks
                                options = []
                                options.append({
                                    'name': meleeAttack,
                                    'num': number
                                })
                                addMultiattackOptions(options, confirmedMultiattackOptions, unconfirmedMultiattackOptions, joiners)
                                joiners['afterOr'] = True
                            joiners['afterOr'] = False
                            number = 0
                            if word.lower() in ['or', 'and']:
                                i -= 1
                            break
                        elif getAttack(word, meleeAttacks):
                            i -= 1  # Return to outer loop to evaluate
                            break
                        elif word.lower() in numbers:
                            i -= 1 # Return to outer loop to evaluate
                            break
                elif word.lower() == 'ranged':
                    while i < len(words):
                        word = words[i]
                        i += 1
                        if word.lower() in ['or', 'and'] or i == len(words): # End of multiattack string. Monster can make any combination of x ranged attacks
                            for rangedAttack in rangedAttacks:    # We assume that the monster will always max x number of the same attack, never making two different ranged attacks
                                options = []
                                options.append({
                                    'name': rangedAttack,
                                    'num': number
                                })
                                addMultiattackOptions(options, confirmedMultiattackOptions, unconfirmedMultiattackOptions, joiners)
                                joiners['afterOr'] = True
                            joiners['afterOr'] = False
                            number = 0
                            if word.lower() in ['or', 'and']:
                                i -= 1
                        elif getAttack(word, rangedAttacks):
                            i -= 1  # Return to outer loop to evaluate
                            break
                        elif word.lower() in numbers:
                            i -= 1 # Return to outer loop to evaluate
                            break
                elif getAttack(word, attacks):
                    attack = getAttack(word, attacks)
                    addMultiattackOptions([{
                        'name': attack,
                        'num': number
                    }], confirmedMultiattackOptions, unconfirmedMultiattackOptions, joiners)
                    number = 0
                    
                elif i == len(words) and len(confirmedMultiattackOptions) < 1 and len(unconfirmedMultiattackOptions) < 1:   # End of multiattack string but there are no multiattack options yet
                    for attack in attacks:
                        options = []
                        options.append({
                            'name': attack,
                            'num': number
                        })
                        addMultiattackOptions(options, confirmedMultiattackOptions, unconfirmedMultiattackOptions, joiners)
                        joiners['afterOr'] = True
                    number = 0
        
        # err(i)
         
    # err(unconfirmedMultiattackOptions)
    if len(unconfirmedMultiattackOptions) > 0:
        confirmedMultiattackOptions += unconfirmedMultiattackOptions
    return confirmedMultiattackOptions
  
def moveTowardsPlayer(monsterCoordinates, playerCoordinates, maxMovement, viableTiles, inverse=False):   # Inverse = True to move away from player instead
    monsterX, monsterY = monsterCoordinates
    playerX, playerY = playerCoordinates
    xDiff = (playerX - monsterX) * GLOBALS.TILE_SIZE
    yDiff = (playerY - monsterY) * GLOBALS.TILE_SIZE
    
    movementLeft = maxMovement
    xMovement = 0
    yMovement = 0
    
    # Try to get on a diagonal line with the player
    if abs(xDiff) > abs(yDiff):
        xMovement = min(abs(xDiff) - abs(yDiff), movementLeft) * (-1 if xDiff < 0 else 1)
        movementLeft -= abs(xMovement)
    elif abs(yDiff) > abs(xDiff):
        yMovement = min(abs(yDiff) - abs(xDiff), movementLeft)  * (-1 if yDiff < 0 else 1)
        movementLeft -= abs(yMovement)
    
    if movementLeft:
        # Move diagonally towards the player
        xMovement += movementLeft * (-1 if xDiff < 0 else 1)
        yMovement += movementLeft * (-1 if yDiff < 0 else 1)
        
    finalX = max(0, min(GLOBALS.MAP_X, int(monsterX+(xMovement/GLOBALS.TILE_SIZE) if not inverse else int(monsterX-(xMovement/GLOBALS.TILE_SIZE)))))
    finalY = max(0, min(GLOBALS.MAP_Y, int(monsterY+(yMovement/GLOBALS.TILE_SIZE) if not inverse else int(monsterY-(yMovement/GLOBALS.TILE_SIZE)))))
    finalTile = (finalX, finalY)
    while finalTile not in viableTiles and maxMovement > 0:
        if not abs(xMovement) == abs(yMovement):
            if abs(xDiff) > abs(yDiff):
                yMovement += GLOBALS.TILE_SIZE * (-1 if yDiff < 0 else 1)
            elif abs(yDiff) > abs(xDiff):
                xMovement += GLOBALS.TILE_SIZE * (-1 if xDiff < 0 else 1)
            finalX = max(0, min(GLOBALS.MAP_X, int(monsterX+(xMovement/GLOBALS.TILE_SIZE) if not inverse else int(monsterX-(xMovement/GLOBALS.TILE_SIZE)))))
            finalY = max(0, min(GLOBALS.MAP_Y, int(monsterY+(yMovement/GLOBALS.TILE_SIZE) if not inverse else int(monsterY-(yMovement/GLOBALS.TILE_SIZE)))))
            finalTile = (finalX, finalY)
        elif maxMovement - GLOBALS.TILE_SIZE > 0:
            finalTile = moveTowardsPlayer(monsterCoordinates, playerCoordinates, maxMovement - GLOBALS.TILE_SIZE, viableTiles, inverse).pop()
        else:
            finalTile = monsterCoordinates
            maxMovement -= GLOBALS.TILE_SIZE
    return {finalTile}
    
def basic(currentCombatant, viableTiles, basicActions, mapInfo, combatantInfo, mapX, mapY, alph, argList, **kwargs):
    """
    * Examples of the structures of attributes below may not be accurate. They are my best guesses from reading the !map alias code and other documentation.
    * Let me know if corrections are needed
    
    Args:
        viableTiles (set): All tiles deemed viable/preferable so far. Coordinates should be stored in index (x, y) format (eg: (2, 10)).
        
        basicActions (dict): All the basic actions that the monster might be able to take. Mainly used to compatability purposes.
        
        mapInfo (dict): Map info, including:
                            - size (eg: "10x10")
                            - walls ([f"-c{wallColor}{wall}]", eg: [f"-crB3-oD3", f"-cD12E12"])
                            - objects ([{objectLocation}{objectColor}{objectId}], eg: ["A1b$la", "B2r$ow"])
                            - fow ([coordinate[:coordinate]], eg: ["A1:B3", "C4"])
                            
        combatantInfo (dict): Information on all combatants on the map. Each key is the combatant's name. Each item is also a dictionary, including:
                                - location (eg: "A1")
                                - effect#, eg: effect, effect2 ({effectName} / {effectTargetName}, eg: "Call Lightning / GO1")
                                - overlay#, eg: overlay, overlay2 ({shape}{size}{colour (optional)}{target}, eg: "c30bI4", "co20~ffc1fa{aim}", "s20r{targ}")
                                
        mapX (int): The horizontal length of the map (in number of tiles).
        
        mapY (int): The vertical height of the map (in number of tiles).
        
        alph (list): Alphanumeric representations for coordinates. For use in util functions.
        
        argList (list): A list of all arguments passed to the alias (From &ARGS&). Has not been parsed.

    Returns:
        tuple: A tuple containing:
            viableTiles (set): All tiles deemed viable/preferable so far. Coordinates should be stored in index (x, y) format (eg: (2, 10)).
            action (str): The name of the action to be taken
    """
    setupGlobals(currentCombatant, combatantInfo, mapX, mapY, alph, argList)
    
    GLOBALS['MONSTER_INFO'] = getMonsterInfo(GLOBALS.CURRENT.monster_name)
    GLOBALS['MONSTER_MULTIATTACKS'] = getMultiattackOptions(GLOBALS.MONSTER_INFO)
    
    action = None
    hasMelee = False
    hasRanged = False
    for attack in GLOBALS.CURRENT.attacks:
        for automation in attack.raw.automation:
            if automation.type == 'text':
                hasMelee = hasMelee or 'Melee' in automation.text
                hasRanged = hasRanged or 'Ranged' in automation.text
                break
            
    speeds = None
    if 'aoo' in GLOBALS.ARGLIST:
        speeds = {
            'walk': 0
        }
    else:
        if not GLOBALS.MONSTER_INFO:
            speeds = {
                'walk': 30
            }
        else:
            speeds = {}
            speedsText = GLOBALS.MONSTER_INFO.Speed
            speedsText = 'walk ' + speedsText
            speedTypeTexts = speedsText.split(', ')
            for speedTypeText in speedTypeTexts:
                speedTypeText = speedTypeText.replace(' ft.', '')
                speedTypeText = speedTypeText.split(' ')
                speedType = speedTypeText[0]
                speedValue = int(speedTypeText[1])
                speeds[speedType] = speedValue
            
    if 'aoo' in argList:
        viableTiles, action = basicMelee(viableTiles, basicActions, speeds)
    elif hasMelee and hasRanged:
        viableTiles, action = basicMeleeAndRanged(viableTiles, basicActions, speeds)            
    elif hasMelee:
        viableTiles, action = basicMelee(viableTiles, basicActions, speeds)
    elif hasRanged:
        viableTiles, action = basicRanged(viableTiles, basicActions, speeds)

    return viableTiles, action

def goblin(currentCombatant, viableTiles, basicActions, mapInfo, combatantInfo, mapX, mapY, alph, argList, **kwargs):
    setupGlobals(currentCombatant, combatantInfo, mapX, mapY, alph, argList)
    viableTiles, action = basicMeleeAndRanged(viableTiles, basicActions, {'walk': 30})            

    return viableTiles, action

def basicMelee(viableTiles, basicActions, speeds, **kwargs):
    action = None

    newViableTiles, newAction = avoidStandingInSpaceWithCombatants(viableTiles)
    tilesWithoutCombatants = newViableTiles if len(newViableTiles) > 0 else viableTiles
    action = newAction if newAction else action
    
    newViableTiles, newAction = movementLimiter(tilesWithoutCombatants, speeds)
    viableTiles = newViableTiles if len(newViableTiles) > 0 else viableTiles
    action = newAction if newAction else action
    
    newViableTiles, newAction = basicMeleeAttacker(viableTiles, basicActions, speeds)
    viableTiles = newViableTiles if len(newViableTiles) > 0 else viableTiles
    action = newAction if newAction else action
    if 'aoo' in GLOBALS.ARGLIST and action in basicActions.values():
        return viableTiles, None
    
    if action == basicActions.dash:
        originalLocation = GLOBALS.COMBATANTS_INFO[GLOBALS.CURRENT.name]['location']
        GLOBALS.COMBATANTS_INFO[GLOBALS.CURRENT.name]['location'] = convertCoordinatesToAlphanumeric(viableTiles.pop())
        
        newViableTiles, newAction = movementLimiter(tilesWithoutCombatants, speeds)
        viableTiles = newViableTiles if len(newViableTiles) > 0 else viableTiles
        
        newViableTiles, newAction = basicMeleeAttacker(viableTiles, basicActions, speeds)
        viableTiles = newViableTiles if len(newViableTiles) > 0 else viableTiles
        
        GLOBALS.COMBATANTS_INFO[GLOBALS.CURRENT.name]['location'] = originalLocation
    
    newViableTiles, newAction = prioritiseLeastMovement(viableTiles)
    viableTiles = newViableTiles if len(newViableTiles) > 0 else viableTiles
    action = newAction if newAction else action
    
    return viableTiles, action

def basicRanged(viableTiles, basicActions, speeds, **kwargs):
    action = None
    
    newViableTiles, newAction = avoidStandingInSpaceWithCombatants(viableTiles)
    tilesWithoutCombatants = newViableTiles if len(newViableTiles) > 0 else viableTiles
    action = newAction if newAction else action
    
    newViableTiles, newAction = movementLimiter(tilesWithoutCombatants, speeds)
    viableTiles = newViableTiles if len(newViableTiles) > 0 else viableTiles
    action = newAction if newAction else action
    
    newViableTiles, newAction = basicRangedAttacker(viableTiles, basicActions, speeds)
    viableTiles = newViableTiles if len(newViableTiles) > 0 else viableTiles
    action = newAction if newAction else action
    
    if action == basicActions.dash:
        originalLocation = GLOBALS.COMBATANTS_INFO[GLOBALS.CURRENT.name]['location']
        GLOBALS.COMBATANTS_INFO[GLOBALS.CURRENT.name]['location'] = convertCoordinatesToAlphanumeric(viableTiles.pop())
        
        newViableTiles, newAction = movementLimiter(tilesWithoutCombatants, speeds)
        viableTiles = newViableTiles if len(newViableTiles) > 0 else viableTiles
        
        newViableTiles, newAction = basicRangedAttacker(viableTiles, basicActions, speeds)
        viableTiles = newViableTiles if len(newViableTiles) > 0 else viableTiles
        
        GLOBALS.COMBATANTS_INFO[GLOBALS.CURRENT.name]['location'] = originalLocation
        
    newViableTiles, newAction = personalSpace(viableTiles)
    viableTiles = newViableTiles if len(newViableTiles) > 0 else viableTiles
    action = newAction if newAction else action
    
    return viableTiles, action      

def basicMeleeAndRanged(viableTiles, basicActions, speeds, **kwargs):
    action = None
    
    newViableTiles, newAction = avoidStandingInSpaceWithCombatants(viableTiles)
    tilesWithoutCombatants = newViableTiles if len(newViableTiles) > 0 else viableTiles
    action = newAction if newAction else action
    
    newViableTiles, newAction = movementLimiter(tilesWithoutCombatants, speeds)
    viableTiles = newViableTiles if len(newViableTiles) > 0 else viableTiles
    action = newAction if newAction else action
    
    newViableTiles, newAction = basicMeleeAttacker(viableTiles, basicActions, speeds)
    preMeleeViableTiles = viableTiles.copy()
    viableTiles = newViableTiles if len(newViableTiles) > 0 else viableTiles
    action = newAction if newAction else action
    
    if action in list(basicActions.values()): # No player within melee range
        newViableTiles, newAction = basicRangedAttacker(preMeleeViableTiles, basicActions, speeds)
        action = newAction if newAction else action
        
        if action == basicActions.dash: # No player within ranged attack range, dash like a melee attacker
            originalLocation = GLOBALS.COMBATANTS_INFO[GLOBALS.CURRENT.name]['location']
            GLOBALS.COMBATANTS_INFO[GLOBALS.CURRENT.name]['location'] = convertCoordinatesToAlphanumeric(viableTiles.pop())
            
            newViableTiles, newAction = movementLimiter(tilesWithoutCombatants, speeds)
            viableTiles = newViableTiles if len(newViableTiles) > 0 else viableTiles
            
            newViableTiles, newAction = basicMeleeAttacker(viableTiles, basicActions, speeds)
            viableTiles = newViableTiles if len(newViableTiles) > 0 else viableTiles
            
            GLOBALS.COMBATANTS_INFO[GLOBALS.CURRENT.name]['location'] = originalLocation
    
    newViableTiles, newAction = prioritiseLeastMovement(viableTiles)
    viableTiles = newViableTiles if len(newViableTiles) > 0 else viableTiles
    action = newAction if newAction else action
    
    return viableTiles, action

def movementLimiter(viableTiles, speeds):
    """
    Tiles that the monster can reach through movement
    """
    speed = speeds.fly if 'fly' in speeds.keys() else speeds.walk
    tempTiles = viableTiles.copy()
    monsterCoordinates = convertCoordinatesToIndexes(GLOBALS.COMBATANTS_INFO[GLOBALS.CURRENT.name]['location'])
    monsterSize = GLOBALS.COMBATANTS_INFO[GLOBALS.CURRENT.name].get('size', 'M')[0].upper()
    monsterSizeMultiplier = getSizeMultiplier(monsterSize)
    minX = int(max(0, monsterCoordinates[0] - ( speed / GLOBALS.TILE_SIZE )))
    minY = int(max(0, monsterCoordinates[1] - ( speed / GLOBALS.TILE_SIZE )))
    maxX = int(min(GLOBALS.MAP_X - monsterSizeMultiplier, monsterCoordinates[0] + ( speed / GLOBALS.TILE_SIZE )))
    maxY = int(min(GLOBALS.MAP_Y - monsterSizeMultiplier, monsterCoordinates[1] + ( speed / GLOBALS.TILE_SIZE )))
    if len(tempTiles) == GLOBALS.MAP_X*GLOBALS.MAP_Y:
        # No tiles have been eliminated yet. It will be more efficient to calculate viable tiles based on monster speed
        tempTiles = {(x, y) for y in range(minY, maxY + 1) for x in range(minX, maxX + 1)}
    else:
        # Some tiles have been eliminated. It should be more efficient eliminate more tiles based on monster speed
        tempTiles = {(x, y) for y in range(minY, maxY + 1) for x in range(minX, maxX + 1) if (x, y) in viableTiles}
        
    return tempTiles, None

def avoidStandingInSpaceWithCombatants(viableTiles):
    selfSize = GLOBALS.COMBATANTS_INFO[GLOBALS.CURRENT.name].get('size', 'M')[0].upper()
    selfSizeMultiplier = getSizeMultiplier(selfSize)
    for name, info in GLOBALS.COMBATANTS_INFO.items():
        if name != GLOBALS.CURRENT.name and 'location' in info:
            x, y = convertCoordinatesToIndexes(info['location'])
            otherCombatantSize = info.get('size', 'M')[0].upper()
            otherSizeMultiplier = getSizeMultiplier(otherCombatantSize)   # Account for extra space other Large or larger combatants take up 
            for ax in range(max(0, x - selfSizeMultiplier + 1), min(GLOBALS.MAP_X, x + otherSizeMultiplier)):
                for ay in range(max(0, y - selfSizeMultiplier + 1), min(GLOBALS.MAP_Y, y + otherSizeMultiplier)):
                    viableTiles.discard((ax, ay))
    
    return viableTiles, None
    
def basicMeleeAttacker(viableTiles, basicActions, speeds):
    speed = speeds.fly if 'fly' in speeds.keys() else speeds.walk
    action = None
    tempTiles = set()
    
    maxMeleeRange = 0
    meleeAttacks = [] # Object of { name, range }
    for attack in GLOBALS.CURRENT.attacks:
        for automation in attack.raw.automation:
            if automation.type == 'text' and 'Melee' in automation.text and not '(1H)' in attack.name:
                attackRange = int(automation.text[automation.text.find('reach ') + 6:automation.text.find(' ft.')])
                meleeAttacks.append({ 'name': attack.name, 'range': attackRange })
                maxMeleeRange = max(maxMeleeRange, attackRange)
                break
            
    monsterCoordinates = convertCoordinatesToIndexes(GLOBALS.COMBATANTS_INFO[GLOBALS.CURRENT.name]['location'])
    monsterSize = GLOBALS.COMBATANTS_INFO[GLOBALS.CURRENT.name].get('size', 'M')[0].upper()
    monsterSizeMultiplier = getSizeMultiplier(monsterSize)
    inaccessibleMeleeTiles = set()
    playersConsidered = []
    closestPlayer = None
    closestPlayerDistance = float('inf')
    while len(tempTiles) < 1 and len(inaccessibleMeleeTiles) < 1 and len(playersConsidered) < len(GLOBALS.PLAYERS_AND_ALLIES):
        closestPlayer = None
        closestPlayerDistance = float('inf')
        closestTilesToPlayerDistance = float('inf')
        for player in [player for player in GLOBALS.PLAYERS_AND_ALLIES if not player in playersConsidered]:
            distance = getDistance(GLOBALS.CURRENT.name, player.name)
            if distance < closestPlayerDistance:
                closestPlayer = player
                closestPlayerDistance = distance
        
        if closestPlayerDistance == GLOBALS.TILE_SIZE:
            tempTiles = {monsterCoordinates}
            closestTilesToPlayerDistance = GLOBALS.TILE_SIZE
            break
        
        playersConsidered.append(closestPlayer)
        playerX, playerY = convertCoordinatesToIndexes(GLOBALS.COMBATANTS_INFO[closestPlayer.name]['location'])
        playerSize = GLOBALS.COMBATANTS_INFO[closestPlayer.name].get('size', 'M')[0].upper()
        playerSizeMultiplier = getSizeMultiplier(playerSize)
        
        tilesAroundPlayer = []
        for ax in range(max(0, int(playerX - monsterSizeMultiplier + 1 - ( maxMeleeRange / GLOBALS.TILE_SIZE ))), min(GLOBALS.MAP_X, int(playerX + playerSizeMultiplier + ( maxMeleeRange / GLOBALS.TILE_SIZE )))):
            for ay in range(max(0, int(playerY - monsterSizeMultiplier + 1 - ( maxMeleeRange / GLOBALS.TILE_SIZE ))), min(GLOBALS.MAP_Y, (int(playerY + playerSizeMultiplier + ( maxMeleeRange / GLOBALS.TILE_SIZE ))))):
                tilesAroundPlayer.append((ax, ay))
        for tile in tilesAroundPlayer:
            if tile in viableTiles:
                distance = getDistance(tile, closestPlayer.name, monsterSize)
                if distance == GLOBALS.TILE_SIZE:
                    tempTiles = {tile}
                    closestTilesToPlayerDistance = GLOBALS.TILE_SIZE
                    break
                elif distance < closestTilesToPlayerDistance:
                    tempTiles = {tile}
                    closestTilesToPlayerDistance = distance
                elif distance == closestTilesToPlayerDistance:  # Remove if more optimisation needed
                    tempTiles.add(tile)
            elif getDistance(monsterCoordinates, tile, monsterSize) > speed:
                inaccessibleMeleeTiles.add(tile)
                    
    if len(tempTiles) > 0:
        
        # leftoverMovement = speed + maxMeleeRange - closestPlayerDistance
        # for meleeAttack in meleeAttacks:
        #     if maxMeleeRange - meleeAttack.range <= leftoverMovement:
        #         maxMeleeRange = meleeAttack.range
                 
        # monsterSize = GLOBALS.COMBATANTS_INFO[GLOBALS.CURRENT.name].get('size', 'M')[0].upper()
        # monsterSizeMultiplier = getSizeMultiplier(monsterSize)
        # playerSize = GLOBALS.COMBATANTS_INFO[closestPlayer.name].get('size', 'M')[0].upper()
        # playerSizeMultiplier = getSizeMultiplier(playerSize)
        # # err((int(playerX - monsterSizeMultiplier + 1 - ( maxMeleeRange / GLOBALS.TILE_SIZE )), int(playerX + 1 + playerSizeMultiplier - 1 + ( maxMeleeRange / GLOBALS.TILE_SIZE )), int(playerY - monsterSizeMultiplier + 2 - ( maxMeleeRange / GLOBALS.TILE_SIZE )), int(playerY + playerSizeMultiplier + ( maxMeleeRange / GLOBALS.TILE_SIZE ))))
        # for ax in range(int(playerX - monsterSizeMultiplier + 1 - ( maxMeleeRange / GLOBALS.TILE_SIZE )), int(playerX + 1 + playerSizeMultiplier - 1 + ( maxMeleeRange / GLOBALS.TILE_SIZE ))):
        #     for ay in range(int(playerY - monsterSizeMultiplier + 2 - ( maxMeleeRange / GLOBALS.TILE_SIZE )), int(playerY + playerSizeMultiplier + ( maxMeleeRange / GLOBALS.TILE_SIZE ))):
        #         if (ax, ay) in viableTiles:
        #             tempTiles.add((ax, ay))
        
        if GLOBALS.MONSTER_MULTIATTACKS and not 'aoo' in GLOBALS.ARGLIST:
            bestMultiattack = None
            bestMultiattackMaxReach = float('inf')
            for multiattackOption in GLOBALS.MONSTER_MULTIATTACKS:
                minReach = float('inf')
                maxReach = 0
                for attack in multiattackOption:
                    if attack.name in [meleeAttack.name for meleeAttack in meleeAttacks]:
                        meleeAttack = [meleeAttack for meleeAttack in meleeAttacks if meleeAttack.name == attack.name][0]
                        minReach = min(meleeAttack.range, minReach)
                        maxReach = max(meleeAttack.range, maxReach)
                    else:   # Attack is a ranged attack
                        maxReach = float('inf')
                if minReach >= closestTilesToPlayerDistance and (not bestMultiattack or maxReach < bestMultiattackMaxReach):
                    bestMultiattack = multiattackOption
                    bestMultiattackMaxReach = maxReach
                    
            if bestMultiattack:
                commands = []
                for attack in bestMultiattack:
                    commands.append(f'i a "{attack.name}" -t "{closestPlayer.name}" -rr {attack.num}')
                action = {
                    'name': 'Multiattack',
                    'commands': commands
                }
        
        if not action:
            bestAttack = None
            for meleeAttack in meleeAttacks:
                if meleeAttack.range >= closestTilesToPlayerDistance and (not bestAttack or meleeAttack.range < bestAttack.range):
                    bestAttack = meleeAttack
            if bestAttack:
                action = {
                    'name': bestAttack.name,
                    'commands': [f'''i {'a' if not 'aoo' in GLOBALS.ARGLIST else 'aoo ' + GLOBALS.CURRENT.name} "{bestAttack.name}" -t "{closestPlayer.name}"''']
                }
        
    else:  # Monster cannot get within melee range of player and also attack
        # leastDistance = float('inf')
        # # err(len(viableTiles))
        # for (x, y) in viableTiles:
        #     distance = getDistance((x, y), closestPlayer.name)
        #     if distance <= closestPlayerDistance - speed:   # Max movement used
        #         err((x, y))
        #         tempTiles = {(x, y)}
        #         break   # Only consider one tile for efficiency
            #     leastDistance = distance
            # elif distance == leastDistance:
            #     tempTiles.add((x, y))
                
        action = basicActions.dash

        if len(inaccessibleMeleeTiles) > 0:   # There are open spaces in melee of the player
            goToMeleeTile = inaccessibleMeleeTiles.pop()
            tempTiles = moveTowardsPlayer(monsterCoordinates, goToMeleeTile, speed, viableTiles)
            targetTile = tempTiles.pop()
            if targetTile == monsterCoordinates:
                action = basicActions.dodge
            else:
                tempTiles.add(targetTile)
        else:
            tempTiles = moveTowardsPlayer(monsterCoordinates, (playerX, playerY), min(closestPlayerDistance - maxMeleeRange, speed), viableTiles)
            action = basicActions.dodge

    return tempTiles, action

def personalSpace(viableTiles):
    monsterSize = GLOBALS.COMBATANTS_INFO[GLOBALS.CURRENT.name].get('size', 'M')[0].upper()
    allPlayerNames = [combatant.name for combatant in GLOBALS.PLAYERS_AND_ALLIES]
            
    mostDistance = 0
    tempTiles = set()
    for (x, y) in viableTiles:
        totalDistance = 0
        for playerName in allPlayerNames:
            totalDistance += getDistance((x, y), playerName, monsterSize)
        if totalDistance > mostDistance:
            mostDistance = totalDistance
            tempTiles = {(x, y)}
        elif totalDistance > mostDistance:
            tempTiles.add((x, y))
    
    return tempTiles, None

def basicRangedAttacker(viableTiles, basicActions, speeds):
    # If there are multiple ranged attacks, the monster will try to get within short range of the ranged attack with the shortest short range
    speed = speeds.fly if 'fly' in speeds.keys() else speeds.walk
    action = None
    tempTiles = viableTiles
    # shortRangeTempTiles = set()
    # longRangeTempTiles = set()
    rangedAttacks = [] # Object of { name, shortRange, longRange }
    shortestRangedAttack = None
    rangedShortRange = float('inf')
    rangedLongRange = 0
    shortestDistanceLongRange = float('inf')    # The shortest distance long ranged attack that can be made (This assumed the monster cannot get close enough to make a short ranged attack)
    
    for attack in GLOBALS.CURRENT.attacks:
        for automation in attack.raw.automation:
            if automation.type == 'text' and 'Ranged' in automation.text:
                rangeTextStartIndex = 0
                if 'range ' in automation.text:
                    rangeTextStartIndex = automation.text.find('range ') + 6
                elif 'ranged ' in automation.text:
                    rangeTextStartIndex = automation.text.find('ranged ') + 7
                attackRangeAll = automation.text[rangeTextStartIndex : rangeTextStartIndex + automation.text[rangeTextStartIndex:].find(' ft.')]
                attackRangeShort, attackRangeLong = attackRangeAll.split('/')
                attackRangeShort, attackRangeLong = int(attackRangeShort), int(attackRangeLong)
                rangedAttack = { 'name': attack.name, 'shortRange': attackRangeShort, 'longRange': attackRangeLong }
                rangedAttacks.append(rangedAttack)
                rangedLongRange = max(rangedLongRange, attackRangeLong)
                if attackRangeShort < rangedShortRange:
                    shortestRangedAttack = rangedAttack
                    rangedShortRange = attackRangeShort
                break
            
    rangedOnlyMultiattacks = []
    if GLOBALS.MONSTER_MULTIATTACKS:
        for multiattack in GLOBALS.MONSTER_MULTIATTACKS:
            rangedOnly = True
            for attack in multiattack:
                if not attack.name in [rangedAttack.name for rangedAttack in rangedAttacks]:
                    rangedOnly = False
                    break
            if rangedOnly:
                rangedOnlyMultiattacks.append(multiattack)
    
    closestPlayer = None
    closestPlayerDistance = float('inf')
    for combatant in GLOBALS.PLAYERS_AND_ALLIES:
        distance = getDistance(GLOBALS.CURRENT.name, combatant.name)
        if distance < closestPlayerDistance:
            closestPlayer = combatant
            closestPlayerDistance = distance

    monsterCoordinates = convertCoordinatesToIndexes(GLOBALS.COMBATANTS_INFO[GLOBALS.CURRENT.name]['location'])
    playerCoordinates = convertCoordinatesToIndexes(GLOBALS.COMBATANTS_INFO[closestPlayer.name]['location'])
    withinShortRange = False
    if closestPlayerDistance <= rangedShortRange:
        tempTiles = moveTowardsPlayer(monsterCoordinates, playerCoordinates, min(rangedShortRange - closestPlayerDistance, speed), viableTiles, True)
        withinShortRange = True
    elif closestPlayerDistance <= rangedShortRange + speed:
        tempTiles = moveTowardsPlayer(monsterCoordinates, playerCoordinates, min(closestPlayerDistance - rangedShortRange, speed), viableTiles)
        withinShortRange = True
    else:
        tempTiles = moveTowardsPlayer(monsterCoordinates, playerCoordinates, speed, viableTiles, getDistance)
        
    if withinShortRange:
        if len(rangedOnlyMultiattacks) > 0:
            bestMultiattack = None
            for multiattack in rangedOnlyMultiattacks:
                if shortestRangedAttack.name in [attack.name for attack in multiattack]:
                    bestMultiattack = multiattack
                    break
            if bestMultiattack:
                commands = []
                for attack in bestMultiattack:
                    commands.append(f'i a "{attack.name}" -t "{closestPlayer.name}" -rr {attack.num}')
                action = {
                    'name': 'Multiattack',
                    'commands': commands
                }
        
        if not action:
            action = {
                'name': shortestRangedAttack.name,
                'commands': [f'i a "{shortestRangedAttack.name}" -t "{closestPlayer.name}"']
            }
        
    else:
        if closestPlayerDistance <= rangedLongRange + speed:
            if len(rangedOnlyMultiattacks) > 0:
                bestMultiattack = None
                bestMultiattackMaxShortRange = float('inf')
                for multiattackOption in rangedOnlyMultiattacks:
                    minLongRange = float('inf')
                    maxShortRange = 0
                    for attack in multiattackOption:
                        rangedAttack = [rangedAttack for rangedAttack in rangedAttacks if rangedAttack.name == attack.name][0]
                        minLongRange = min(rangedAttack.longRange, minLongRange)
                        maxShortRange = max(rangedAttack.shortRange, maxShortRange)
                if (not bestMultiattack or maxShortRange < bestMultiattackMaxShortRange) and minLongRange >= shortestDistanceLongRange:
                    bestMultiattack = multiattackOption
                    bestMultiattackMaxShortRange = maxShortRange
                
                if bestMultiattack:
                    commands = []
                    for attack in bestMultiattack:
                        commands.append(f'i a "{attack.name}" -t "{closestPlayer.name}" -rr {attack.num} dis')
                    action = {
                        'name': 'Multiattack',
                        'commands': commands
                    }
                    
            if not action:
                shortestRangedAttackWithinRange = None
                for rangedAttack in rangedAttacks:
                    if not shortestRangedAttackWithinRange or rangedAttack.longRange < shortestRangedAttackWithinRange.longRange:
                        shortestRangedAttackWithinRange = rangedAttack
                    
                action = {
                    'name': shortestRangedAttackWithinRange.name,
                    'commands': [f'i a "{shortestRangedAttackWithinRange.name}" -t "{closestPlayer.name}" dis']
                }
        else:
            action = basicActions.dash
    
    return tempTiles, action

# def basicRangedAttacker(viableTiles, basicActions, combatantInfo, GLOBALS.MAP_X, GLOBALS.MAP_Y, convertCoordinatesToIndexes, getDistance, getSizeMultiplier):
    
#     shortRangeTempTiles = viableTiles.copy()
#     longRangeTempTiles = viableTiles.copy()
#     rangedShortRange = 0
#     rangedLongRange = 0
#     rangedAttacks = [] # Object of { name, shortRange, longRange }
    
#     for attack in CURRENT.attacks:
#         for automation in attack.raw.automation:
#             if automation.type == 'text' and 'Ranged' in automation.text:
#                 attackRangeAll = automation.text[automation.text.find('reach ') + 6:automation.text.find(' ft.')]
#                 attackRangeShort, attackRangeLong = attackRangeAll.split('/')
#                 rangedAttacks.append({ 'name': attack.name, 'shortRange': attackRangeShort, 'longRange': attackRangeLong })
#                 rangedShortRange = max(rangedShortRange, attackRangeShort)
#                 rangedLongRange = max(rangedLongRange, attackRangeLong)
#                 break
    
#     if rangedShortRange / GLOBALS.TILE_SIZE < max(GLOBALS.MAP_X, GLOBALS.MAP_Y) - 1:
#         # There are tiles on the map from which the monster cannot ranged attack all tiles on the map without disadvantage due to long range
    
#         # The coordinate limits within which a coordinate is guaranteed to have a target within range
#         shortMinX = None
#         shortMinY = None
#         shortMaxX = None
#         shortMaxY = None
#         longMinX = None
#         longMinY = None
#         longMaxX = None
#         longMaxY = None
        
#         allPlayerNames = []
#         for combatant in combat().combatants:
#             if not combatant.monster_name and 'location' in combatantInfo[combatant.name]:  # Combatant is a player
#                 allPlayerNames.append(combatant.name)

#         # To be used in case no players are in range, and monster does not have enough speed to get a player in range
#         closestDistance = float('inf')
#         closestTilesToTarget = set()
    
#         # This method of trying to eliminate loops is greedy.
#         # It basically builds a square around each player, and then takes the maximum and minimum x and y coordinates between those squares to make one giant square. It is assumed the monster can make a ranged attack against a player from any tile within that giant square
#         # However, on a big enough map or with a short enough ranged attack range, the giant square will contain holes in it where the monster cannot actually make a ranged attack against a player like it thinks it can
#         # I have deemed this scenario rare enough that the benefits of this method outweigh this edge case
#         # The benefits being the efficiency, and that the monster takes into account all the players on the map, instead of just the closest one like with the basic melee monster
#         for (x, y) in viableTiles:
#             if shortMinX is None or not (x >= shortMinX and x <= shortMaxX and y >= shortMinY and y <= shortMaxY):
#                 if shortMinX and x >= longMinX and x <= longMaxX and y >= longMinX and y <= longMaxY:   # tile is within long ranged attack range of a player but not within short ranged attack range
#                     shortRangeTempTiles.discard((x, y))
#                 else:
#                     playerWithinShortRange = False
#                     playerWithinLongRange = False
#                     for playerName in allPlayerNames:
#                         distance = getDistance((x, y), playerName)
#                         if distance <= rangedShortRange:
#                             playerWithinShortRange = True
#                             playerSize = combatantInfo[playerName].get('size', 'M')[0].upper()
#                             playerSizeMultiplier = getSizeMultiplier(playerSize)
#                             playerX, playerY = convertCoordinatesToIndexes(combatantInfo[playerName]['location'])
#                             shortMinX = playerX - rangedShortRange / GLOBALS.TILE_SIZE
#                             shortMinY = playerY - rangedShortRange / GLOBALS.TILE_SIZE
#                             shortMaxX = playerX + rangedShortRange / GLOBALS.TILE_SIZE + playerSizeMultiplier - 1
#                             shortMaxY = playerY + rangedShortRange / GLOBALS.TILE_SIZE + playerSizeMultiplier - 1
#                             break
#                         elif distance <= rangedLongRange:
#                             playerWithinLongRange = True
#                             playerSize = combatantInfo[playerName].get('size', 'M')[0].upper()
#                             playerSizeMultiplier = getSizeMultiplier(playerSize)
#                             playerX, playerY = convertCoordinatesToIndexes(combatantInfo[playerName]['location'])
#                             longMinX = playerX - rangedLongRange / GLOBALS.TILE_SIZE
#                             longMinY = playerY - rangedLongRange / GLOBALS.TILE_SIZE
#                             longMaxX = playerX + rangedLongRange / GLOBALS.TILE_SIZE + playerSizeMultiplier - 1
#                             longMaxY = playerY + rangedLongRange / GLOBALS.TILE_SIZE + playerSizeMultiplier - 1
#                             break
#                         elif distance < closestDistance:
#                             closestDistance = distance
#                             closestTilesToTarget = {(x, y)}
#                         elif distance == closestDistance:
#                             closestTilesToTarget.add((x, y))
#                     if not playerWithinRange:
#                         tempTiles.discard((x, y))
                    
#         if len(tempTiles) < 1:  # There are no players within the monster's short range ranged attack
#             minX = None
#             minY = None
#             maxX = None
#             maxY = None
#             tempTiles = closestTilesToTarget
                    
#     return tempTiles, None

def prioritiseLeastMovement(viableTiles):
    minDistance = float('inf')
    tempTiles = viableTiles.copy()
    for (x, y) in viableTiles:
        distance = getDistance(GLOBALS.CURRENT.name, (x, y))
        if distance == 0:
            tempTiles = {(x, y)}
            break
        elif distance < minDistance:
            minDistance = distance
            tempTiles = {(x, y)}
        elif distance == minDistance:
            tempTiles.add((x, y))
        else:
            tempTiles.discard((x, y))
    
    return tempTiles, None
    
FUNCTIONS = {
    'movementLimiter': movementLimiter,
    'avoidStandingInSpaceWithCombatants': avoidStandingInSpaceWithCombatants,
    'basicMeleeAttacker': basicMeleeAttacker,
    'basicRangedAttacker': basicRangedAttacker,
    'personalSpace': personalSpace,
    'prioritiseLeastMovement': prioritiseLeastMovement,
    'basicMelee': basicMelee,
    'basicRanged': basicRanged,
    'basicMeleeAndRanged': basicMeleeAndRanged
}

MONSTERS = {
    'basic': basic
}

def getMonster(monsterName):
    return MONSTERS[monsterName]