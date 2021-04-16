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

hex_w = 20
hex_h = 30
feature_w = 10
feature_h = 10
Champions = [
    'Aatrox',
    'Gragas',
    'Kalista',
    'Khazix',
    'Kled',
    'Leona',
    'Lissandra',
    'Poppy',
    'Udyr',
    'Vayne',
    'Vladimir',
    'Warwick',
    'Ziggs'
    ]

#im1 = Image.open('data/generated_data/hexes/Leona.jpg')


def localize_client():
    hwnd = win32gui.FindWindow(None, 'League of Legends (TM) Client') # Find the LoL client
    dim = win32gui.GetWindowRect(hwnd)                          # Provides position (left,upper,right,lower) position of the client
    #win32gui.SetForegroundWindow(hwnd)                                                                 # Put the window in foreground (optional
    return dim

def initilize_naked_board(dim,hexes):
    im = ImageGrab.grab(dim)
    im.save('data/naked_board/naked_board.jpg',format='jpeg')
    print('Naked board updated')
    for i in range(hexes.shape[0]):
        file_name = 'data/naked_board/naked_board_' + str(i)+'.jpg'
        img = im.crop([hexes[i,0]-hex_w,hexes[i,1]-hex_h,hexes[i,0]+hex_w,hexes[i,1]+hex_h])
        img.save(file_name,format='jpeg')
    print('Naked board hexes updated.')

def capture(dim,fn):
    im = ImageGrab.grab(dim)
    im.save('data/generated_data/whole_screenshot/'+fn+'.jpg',format='jpeg')
    print('Screenshot pris')
    return im

def extract_hexes(im,hexes,fn):
    for i in range(hexes.shape[0]):
        file_name = fn + '_' + str(i)
        img = im.crop([hexes[i,0]-hex_w,hexes[i,1]-hex_h,hexes[i,0]+hex_w,hexes[i,1]+hex_h])
        img.save('data/generated_data/hexes/'+file_name+'.jpg',format='jpeg')
    print('hexes extracted.')
    
def detect_empty_hex(hexes,fn):
    occupation = np.empty((1,hexes.shape[0]+1));
    occupation_boolean = np.empty((1,hexes.shape[0]+1));
    string_to_print = 'Les hex vides sont : '
    for i in range(hexes.shape[0]):
        mat1 = np.array(Image.open('data/naked_board/naked_board_'+str(i)+'.jpg')).flatten()
        mat2 = np.array(Image.open('data/generated_data/hexes/'+fn+'_'+str(i)+'.jpg')).flatten()
        diff_hex = cv.subtract(mat1,mat2)
        occupation[0,i] = math.floor(np.mean(diff_hex))
        if(occupation[0,i] < 5):
            occupation_boolean[0,i] = 0
        else:
            occupation_boolean[0,i] = 1
            string_to_print = string_to_print + str(i) + ' '
    print('Subtraction computed.')
    return string_to_print

def record_feature_champion(dim,fn,hexes):
    i = 28
    file_name = 'data/features_champion/' + fn
    im = ImageGrab.grab(dim)
    img = im.crop([hexes[i,0]-feature_w,hexes[i,1]-feature_h,hexes[i,0]+feature_w,hexes[i,1]+feature_h])
    img.save(file_name + '.jpg',format='jpeg')
    img.show()
    print('Feature saved')

def detect_champion(dim,hexes):
    i = 28
    im = ImageGrab.grab(dim)
    img = im.crop([hexes[i,0]-hex_w,hexes[i,1]-hex_h,hexes[i,0]+hex_w,hexes[i,1]+hex_h])
    mat1 = np.array(img)
    val_ = np.empty(len(Champions))
    val = 0
    k = 0
    for j in range(len(Champions)):
        fn = 'data/features_champion/'+Champions[j]+'.jpg'
        im2 = Image.open(fn)
        mat2 = np.array(im2)
        result = cv.matchTemplate(mat1,mat2,4)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        max_val = math.floor(max_val)
        val_[j] = max_val
        print(Champions[j],max_val)
        if max_val > val:
            k = j
            val=max_val
    print(val_/val)
    print(Champions[k])
 #   plt.plot(val_)
#    plt.show(block=False)
    return k
#        
#        mat_comp = np.array(img)
''' TODO : incorporer ça à la fonction detect_champion
mat1 = np.array(im1)
k = 0
val = 0
val_ = np.empty(len(Champions))
for j in range(len(Champions)):
    fn = 'data/features_champion/'+Champions[j]+'.jpg'
    im2 = Image.open(fn)
    mat2 = np.array(im2)
    result = cv.matchTemplate(mat1,mat2,4)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    val_[j] = max_val
    print(Champions[j],max_val)
    if max_val > val:
        k = j
        val=max_val
print(Champions[k])
plt.plot(val_)
plt.show(block=False)
'''

def main():
    # Initialisation
    HexesPosition = pd.read_csv("data/hexes/HexesPosition.csv",delimiter = ';')                         # Importation of the hex position from a CSV file              
    hexes = HexesPosition.values
    keyboard.wait('7')
    dim = localize_client()
    flag = True
    while(flag == True):
        recorded = keyboard.read_key()
        if recorded == '5':
            fn = datetime.now().strftime("%m%d%Y%H%M%S")
            im = capture(dim,fn)
            extract_hexes(im,HexesPosition.values,fn)          # Calls the function to extract the hexes from the image and save them
            occupation = detect_empty_hex(hexes,fn)
            print(occupation)
            im.close()
        elif recorded == '9':
            flag = False
            print('Exit')
        elif recorded == '6':
            initilize_naked_board(dim,hexes)
        elif recorded == '8':
            fn = datetime.now().strftime("%m%d%Y%H%M%S")
            record_feature_champion(dim,fn,hexes)
        elif recorded == '4':
            detect_champion(dim,hexes)
        else:
            print('Aucun intérêt')
        time.sleep(1)
        
main()












