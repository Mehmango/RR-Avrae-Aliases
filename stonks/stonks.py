multiline
!embed
<drac2>
args = &ARGS&
title = "⊱ꕥ⊰ ・Stocks Guide・⊱ꕥ⊰ <:sans_wink:921803297503973476>"
desc = "**₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪**"
footer = ""
image = "https://i.kym-cdn.com/entries/icons/original/000/029/959/Screen_Shot_2019-06-05_at_1.26.32_PM.jpg" if randint(1,100) <= 1 else ""
debug = ""

INDUSTRY_MINIMUM_STOCK_VALUE = 10
INDUSTRY_PLAYER_STOCK_BUY_EFFECT = 0.005                # The percentage of an industry's stock's value that is gained when a player buys a stock
INDUSTRY_PLAYER_STOCK_SELL_EFFECT = 0.005               # The percentage of an industry's stock's value that is lost when a player sells a stock
INDUSTRY_MAX_TOTAL_PLAYER_STOCK_BUY_EFFECT = 1          # The maximum percentage of an industry's stock value that can be gained from players buying stocks
INDUSTRY_MAX_TOTAL_PLAYER_STOCK_SELL_EFFECT = 1         # The maximum percentage of an industry's stock value that can be lost from players selling stocks
INDUSTRY_BASELINE_STOCK_VALUE = 100
INDUSTRY_BASELINE_PULL_WEIGHT = 0.01                   # A factor affecting how much a stock's deviation from the baseline stock vlaue decreases further deviation from the baseline stock value
INDUSTRY_MAXIMUM_STOCK_VALUE_CHANGE_REDUCTION = 0.9     # The maximum percentage of change in a stock's value that can be overridden as a result of its deviation from the baseline stock value
INDUSTRY_NON_PREDICTED_STOCK_VALUE_CHANGE_DIVISION = 2  # The amount by which a stock value's change is divided if the report turns out to be wrong (The change is always a drop for a wrong positive report, and a rise for a wrong negative report)

CLAN_PLAYER_STOCK_BUY_EFFECT = 0.01                 # The percentage of a clan's stock's value that is gained when a player buys a stock
CLAN_PLAYER_STOCK_SELL_EFFECT = 0.01                  # The percentage of a clan's stock's value that is lost when a player sells a stock
CLAN_MAX_TOTAL_PLAYER_STOCK_BUY_EFFECT = 1.2        # The maximum percentage of a clan's stock value that can be gained from players buying stocks
CLAN_MAX_TOTAL_PLAYER_STOCK_SELL_EFFECT = 1.2       # The maximum percentage of a clan's stock value that can be lost from players selling stocks
CLAN_STOCK_STARTING_VALUE = 100                     # The starting value of a newly introduced clan's stock
CLAN_STOCK_STARTING_COUNT = 300                     # The starting count of a newly introduced clan's stock
CLAN_NON_PREDICTED_STOCK_VALUE_CHANGE_DIVISION = 1  # The amount by which a stock value's change is divided if the report turns out to be wrong (The change is always a drop for a wrong positive report, and a rise for a wrong negative report)

INTERACTIONS_PER_LEVEL = 2
NUM_REFRESHES_BEFORE_INTERACTION_REFRESH = 1          # The number of refreshes until player interactions are refreshed

backupStonksGvar = "2fe476e1-52f0-406e-a7d0-3a4c3c14aff0"
backupStonksJson = get_gvar(backupStonksGvar)
backupStonksDict = load_json(backupStonksJson)

stonksGvar = "1c39ee5d-0ff6-42e3-89a9-cda963feef7e"
stonksDict = load_json(get_gvar(stonksGvar))

backupPlayersGvar = "387f6c45-f072-412e-8933-255b9a503466"
backupPlayersJson = get_gvar(backupPlayersGvar)
backupPlayersDict = load_json(backupPlayersJson)

playersGvar = "232847e9-2e6b-4a40-b269-8509077a2ad6"
playersDict = load_json(get_gvar(playersGvar))

worldDict = stonksDict.world
industryDict = stonksDict.industries
clanDict = stonksDict.clans

backupStonksUpdated = False
stonksUpdated = False
backupPlayersUpdated = False
playersUpdated = False

helpMessage = "\n\n**A little lost? Here's a guide for you! <:sans_wink:921803297503973476> **"
helpMessage += "\n\n✦ `!stonks report` ⟶ Displays an up-to-date report of the whole stock market 📈"
helpMessage += "\n\n✦ `!stonks me` ⟶ Displays all your personal stocks :moneybag:"
helpMessage += "\n\n✦ `!stonks buy <industry> [count]` ⟶ Purchase stocks from an industry! *(Eg: `!stonks buy arts 3`)* <:NezukoHappy:921798493478195200>"
helpMessage += "\n\n✦ `!stonks sell <industry> [count]` ⟶ Sell an industry's stocks! *(Eg: `!stonks sell arts 2`)* <:nezukostare:921798265207402516>"

