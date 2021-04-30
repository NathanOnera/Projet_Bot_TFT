import numpy as np
import pandas as pd
from PIL import ImageGrab, Image
import cv2 as cv
import glob

def normalize_array(arr):
    return arr/np.linalg.norm(arr)

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
crop_POV = [855,926,1047,984]

mat1dmg =  normalize_array(np.array(Image.open('data/red_circle/LookingAtDmg.jpg')).flatten()*1.0)
mat1notdmg = normalize_array(np.array(Image.open('data/red_circle/NotLookingAtDmg.jpg')).flatten()*1.0)
mat_ennemy_not_pov = np.array(Image.open('data/red_circle/ennemy_not_pov.jpg'))
mat_ennemy_pov = np.array(Image.open('data/red_circle/ennemy_pov.jpg'))
mat_us = np.array(Image.open('data/red_circle/us.jpg'))
matPOV = normalize_array(np.array(Image.open('data/red_circle/POV.jpg')).flatten()*1.0)
matPOVcarou = normalize_array(np.array(Image.open('data/red_circle/POVcarou.jpg')).flatten()*1.0)

verbose = False
k = 0


class player:
    def __init__(self,key,order):
        self.key = key
        self.img = Image.fromarray(self.key)
        self.order = order
        self.boardbench = Image.open('data/analyze_boards/01.jpg')

championsOut = np.zeros(len(championsName),dtype = int)

