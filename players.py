import numpy as np
import pandas as pd
from PIL import ImageGrab, Image
import cv2 as cv
import glob
import time
from datetime import datetime
import keyboard

stageToInt = {"2-1":0,"2-2":1,"2-3":2,"2-5":3,"2-6":4,"3-1":5,"3-2":6,"3-3":7,"3-5":8,"3-6":9,"4-1":10,"4-2":11,"4-3":12,"4-5":13,"4-6":14,"5-1":15,"5-2":16,"5-3":17,"5-5":18,"5-6":19,"6-1":20,"6-2":21,"6-3":22,"6-5":23,"6-6":24,"7-1":25,"7-2":26,"7-3":27,"7-5":28,"7-6":29,"1-1":2000,"1-2":1001,"1-3":1001,"1-4":1001,"2-4":2000,"2-7":1000,"3-4":2000,"3-7":1000,"4-4":2000,"4-7":1000,"5-4":2000,"5-7":1000,"6-4":2000,"6-7":1000,"7-4":2000,"7-7":1000}

def normalize_array(arr):
    return arr/np.linalg.norm(arr)

localization = [[0,1,2,3,4,5,6,7] for _ in range(30)]
matchup = [[0,1,2,3,4,5,6,7] for _ in range(30)]

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
crop_littleLegend = [44,1,64,21]
crop_POV = [855,926,1047,984]
crop_diffHBitem = [2,10,26,33]
crop_diffHBitem2 = [crop_diffHBitem[2]+2, crop_diffHBitem[1], crop_diffHBitem[2]+crop_diffHBitem[2]-crop_diffHBitem[0] +2 ,crop_diffHBitem[3]]
crop_diffHBitem3 = [crop_diffHBitem[2] + crop_diffHBitem[2]-crop_diffHBitem[0] +4, crop_diffHBitem[1], crop_diffHBitem[2] + crop_diffHBitem[2]-crop_diffHBitem[0] +4+ crop_diffHBitem[2]-crop_diffHBitem[0], crop_diffHBitem[3]]
crop_diffHB2item = [5,12,29,35]
crop_diffHB2item2 = [crop_diffHB2item[2]+2, crop_diffHB2item[1], crop_diffHB2item[2]+crop_diffHB2item[2]-crop_diffHB2item[0] +2 ,crop_diffHB2item[3]]
crop_diffHB2item3 = [crop_diffHB2item[2] + crop_diffHB2item[2]-crop_diffHB2item[0] +4, crop_diffHB2item[1], crop_diffHB2item[2] + crop_diffHB2item[2]-crop_diffHB2item[0] +4 + crop_diffHB2item[2]-crop_diffHB2item[0], crop_diffHB2item[3]]
crop_minimap = [1750,870,1915,1035]
crop_minimaps = [[60,20,110,60],[110,20,160,60],[110,60,160,110],[110,115,160,165],[60,115,110,165],[10,115,60,165],[10,60,60,110],[10,20,60,60]]

mat1dmg =  normalize_array(np.array(Image.open('data/red_circle/LookingAtDmg.jpg')).flatten()*1.0)
mat1notdmg = normalize_array(np.array(Image.open('data/red_circle/NotLookingAtDmg.jpg')).flatten()*1.0)
mat_ennemy_not_pov = np.array(Image.open('data/red_circle/ennemy_not_pov.jpg'))
mat_ennemy_pov = np.array(Image.open('data/red_circle/ennemy_pov.jpg'))
mat_us = np.array(Image.open('data/red_circle/us.jpg'))
matPOV = normalize_array(np.array(Image.open('data/red_circle/POV.jpg')).flatten()*1.0)
matPOVcarou = normalize_array(np.array(Image.open('data/red_circle/POVcarou.jpg')).flatten()*1.0)

verbose = False
k = 0

RecordNewItems = False

