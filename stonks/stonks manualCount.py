multiline
!embed
<drac2>
args = &ARGS&
title = "⊱ꕥ⊰ ・Manual Stock Count Alteration・⊱ꕥ⊰"
desc = ""
footer = ""
image = "https://i.kym-cdn.com/entries/icons/original/000/029/959/Screen_Shot_2019-06-05_at_1.26.32_PM.jpg" if randint(1,100) <= 1 else ""
stonksGvar = "1c39ee5d-0ff6-42e3-89a9-cda963feef7e"
stonksDict = load_json(get_gvar(stonksGvar))
marketDict = stonksDict.market

industry = args[0]
amount = int(args[1])

if industry not in marketDict.keys():
    desc += "**Please input a valid industry**"
    desc += "\n\n__Valid Industries:__"
    for industry in marketDict.keys():
        desc += "\n✦ " + industry

oldStockCount = marketDict[industry].stockCount
newStockCount = oldStockCount+amount

marketDict[industry].update(stockCount=newStockCount)

desc = "**" + industry.title() + " stock count: `" + oldStockCount + " ⟶ " + newStockCount + "`**"

stonksJson = dump_json(stonksDict)

return f""" -title "{title}" -desc "{desc}" -footer "{footer}" -image "{image}" """
</drac2>
!gvar edit {{stonksGvar}} {{stonksJson}}