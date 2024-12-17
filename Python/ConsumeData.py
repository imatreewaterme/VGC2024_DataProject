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


#Top 20#
top20Abilities = countsAbilites.head(5)
print(top20Abilities)
top20Moves = countsMoves.head(20)
top20Pokemon = countsPokemon.head(20)

#top = df.loc[df['pokemon'] == 'Urshifu-Rapid-Strike']
#sum = top['rank'].sum()
#averageRank = sum/(top['pokemon'].count())
#averageRank = str(round(averageRank, 2))
#print(averageRank)
ranking = []
for pokemon in top20Pokemon.index:
    top = df.loc[df['pokemon'] == pokemon]
    sum = top['rank'].sum()
    averageRank = sum/(top['pokemon'].count())
    averageRank = int(averageRank)
    ranking.append(averageRank)
series = pd.Series(top20Pokemon.index)

#Plots#
#Top 20 Most Common Pokemon - Average Ranking
fig, ax = plt.subplots()
ax.barh(series, ranking, align='center', color="orange")
ax.set_yticks(series, labels=series)
ax.invert_yaxis
ax.set_xlabel('Rank out of 106')
ax.set_title('VGC 2024: 20 Most Common Pokemon Avg. Rank')
plt.tight_layout()
#plt.show()
#fig.savefig('avgRank.png')

#Most Common Moves
series=pd.Series(top20Moves.index)
series2=pd.Series(top20Moves)
fig, ax = plt.subplots()
ax.barh(series, series2, align='center')
ax.set_yticks(series, labels=series)
ax.invert_yaxis
ax.set_xlabel('Count for 106 Teams (636 Pokemon)')
ax.set_title('VGC 2024: Top 20 Most Common Moves')
plt.tight_layout()
#plt.show()
#fig.savefig('top20moves.png')

#Most Common Abilities
series=pd.Series(top20Abilities.index)
series2=pd.Series(top20Abilities)
fig, ax = plt.subplots()

ax.bar(series, series2, label=series, color="red")
ax.set_ylabel("Count out of 636 Pokemon")
ax.set_title("VGC 2024: Top 20 Most Common Abilities'")
plt.tight_layout()
#plt.show()