class player:
    def __init__(self,playerName,imgLittleLegend,imgLittleLegendMinimap,minimapIndex,minimap,rank):
        # Player name as a key (image & array)
        self.playerName = playerName
        self.imgKey = Image.fromarray(self.playerName)
        # Player little legend -- right-hand side version(image & array)
        self.imgLittleLegend = imgLittleLegend
        self.littleLegend = np.array(self.imgLittleLegend)
        # Player little legend -- minimap version (image & array)
        self.imgLittleLegendMinimap = imgLittleLegendMinimap
        self.littleLegendMinimap = np.array(self.imgLittleLegendMinimap)
        # Position of the player's home in the minimap -- from 0 to 7
        ## TODO : find how to initialize it better than this !!! ##
        self.minimap = minimap
        self.minimapPosition = minimapIndex
        self.minimapCurrentPosition = minimapIndex
        self.emptyMinimap = Image.open('data/minimaps/'+str(minimapIndex)+'.jpg')
        # Player current rank
        self.rank = rank
        self.minimapIndex = minimapIndex
        # Player board image
        self.boardbench = Image.open('data/analyze_boards/01.jpg')
        # Player champion list
        self.championsList = championsList.copy()
        # Player champions position
        self.oneStarchampionsPosition = []
        self.twoStarchampionsPosition = []
        self.isEmptyMinimap()
        self.itemList = ''
        self.arrayImgItemList = np.empty((23,1,3),dtype=np.uint8)
        self.imgItemList = Image.fromarray(self.arrayImgItemList)
        
    def updateBoardBench(self,im):
        # Updates the board/bench image of the player
        self.boardbench = im
        self.findChampionsPosition()
        self.findItems()

    def updateMinimap(self,im):
        self.minimap = im

    def isEmptyMinimap(self):
        if verbose:
            print(len(np.nonzero( cv.subtract(np.array(self.emptyMinimap),np.array(self.minimap)) > 15)[0]))
        if len(np.nonzero( cv.subtract(np.array(self.emptyMinimap),np.array(self.minimap)) > 15)[0]) > 30:
