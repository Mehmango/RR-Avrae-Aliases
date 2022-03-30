multiline
!embed
<drac2>
args = &ARGS&
title = "⊱ꕥ⊰ ・Stocks Guide・⊱ꕥ⊰ <:sans_wink:921803297503973476>"
desc = "**₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪**"
footer = ""
image = "https://i.kym-cdn.com/entries/icons/original/000/029/959/Screen_Shot_2019-06-05_at_1.26.32_PM.jpg" if randint(1,100) <= 1 else ""

MINIMUM_STOCK_VALUE = 10
PLAYER_STOCK_BUY_EFFECT = 0.01              # The percentage of an industry's stock's value that is gained when a player buys a stock
PLAYER_STOCK_SELL_EFFECT = 0.01             # The percentage of an industry's stock's value that is lost when a player sells a stock
BASELINE_STOCK_VALUE = 100
BASELINE_PULL_WEIGHT = 0.008                # A factor affecting how much a stock's deviation from the baseline stock vlaue decreases further deviation from the baseline stock value
MAXIMUM_STOCK_VALUE_CHANGE_REDUCTION = 0.9  # The maximum percentage of change in a stock's value that can be overridden as a result of its deviation from the baseline stock value
INTERACTIONS_PER_LEVEL = 2

stonksGvar = "1c39ee5d-0ff6-42e3-89a9-cda963feef7e"
stonksDict = load_json(get_gvar(stonksGvar))
marketDict = stonksDict.market
playersDict = stonksDict.players

helpMessage = "\n\n**A little lost? Here's a guide for you! <:sans_wink:921803297503973476> **"
helpMessage += "\n\n✦ `!stonks report` ⟶ Displays an up-to-date report of the whole stock market 📈"
helpMessage += "\n\n✦ `!stonks me` ⟶ Displays all your personal stocks :moneybag:"
helpMessage += "\n\n✦ `!stonks buy <industry> [count]` ⟶ Purchase stocks from an industry! *(Eg: `!stonks buy arts 3`)* <:NezukoHappy:921798493478195200>"
helpMessage += "\n\n✦ `!stonks sell <industry> [count]` ⟶ Sell an industry's stocks! *(Eg: `!stonks sell arts 2`)* <:nezukostare:921798265207402516>"

# Sets up the player's object (data) if this is their first time running the alias. Also assigns them a unique player ID
playerId = get("stonksPlayerId")
if playerId is None:
    playerId = int(list(playersDict.keys())[-1]) + 1 if len(playersDict.keys()) > 0 else 0
    playersDict.update({playerId:{
        "name": name,
        "level": level,
        "interactions": level * INTERACTIONS_PER_LEVEL,
        "stocks": {}
    }})
    character().set_cvar("stonksPlayerId", playerId)
    
playerStonksDict = playersDict[playerId]

playerStonksDict.update(name=name)

oldLevel = playerStonksDict.level
newLevel = level
if newLevel>oldLevel:
    playerStonksDict.update(interactions=playerStonksDict.interactions+(INTERACTIONS_PER_LEVEL*(newLevel-oldLevel)))
    playerStonksDict.update(level=newLevel)

# Transfers data from the player stonks cvar to the stonks gvar, then deletes the cvar (to update the data storage method)
playerStonksCvar = get("stonks")
if playerStonksCvar is not None:
    playerStonksCvar = load_json(playerStonksCvar)
    for industry in playerStonksCvar.keys():
        playerStonksDict.stocks.update({industry:playerStonksCvar[industry]})
        
    character().delete_cvar("stonks")
        

# Updates the player stonks dictionary with any new industries
for industry in marketDict:
    if industry != "world" and industry not in playerStonksDict.stocks:
        playerStonksDict.stocks.update({industry:0})

