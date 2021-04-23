from PIL import ImageGrab, Image
import win32gui
import time
import keyboard
from datetime import datetime
import pandas as pd
import cv2 as cv
import numpy as np
import math
import matplotlib.pyplot as plt
import glob
from lobe import ImageModel

import players as p
import Record_data as rec

# Data to load
crop_right = [1720,80,1920,800]
hexes = pd.read_csv("data/csv_files/HexesPosition.csv",delimiter = ';').values                         # Importation of the hex position from a CSV file              

crop_topright = [1885,130,1910,155]

def main():
    ## 1) initialization
    # Wait for a particular key to be pushed
    # Localize the client (or wait until it can be localized?)
    # Once localized, take screenshot(s) until one is 'valid' (i.e. in game screenshot that can provide enough info to initialize a p.game instance)

    ## 2) Initalization of a game instance
    # Get current stage, number of players, their current hp, and unique ID

    ## 3) Core of the program: while loop
    # Get current stage
    # Update players hp
    # Update victory loss (if available)
    # If own POV
        # Get shop, gold, xp
    # If (other POV or own POV) AND adequate moment
        # Update player bench/board
        # Update game available champions
    pass

if __name__ == "__main__":
##    main()
##    CPos = rec.initialize()
##    Image.open('data/analyze_boards/04222021103914.jpg').crop(crop_topright).save('data/red_circle/LookingAtDmg.jpg')
    Flag = True
    if Flag:
        Image.open('data/analyze_boards/07.jpg').crop([1807,213,1815,221]).save('data/red_circle/ennemy_pov.jpg')


    Cropping = False
    if Cropping:
        item_list = glob.glob('data/analyze_boards/1.jpg')
        mat1 = np.array(Image.open('data/red_circle/ennemy_not_pov.jpg'))
        k = 1
        for item in item_list:
            Image_right = Image.open(item).crop(crop_right)
            mat2 = np.array(Image_right)
            result = cv.matchTemplate(mat1,mat2,3)
            ennemy_pos = np.nonzero(result[:,104] > 0.95)
            k2 = 1
            for y in ennemy_pos[0]:
                img = Image_right.crop([104-51,y,104-8,y+20])
                img.save('data/red_circle/player' + str(k2) + '.jpg')
                k2 = k2 +1
            k = k+1
##            print(str(k)+ ' : ' + str(len(result[result>0.90])))
##            k = k+1
##            Image.open('data/analyze_boards/1.jpg').crop([1760,220,1820,235]).save('data/red_circle/lorkenlol.jpg')        

    AnalyzeGameInstance = True
    if AnalyzeGameInstance:
        G = p.game(Image.open('data/analyze_boards/01.jpg'))
        item_list = glob.glob('data/analyze_boards/*.jpg')
        k = 1
        for item in item_list:
            print(item)
            G.update_image(Image.open(item))
            k = k+1
            
                              




    AnalyzeGameInstance = False
    if AnalyzeGameInstance:
        item_list = glob.glob('data/analyze_boards/*.jpg')
        k = 1
        mat1b = np.array(Image.open('data/red_circle/lorkenlol.jpg'))
        for item in item_list:
            print('Image number '+str(k))
            G = p.game(Image.open(item))
            G.initialize()
            G.crop_image()
            G.update_nbPlayers()
            if G.dmgPOV == True:
                print('Current stage: ' + G.stage + ', we have the DMGPOV.')
            else:
                print('Current stage: ' + G.stage + ', we have the NOTDMGPOV, and there are ' + str(G.nbPlayers)+ ' players in the game.')
##                for item2 in item_list2:
##                    mat2 = np.array(Image.open(item2))
##                    result = cv.matchTemplate(np.array(G.imright),mat2,3)
##                    if len(result[result>0.95]) == 0:
##                        print('We did not find player '+ str(k2))
##                    elif len(result[result>0.95]) == 1:
##                        print('We found player '+ str(k2)+ ' exactly once')
##                    elif len(result[result>0.95]) > 1:
##                        print('We found player '+ str(k2)+ ' exactly ' + str (len(result[result>0.90])) + ' times')
##                    k2 = k2 +1
            k = k+1
##            mat2 = np.array(Image.open(item).crop(crop_right))
##            result = cv.matchTemplate(mat1b,mat2,3)
##            minval,maxval,minloc,maxloc = cv.minMaxLoc(result)
##            if len(result[result>0.90]) == 0:
##                print('We did not find this name')
##            elif len(result[result>0.90]) == 1:
##                print('We found it exactly once')
##            elif len(result[result>0.90]) > 1:
##                print('We found it too many times')
##            k = k+1

            
    AnalyzeNamePresence = False
    if AnalyzeNamePresence:
        item_list = glob.glob('data/analyze_boards/*.jpg')
        item_list2 = glob.glob('data/red_circle/player*.jpg')
        k = 1
        for item in item_list:
            mat2 = np.array(Image.open(item).crop(crop_right))
            for item2 in item_list2:
                mat1 = np.array(Image.open( ))
                
                result = cv.matchTemplate(mat1,mat2,3)
                minval,maxval,minloc,maxloc = cv.minMaxLoc(result)
                print(str(k)+ ' : ' + str(len(result[result>0.90])))
                k = k+1
##            test = Image.fromarray((result>0.95)*255)
##            if k == 7:
##                test.show()
            
##            print("Their indices are ", np.nonzero(result > 0.90))
##            k = k+1
##            result = (result-np.amin(result))/(np.amax(result)-np.amin(result))
##            test = Image.fromarray(result*255)
##            test.show()
            
##    ## Check if there is a match with ennemy_not_pov in the whole picture
##    for item in item_list:
##        mat2 = np.array(Image.open(item).crop(crop_right))
##        result = cv.matchTemplate(mat1,mat2,3)
##        print(str(k)+ ' : ' + str(len(result[result>0.98])))
##        print("Their indices are ", np.nonzero(result > 0.98))
##        k = k+1
##    ## Check if there is a match with ennemy_not_pov with x = 104
##    k = 1
##    for item in item_list:
##        mat2 = np.array(Image.open(item).crop(crop_right))
##        result = cv.matchTemplate(mat1,mat2,3)
##        print(str(k)+ ' : ' + str(len(result[result[:,104]>0.95])))
##        print("Their indices are ", np.nonzero(result[:,104] > 0.95))
##        k = k+1

        

   















'''

def get_POV(im):
# returns the POV
#   - 1,2,...,8,center
    pass



def get_phase(im):
# returns the current phase
#   - preparation, travel, combat, after combat, travel back
    pass

def get_names(im):
# returns the lobby names
    pass

def get_hp(im):
# returns the lobby hp
    pass


'''

'''

'''
'''
    im = Image.open('data/naked_board/naked_board.jpg')
    Game = p.game(im)
    Game.crop_image()
    Game.get_stage()
    print(Game.stage)

   dim = rec.initialize()
    Game = p.game(im)
    flag = True
    while(flag == True):
        im = ImageGrab.grab(dim)
        fou,stage,estage,boardbench = crop_image(im)
        Stage = get_stage(fou,stage,estage)
        print(Stage)
'''
    



'''
What info can we get from a single screenshot
    - current stage
    - current phase ? (preparation, travel, combat, after combat, travel back?)
    - lobby names
    - lobby hp
    - 

Image cropping :
    - stage : 780/35 -> 820/55
    - hp/names/POV : 1720/80 -> 1920/800
    - board & bench : 375/80 -> 375+1077/80+755 = 1460/840


'''