class game:
    def crop_image(self):
        self.imfou = self.im.crop(crop_fou)
        self.imstage = self.im.crop(crop_stage)
        self.imestage = self.im.crop(crop_estage)
        self.imboardbench = self.im.crop(crop_boardbench)
        self.imtopright = self.im.crop(crop_topright)
        self.imright = self.im.crop(crop_right)
        self.imPOV = self.im.crop(crop_POV)
        if verbose:
            print('Image cropped')

    def get_POV(self):
        mat = normalize_array(np.array(self.imPOV).flatten()*1.0)
        if np.inner(mat,matPOV) > 0.98:
            self.POV = False
        else:
            if verbose:
                print(str(np.inner(mat,matPOV)))
            self.POV = True

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
            print('Stage identified: ' + out)

    def get_dmgPOV(self):
        mat2 = normalize_array(np.array(self.imtopright).flatten()*1.0)
        if np.inner(mat1dmg,mat2)/np.inner(mat1notdmg,mat2)<1:
            self.dmgPOV = False
            str_print = 'Not Dmg POV'
        else:
            self.dmgPOV = True
            str_print = 'Dmg POV'
        if verbose:
            print(str_print)

    def localizePlayers(self):
        mat_right = np.array(self.imright)
        # First thing: localize ourself
        result = cv.matchTemplate(mat_us,mat_right,3)
        pLocUsx = np.nonzero(result[:,60] > 0.92)[0]
        del_ = []
        for i in range(len(pLocUsx)-1):
            if pLocUsx[i+1]-pLocUsx[i] < 40:
                del_.append(i)
        pLocUsx = np.delete(pLocUsx,del_)
        pLocUsy = (np.ones(pLocUsx.shape)*60).astype(int)
        # Second thing: localize ennemies
        #First case: we are not on their POV
        result = cv.matchTemplate(mat_ennemy_not_pov,mat_right,3)
        pLocEnx = np.nonzero(result[:,104] > 0.92)[0]
        del_ = []
        for i in range(len(pLocEnx)-1):
            if pLocEnx[i+1]-pLocEnx[i] < 40:
                del_.append(i)
        pLocEnx = np.delete(pLocEnx,del_)
        pLocEny = (np.ones(pLocEnx.shape)*104).astype(int)
        # Second case: we are on their POV
        result = cv.matchTemplate(mat_ennemy_pov,mat_right,3)
        pLocEnx2 = np.nonzero(result[:,87] > 0.92)[0]+2
        del_ = []
        for i in range(len(pLocEnx2)-1):
            if pLocEnx2[i+1]-pLocEnx2[i] < 20:
                del_.append(i)
        pLocEnx2 = np.delete(pLocEnx2,del_)
        if len(pLocEnx2) !=0:
            self.POV = False
        pLocEny2 = (np.ones(pLocEnx2.shape)*90).astype(int)
        pLocx = np.concatenate((pLocUsx,pLocEnx,pLocEnx2),axis = None)
        pLocy = np.concatenate((pLocUsy,pLocEny,pLocEny2),axis = None)
        pLoc = np.array((pLocx,pLocy))
        self.pLoc = pLoc
        if verbose:
            if self.POV == True:
                print('There are ' + str(self.pLoc.shape[1])+ ' ennemies visible, and we have our POV')
            else:
                print('There are ' + str(self.pLoc.shape[1])+ ' ennemies visible, and we do not have our POV')
        # At the end of this function, we have an array with the (x,y) of the players position, including ours. Our position is always the first element. If it is an ennemy POV, its position is the last element.
        # Question: How can we define an 'order', that is order according to x
        temp = pLoc[0].copy() # sort according to x
        temp.sort()
        pOrder = []
        for i in range(len(pLoc[0])):
            for j in range(len(temp)):
                if pLoc[0,i] == temp[j]:
                    pOrder.append(j+1)
        self.pOrder = pOrder
        self.pLocxSorted = temp
        self.pLocx = pLoc[0]

    def initialize_players(self):
        list_players = []
        list_players.append(player(np.array(Image.open('data/checks/keyPlayer.jpg')),self.pOrder[0]))
        for i in range(1,self.pLoc.shape[1]):
            key = np.array(self.imright.crop([crop_id[0]+self.pLoc[1,i],crop_id[1]+self.pLoc[0,i],crop_id[2]+self.pLoc[1,i],crop_id[3]+self.pLoc[0,i]]))
            list_players.append(player(key,self.pOrder[i]))
            Image.fromarray(key).save('data/checks/keyPlayer_'+str(i)+'.jpg')
        self.players = list_players
        if verbose:
            print('We have initialized ' + str(len(self.players)) + ' players!')
        self.playersInitialized = True

    def __init__(self,im):
        self.playersInitialized = False
        self.update(im)
        
    def update(self,im):
        self.im = im
        self.crop_image()
        self.get_stage()
        self.get_POV()
        self.get_dmgPOV()
        if self.dmgPOV == False:
            self.localizePlayers()
            if self.playersInitialized == False:
                self.initialize_players()
            if len(self.pLoc) != 0:
                self.find_players()
                self.associateBoard()

    def associateBoard(self):
        if self.POV == True:
            self.players[0].boardbench = self.imboardbench
        else:
            self.players[self.playersPosition[-1]].boardbench = self.imboardbench

    def find_players(self):
        playersPosition = []
        self.players[0].order = self.pOrder[0]
        for i in range(1,self.pLoc.shape[1]):
            mat1 =  normalize_array(np.array(self.imright.crop([crop_id[0]+self.pLoc[1,i],crop_id[1]+self.pLoc[0,i],crop_id[2]+self.pLoc[1,i],crop_id[3]+self.pLoc[0,i]])).flatten())
            val = 0
            index = 0
            for j in range(1,len(self.players)):
                mat2 = normalize_array(np.array(self.players[j].key).flatten())
                val_ = np.inner(mat1,mat2)
                if val_ > val:
                    index = j
                    val = val_
            self.players[index].order = self.pOrder[i]
            if verbose:
                print(val)
                print(index)
            playersPosition.append(index)
        self.playersPosition = playersPosition
        if verbose:
            print(playersPosition)
        if verbose:
            if len(playersPosition) == len(set(playersPosition)):
                print('We found every player!')
            else:
                print('We have found the same player twice !!!!!!')

##    def update_championsOut():
##        self.championsOut = championsOut
##        for player in self.players:
##            self.championsOut = self.championsOut + self.players.championsOwned
##        self.championsRemaining = championsCopies - self.championsOut


##G = game(Image.open('data/analyze_boards/04.jpg'))
##G.players[-1].boardbench.show()




    