# Sets up the player's object (data) if this is their first time running the alias. Also assigns them a unique player ID
playerId = get("stonksPlayerId")
if playerId is None or playerId not in playersDict:
    playerId = (int(list(playersDict.keys())[-1]) + 1) if len(playersDict.keys()) > 0 else 0
    playersDict.update({playerId:{
        "name": name,
        "level": level,
        "interactions": level * INTERACTIONS_PER_LEVEL,
        "stocks": {}
    }})
    character().set_cvar("stonksPlayerId", playerId)
    playersUpdated = True
    
playerStonksDict = playersDict[playerId]

playerStonksDict.update(name=name)

oldLevel = playerStonksDict.level
newLevel = level
if newLevel>oldLevel:
    playerStonksDict.update(interactions=playerStonksDict.interactions+(INTERACTIONS_PER_LEVEL*(newLevel-oldLevel)))
    playerStonksDict.update(level=newLevel)
    playersUpdated = True
    
# Updates the player stonks dictionary with any new industries or clans
for stock in industryDict | clanDict:
    if stock not in playerStonksDict.stocks:
        playerStonksDict.stocks.update({
            stock:{
                "count": 0,
                "avgBoughtAt": 0,
                "stocksBoughtThisRefresh": 0,
                    }
            })
        playersUpdated = True
        