#        if np.inner(normalize_array(np.array(self.emptyMinimap).flatten()),normalize_array(np.array(self.minimap).flatten())) > 0.98:              OLD CONDITION
            self.minimapEmpty = False
        else:
            self.minimapEmpty = True
        return self.minimapEmpty

    def setLittleLegendMinimap(self,img):
        self.imgLittleLegendMinimap = img
        self.littleLegendMinimap = np.array(self.imgLittleLegendMinimap)

    def findChampionsPosition(self):
        toCompare1 = Image.open('data/HB/HB1.jpg')
        result1 = cv.matchTemplate(np.array(self.boardbench),np.array(toCompare1),3)
        toCompare2 = Image.open('data/HB/HB2.jpg')
        result2 = cv.matchTemplate(np.array(self.boardbench),np.array(toCompare2),3)

        index1 = np.nonzero(result1 > 0.97)
        index2 = np.nonzero(result2 > 0.97)

        self.oneStarchampionsPosition = index1
        self.twoStarchampionsPosition = index2
        
        if RecordNewItems == True:
            # From 1 star champions
            for i in range(len(index1[0])):
                print('new save')
                temps = datetime.now().strftime("%m%d%Y%H%M%S%f")
                fn = 'data/potential_items/' + temps
                self.boardbench.crop((index1[1][i] + crop_diffHBitem[0],index1[0][i]+ crop_diffHBitem[1],index1[1][i] + crop_diffHBitem[2],index1[0][i] + crop_diffHBitem[3])).save(fn+'_item1.jpg')
                time.sleep(0.1)
                self.boardbench.crop((index1[1][i] + crop_diffHBitem2[0],index1[0][i]+ crop_diffHBitem2[1],index1[1][i] + crop_diffHBitem2[2],index1[0][i] + crop_diffHBitem2[3])).save(fn+'_item2.jpg')
                time.sleep(0.1)
                self.boardbench.crop((index1[1][i] + crop_diffHBitem3[0],index1[0][i]+ crop_diffHBitem3[1],index1[1][i] + crop_diffHBitem3[2],index1[0][i] + crop_diffHBitem3[3])).save(fn+'_item3.jpg')
                time.sleep(0.1)
            # From 2 star champions
            for i in range(len(index2[0])):
                print('new save')
                temps = datetime.now().strftime("%m%d%Y%H%M%S%f")
                fn = 'data/potential_items/2STAR' + temps
                self.boardbench.crop((index2[1][i] + crop_diffHB2item[0],index2[0][i]+ crop_diffHB2item[1],index2[1][i] + crop_diffHB2item[2],index2[0][i] + crop_diffHB2item[3])).save(fn+'_item1.jpg')
                time.sleep(0.1)
                self.boardbench.crop((index2[1][i] + crop_diffHB2item2[0],index2[0][i]+ crop_diffHB2item2[1],index2[1][i] + crop_diffHB2item2[2],index2[0][i] + crop_diffHB2item2[3])).save(fn+'_item2.jpg')
                time.sleep(0.1)
                self.boardbench.crop((index2[1][i] + crop_diffHB2item3[0],index2[0][i]+ crop_diffHB2item3[1],index2[1][i] + crop_diffHB2item3[2],index2[0][i] + crop_diffHB2item3[3])).save(fn+'_item3.jpg')
                time.sleep(0.1)

    def findItems(self):
        self.itemList = []
        self.arrayImgItemList = np.empty((23,1,3),dtype=np.uint8)
        pos1 = self.oneStarchampionsPosition
        pos2 = self.twoStarchampionsPosition
        list_item = glob.glob('data/items/*.jpg')
        for i in range(len(pos1[0])):
            toCompare = normalize_array(np.array(self.boardbench.crop((pos1[1][i] + crop_diffHBitem[0],pos1[0][i]+ crop_diffHBitem[1],pos1[1][i] + crop_diffHBitem[2],pos1[0][i] + crop_diffHBitem[3]))).flatten()*1.0)
            for item in list_item:
                self.itemRecognition(toCompare,item)
            toCompare2 = normalize_array(np.array(self.boardbench.crop((pos1[1][i] + crop_diffHBitem2[0],pos1[0][i]+ crop_diffHBitem2[1],pos1[1][i] + crop_diffHBitem2[2],pos1[0][i] + crop_diffHBitem2[3]))).flatten()*1.0)
            for item in list_item:
                self.itemRecognition(toCompare2,item)
            toCompare3 = normalize_array(np.array(self.boardbench.crop((pos1[1][i] + crop_diffHBitem3[0],pos1[0][i]+ crop_diffHBitem3[1],pos1[1][i] + crop_diffHBitem3[2],pos1[0][i] + crop_diffHBitem3[3]))).flatten()*1.0)
            for item in list_item:
                self.itemRecognition(toCompare3,item)
        for i in range(len(pos2[0])):
            toCompare = normalize_array(np.array(self.boardbench.crop((pos2[1][i] + crop_diffHB2item[0],pos2[0][i]+ crop_diffHB2item[1],pos2[1][i] + crop_diffHB2item[2],pos2[0][i] + crop_diffHB2item[3]))).flatten()*1.0)
            for item in list_item:
                self.itemRecognition(toCompare,item)
            toCompare2 = normalize_array(np.array(self.boardbench.crop((pos2[1][i] + crop_diffHB2item2[0],pos2[0][i]+ crop_diffHB2item2[1],pos2[1][i] + crop_diffHB2item2[2],pos2[0][i] + crop_diffHB2item2[3]))).flatten()*1.0)
            for item in list_item:
                self.itemRecognition(toCompare2,item)
            toCompare3 = normalize_array(np.array(self.boardbench.crop((pos2[1][i] + crop_diffHB2item3[0],pos2[0][i]+ crop_diffHB2item3[1],pos2[1][i] + crop_diffHB2item3[2],pos2[0][i] + crop_diffHB2item3[3]))).flatten()*1.0)
            for item in list_item:
                self.itemRecognition(toCompare3,item)
        self.imgItemList = Image.fromarray(self.arrayImgItemList)



    def itemRecognition(self,toCompare,item):
        toCompareItem = normalize_array(np.array(Image.open(item)).flatten()*1.0)
        if np.inner(toCompare,toCompareItem) > 0.92:
            out = item.replace('data/items\\','').replace('.jpg','')
            self.itemList.append(out)
            self.arrayImgItemList = np.concatenate((self.arrayImgItemList,np.array(Image.open(item))),1)
            if verbose:
                print('Nous avons trouvé un objet : ' + out)
                    
    def identifyChampions(self):
        pass

