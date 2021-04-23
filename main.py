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


crop_right = [1720,80,1920,800]

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

##def main():

##im = Image.open('data/analyze_boards/04222021101652.jpg')
##red_circle = im.crop([1824,284,1826,304])
##red_circle.save('data/red_circle/red_circle.jpg')
    


item_list = glob.glob('data/analyze_boards/*.jpg')
mat1 = np.array(Image.open('data/red_circle/red_circle.jpg'))
k = 1
for item in item_list:
    im = Image.open(item).crop(crop_right)
    item.replace('.jpg','')
##    im.save(item+'_RC.jpg')
    mat2 = np.array(im)
    result = cv.matchTemplate(mat1,mat2,3)
    print(str(k)+ ' : ' + str(len(result[result>0.98])))
    print("Their indices are ", np.nonzero(result > 0.98))
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    k = k+1
    print(item,max_val,max_loc)

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
    
##if __name__ == "__main__":
##    main()



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
