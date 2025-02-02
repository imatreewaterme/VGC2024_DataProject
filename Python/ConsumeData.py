import sys
import numpy as np
import pandas as pd
df = pd.read_csv("../csvFiles/data.csv")
import matplotlib.pyplot as plt

allMoves = pd.concat([df['move1'],df['move2'],df['move3'],df['move4']])

#Unique Values#
uniqueMoves = allMoves.unique()
uniqueMoves = uniqueMoves[~pd.isnull(uniqueMoves)]
uniqueMoves = (np.sort(uniqueMoves))

uniquePokemon = df['pokemon'].unique()
uniquePokemon = (np.sort(uniquePokemon))

uniqueAbilites = df['ability'].unique()
uniqueAbilites = (np.sort(uniqueAbilites))

uniqueItems = df['helditem'].unique()
uniqueItems = (np.sort(uniqueItems))


#Counts#
countsAbilites = df['ability'].value_counts()
countsMoves = allMoves.value_counts()
countsPokemon = df['pokemon'].value_counts()
countsItems = df['helditem'].value_counts()


#Most Common#
top25Abilities = countsAbilites.head(25)
top20Moves = countsMoves.head(20)
top20Pokemon = countsPokemon.head(20)
top20Items = countsItems.head(20)
uniquePokemonSeries = pd.Series(uniquePokemon)

ranking = []
count = []
for pokemon in uniquePokemonSeries.values:
    top = df.loc[df['pokemon'] == pokemon]
    sum = top['rank'].sum()
    occurrences = top['pokemon'].count()
    averageRank = sum/occurrences
    averageRank = int(averageRank)
    ranking.append(averageRank)
    count.append(occurrences)

ranking2 = []
for pokemon in top20Pokemon.index:
    top = df.loc[df['pokemon'] == pokemon]
    sum = top['rank'].sum()
    averageRank = sum/(top['pokemon'].count())
    averageRank = int(averageRank)
    ranking2.append(averageRank)

#sort the list by ranking#
uniquePokemonList = uniquePokemonSeries.values.tolist()
rankingSorted, uniquePokemonListSorted, countSorted = zip(*sorted(zip(ranking,uniquePokemonList, count)))
rankingSorted = pd.Series(rankingSorted)
uniquePokemonListSorted = pd.Series(uniquePokemonListSorted)
countSorted = pd.Series(countSorted)
#top 20
rankingTop20 = rankingSorted.head(20)
uniquePokemonListTop20 = uniquePokemonListSorted.head(20)
countTop20=countSorted.head(20)


colors21 = [
    "red","blue","green","orange","purple","cyan","dimgrey","orchid","gold","royalblue",
    "olive","yellow","pink","sienna","palegreen","steelblue","lavender","tomato","peru","aqua","black"
          ]
colors20 = colors21[:20]
colors26=[
        "red","blue","green","orange","purple","cyan","dimgrey","orchid","gold","royalblue",
    "olive","rosybrown","pink","sienna","palegreen","steelblue","lavender","tomato","peru","aqua",
    "grey","orchid","darkgreen","royalblue","wheat","black"
]

#####Plots######

#Highest ranking pokemon and number of teams used in
fig, ax = plt.subplots()
patches = ax.scatter(rankingTop20,countTop20,c=colors20)
ax.set_yticks(np.arange(0, 20, 2))
ax.set_xticks(np.arange(0, 50, 5))
ax.set_title('Top 20 Performing Pokemon')
ax.set_xlabel('Average Ranking')
ax.set_ylabel('Frequency (Out of 106 Teams)')
ax.set_facecolor('xkcd:grey')
plt.tight_layout()
plt.show()
fig.savefig('../Figures/top20Ranking.png')

#Average ranking for each unique pokemon
N = np.size(uniquePokemon)
colors=np.random.rand(N)
fig, ax = plt.subplots()
patches = plt.scatter(ranking,uniquePokemonSeries.index,c=colors, alpha=0.5)
ax.set_yticks(np.arange(0, 106, 10))
ax.set_xticks(np.arange(0, 106, 10))
ax.set_facecolor('xkcd:grey')
ax.set_title('Average Ranking Per Unique Pokemon')
ax.set_xlabel('Ranking')
ax.set_ylabel('Frequency')
plt.tight_layout()
plt.show()
fig.savefig('../Figures/avgRankScatter.png')

#Top 20 Most Common Pokemon - Average Ranking
series = pd.Series(top20Pokemon.index)
fig, ax = plt.subplots()
patches = ax.barh(series, ranking2, align='center', color=colors21)
ax.set_yticks(series, labels=series)
ax.invert_yaxis
ax.set_title('20 Most Common Pokemon Rankings')
ax.set_facecolor('xkcd:grey')
ax.set_xlabel('Ranking')
ax.bar_label(patches,ranking2)
plt.tight_layout()
plt.show()
fig.savefig('../Figures/avgRank.png')

#Most Common Moves
series=pd.Series(top20Moves.index)
series2=pd.Series(top20Moves)
fig, ax = plt.subplots()
fig.set_size_inches(10.5, 6.5)
patches = ax.barh(series, series2, align='center', color=colors21)
ax.set_yticks(series, labels=series)
ax.invert_yaxis
ax.set_title('Top 20 Most Common Moves')
ax.set_xlabel('Frequency (Out of 636 Pokemon)')
ax.set_facecolor('xkcd:grey')
ax.legend(patches, top20Moves.index, bbox_to_anchor=(1, 1), fontsize=9)
ax.bar_label(patches,top20Moves)
plt.tight_layout()
plt.show()
fig.savefig('../Figures/top20moves.png')

#Most Common Abilities
otherAbilities = (countsAbilites.sum() - top25Abilities.sum())
other = pd.Series([otherAbilities], index=["Other Abilities"])
top25Abilities = pd.concat([top25Abilities,other])
series=pd.Series(top25Abilities.index)
series2=pd.Series(top25Abilities)

fig, ax = plt.subplots()
fig.set_size_inches(9.5, 9)
percent = 100.*top25Abilities/top25Abilities.sum()
labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(series,percent)]
patches = ax.bar(series, series2, color=colors26)
ax.axes.xaxis.set_ticklabels([])
ax.set_facecolor('xkcd:grey')
ax.set_title('Top 25 Most Common Abilities')
ax.set_xlabel("Pokemon Ability")
ax.set_ylabel("Frequency (Out of 616)")
ax.legend(patches, labels, bbox_to_anchor=(1, 1), fontsize=9)
ax.bar_label(patches,top25Abilities)
plt.tight_layout()
fig.savefig('../Figures/top25Abilites.png')
plt.show()

#Items
otherItems = (countsItems.sum() - top20Items.sum())
other = pd.Series([otherItems], index=["Other Items"])
top20Items = pd.concat([top20Items,other])
series=pd.Series(top20Items.index)
series2=pd.Series(top20Items)

fig, ax = plt.subplots()
fig.set_size_inches(10.5, 6.5)
percent = 100.*top20Items/106
labels = ['{1:1.2f}%'.format(i,j) for i,j in zip(series,percent)]

patches = ax.barh(series, series2, align='center', color=colors21)
ax.set_yticks(series, labels=series,)
ax.invert_yaxis
ax.set_facecolor('xkcd:grey')
ax.set_title('Top 20 Most Common Held Items')
ax.set_xlabel("Frequency Percentage (Out of 106 Teams)")
ax.set_label("Held Item Name")
ax.bar_label(patches,labels)
plt.xlim(0,107)
plt.tight_layout()
plt.show()
fig.savefig('../Figures/heldItems.png')