class game:
    def cropImage(self):
        self.imfou = self.im.crop(crop_fou)
        self.imstage = self.im.crop(crop_stage)
        self.imestage = self.im.crop(crop_estage)
        self.imboardbench = self.im.crop(crop_boardbench)
        self.imtopright = self.im.crop(crop_topright)
        self.imright = self.im.crop(crop_right)
        self.imPOV = self.im.crop(crop_POV)
        self.minimap = self.im.crop(crop_minimap)
        self.minimaps = []
        for minimap in crop_minimaps:
            self.minimaps.append(self.minimap.crop(minimap))
        if verbose:
            print('Image cropped')

    def detectPointOfView(self):
        mat = normalize_array(np.array(self.imPOV).flatten()*1.0)
        if np.inner(mat,matPOV) > 0.98:
            self.ownPointOfView = False
        else:
            if verbose:
                print(str(np.inner(mat,matPOV)))
            self.ownPointOfView = True

    def detectStage(self):
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
        self.stage = stageToInt[out]
        if verbose:
            print('Stage identified: ' + str(self.stage))

    def detectPlayersVisible(self):
        mat2 = normalize_array(np.array(self.imtopright).flatten()*1.0)
        if np.inner(mat1dmg,mat2)/np.inner(mat1notdmg,mat2)<1:
            self.playersVisible = True
            str_print = 'The players are visible'
        else:
            self.playersVisible = False
            str_print = 'The players are not visible'
        if verbose:
            print(str_print)

    def detectPhase(self):
        if self.stage == 1000:
            phase = 'PvE'
            minimapInitializable = True
        if self.stage == 1001:
            phase = 'PvE'
            minimapInitializable = True
        elif self.stage == 2000:
            phase = 'Carou'
            minimapInitializable = False
        elif self.stage < 500:
            if self.playersVisible == True:
                nbPlayers = len(self.pLoc[0])
                nbNonEmptyMinimaps = self.countNonEmptyMinimaps()
                print(nbPlayers,nbNonEmptyMinimaps)
                if nbPlayers == nbNonEmptyMinimaps:
                    phase = 'Prepare'
                    minimapInitializable = True
                else:
                    phase = 'Fight'
                    minimapInitializable = False
            else:
                minimapInitializable = False
                phase = 'Unknown'
        self.minimapInitializable = minimapInitializable
        self.phase = phase
        return phase

    def loadData(self,im):
        self.im = im
        self.cropImage()
        self.detectStage()
        self.detectPointOfView()
        self.detectPlayersVisible()
        if self.playersVisible == True:
            self.localizePlayers()
        self.detectPhase()

    def initializeGame(self):
        if self.initialized == False:
            if self.playersVisible == True and self.minimapInitializable == True:
                self.initializationErrors = 0
                print('Starting the initialization!')
                self.initializePlayers()
            else:
                print(self.minimapInitializable)
                print('TFT Helper v0 cannot be initialized!')

    def __init__(self,im):
        self.initialized = False
        self.championsList = championsList.copy()
        self.update(im)

    def update(self,im):
        self.loadData(im)
        self.initializeGame()
        if self.initialized and self.playersVisible:
            self.findPlayers()
