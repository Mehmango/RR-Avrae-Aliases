multiline
{{ctx.prefix}}embed
<drac2>
testVersion = False
argList = &ARGS&

# **********************
# *** Base Variables ***
# **********************

args = argparse(argList, parse_ephem=False)

defaults = load_json(get_svar("mapDefaults") or "{}") or {}
mapsize = defaults.get("size", "10x10") or "10x10"
maxSize = 99
if mapsize != "JSON":
    mapSplitX, mapSplitY = mapsize.lower().split('x')
    mapX = max(min(int(mapSplitX) if mapSplitX.isdigit() else 1, maxSize), 1)
    mapY = max(min(int(mapSplitY) if mapSplitY.isdigit() else 1, maxSize), 1)
    mapsize = f"{mapX}x{mapY}"
mapoptions = defaults.get("options", "")
mapbg = defaults.get("background", "")
mapinfo = {}
mapview = ""
mapviewsize = ""
mapviewlocation = ""
mapattach = None
map = get("otfbm_base_url", "http://otfbm.io/")
walls = []
objects = []
loadedjson = []
fow = []
targ = None
out = {}
baseAlph = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alph = []
for index in range(maxSize):
    letter = ""
    if index // 26:
        letter = baseAlph[(index // 26) - 1]
    letter += baseAlph[index % 26]
    alph.append(letter)
presetObjects = load_json(get_gvar("9b15344a-1f09-43b5-b84e-f61e32e4a89a"))
overlays = []
spelllist = []
c = combat()
gt = c.get_combatant if c else None
debug = []
desc = []
finalMap = ""
sizeOffset = {"T": 0, "S": 0, "M": 0, "L": 1, "H": 1, "G": 2}
COL, SIZ = {"w": "white", "bk": "black", "gy": "grey", "r": "red", "g": "green", "b": "blue", "y": "yellow", "p": "purple", "pk": "pink",
            "c": "cyan", "bn": "brown", "o": "orange"}, {"T": "Tiny", "S": "Small", "M": "Medium", "L": "Large", "H": "Huge", "G": "Gargantuan"}

# We don't have an aim point/target yet
aimPoint = ""
aimTarget = ""
targAimPoint = ""
targAimTarget = ""
aimStick = False
targPoint = ""
aim = ""
effect = None
effectName = ""
effectTarget = ""
prevLoc = ""

# F-Strings like to yell at me for \'s
newline, targD, aimD, quote = "\n", "{targ}", "{aim}", '\\"'

# What characters do we need to strip from names?
nameStrip = r"""'"()[]{}*?^%$&#/-_~“”‘’"""
</drac2>

# <drac2>
# # Pulling up tokenlist to view all created tokens
# serverTokens = load_json(get_svar('mapTokens') or '{}')
# userTokens = load_json(get('mapTokens', '{}'))
# serverTokens.update(userTokens)
# userTokens = serverTokens
# tokenlist = [f"""**{tokens}** - `{str(over).replace('"',quote)}`""" for tokens,
#              over in userTokens.items() if args.last('search', '').lower() in tokens.lower()]
# tokenPagin = [tokenlist[i:i+20] for i in range(0, len(tokenlist), 20)]
# </drac2>

<drac2>
# If we're in combat, check all the things
if c:
    # Collect information on every combatant
    for combatant in combat().combatants:
        # Grab map information, if it exists
        for attack in combatant.attacks:
            if attack.name == 'map':
                mapattach = combatant
                mapinfo = attack.raw.automation[-1].text
                break
        if mapattach:
            break
</drac2>

<drac2>
if c:
    # If we found a `map` attack with information, parse it now
    if mapinfo:
        # Split and convert to dict. Couldn't use | here because of how -attack effects are parsed
        mapinfo = mapinfo.split(' ~ ')
        mapinfo = {x[0].lower(): x[1] for x in [item.split(': ')
                                                for item in mapinfo]}
        if mapinfo.get('size') == None:
            mapsize = defaults.get("size", "10x10") or "10x10"
        else:
            mapsize = mapinfo.get('size')
        # If user hasn't set mapsize = "JSON" then continue
        if mapsize != "JSON":
            if ":" in mapsize:
                mapLocSize = mapsize.split(':')
                mapviewlocation = f"{mapLocSize[0]}:"
                mapsize = mapviewsize = mapLocSize[1]
            if mapsize[0].isdigit():
                mapSplitX, mapSplitY = mapsize.lower().split('x')
                mapX = min(int(mapSplitX) if mapSplitX.isdigit()
                           else 1, maxSize)
                mapY = min(int(mapSplitY) if mapSplitY.isdigit()
                           else 1, maxSize)
            else:
                mapX = alph.index(''.join(x.upper()
                                  for x in mapsize if x.isalpha()))
                mapY = int(''.join(y for y in mapsize if y.isdigit()))
            mapsize = f"{mapX}x{mapY}"
        mapbg = mapinfo.get('background')
        mapoptions = mapinfo.get('options')
        walls = mapinfo.get('walls')
        walls = walls.split(', ') if walls else []
        objects = mapinfo.get('objects')
        objects = objects.split('/') if objects else []
        loadedjson = mapinfo.get('json')
        loadedjson = loadedjson.split(', ') if loadedjson else []
        fow = mapinfo.get('fow')
        fow = fow.split(', ') if fow else []
        if mapinfo.get('view'):
            mapviewlocation, mapviewsize = mapinfo.get(
                'view').replace('::', ':').split(':')
</drac2>

<drac2>
if c:
    # Read each combatants notes for their information
    for target in combat().combatants:
        # If they have a note, perse it into a dict
        if target.note and ':' in target.note:
            note = target.note
            note = note.split(" | ")
            note = {x[0].lower(): x[1] for x in [item.split(": ")
                                                 for item in note]}
            if note.get('location'):
                note['location'] = note['location'].upper()
            out[target.name] = note
            # Check if we have any overlays attached to effects, and then if at effect exists
            for overNum in [""]+[str(x) for x in range(1, 11)]:
                if out[target.name].get('effect'+overNum):
                    checkEffect, checkEffectTarget = out[target.name].get(
                        'effect'+overNum).split(' / ')
                    # If the effect (or the target it was on) are gone, remove the effect
                    if not gt(checkEffectTarget) or not gt(checkEffectTarget).get_effect(checkEffect):
                        _ = out[target.name].pop(
                            'effect'+overNum) if 'effect'+overNum in out[target.name] else None
                        _ = out[target.name].pop(
                            'aim'+overNum) if 'aim'+overNum in out[target.name] else None
                        _ = out[target.name].pop(
                            'overlay'+overNum) if 'overlay'+overNum in out[target.name] else None
                        desc.append(
                            f"""Overlay {overNum} removed from `{target.name}` because effect `{checkEffect}` no longer present{f" on {checkEffectTarget}" if checkEffectTarget!=target.name else ""}.""")
                        desc.append("")
        elif target.note:
            note = target.note
            desc.append(
                f"Found a incorrectly formatted note on {target.name}, reformatted as a `-note`. ")
            out[target.name] = {"note": note.replace(
                ':', ' ').replace('|', ' ')}
        else:
            out[target.name] = {}
</drac2>

<drac2>
# Lets back up our map each time we run it, why not
# This will back the entire `out` dictionary containing everyones positions and states
# to a uvar named mapStates, with the current channels id added as s key inside it.
# This way you won't accidentally overwrite your backup with the backup from another channel

mapStates = load_json(get('mapStates', '{}'))
prevBack = mapStates.get(str(ctx.channel.id))
mapStates.update({str(ctx.channel.id): out})
lengthTotal = len(dump_json(mapStates))
if lengthTotal >= 8000:
    delete_uvar("mapStates")
    mapStates = {str(ctx.channel.id): out}
    set_uvar('mapStates', dump_json(mapStates))
    desc.append(f"The uvar `mapStates`, which contains information for `!map undo`, was full, so it was cleared and current map setup was backed up.")
else:
    mapStates.update({str(ctx.channel.id): out})
    set_uvar('mapStates', dump_json(mapStates))
# Clean up old uvars that are no longer needed
delete_uvar("mapState"+str(ctx.channel.id))
delete_uvar("mapSize"+str(ctx.channel.id))
</drac2>

<drac2>
outputTitle = "**:space_invader: Toggling Allies :space_invader:**"
outputDesc = ""
if not c:
    outputDesc = "**:warning: Error: Channel is not in combat**"
else:
    debug = ''
    removedAllyNames = []
    newAllyNames = []
    for combatantName in argList:
        combatant = gt(combatantName)
        if not out.get(combatant.name):
            out[combatant.name] = {}
        combatantIsAlly = 'ally' in out[combatant.name].keys()
        if combatantIsAlly:
            debug += 'marking as enemy'
            out[combatant.name].pop('ally')
            removedAllyNames.append(combatant.name)
        else:
            debug += 'marking as ally'
            out[combatant.name].update({"ally": True})
            newAllyNames.append(combatant.name)
    
    if len(newAllyNames) > 0:
        outputDesc += "**__Marked as allies__**"
        for newAlly in newAllyNames:
            outputDesc += "\n- " + newAlly
    if len(removedAllyNames) > 0:
        outputDesc += "\n\n**__Marked as enemies__**"
        for removedAlly in removedAllyNames:
            outputDesc += "\n- " + removedAlly

    # output += '\n\n' + debug + '\n\n'
</drac2>

<drac2>
if c:
    # Parse the collected notes and information into the format readable by otfbm.com
    people = []
    for target in out:
        tLocation = out[target].get('location')
        tSize = out[target].get('size', 'M')[0].upper()
        tColor = out[target].get(
            'color', 'b' if '/' in gt(target).hp_str() else 'r') + " "
        tColor = tColor[:tColor.index(" ")].strip('#')
        tToken = out[target].get('token')
        # Account for hex colors
        if len(tColor) in (3, 6):
            tColor = f"~{tColor}".upper()
        tName = target.translate(str.maketrans(' ', '_', nameStrip))
        tName = tName.splitlines()[0]
        # Only display if they have a location
        if tLocation:
            people.append(
                f"{tLocation}{tSize}{tColor}-{tName}{f'~{tToken}' if tToken else ''}")
        # Do they have a height set? If so, display it
        if out[target].get('height'):
            desc.append(
                f"{target} is currently {out[target].get('height').strip('-+')} ft. {['above','below'][int(out[target].get('height').strip(' ft.m'))<0] if out[target].get('height').strip(' -+ft.m').isdigit() else 'above'} the ground.")
        # Do they have overlays?
        for overNum in [""]+[str(x) for x in range(1, 11)]:
            # Ensure we're not grabbing the previous overlays aim point
            targAimPoint = ""
            if out[target].get('overlay'+overNum):
                targPoint = out[target].get('location', 'A1')
                # Is our target Large or bigger? If so, adjust accordingly
                if out[target].get('size', "M")[0] in "LHG":
                    targOffset = sizeOffset.get(
                        out[target].get('size', "M")[0])
                    TargX = ''.join(x for x in targPoint if x.isalpha())
                    TargY = int(''.join(y for y in targPoint if y.isdigit()))
                    TargX = alph[alph.index(TargX)+targOffset]
                    TargY += targOffset
                    targPoint = f"{TargX}{TargY}"
                # If the target has an aim point set
                if out[target].get('aim'+overNum):
                    for aimTarget in out:
                        # We need to check to see if they were targetting a... target
                        if out[target].get('aim'+overNum).lower() in aimTarget.lower():
                            targAimPoint = out[aimTarget]['location']
                            # Is our aimTarget larger than medium? If so, we need to offset to adjust
                            if out[aimTarget].get('size', "M")[0] in "LHG":
                                targAimOffset = sizeOffset.get(
                                    out[aimTarget].get('size', "M")[0])
                                targAimTargX = ''.join(
                                    x for x in targAimPoint if x.isalpha())
                                targAimTargY = int(
                                    ''.join(y for y in targAimPoint if y.isdigit()))
                                targAimTargX = alph[alph.index(
                                    targAimTargX)+targAimOffset]
                                targAimTargY += targAimOffset
                                targAimPoint = f"{targAimTargX}{targAimTargY}"
                        # If the aimTarget wasn't a target, it was coordinates. Use them.
                        if not targAimPoint:
                            targAimPoint = out[target].get(
                                'aim'+overNum).upper()
                # Add each targets overlay to the overlays list
                overlays.append(out[target].get(
                    'overlay'+overNum).replace("{targ}", targPoint).replace("{aim}", targAimPoint).strip("*"))
    # Reconvert all of our map information back into the readable note format
    dataout = {x: ' | '.join(
        [f"{item[0].title()}: {item[1]}"for item in out[x].items()])for x in out}
    # Then set everyones note again. Kinda a chainsaw instead of a scalpel situation here.
    for target in dataout:
        gt(target).set_note(dataout[target])
    # If a 'clear' arg is given, clear the entire map (clears everyones notes)
    if args.last('clear'):
        [i.set_note(None)for i in combat().combatants]
        people = []
        overlays = []
    # Join everything together and display the map if we aren't displaying the help

    # Analytics removed, temporarily:
    # &cid={ctx.channel.id}&sid={ctx.guild.id}&uid={ctx.author.id}{"&d=1" if testVersion else ""}

    overlays = [f"*{overlay.strip('*')}" for overlay in overlays]
    if not any(args.get(arg) for arg in ('help')):
        finalMap = f"""{map}{mapsize}{f"/{mapviewlocation}:{mapviewsize}" if mapviewsize and mapviewlocation else ""}/{f'_{"_".join(walls)}/' if walls else ""}{f"@{mapoptions}/"if mapoptions else""}{f'{"/".join(objects)}/' if objects else ""}{f'{"*f"+"/*f".join(fow).replace(":", "")}/' if fow else ""}{'/'.join(people+overlays)}/?a=2{f"&load={'&load='.join(loadedjson)}" if loadedjson else ""}{f"&bg={mapbg.split('?')[0]}" if mapbg else ""}"""
        return f"""{'' if args.last('silent') else f'-image "{finalMap}"'} -f "[Map]({finalMap})" """ + (f"""  -desc "{newline.join([outputDesc] + desc)}"  """ if outputDesc or desc else "") + (f"""  -title "{outputTitle}"  """)
</drac2>

-footer "!amimo help | By @mehmango | {{f" | Map settings attached to {mapattach.name}" if mapattach else ""}}"
-color < color >