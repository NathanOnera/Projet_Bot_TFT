import numpy as np
import pandas as pd

championsList = pd.read_csv("data/csv_files/Champions.csv",delimiter = ';')
championsName = championsList.values[:,0]
championsCost = championsList.values[:,1]
championsCopies = championsList.values[:,2]
championsIndex = {}
for i in range(len(championsName)):
    championsIndex[championsName[i]] = i
championsOwned = np.zeros(len(championsName),dtype = int)


class player:
    def __init__(self):
        self.pv = 100
        self.gold = 0
        self.lastFaced = 10
        self.level = 1
        self.championsOwned = championsOwned
        self.name = ''
        self.updated = False

    def update_pv(pv):
        self.pv = a

    def update_gold(gold):
        self.gold = gold

    def update_level(level):
        self.level = level

    def update_lastFaced(lastFaced):
        self.lastFaced = lastFaced

    def update_championsOwned(co):
        self.championsOwned = co

    def update_name(name):
        self.name = name

championsOut = np.zeros(len(championsName),dtype = int)
players = []
for _ in range(8):
    players.append(player())

class game:
    def __init__(self):
        self.players = players
        self.championsOut = championsOut
        self.championsRemaining = championsCopies

    def update_championsOut():
        self.championsOut = championsOut
        for player in self.players:
            self.championsOut = self.championsOut + self.players.championsOwned
        self.championsRemaining = championsCopies - self.championsOut





        
    