#            if self.phase == 'Prepare' or self.stage > 500:
            self.associateBoard()
                
            #self.updateMinimapPlayers()
            
    def initializePlayers(self):
        minimapIndexes = [i for i in range(self.pLoc.shape[1])]
        playerPlacement = []
        list_players = []
        for i in range(1,self.pLoc.shape[1]):
            # Extract the name from the right hand side
            playerName = np.array(self.imright.crop([crop_id[0]+self.pLoc[1,i],crop_id[1]+self.pLoc[0,i],crop_id[2]+self.pLoc[1,i],crop_id[3]+self.pLoc[0,i]]))
            # Extract the little legend from the right hand side
            imgLittleLegend = self.imright.crop([crop_littleLegend[0]+self.pLoc[1,i],crop_littleLegend[1]+self.pLoc[0,i],crop_littleLegend[2]+self.pLoc[1,i],crop_littleLegend[3]+self.pLoc[0,i]])
            # Find the minimap corresponding to the players
            # First case: early game and players are in the same order as the minimap
            # Second case: Find the little legend in the minimap to find player's home
            value = 0
            for index in minimapIndexes:
                min_val, val_, min_loc, max_loc = cv.minMaxLoc(cv.matchTemplate(np.array(imgLittleLegend.resize((13,13))),np.array(self.minimaps[index]),3))
                if val_ > value:
                    minimapIndex = index
                    value = val_
                    imgLittleLegendMinimap = self.minimaps[index].crop((max_loc[0],max_loc[1],max_loc[0]+13,max_loc[1]+13))
            if value < 0.90:
                self.initializationErrors = self.initializationErrors + 1
            if self.stage == 1001:
                minimapIndex = self.pOrder[i]
            minimapIndexes.remove(minimapIndex)
            playerPlacement.append(minimapIndex)
            list_players.append(player(playerName,imgLittleLegend,imgLittleLegendMinimap,minimapIndex,self.minimaps[minimapIndex],self.pOrder[i]))
            Image.fromarray(playerName).save('data/checks/keyPlayer_'+str(minimapIndex)+'.jpg')
            imgLittleLegend.save('data/checks/littleLegendPlayer_'+str(minimapIndex)+'.jpg')
            imgLittleLegendMinimap.save('data/checks/littleLegendMinimapPlayer_'+str(minimapIndex)+'.jpg')
        self.ownPosition = minimapIndexes[0]
        list_players.append(player(np.array(Image.open('data/checks/keyPlayer.jpg')),Image.open('data/checks/littleLegendPlayer.jpg'),Image.open('data/checks/littleLegendPlayer.jpg').resize((13,13)),self.ownPosition,self.minimaps[self.ownPosition],self.pOrder[0]))
        onRange = []
        for i in range(self.pLoc.shape[1]):
            for j in range(len(list_players)):
                if list_players[j].minimapIndex == i:
                    onRange.append(j)
        if self.initializationErrors < 2:
            self.players = [list_players[i] for i in onRange]
            if verbose:
                print('We have initialized ' + str(len(self.players)) + ' players!')
            self.initialized = True
        else:
            print('Initialization failed!!')

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
            self.ownPointOfView = False
        pLocEny2 = (np.ones(pLocEnx2.shape)*90).astype(int)
        pLocx = np.concatenate((pLocUsx,pLocEnx,pLocEnx2),axis = None)
        pLocy = np.concatenate((pLocUsy,pLocEny,pLocEny2),axis = None)
        pLoc = np.array((pLocx,pLocy))
        self.pLoc = pLoc
        if verbose:
            if self.ownPointOfView == True:
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
                    pOrder.append(j)
        self.pOrder = pOrder
        self.pLocxSorted = temp
        self.pLocx = pLoc[0]

    def countNonEmptyMinimaps(self):
        nbNonEmptyMinimaps = 0
        for i in range(len(self.minimaps)):
            temp = Image.open('data/minimaps/'+str(i)+'.jpg')
            if len(np.nonzero(cv.subtract(np.array(temp),np.array(self.minimaps[i])) > 15)[0]) > 30:
    #        if np.inner(normalize_array(np.array(self.emptyMinimap).flatten()),normalize_array(np.array(self.minimap).flatten())) > 0.98:              OLD CONDITION
                nbNonEmptyMinimaps = nbNonEmptyMinimaps + 1
        return nbNonEmptyMinimaps

    def associateBoard(self):
        if self.ownPointOfView == True:
            print('Associating the boardbench image to the player (' + str(self.ownPosition)+')')
            self.players[self.ownPosition].updateBoardBench(self.imboardbench)
        else:
            print('Associating the boardbench image to the player associated to the minimap ' + str(self.playersMinimapPosition[-1]))
            self.players[self.playersMinimapPosition[-1]].updateBoardBench(self.imboardbench)

    def findPlayers(self):
        playersRank = [10 for i in range(len(self.players))]
        playersRank[self.ownPosition] = self.pOrder[0]
        playersMinimapPosition = []
        playersMinimapPosition.append(self.ownPosition)
        self.players[self.ownPosition].rank = self.pOrder[0]
        playersIndexes = [i for i in range(len(self.players))]
        playersIndexes.remove(self.ownPosition)
        for i in range(1,self.pLoc.shape[1]):
            mat1 =  normalize_array(np.array(self.imright.crop([crop_id[0]+self.pLoc[1,i],crop_id[1]+self.pLoc[0,i],crop_id[2]+self.pLoc[1,i],crop_id[3]+self.pLoc[0,i]])).flatten())
            val = 0
            index = 0
            for j in playersIndexes:
                mat2 = normalize_array(np.array(self.players[j].playerName).flatten())
                val_ = np.inner(mat1,mat2)
                if val_ > val:
                    index = j
                    val = val_
            playersIndexes.remove(index)
            self.players[index].rank = self.pOrder[i]
            if verbose:
                print(val)
                print(index)
            playersRank[index] = self.pOrder[i]
            playersMinimapPosition.append(index)
            self.playersMinimapPosition = playersMinimapPosition
        self.playersRank = playersRank
        if verbose:
            print(playersPosition)

