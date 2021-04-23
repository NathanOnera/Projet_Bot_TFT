import numpy as np
import pandas as pd
from PIL import ImageGrab, Image
import cv2 as cv
import glob

championsList = pd.read_csv("data/csv_files/Champions.csv",delimiter = ';')
championsName = championsList.values[:,0]
championsCost = championsList.values[:,1]
championsCopies = championsList.values[:,2]
championsIndex = {}
for i in range(len(championsName)):
    championsIndex[championsName[i]] = i
championsOwned = np.zeros(len(championsName),dtype = int)

crop_fou = [760,35,770,50]
crop_stage = [780,35,820,55]
crop_estage = [830,35,870,55]
crop_right = [1720,80,1920,800]
crop_boardbench = [250,80,1460,840]


class player:
    def __init__(self):
        self.hp = 100
        self.gold = 0
        self.lastFaced = 10
        self.level = 1
        self.championsBoard = championsOwned
        self.championsBench = championsOwned
        self.championsOwned = championsOwned
        self.name = ''
        self.updated = False
        self.items = []
        self.power = 0

    def update_pv(hp):
        self.hp = a

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

    def update_img(im):
        self.img = im

championsOut = np.zeros(len(championsName),dtype = int)
players = []
for _ in range(8):
    players.append(player())

class game:
    def __init__(self,im):
        self.players = []
        self.championsOut = championsOut
        self.championsRemaining = championsCopies
        self.im = im
        self.stage = ''

    def update_championsOut():
        self.championsOut = championsOut
        for player in self.players:
            self.championsOut = self.championsOut + self.players.championsOwned
        self.championsRemaining = championsCopies - self.championsOut

    def crop_image(self):
        self.imfou = self.im.crop(crop_fou)
        self.imstage = self.im.crop(crop_stage)
        self_imestage = self.im.crop(crop_estage)
        self_imboardbench = self.im.crop(crop_boardbench)

    def get_stage(self):
        # Spot if we are in the early stages
        diff = cv.subtract(np.array(self.imfou).flatten(),np.array(Image.open('data/naked_board/fou.jpg')).flatten())
        if np.mean(diff) > 1:   # If it is the case
            radical = 'data/estages'
            variable = self.imestage
        else:                   # If it is not the case
            radical = 'data/stages'
            variable = self.imstage
        list_item = glob.glob(radical+'/*.jpg')
        Diff = 1000
        out = ''
        for item in list_item:
            diff = np.mean(cv.subtract(np.array(variable).flatten(),np.array(Image.open(item)).flatten()))
            if diff < Diff:
                Diff = diff
                out = item.replace(radical+'\\','')
                out = out.replace('.jpg','')
        self.stage = out

    def add_players(self):
        pass



        
    
