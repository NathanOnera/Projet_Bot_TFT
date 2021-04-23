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
crop_topright = [1885,130,1910,155]
crop_id = [-51,0,-8,20]

mat1dmg =  np.array(Image.open('data/red_circle/LookingAtDmg.jpg')).flatten()*1.0
mat1dmg = mat1dmg/np.linalg.norm(mat1dmg)
mat1notdmg = np.array(Image.open('data/red_circle/NotLookingAtDmg.jpg')).flatten()*1.0
mat1notdmg = mat1notdmg/np.linalg.norm(mat1notdmg)
mat_ennemy_not_pov = np.array(Image.open('data/red_circle/ennemy_not_pov.jpg'))
mat_ennemy_pov = np.array(Image.open('data/red_circle/ennemy_pov.jpg'))

verbose = False

def normalize(v):
    norm=np.linalg.norm(v, ord=1)
    if norm==0:
        norm=np.finfo(v.dtype).eps
    return v/norm


class player:
    def __init__(self,key):
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
        self.key = key

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

class game:
    def crop_image(self):
        self.imfou = self.im.crop(crop_fou)
        self.imstage = self.im.crop(crop_stage)
        self.imestage = self.im.crop(crop_estage)
        self.imboardbench = self.im.crop(crop_boardbench)
        self.imtopright = self.im.crop(crop_topright)
        self.imright = self.im.crop(crop_right)
        if verbose:
            print('Image cropped')

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
        if verbose:
            print('Stage identified')

    def get_dmgPOV(self):
        mat2 = np.array(self.imtopright).flatten()*1.0
        mat2 = mat2/np.linalg.norm(mat2)
        if np.inner(mat1dmg,mat2)/np.inner(mat1notdmg,mat2)<1:
            self.dmgPOV = False
            str_print = 'Not Dmg POV'
        else:
            self.dmgPOV = True
            str_print = 'Dmg POV'
        if verbose:
            print(str_print)

    def find_player_pos(self):
        if self.dmgPOV == False:
            mat_right = np.array(self.imright)
            # Ennemy not POV
            result = cv.matchTemplate(mat_ennemy_not_pov,mat_right,3)
            self.nbPlayers = len(result[result[:,104]>0.95])
            
            idpos = np.nonzero(result[:,104] > 0.95)
            idposx = idpos[0]
            idposy = (np.ones(idpos[0].shape)*104).astype(int)
            idpos = np.array((idposx,idposy))
            # Ennemy POV
            result = cv.matchTemplate(mat_ennemy_pov,mat_right,3)
            self.nbPlayersPOV = len(result[result[:,87]>0.95])
            if self.nbPlayersPOV != 0:
                idposx2 = np.nonzero(result[:,87] > 0.95)
                idposx2 = idposx2[0]+3
                idposy2 = (np.ones(idposx2[0].shape)*90).astype(int)
                idposx = np.concatenate((idposx,idposx2),axis = None)
                idposy = np.concatenate((idposy,idposy2),axis = None)
                idpos = np.array((idposx,idposy))
                self.ownPOV = False
            self.idpos = idpos
            if verbose:
                if self.nbPlayersPOV == 0:
                    print('There are ' + str(self.idpos.shape[1])+ ' ennemies visible, and we have our POV')
                    self.ownPOV = True
                else:
                    print('There are ' + str(self.idpos.shape[1])+ ' ennemies visible, and we do not have our POV')
                    self.ownPOV = False
        else:
            if verbose:
                print('There are no visible players')

    def initialize_players(self):
        if self.initialized == False:
            if self.dmgPOV == False:
                list_players = []
                for i in range(self.idpos.shape[1]):
                    key = np.array(self.imright.crop([crop_id[0]+self.idpos[1,i],crop_id[1]+self.idpos[0,i],crop_id[2]+self.idpos[1,i],crop_id[3]+self.idpos[0,i]]))
                    list_players.append(player(Image.fromarray(key)))
                    Image.fromarray(key).save('data/checks/keyPlayer_'+str(i)+'.jpg')
                self.players = list_players
                print('We have initialized ' + str(len(self.players)) + ' players!')
                self.initialized = True

    def __init__(self,im):
        self.players = []
        self.initialized = False
        self.update_image(im)
        
    def update_image(self,im):
        self.im = im
        self.crop_image()
        self.get_stage()
        self.get_dmgPOV()
        self.find_player_pos()
        self.initialize_players()
        self.find_players()

    def find_players(self):
        if self.initialized == True:
            if self.dmgPOV == False:
                ennemypos = []
                for i in range(self.idpos.shape[1]):
                    tocompare =  np.array(self.imright.crop([crop_id[0]+self.idpos[1,i],crop_id[1]+self.idpos[0,i],crop_id[2]+self.idpos[1,i],crop_id[3]+self.idpos[0,i]])).flatten()
                    mat1 = tocompare/np.linalg.norm(tocompare)
                    val = 0
                    index = 0
                    for j in range(len(self.players)):
                        tocompare2 = np.array(self.players[j].key).flatten()
                        mat2 = tocompare2/np.linalg.norm(tocompare2)
                        val_ = np.inner(mat1,mat2)
                        if val_ > val:
                            index = j
                            val = val_
                    print(val)
                    ennemypos.append(index)
                self.ennemypos = ennemypos
                print(self.ennemypos)
                if len(ennemypos) == len(set(ennemypos)):
                    print('We found every player!')
                else:
                    print('We have found the same player twice !!!!!!')

##    def update_championsOut():
##        self.championsOut = championsOut
##        for player in self.players:
##            self.championsOut = self.championsOut + self.players.championsOwned
##        self.championsRemaining = championsCopies - self.championsOut




        
    