class minimap:
    def __init__(self,im,ims,stage,phase,players):
        self.image = im
        self.images = ims
        self.associatePlayers()
        if self.stage < 500:
            self.localizeAndMatchups()

    def update(self,im,ims,stage,phase):
        if stage > 500:
            print('Nothing new under the Sun!')
        else:
            if stage != self.stage:
                self.localized == False
                print('New stage!')
            if self.localized == False and phase == 'Fight':
                self.localizeAndMatchups()

    def localizeAndMatchups(self):
            self.currentLocalization = self.localizePlayers()
            self.localization[stage][:] = self.currentLocalization
            self.currentMatchup = self.findMatchup()
            self.matchup[stage][:] = self.currentMatchup
        
    def localizePlayers(self):
        # First: find which minimap is empty to known who is at home
        localization = [0,0,2,2,4,4,6,6]
        # Second: localize those who are away from home
        return localization

    def findMatchup(self):
        matchup = [0]*8
        # Find the indexes leading to the same localization
        for i in range(len(self.currentLocalization)-1):
            for j in range(i,len(self.currentLocalization)):
                if self.currentLocalization[i] == self.currentLocalization[j]:
                    matchup[i] = j
                    matchup[j] = i
        return matchup






test0 = np.empty((0,24,3),dtype=np.uint8)
test = Image.open('data/items/Bloodthirster.jpg')
test2 = np.array(test)

test3 = np.concatenate((test0,test2),0)
test4 = Image.fromarray(test3)


'''
g = game(Image.open('data/analyze_boards/01.jpg'))
print('initialization')
print(g.initialized)
list_item = glob.glob('data/analyze_boards/*.jpg')
for item in list_item:
    print(item)
    g.update(Image.open(item))
    print('updated')

for player in g.players:
    keyboard.wait('7')
    print(player.itemList)
    player.boardbench.show()
'''








'''
list_item = glob.glob('data/analyze_boards/08.jpg')
for item in list_item:
    print('new jpg')
    g = game(Image.open(item))
Image.open('data/analyze_boards/01.jpg').crop(crop_littleLegend).save('data/littleLegends/test.jpg')
Image.open('data/analyze_boards/01.jpg').crop(crop_minimap).save('data/littleLegends/minimap.jpg')

i = 0
for minimap in crop_minimaps:
    Image.open('data/littleLegends/minimap.jpg').crop(minimap).save('data/littleLegends/minimap_'+str(i)+'.jpg')
    i = i +1
    
toCompare1 = Image.open('data/littleLegends/test.jpg').resize((13,13))
toCompare2 = Image.open('data/analyze_boards/01.jpg').crop(crop_minimap)
result = cv.matchTemplate(np.array(toCompare1),np.array(toCompare2),3)
min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
print(max_val)
index = np.nonzero(result > 0.95)
print(crop_minimaps)
print(index)




##    def update_championsOut():
##        self.championsOut = championsOut
##        for player in self.players:
##            self.championsOut = self.championsOut + self.players.championsOwned
##        self.championsRemaining = championsCopies - self.championsOut

# Item cropping
# Image.open('data/analyze_boards/01.jpg').crop((927,547,951,570)).save('data/items/spatula.jpg')

# Position item vs HB:
# 2 10 26 33

# Health bar cropping
#Image.open('data/analyze_boards/01.jpg').crop((925,537,930,543)).save('data/HB/HB1.jpg')
#Image.open('data/analyze_boards/04.jpg').crop((866,363,874,369)).save('data/HB/HB2.jpg')
'''