if len(args) > 0:
    if args[0].lower() == "refresh":
        
        title = "⊱ꕥ⊰ ・Refreshing the stock market...・⊱ꕥ⊰"
        
        backupStonksJson = dump_json(stonksDict)
        backupPlayersJson = dump_json(playersDict)
        
        if stonksDict.refreshesBeforeInteractionRefresh <= 0:
            stonksDict.update(refreshesBeforeInteractionRefresh=NUM_REFRESHES_BEFORE_INTERACTION_REFRESH)
            # Resetting player interaction count
            for player in playersDict.keys():
                maxInteractions = int(playersDict[player].level) * INTERACTIONS_PER_LEVEL
                playersDict[player].update(interactions=maxInteractions)
                for stock in playersDict[player].stocks:
                    playersDict[player].stocks[stock].update(stocksBoughtThisRefresh=0)
            desc += "\n\n**Player interactions have been refreshed!** <:NezukoHappy:921798493478195200>"
            
        else:
            stonksDict.update(refreshesBeforeInteractionRefresh=stonksDict.refreshesBeforeInteractionRefresh-1)
        
        worldEvents = worldDict.events
        currentWorldEvent = worldEvents[worldDict.currentEvent]
        worldDict.update(currentEvent=randint(0,len(worldEvents)))
        
        desc += "\n\n:globe_with_meridians: __**༺༻ World ༺༻**__ :globe_with_meridians:\n\n*" + worldDict.events[worldDict.currentEvent].hint + "*"
        
        desc += "\n\n**₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪**"
        desc += "\n\n**༺༻ :factory: INDUSTRIES :factory: ༺༻**"
        
        # Resetting and randomising hints and stock values for industries
        for industry, values in industryDict.items():
            industryEvents = values.events
            currentIndustryEvent = industryEvents[values.currentEvent]
            nextRefreshPlayerActionEffect = values.nextRefreshPlayerActionEffect
            oldStockValue = values.stockValue
            worldEventEffect = oldStockValue*currentWorldEvent.stockEffect if randint(1,100)/100 <= currentWorldEvent.effectChance else -(oldStockValue*currentWorldEvent.stockEffect/INDUSTRY_NON_PREDICTED_STOCK_VALUE_CHANGE_DIVISION)   # Possible multiplication by current world event's stock effect based on effect chance
            industryEventEffect = oldStockValue*currentIndustryEvent.stockEffect if randint(1,100)/100 <= currentIndustryEvent.effectChance else -(oldStockValue*currentIndustryEvent.stockEffect/INDUSTRY_NON_PREDICTED_STOCK_VALUE_CHANGE_DIVISION)   # Possible effect by current industry event's stock effect based on effect chance
            randomEffect = oldStockValue * (randint(-5,5)/100)  # Random stock value fluctuation
            newStockValue = max((oldStockValue + industryEventEffect + worldEventEffect + randomEffect),    
                                INDUSTRY_MINIMUM_STOCK_VALUE) # Minimum value of a stock
            
            playerActionEffectTotal = 0
            if newStockValue < oldStockValue:
                if nextRefreshPlayerActionEffect < 0:   # Only apply value drop caused by players selling if the stock value drops
                    playerActionEffectTotal = (newStockValue - oldStockValue) * min(abs(nextRefreshPlayerActionEffect), INDUSTRY_MAX_TOTAL_PLAYER_STOCK_SELL_EFFECT)
                    newStockValue += playerActionEffectTotal
                if oldStockValue < INDUSTRY_BASELINE_STOCK_VALUE:    # Decreasing the stock value drop/rise based on how much higher/lower the stock value is compared to the baseline stock value
                    newStockValue += (oldStockValue - newStockValue) * min(INDUSTRY_BASELINE_PULL_WEIGHT * (INDUSTRY_BASELINE_STOCK_VALUE - oldStockValue), INDUSTRY_MAXIMUM_STOCK_VALUE_CHANGE_REDUCTION)
            elif newStockValue > oldStockValue:
                if nextRefreshPlayerActionEffect > 0:   # Only apply value rise caused by players buying if the stock value rises
                    playerActionEffectTotal = (newStockValue - oldStockValue) * min(abs(nextRefreshPlayerActionEffect), INDUSTRY_MAX_TOTAL_PLAYER_STOCK_BUY_EFFECT)
                    newStockValue += playerActionEffectTotal
                if oldStockValue > INDUSTRY_BASELINE_STOCK_VALUE:    # Decreasing the stock value drop/rise based on how much higher/lower the stock value is compared to the baseline stock value
                    newStockValue -= (newStockValue - oldStockValue) * min(INDUSTRY_BASELINE_PULL_WEIGHT * (oldStockValue - INDUSTRY_BASELINE_STOCK_VALUE), INDUSTRY_MAXIMUM_STOCK_VALUE_CHANGE_REDUCTION)
            
            
            newStockValue = round(max(newStockValue, INDUSTRY_MINIMUM_STOCK_VALUE), 2)
            
            values.update(stockValue=newStockValue,
                                        currentEvent=randint(0,len(industryEvents)),
                                        nextRefreshPlayerActionEffect=0)

            desc += "\n\n**₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪**"
            desc += "\n\n" + values.icon + " __**༺༻ " + " " + industry.title() + " ༺༻**__ " + values.icon
            desc += "\n\n**✦ Stock Value: `" + oldStockValue + "gp` ► `" + values.stockValue + "gp`**  " + ("📈" if oldStockValue <= values.stockValue else ":chart_with_downwards_trend:")
            if (newStockValue > oldStockValue and nextRefreshPlayerActionEffect > 0) or (newStockValue < oldStockValue and nextRefreshPlayerActionEffect < 0):
                desc += "\n\n*Player actions contributed to an approximate `" + round(abs(playerActionEffectTotal), 2) + "gp` " + ("gain" if nextRefreshPlayerActionEffect >= 0 else "loss") + " in stock value this cycle!* " + ("<:HuTaoFingerGuns:939529495222841415>" if nextRefreshPlayerActionEffect >= 0 else "<:zyPaimonhehe:939528028097216592>") 
            # desc += "\n\n**✦ Stocks Left: `" + values.stockCount + "`**"
            desc += "\n\n*" + values.events[values.currentEvent].hint + "*"
            
        newClans = []
        desc += "\n\n**₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪**"
        desc += "\n\n**༺༻ :beginner: CLANS :beginner: ༺༻**"
        
        for clan, values in clanDict.items():
            if values["active"] and clan not in newClans:
                clanEvents = values["events"]
                currentClanEvent = clanEvents[values["currentEvent"]]
                nextRefreshPlayerActionEffect = values["nextRefreshPlayerActionEffect"]
                oldStockValue = values["stockValue"]
                dummy_old_stock_value = max(oldStockValue, 100)     # The value used to calculate fluctuations in stock value. Set to a minimum to prevent inconsequential changes when the stock value is very low
                worldEffect = dummy_old_stock_value * currentWorldEvent["stockEffect"] if randint(1,100)/100 <= currentWorldEvent["effectChance"] else -(dummy_old_stock_value * currentWorldEvent["stockEffect"] / CLAN_NON_PREDICTED_STOCK_VALUE_CHANGE_DIVISION) # Possible effect by current clan event's stock effect based on effect chance
                clanEffect = dummy_old_stock_value * currentClanEvent["stockEffect"] if randint(1,100)/100 <= currentClanEvent["effectChance"] else -(dummy_old_stock_value * currentClanEvent["stockEffect"] / CLAN_NON_PREDICTED_STOCK_VALUE_CHANGE_DIVISION) # Possible multiplication by current world event's stock effect based on effect chance
                randomEffect = dummy_old_stock_value * (randint(-5,5)/100)  # Random stock value fluctuation
                newStockValue = (oldStockValue + clanEffect + worldEffect + randomEffect)
                
                playerActionEffectTotal = 0
                if newStockValue < oldStockValue and nextRefreshPlayerActionEffect < 0:     # Only apply value drop caused by players selling if the stock value drops
                    playerActionEffectTotal = (newStockValue - oldStockValue) * min(abs(nextRefreshPlayerActionEffect), CLAN_MAX_TOTAL_PLAYER_STOCK_SELL_EFFECT)
                    newStockValue += playerActionEffectTotal
                elif newStockValue > oldStockValue and nextRefreshPlayerActionEffect > 0:   # Only apply value rise caused by players buying if the stock value rises
                    playerActionEffectTotal = (newStockValue - oldStockValue) * min(abs(nextRefreshPlayerActionEffect), CLAN_MAX_TOTAL_PLAYER_STOCK_BUY_EFFECT)
                    newStockValue += playerActionEffectTotal
                    
                newStockValue = round(newStockValue, 2)
                
                if newStockValue <= 0:  # Clan's stock has crashed, choose a new clan to replace it 
                    newClans.append(randchoice([clan for clan, values in clanDict.items() if not values["active"] and clan not in newClans]))
                    clanDict[clan].update(active=False)
                
                clanDict[clan].update(stockValue=newStockValue,
                                        currentEvent=randint(0,len(clanEvents)),
                                        nextRefreshPlayerActionEffect=0)
                
                # For Kankin's quest
                # if clan == 'tigersun':
                #     clanDict[clan].update(currentEvent=6)
                
                desc += "\n\n**₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪**"
                desc += "\n\n" + values["icon"] + " __**༺༻ " + " " + clan.title() + " ༺༻**__ " + values["icon"]
                desc += "\n\n**✦ Stock Value: `" + oldStockValue + "gp` ► `" + values["stockValue"] + "gp`**  " + ("📈" if oldStockValue <= values["stockValue"] else ":chart_with_downwards_trend:")
                if (newStockValue > oldStockValue and nextRefreshPlayerActionEffect > 0) or (newStockValue < oldStockValue and nextRefreshPlayerActionEffect < 0):
                    desc += "\n\n*Player actions contributed to an approximate `" + round(abs(playerActionEffectTotal), 2) + "gp` " + ("gain" if nextRefreshPlayerActionEffect >= 0 else "loss") + " in stock value this cycle!* " + ("<:HuTaoFingerGuns:939529495222841415>" if nextRefreshPlayerActionEffect >= 0 else "<:zyPaimonhehe:939528028097216592>") 
                if newStockValue <= 0:
                    desc += "\n\n**" + clan.title() + "'s stock has CRASHED!** <:PL_ThisIsFine:939659376212459541>"
                else:
                    # desc += "\n\n**✦ Stocks Left: `" + values["stockCount"] + "`**"
                    desc += "\n\n*" + values["events"][values["currentEvent"]]["hint"] + "*"
                    
        for clan, values in clanDict.items():
            if clan in newClans:
                debug += "\nNew Clan: " + clan
                clanEvents = values["events"]
                currentClanEvent = randint(0,len(clanEvents))
                clanDict[clan].update(active=True, 
                                      stockValue=CLAN_STOCK_STARTING_VALUE,
                                      stockCount=CLAN_STOCK_STARTING_COUNT,
                                      currentEvent=currentClanEvent,
                                      nextRefreshPlayerActionEffect=0)
                desc += "\n\n**₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪**"
                desc += "\n\n" + values["icon"] + " __**༺༻ " + " " + clan.title() + " ༺༻**__ " + values["icon"]
                desc += "\n\n**✦ Stock Value: `" + CLAN_STOCK_STARTING_VALUE + "gp`**"
                # desc += "\n\n**✦ Stocks Left: `" + CLAN_STOCK_STARTING_COUNT + "`**"
                desc += "\n\n*" + clanEvents[currentClanEvent]["hint"] + "*"
                
                for playerId, values in playersDict.items():
                    if clan in values["stocks"]:
                        playersDict[playerId]["stocks"][clan].update(count=0, avgBoughtAt=0)
                        playersUpdated = True
                        
        for player in playersDict.keys():
            for stock in playersDict[player].stocks:
                playersDict[player].stocks[stock].update(stocksBoughtThisRefresh=0)
                
        backupStonksUpdated = True
        stonksUpdated = True
        backupPlayersUpdated = True
        playersUpdated = True
                
    elif args[0].lower() == "rollback":
        
        title = "⊱ꕥ⊰ ・ :hourglass: Rewinding time :hourglass:・⊱ꕥ⊰"
        stonksDict = load_json(backupStonksJson)
        playersDict = load_json(backupPlayersJson)
        desc += "\n\n**The last refresh has been undone <:nezuko_yay:939529977555202048>**"
        
        stonksUpdated = True
        playersUpdated = True

    elif args[0].lower() == "report":
        
        title = "⊱ꕥ⊰ ・This week's report・⊱ꕥ⊰"
        
        desc += "\n\n:globe_with_meridians: __**༺༻ World ༺༻**__ :globe_with_meridians:\n\n*" + worldDict.events[worldDict.currentEvent].hint + "*"
        
        # Displaying data for all industries
        desc += "\n\n**₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪**"
        desc += "\n\n**༺༻ :factory: INDUSTRIES :factory: ༺༻**"
        for industry, values in industryDict.items():
            desc += "\n\n**₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪**"
            desc += "\n\n" + values.icon + " __**༺༻ " + " " + industry.title() + " ༺༻**__ " + values.icon
            desc += "\n\n**✦ Stock Value: `" + values.stockValue + "gp`**"
            # desc += "\n\n**✦ Stocks Left: `" + values.stockCount + "`**"
            desc += "\n\n*" + values.events[values.currentEvent].hint + "*"
            
        # Displaying data for all clans
        desc += "\n\n**₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪**"
        desc += "\n\n**༺༻ :beginner: CLANS :beginner: ༺༻**"
        for clan, values in clanDict.items():
            if values["active"]:
                desc += "\n\n**₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪**"
                desc += "\n\n" + values.icon + " __**༺༻ " + " " + clan.title() + " ༺༻**__ " + values.icon
                desc += "\n\n**✦ Stock Value: `" + values.stockValue + "gp`**"
                # desc += "\n\n**✦ Stocks Left: `" + values.stockCount + "`**"
                desc += "\n\n*" + values.events[values.currentEvent].hint + "*"
                
    elif args[0].lower() == "buy":
        
        title = "⊱ꕥ⊰ ・" + name + " buys some stocks!・⊱ꕥ⊰"
        
        # Checking for valid industry or clan input. Displays valid industry and clan inputs if input is invalid
        if len(args)<2 or args[1].lower() not in [stock for stock in industryDict | {clan:values for (clan,values) in clanDict.items() if values["active"]}]:
            desc += "\n\n**Please input a valid industry or clan to buy stocks in! <:surprisedpikachu:921798527875702786>**"
            desc += "\n\n*(Eg: `!stonks buy arts 4`)*"
            desc += "\n\n**₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪**"
            desc += "\n\n**__༺༻ :factory: Valid Industries :factory: ༺༻__**"
            for industry in industryDict:
                desc += "\n\n✦ " + industry.title() + " | " + industryDict[industry].icon
            desc += "\n\n**__༺༻ :beginner: Valid Clans :beginner: ༺༻__**"
            for clan, values in {clan:values for (clan,values) in clanDict.items() if values["active"]}.items():
                if values["active"]:
                    desc += "\n\n✦ " + clan.title() + " | " + values["icon"]
                    
        else:
            stock = args[1].lower()
            count = int(args[2]) if len(args) > 2 and args[2].isnumeric() else 1
            marketDict = None
            stockBuyEffect = 0
            if stock in industryDict:
                marketDict = industryDict
                stockBuyEffect = INDUSTRY_PLAYER_STOCK_BUY_EFFECT
            elif stock in clanDict:
                marketDict = clanDict
                stockBuyEffect = CLAN_PLAYER_STOCK_BUY_EFFECT
            # stockCount = int(marketDict[stock].stockCount)
            stockValue = marketDict[stock].stockValue
            coinPurse = character().coinpurse
            totalCoins = coinPurse.total
            interactionsNeeded = count
            stocksSoldThisRefresh = -min(playerStonksDict.stocks[stock].stocksBoughtThisRefresh, 0)
            interactionsNeeded -= 2*(min(interactionsNeeded, stocksSoldThisRefresh))     # Refund interactions when buying stocks the player sold this refresh
            
            if count<1:
                desc += "\n\n**You have to buy at least one stock, ya dingus! <:doge_kek:905836743289344031>**"
                # desc += "\n\n--------------------------------------------"
                # desc += "\n\n**" + marketDict[stock].icon + " Stocks Left: `" + marketDict[stock].stockCount + "`**"
            
            # elif stockCount < count:
            #     desc += "\n\n**There aren't enough " + stock.title() + " stocks for this purchase! <:surprisedpikachu:921798527875702786>**"
            #     desc += "\n\n--------------------------------------------"
            #     desc += "\n\n**" + marketDict[stock].icon + " Stocks Left: `" + marketDict[stock].stockCount + "`**"
                
            elif stockValue*count > totalCoins:
                desc += "\n\n**" + name + " does not have enough gold for this purchase! <:surprisedpikachu:921798527875702786>**"
                desc += "\n\n--------------------------------------------"
                desc += "\n\n**:moneybag: Required Gold: `" + stockValue*count + "`**"
                desc += "\n\n**:moneybag: Available Gold: `" + str(totalCoins) + "`**"
                
            elif interactionsNeeded > playerStonksDict.interactions:
                desc += "\n\n**" + name + " does not have enough interactions left for this purchase! <:surprisedpikachu:921798527875702786>**"
                desc += "\n\n--------------------------------------------"
                desc += "\n\n**<:nezukodead:921798440789377024> Interactions Left: `" + playerStonksDict.interactions + "`**"
                
            else:
                # # Updates the industry or clan's stock count and stock value 
                # marketDict[stock].update(stockCount=stockCount-count,
                #                             nextRefreshPlayerActionEffect = marketDict[stock].nextRefreshPlayerActionEffect + round(stockBuyEffect*count,2))
                
                # Updates the industry or clan's stock value and the player action effect for the next refresh
                marketDict[stock].update(nextRefreshPlayerActionEffect = marketDict[stock].nextRefreshPlayerActionEffect + (stockBuyEffect*count))
                
                # Updates player's coin pouch
                coinPurse.modify_coins(gp=-(int(stockValue*count)))
                footer += name + "'s Coin Pouch: " + str(totalCoins) + "gp -> " + str(coinPurse.get_coins().total) + "gp"
                
                playerStonksDict.update(interactions=playerStonksDict.interactions - interactionsNeeded)
                playerStonksDict.stocks[stock].update(
                    count=playerStonksDict.stocks[stock].count + count, 
                    avgBoughtAt=round(((count*stockValue)+(playerStonksDict.stocks[stock].avgBoughtAt*playerStonksDict.stocks[stock].count))/(playerStonksDict.stocks[stock].count+count), 2),
                    stocksBoughtThisRefresh=playerStonksDict.stocks[stock].stocksBoughtThisRefresh+count)
                
                # Displays player and industry's updated data
                desc += "\n\n**" + name + " successfully purchases `" + count + "` " + stock.title() + " stocks! <:tanjirowow:922537039524692088>**"
                desc += "\n\n**₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪**"                
                desc += "\n\n**💰 " + name + "'s " + stock.title() + " stocks: `" + playerStonksDict.stocks[stock].count + "`💰**"
                desc += "\n\n**<:nezukodead:921798440789377024> Interactions Left: `" + playerStonksDict.interactions + "`**"
                # desc += "\n\n--------------------------------------------"
                # desc += "\n\n**✦ Updated " + marketDict[stock].icon + " " + industry.title() + " Stock Value: `" + marketDict[stock].stockValue + "gp`**"
                # desc += "\n**✦ Updated " + marketDict[stock].icon + " " + stock.title() + " Stock Count: `" + marketDict[stock].stockCount + "`**"
        
                playersUpdated = True
                stonksUpdated = True
        
    elif args[0].lower() == "sell":
        
        title = "⊱ꕥ⊰ ・" + name + " sells some stocks!・⊱ꕥ⊰"
        
        # Checking for valid industry or clan input. Displays valid industry and clan inputs if input is invalid
        if len(args)<2 or args[1].lower() not in [stock for stock in industryDict | {clan:values for (clan,values) in clanDict.items() if values["active"]}]:
            desc += "\n\n**Please input a valid industry or clan to sell stocks to! <:surprisedpikachu:921798527875702786>**"
            desc += "\n\n*(Eg: `!stonks sell arts 4`)*"
            desc += "\n\n**₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪**"
            desc += "\n\n**__༺༻ :factory: Valid Industries :factory: ༺༻__**"
            for industry in industryDict:
                desc += "\n\n✦ " + industry.title() + " | " + industryDict[industry].icon
            desc += "\n\n**__༺༻ :beginner: Valid Clans :beginner: ༺༻__**"
            for clan, values in clanDict.items():
                if values["active"]:
                    desc += "\n\n✦ " + clan.title() + " | " + values["icon"]
                    
        else:
            stock = args[1].lower()
            count = int(args[2]) if len(args) > 2 and args[2].isnumeric() else 1
            marketDict = None
            stockSellEffect = 0
            if stock in industryDict:
                marketDict = industryDict
                stockSellEffect = INDUSTRY_PLAYER_STOCK_SELL_EFFECT
            elif stock in clanDict:
                marketDict = clanDict
                stockSellEffect = CLAN_PLAYER_STOCK_SELL_EFFECT
            
            playerStockCount = int(playerStonksDict.stocks[stock].count if stock in playerStonksDict.stocks else 0)
            stockValue = marketDict[stock].stockValue
            coinPurse = character().coinpurse
            totalCoins = coinPurse.total
            interactionsNeeded = count
            stocksBoughtThisRefresh = max(0, playerStonksDict.stocks[stock].stocksBoughtThisRefresh)
            interactionsNeeded -= 2*(min(interactionsNeeded, stocksBoughtThisRefresh))     # Refund interactions when selling stocks the player bought this refresh
            
            if count<1:
                desc += "\n\n**You have to sell at least one stock, ya dingus! <:doge_kek:905836743289344031>**"
                desc += "\n\n--------------------------------------------"
                desc += "\n\n**" + name + "'s " + marketDict[stock].icon + " " + stock.title() + " Stocks: `" + playerStockCount + "`**" 

            elif count > playerStockCount:
                desc += "\n\n**" + name + " does not have that many stocks to sell! <:surprisedpikachu:921798527875702786>**"
                desc += "\n\n**--------------------------------------------**"
                desc += "\n\n**" + name + "'s " + marketDict[stock].icon + " " + stock.title() + " Stocks: `" + playerStockCount + "`**" 
            
            
            elif interactionsNeeded > playerStonksDict.interactions:
                desc += "\n\n**" + name + " does not have enough interactions left for this transaction! <:surprisedpikachu:921798527875702786>**"
                desc += "\n\n--------------------------------------------"
                desc += "\n\n**<:nezukodead:921798440789377024> Interactions Left: `" + playerStonksDict.interactions + "`**"
            
            else:
                playerStonksDict.update(interactions=playerStonksDict.interactions - interactionsNeeded)
                playerStonksDict.stocks[stock].update(count=playerStonksDict.stocks[stock].count - count, stocksBoughtThisRefresh=playerStonksDict.stocks[stock].stocksBoughtThisRefresh-count)
                if playerStonksDict.stocks[stock].count < 1:
                    playerStonksDict.stocks[stock].update(avgBoughtAt=0)

                # Updates player's coin pouch
                coinPurse.modify_coins(gp=int(stockValue*count))
                footer += name + "'s Coin Pouch: " + str(totalCoins) + "gp -> " + str(coinPurse.get_coins().total) + "gp"
                
                # # Updates industry or clan's data
                # marketDict[stock].update(stockCount = marketDict[stock].stockCount+count,
                #                             nextRefreshPlayerActionEffect = marketDict[stock].nextRefreshPlayerActionEffect - round(stockSellEffect*count,2))

                # Updates industry or clan's data
                marketDict[stock].update(nextRefreshPlayerActionEffect = marketDict[stock].nextRefreshPlayerActionEffect - (stockSellEffect*count))
           

                # Displays player and industry's updated data
                desc += "\n\n**" + name + " successfully sells `" + count + "` " + stock.title() + " stocks! <:tanjirowow:922537039524692088>**"
                desc += "\n\n**₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪**"                
                desc += "\n\n**💰 " + name + "'s " + stock.title() + " stocks: `" + playerStonksDict.stocks[stock].count + "`💰**"
                desc += "\n\n**<:nezukodead:921798440789377024> Interactions Left: `" + playerStonksDict.interactions + "`**"
                # desc += "\n\n--------------------------------------------"
                # desc += "\n\n**✦ Updated " + marketDict[stock].icon + " " + industry.title() + " Stock Value: `" + marketDict[stock].stockValue + "gp`**"
                # desc += "\n**✦ Updated " + marketDict[stock].icon + " " + stock.title() + " Stock Count: `" + marketDict[stock].stockCount + "`**"
                
                playersUpdated = True
                stonksUpdated = True
                
    # elif args[0].lower() == "trade":
        
    #     title = "⊱ꕥ⊰ ・" + name + " trades some stocks!・⊱ꕥ⊰"
        
    #     if len(args)<2 or args[1] not in [player.name for player in playersDict.values()]:
    #         desc += "\n\n**Please input a valid name of a player to trade stocks to! <:surprisedpikachu:921798527875702786>**"
    #         desc += "\n\n*(Eg: `!stonks trade Bob arts 4`)*"
                    
    #     # Checking for valid industry or clan input. Displays valid industry and clan inputs if input is invalid
    #     if len(args)<3 or args[2].lower() not in [stock for stock in industryDict | {clan:values for (clan,values) in clanDict.items() if values["active"]}]:
    #         desc += "\n\n**Please input a valid industry or clan to trade stocks in! <:surprisedpikachu:921798527875702786>**"
    #         desc += "\n\n*(Eg: `!stonks trade Bob arts 4`)*"
    #         desc += "\n\n**₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪**"
    #         desc += "\n\n**__༺༻ :factory: Valid Industries :factory: ༺༻__**"
    #         for industry in industryDict:
    #             desc += "\n\n✦ " + industry.title() + " | " + industryDict[industry].icon
    #         desc += "\n\n**__༺༻ :beginner: Valid Clans :beginner: ༺༻__**"
    #         for clan, values in clanDict.items():
    #             if values["active"]:
    #                 desc += "\n\n✦ " + clan.title() + " | " + values["icon"]
                    
    #     else:
    #         targetPlayerName = args[1]
    #         targetPlayerId = ""
    #         for id, values in playersDict.items():
    #             if values.name == targetPlayerName:
    #                 targetPlayerId = id
    #                 break;
                 
    #         stock = args[2].lower()
    #         count = int(args[3]) if len(args) > 3 and args[3].isnumeric() else 1
            
    #         if stock in industryDict:
    #             marketDict = industryDict
    #         elif stock in clanDict:
    #             marketDict = clanDict
    
    #         playerStockCount = int(playerStonksDict.stocks[stock].count if stock in playerStonksDict.stocks else 0)
            
    #         if count > playerStockCount:
    #             desc += "\n\n**" + name + " does not have that many stocks to trade! <:surprisedpikachu:921798527875702786>**"
    #             desc += "\n\n**--------------------------------------------**"
    #             desc += "\n\n**" + name + "'s " + marketDict[stock].icon + " " + stock.title() + " Stocks: `" + playerStockCount + "`**" 
            
    #         elif count<1:
    #             desc += "\n\n**You have to trade at least one stock, ya dingus! <:doge_kek:905836743289344031>**"
    #             desc += "\n\n--------------------------------------------"
    #             desc += "\n\n**" + name + "'s " + marketDict[stock].icon + " " + stock.title() + " Stocks: `" + playerStockCount + "`**"
                
    #         else:
    #             playerStonksDict.stocks[stock].update(count=playerStonksDict.stocks[stock].count - count)
    #             playersDict[targetPlayerId].stocks[stock].update(count=playersDict[targetPlayerId].stocks[stock].count + count)
                
    #             desc += "\n\n**" + name + " successfully trades `" + count + "` " + marketDict[stock].icon + " " + stock.title() + " stocks to " + targetPlayerName + "! <:tanjirowow:922537039524692088>**"
    #             desc += "\n\n**₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪**"
    #             desc += "\n\n**💰 " + name + "'s " + stock.title() + " stocks: `" + playerStonksDict.stocks[stock].count + "` 💰**"
    #             desc += "\n\n**💰 " + targetPlayerName + "'s " + stock.title() + " stocks: `" + playersDict[targetPlayerId].stocks[stock].count + "` 💰**"
            
    #             playerUpdated = True
            
    elif args[0].lower() == "me":
        
        title = "⊱ꕥ⊰ ・" + name + " checks their stocks!・⊱ꕥ⊰"
        desc += "\n\n**__༺༻ Stock Count: ༺༻__**"
        
        for stock, stockInfo in playerStonksDict.stocks.items():
            stock = stock.lower()
            if stock in industryDict:
                marketDict = industryDict
            elif stock in clanDict:
                marketDict = clanDict
                
            if not (marketDict == clanDict and not clanDict[stock]["active"]):
                desc += "\n\n**✦ " + marketDict[stock].icon + " " + stock.title() + " stocks:** `" + int(stockInfo.count) + "`"
                desc += "\n∘  *Stocks purchased for an average of `" + round(stockInfo.avgBoughtAt, 2) + "gp`*"
            
        desc += "\n\n**₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪**"
        desc += "\n\n**<:nezukodead:921798440789377024> Interactions Left: `" + playerStonksDict.interactions + "`**"
            
    else:
        desc = helpMessage
else:
    desc = helpMessage
    
desc += "\n\n**₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪**"
stonksJson = dump_json(stonksDict)
playersJson = dump_json(playersDict)
                
return f""" -title "{title}" -desc "{desc}" -footer "{footer}" -image "{image}" """
</drac2>
{{("!gvar edit " + backupStonksGvar + " " + backupStonksJson) if backupStonksUpdated else ""}}
{{("!gvar edit " + stonksGvar + " " + stonksJson) if stonksUpdated else ""}}
{{("!gvar edit " + backupPlayersGvar + " " + backupPlayersJson) if backupPlayersUpdated else ""}}
{{("!gvar edit " + playersGvar + " " + playersJson) if playersUpdated else ""}}