if len(args) > 0:
    if args[0].lower() == "refresh":
        
        title = "⊱ꕥ⊰ ・Refreshing the stock market...・⊱ꕥ⊰"
        
        worldEvents = marketDict.world.events
        currentWorldEvent = worldEvents[marketDict.world.currentEvent]
        marketDict.world.update(currentEvent=randint(0,len(worldEvents)))
        
        desc += "\n\n:globe_with_meridians: __**༺༻ World ༺༻**__ :globe_with_meridians:\n\n*" + marketDict.world.events[marketDict.world.currentEvent].hint + "*"
        
        # Resetting player interaction count
        for player in playersDict.keys():
            maxInteractions = int(playersDict[player].level) * 2
            playersDict[player].update(interactions=maxInteractions)
        
        # Resetting and randomising hints and stock values
        for industry, values in marketDict.items():
            if industry != "world":
                
                for i in range(1):
                    industryEvents = marketDict[industry].events
                    currentIndustryEvent = industryEvents[marketDict[industry].currentEvent]
                    oldStockValue = marketDict[industry].stockValue
                    newStockValue = max(
                                            (
                                                oldStockValue
                                                + (oldStockValue*currentIndustryEvent.stockEffect if randint(1,100)/100 <= currentIndustryEvent.effectChance else 0)    # Possible effect by current industry event's stock effect based on effect chance
                                                + (oldStockValue*currentWorldEvent.stockEffect if randint(1,100)/100 <= currentWorldEvent.effectChance else 0)  # Possible multiplication by current world event's stock effect based on effect chance
                                            )
                                            * (1+randint(-5,5)/100),    # Random stock value fluctuation
                                        MINIMUM_STOCK_VALUE) # Minimum value of a stock
                    
                    # Decreasing the stock value drop/rise based on how much higher/lower the stock value is compared to the baseline stock value
                    
                    if newStockValue < oldStockValue and oldStockValue < BASELINE_STOCK_VALUE:
                        newStockValue += (oldStockValue - newStockValue) * min(BASELINE_PULL_WEIGHT * (BASELINE_STOCK_VALUE - oldStockValue), MAXIMUM_STOCK_VALUE_CHANGE_REDUCTION)
                    elif newStockValue > oldStockValue and oldStockValue > BASELINE_STOCK_VALUE:
                        newStockValue -= (newStockValue - oldStockValue) * min(BASELINE_PULL_WEIGHT * (oldStockValue - BASELINE_STOCK_VALUE), MAXIMUM_STOCK_VALUE_CHANGE_REDUCTION)
                    
                    newStockValue = round(max(newStockValue, MINIMUM_STOCK_VALUE), 2)
                    
                    marketDict[industry].update(stockValue=newStockValue,
                                                currentEvent=randint(0,len(industryEvents)))

                desc += "\n\n**₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪**"
                desc += "\n\n" + values.icon + " __**༺༻ " + " " + industry.title() + " ༺༻**__ " + values.icon
                desc += "\n\n**✦ Stock Value: `" + oldStockValue + "gp` ► `" + values.stockValue + "gp`**  " + ("📈" if oldStockValue <= values.stockValue else ":chart_with_downwards_trend:")
                desc += "\n\n**✦ Stocks Left: `" + values.stockCount + "`**"
                desc += "\n\n*" + values.events[values.currentEvent].hint + "*"

    elif args[0].lower() == "report":
        
        title = "⊱ꕥ⊰ ・This week's report・⊱ꕥ⊰"
        
        desc += "\n\n:globe_with_meridians: __**༺༻ World ༺༻**__ :globe_with_meridians:\n\n*" + marketDict.world.events[marketDict.world.currentEvent].hint + "*"
        
        # Displaying data for all industries
        for industry, values in marketDict.items():
            if industry != "world":
                desc += "\n\n**₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪**"
                desc += "\n\n" + values.icon + " __**༺༻ " + " " + industry.title() + " ༺༻**__ " + values.icon
                desc += "\n\n**✦ Stock Value: `" + values.stockValue + "gp`**"
                desc += "\n\n**✦ Stocks Left: `" + values.stockCount + "`**"
                desc += "\n\n*" + values.events[values.currentEvent].hint + "*"
                
    elif args[0].lower() == "buy":
        
        title = "⊱ꕥ⊰ ・" + name + " buys some stocks!・⊱ꕥ⊰"
        
        if playerStonksDict.interactions < 1:
            desc += "\n\n**" + name + " doesn't have any interactions left this week! <:surprisedpikachu:921798527875702786>**"
        
        # Checking for valid industry input. Displays valid industry inputs if input is invalid
        elif len(args)<2 or args[1].lower() not in [industry for industry in marketDict if industry!="world"]:
            desc += "\n\n**Please input a valid industry to buy stocks in! <:surprisedpikachu:921798527875702786>**"
            desc += "\n\n*(Eg: `!stonks buy arts 4`)*"
            desc += "\n\n**₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪**"
            desc += "\n\n**__༺༻ Valid Industries ༺༻__**"
            for industry in marketDict:
                if industry != "world":
                    desc += "\n\n✦ " + industry.title() + " | " + marketDict[industry].icon
                    
        else:
            industry = args[1].lower()
            count = int(args[2]) if len(args) > 2 and args[2].isnumeric() else 1
            stockCount = int(marketDict[industry].stockCount)
            stockValue = marketDict[industry].stockValue
            bags = load_json(bags)
            oldGP=[bags[x][1].get("gp") for x in range(len(bags)) if bags[x][0] == 'Coin Pouch'][0]
            
            if count<1:
                desc += "\n\n**You have to buy at least one stock, ya dingus! <:doge_kek:905836743289344031>**"
                desc += "\n\n--------------------------------------------"
                desc += "\n\n**" + marketDict[industry].icon + " Stocks Left: `" + marketDict[industry].stockCount + "`**"
            
            elif stockCount < count:
                desc += "\n\n**The " + industry.title() + " industry doesn't have enough stocks for this purchase! <:surprisedpikachu:921798527875702786>**"
                desc += "\n\n--------------------------------------------"
                desc += "\n\n**" + marketDict[industry].icon + " Stocks Left: `" + marketDict[industry].stockCount + "`**"
                
            elif stockValue*count > oldGP:
                desc += "\n\n**" + name + " does not have enough gold for this purchase! <:surprisedpikachu:921798527875702786>**"
                desc += "\n\n--------------------------------------------"
                desc += "\n\n**:moneybag: Required Gold: `" + stockValue*count + "`**"
                desc += "\n\n**:moneybag: Available Gold: `" + oldGP + "`**"
                
            elif count > playerStonksDict.interactions:
                desc += "\n\n**" + name + " does not have enough interactions left for this purchase! <:surprisedpikachu:921798527875702786>**"
                desc += "\n\n--------------------------------------------"
                desc += "\n\n**<:nezukodead:921798440789377024> Interactions Left: `" + playerStonksDict.interactions + "`**"
                
            else:
                # Updates the industry's stock count and stock value 
                marketDict[industry].update(stockCount=stockCount-count,
                                            stockValue=round(stockValue + abs(stockValue)*PLAYER_STOCK_BUY_EFFECT*count,2))
                
                # Updates player's coin pouch
                [bags[x][1].update({"gp":round(bags[x][1].gp-stockValue*count,2)}) for x in range(len(bags)) if bags[x][0] == 'Coin Pouch'][0]
                set_cvar("bags",dump_json(bags))
                bags = load_json(bags)
                newGP=[bags[x][1].get("gp") for x in range(len(bags)) if bags[x][0] == 'Coin Pouch'][0]
                footer = name + "'s Coin Pouch: " + str(oldGP) + "gp -> " + str(newGP) + "gp"
                
                playerStonksDict.update(interactions=playerStonksDict.interactions - count)
                playerStonksDict.stocks.update({industry:playerStonksDict.stocks[industry] + count})
                
                # Displays player and industry's updated data
                desc += "\n\n**" + name + " successfully purchases `" + count + "` stocks in the " + industry + " industry! <:tanjirowow:922537039524692088>**"
                desc += "\n\n**₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪**"                
                desc += "\n\n**💰 " + name + "'s stocks in the " + industry + " industry: `" + playerStonksDict.stocks[industry] + "`💰**"
                desc += "\n\n**<:nezukodead:921798440789377024> Interactions Left: `" + playerStonksDict.interactions + "`**"
                desc += "\n\n--------------------------------------------"
                desc += "\n\n**✦ Updated " + marketDict[industry].icon + " " + industry.title() + " Stock Value: `" + marketDict[industry].stockValue + "gp`**"
                desc += "\n**✦ Updated " + marketDict[industry].icon + " " + industry.title() + " Stock Count: `" + marketDict[industry].stockCount + "`**"
        
    elif args[0].lower() == "sell":
        
        title = "⊱ꕥ⊰ ・" + name + " sells some stocks!・⊱ꕥ⊰"
        
        if playerStonksDict.interactions < 1:
            desc += "\n\n**" + name + " doesn't have any interactions left this week! <:surprisedpikachu:921798527875702786>**"
        
        # Checking for valid industry input. Displays valid industry inputs if input is invalid
        elif len(args)<2 or args[1].lower() not in [industry for industry in marketDict if industry!="world"]:
            desc += "\n\n**Please input a valid industry to sell stocks to! <:surprisedpikachu:921798527875702786>**"
            desc += "\n\n*(Eg: `!stonks sell arts 4`)*"
            desc += "\n\n**₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪**"
            desc += "\n\n**__༺༻ Valid Industries ༺༻__**"
            for industry in marketDict:
                if industry != "world":
                    desc += "\n\n✦ " + industry.title() + " | " + marketDict[industry].icon 
                    
        else:
            industry = args[1].lower()
            count = int(args[2]) if len(args) > 2 and args[2].isnumeric() else 1
            
            playerStockCount = int(playerStonksDict.stocks[industry] if industry in playerStonksDict.stocks else 0)
            stockValue = marketDict[industry].stockValue
            bags = load_json(bags)
            oldGP=[bags[x][1].get("gp") for x in range(len(bags)) if bags[x][0] == 'Coin Pouch'][0]
            
            if count > playerStockCount:
                desc += "\n\n**" + name + " does not have that many stocks to sell! <:surprisedpikachu:921798527875702786>**"
                desc += "\n\n**--------------------------------------------**"
                desc += "\n\n**" + name + "'s " + marketDict[industry].icon + " " + industry.title() + " Stocks: `" + playerStockCount + "`**" 
            
            elif count<1:
                desc += "\n\n**You have to sell at least one stock, ya dingus! <:doge_kek:905836743289344031>**"
                desc += "\n\n--------------------------------------------"
                desc += "\n\n**" + name + "'s " + marketDict[industry].icon + " " + industry.title() + " Stocks: `" + playerStockCount + "`**" 
            
            elif count > playerStonksDict.interactions:
                desc += "\n\n**" + name + " does not have enough interactions left for this transaction! <:surprisedpikachu:921798527875702786>**"
                desc += "\n\n--------------------------------------------"
                desc += "\n\n**<:nezukodead:921798440789377024> Interactions Left: `" + playerStonksDict.interactions + "`**"
            
            else:
                playerStonksDict.update(interactions=playerStonksDict.interactions - count)
                playerStonksDict.stocks.update({industry:playerStonksDict.stocks[industry] - count})
                
                # Updates player's coin pouch
                [bags[x][1].update({"gp":round(bags[x][1].gp+stockValue*count,2)}) for x in range(len(bags)) if bags[x][0] == 'Coin Pouch'][0]
                set_cvar("bags",dump_json(bags))
                bags = load_json(bags)
                newGP=[bags[x][1].get("gp") for x in range(len(bags)) if bags[x][0] == 'Coin Pouch'][0]
                footer = name + "'s Coin Pouch: " + str(oldGP) + "gp -> " + str(newGP) + "gp"
                
                # Updates industry's data
                marketDict[industry].update(stockCount=marketDict[industry].stockCount+count,
                                            stockValue=round(max(marketDict[industry].stockValue - abs(stockValue)*PLAYER_STOCK_SELL_EFFECT*count, MINIMUM_STOCK_VALUE),2))
                
                # Displays player and industry's updated data
                desc += "\n\n**" + name + " successfully sells `" + count + "` stocks in the " + industry + " industry! <:tanjirowow:922537039524692088>**"
                desc += "\n\n**₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪**"
                desc += "\n\n**💰 " + name + "'s stocks in the " + industry + " industry: `" + playerStonksDict.stocks[industry] + "` 💰**"
                desc += "\n\n**<:nezukodead:921798440789377024> Interactions Left: `" + playerStonksDict.interactions + "`**"
                desc += "\n\n--------------------------------------------"
                desc += "\n\n**✦ Updated " + marketDict[industry].icon + " " + industry.title() + " Stock Value: `" + marketDict[industry].stockValue + "gp`**"
                desc += "\n**✦ Updated " + marketDict[industry].icon + " " + industry.title() + " Stock Count: `" + marketDict[industry].stockCount + "`**"
                
                
    elif args[0].lower() == "trade":
        
        title = "⊱ꕥ⊰ ・" + name + " trades some stocks!・⊱ꕥ⊰"
        
        if len(args)<2 or args[1] not in [player.name for player in playersDict.values()]:
            desc += "\n\n**Please input a valid name of a player to trade stocks to! <:surprisedpikachu:921798527875702786>**"
            desc += "\n\n*(Eg: `!stonks trade Bob arts 4`)*"
                    
        # Checking for valid industry input. Displays valid industry inputs if input is invalid
        elif len(args)<3 or args[2].lower() not in [industry for industry in marketDict if industry!="world"]:
            desc += "\n\n**Please input a valid industry to sell stocks to! <:surprisedpikachu:921798527875702786>**"
            desc += "\n\n*(Eg: `!stonks trade Bob arts 4`)*"
            desc += "\n\n**₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪**"
            desc += "\n\n**__༺༻ Valid Industries ༺༻__**"
            for industry in marketDict:
                if industry != "world":
                    desc += "\n\n✦ " + industry.title() + " | " + marketDict[industry].icon 
                    
        else:
            targetPlayerName = args[1]
            targetPlayerId = ""
            for id, values in playersDict.items():
                if values.name == targetPlayerName:
                    targetPlayerId = id
                    break;
                 
            industry = args[2].lower()
            count = int(args[3]) if len(args) > 3 and args[3].isnumeric() else 1
    
            playerStockCount = int(playerStonksDict.stocks[industry] if industry in playerStonksDict.stocks else 0)
            
            if count > playerStockCount:
                desc += "\n\n**" + name + " does not have that many stocks to trade! <:surprisedpikachu:921798527875702786>**"
                desc += "\n\n**--------------------------------------------**"
                desc += "\n\n**" + name + "'s " + marketDict[industry].icon + " " + industry.title() + " Stocks: `" + playerStockCount + "`**" 
            
            elif count<1:
                desc += "\n\n**You have to trade at least one stock, ya dingus! <:doge_kek:905836743289344031>**"
                desc += "\n\n--------------------------------------------"
                desc += "\n\n**" + name + "'s " + marketDict[industry].icon + " " + industry.title() + " Stocks: `" + playerStockCount + "`**"
                
            else:
                playerStonksDict.stocks.update({industry:playerStonksDict.stocks[industry] - count})
                playersDict[targetPlayerId].stocks.update({industry:playersDict[targetPlayerId].stocks[industry] + count})
                
                desc += "\n\n**" + name + " successfully trades `" + count + "` " + marketDict[industry].icon + " " + industry + " stocks to " + targetPlayerName + "! <:tanjirowow:922537039524692088>**"
                desc += "\n\n**₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪**"
                desc += "\n\n**💰 " + name + "'s stocks in the " + industry + " industry: `" + playerStonksDict.stocks[industry] + "` 💰**"
                desc += "\n\n**💰 " + targetPlayerName + "'s stocks in the " + industry + " industry: `" + playersDict[targetPlayerId].stocks[industry] + "` 💰**"
            
    elif args[0].lower() == "me":
        
        title = name + " checks their stocks"
        desc += "\n\n**__༺༻ Stock Count: ༺༻__**"
        
        for industry, stockCount in playerStonksDict.stocks.items():
            desc += "\n\n**✦ " + marketDict[industry].icon + " " + industry.title() + " stocks:** `" + int(stockCount) + "`"
            
        desc += "\n\n**₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪**"
        desc += "\n\n**<:nezukodead:921798440789377024> Interactions Left: `" + playerStonksDict.interactions + "`**"
            
    else:
        desc = helpMessage
else:
    desc = helpMessage
    
desc += "\n\n**₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪**"
stonksJson = dump_json(stonksDict)
                
return f""" -title "{title}" -desc "{desc}" -footer "{footer}" -image "{image}" """
</drac2>
!gvar edit {{stonksGvar}} {{stonksJson}}