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

def localize_client():
    hwnd = win32gui.FindWindow(None, 'League of Legends (TM) Client') # Find the LoL client
    dim = win32gui.GetWindowRect(hwnd)                          # Provides position (left,upper,right,lower) position of the client
    #win32gui.SetForegroundWindow(hwnd)                                                                 # Put the window in foreground (optional
    return dim

def initilize_naked_board(im,hexes):
    im.save('data/naked_board/naked_board.jpg',format='jpeg')
    print('Naked board updated')
    for i in range(hexes.shape[0]):
        file_name = 'data/naked_board/naked_board_' + str(i)+'.jpg'
        img = im.crop([hexes[i,0]-hex_w,hexes[i,1]-hex_h,hexes[i,0]+hex_w,hexes[i,1]+hex_h])
        img.save(file_name,format='jpeg')
    print('Naked board hexes updated.')

def extract_hexes(im,hexes,fn):
    for i in range(hexes.shape[0]):
        file_name = fn + '_' + str(i)
        img = im.crop([hexes[i,0]-hex_w,hexes[i,1]-hex_h,hexes[i,0]+hex_w,hexes[i,1]+hex_h])
        img.save('data/generated_data/hexes/'+file_name+'.jpg',format='jpeg')
    print('Hexes screenshot saved.')
    
def detect_empty_hex(im,hexes):
    occupation = np.empty((1,hexes.shape[0]+1));
    occupation_boolean = np.empty((1,hexes.shape[0]+1));
    string_to_print = 'Les hex vides sont : '
    for i in range(hexes.shape[0]):
        print(str(i))
        img = im.crop([hexes[i,0]-hex_w,hexes[i,1]-hex_h,hexes[i,0]+hex_w,hexes[i,1]+hex_h])
        mat1 = np.array(img).flatten()
        print(mat1.shape)
        mat2 = np.array(Image.open('data/naked_board/naked_board_'+str(i)+'.jpg')).flatten()
        diff_hex = cv.subtract(mat1,mat2)
        occupation[0,i] = math.floor(np.mean(diff_hex))
        if(occupation[0,i] < 5):
            occupation_boolean[0,i] = 0
        else:
            occupation_boolean[0,i] = 1
            string_to_print = string_to_print + str(i) + ' '
    print(string_to_print)
    return occupation_boolean

def record_feature_champion(im,fn,hexes):
    i = 28
    file_name = 'data/features_champion/' + fn
    img = im.crop([hexes[i,0]-feature_w,hexes[i,1]-feature_h,hexes[i,0]+feature_w,hexes[i,1]+feature_h])
    img.save(file_name + '.jpg',format='jpeg')
    img.show()
    print('Feature saved')

def detect_champion(im,hexes,i):
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
        im2.close()            
    print(val_/val)
    print(Champions[k])
    return Champions[k]

def detect_champion_all_board(im,hexes):
    occupation = detect_empty_hex(im,hexes)
    print(occupation.shape)
    detected_Champions = []
    for i in range(hexes.shape[0]):
        if occupation[0,i] == 1:
            detected_Champions.append(detect_champion(im,hexes,i))
            print('The hex ' + str(i) + ' contains ' + detected_Champions[-1])
        else:
            detected_Champions.append("Empty")
            print('The hex ' + str(i) + ' is empty')
    return detected_Champions

def main():
    # Initialisation
    HexesPosition = pd.read_csv("data/csv_files/HexesPosition.csv",delimiter = ';')                         # Importation of the hex position from a CSV file              
    hexes = HexesPosition.values
    keyboard.wait('7')
    dim = localize_client()
    flag = True
    while(flag == True):
        recorded = keyboard.read_key()
        fn = datetime.now().strftime("%m%d%Y%H%M%S")
        im = ImageGrab.grab(dim)
        if recorded == '5':
            # Screenshot of the whole board
            im.save('data/generated_data/whole_screenshot/'+fn+'.jpg',format='jpeg')
            print('Whole board and bench screenshot saved')
            # Screenshot of the hexes
            extract_hexes(im,hexes,fn)          # Calls the function to extract the hexes from the image and save them
        elif recorded == '6':
            initilize_naked_board(im,hexes)
        elif recorded == '8':
            fn = datetime.now().strftime("%m%d%Y%H%M%S")
            record_feature_champion(im,fn,hexes)
        elif recorded == '1':
            # Detect empty hex in the board and bench
            occupation = detect_empty_hex(im,hexes)
        elif recorded == '2':
            detect_champion(im,hexes,28)
        elif recorded == '3':
            detect_champion_all_board(im,hexes)
        elif recorded == '9':
            flag = False
            print('Exit')
        else:
            print('Aucun intérêt')
        im.close()
        time.sleep(1)
        
main()












