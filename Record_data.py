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
#from lobe import ImageModel

crop_stage = [780,35,820,55]
crop_estage = [830,35,870,55]

hex_w = 30
hex_h = 50
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

def initialize():
    print('Push 7 to localize the client')
    keyboard.wait('7')
    dim = localize_client()
    return dim

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

def detect_empty_hexes(im,hexes):
    occupation = np.empty((1,hexes.shape[0]+1));
    occupation_boolean = np.empty((1,hexes.shape[0]+1));
    string_to_print = 'Les hex vides sont : '
    for i in range(hexes.shape[0]):
        img = im.crop([hexes[i,0]-hex_w,hexes[i,1]-hex_h,hexes[i,0]+hex_w,hexes[i,1]+hex_h])
        mat1 = np.array(img).flatten()
        mat2 = np.array(Image.open('data/naked_board/naked_board_'+str(i)+'.jpg')).flatten()
        diff_hex = cv.subtract(mat1,mat2)
            occupation_boolean[0,i] = 0
            fn = datetime.now().strftime("%m%d%Y%H%M%S")
            img.save('data/generated_data/hexes/Empty'+fn+'.jpg')
        else:
            occupation_boolean[0,i] = 1
            string_to_print = string_to_print + str(i) + ' '
    print(string_to_print)
    return occupation_boolean

def record_feature_champion(im,fn,hexes):
    i = 28
    file_name = 'data/features_champion/' + fn
    img = im.crop([hexes[i,0],hexes[i,1]+feature_h,hexes[i,0]+2*feature_w,hexes[i,1]+3*feature_h])
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
        result = cv.matchTemplate(mat1,mat2,3)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        #max_val = math.floor(max_val)
        val_[j] = max_val
#        print(Champions[j],max_val)
        if max_val > val:
            k = j
            val=max_val
        im2.close()            
    #print(val_)
#    print(Champions[k])
    fn = datetime.now().strftime("%m%d%Y%H%M%S")
    img.save('data/generated_data/hexes/'+Champions[k]+fn+'.jpg')
    return Champions[k]

def detect_champion_multiple_features(im,hexes,i):
    img = im.crop([hexes[i,0]-hex_w,hexes[i,1]-hex_h,hexes[i,0]+hex_w,hexes[i,1]+hex_h])
    mat1 = np.array(img)
    val_ = np.empty(len(Champions))
    val = 0
    k = 0
    path = 'data/features_champion/'
    for j in range(len(Champions)):
        val_[j] = 0
        list_features = glob.glob('data/features_champion/'+Champions[j]+'*.jpg')
        for item in list_features:
            im2 = Image.open(item)
            mat2 = np.array(im2)
            result = cv.matchTemplate(mat1,mat2,3)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
            if max_val > val_[j]:
                val_[j] = max_val
            im2.close()
        if val_[j] > val:
            k = j
            val=val_[j]
    fn = datetime.now().strftime("%m%d%Y%H%M%S")
    img.save('data/generated_data/hexes/'+Champions[k]+fn+'.jpg')
    return Champions[k]

def detect_champion_all_board_multiple_features(im,hexes):
    occupation = detect_empty_hexes(im,hexes)
    detected_Champions = []
    for i in range(hexes.shape[0]):
        if occupation[0,i] == 1:
            detected_Champions.append(detect_champion_multiple_features(im,hexes,i))
            print(str(i) + ': ' + detected_Champions[-1])
        else:
            detected_Champions.append("Empty")
            #print(str(i) + ': Empty')
    return detected_Champions

def detect_champion_all_board(im,hexes):
    occupation = detect_empty_hexes(im,hexes)
    detected_Champions = []
    for i in range(hexes.shape[0]):
        if occupation[0,i] == 1:
            detected_Champions.append(detect_champion(im,hexes,i))
            print(str(i) + ': ' + detected_Champions[-1])
        else:
            detected_Champions.append("Empty")
            print(str(i) + ': Empty')
    return detected_Champions

def record_all_features(im,hexes):
    detected_Champions = detect_champion_all_board(im,hexes)
    file_name = 'data/potential_features/'
    for i in range(hexes.shape[0]):
        image_hex = im.crop([hexes[i,0]-hex_w,hexes[i,1]-hex_h,hexes[i,0]+hex_w,hexes[i,1]+hex_h])
        temps = datetime.now().strftime("%m%d%Y%H%M%S%f")
        fn = file_name + detected_Champions[i]+temps+'.jpg'
        image_hex.save(fn)
        if detected_Champions[i] != "Empty":
            image_feature = im.crop([hexes[i,0],hexes[i,1]+feature_h,hexes[i,0]+2*feature_w,hexes[i,1]+3*feature_h])
            temps = datetime.now().strftime("%m%d%Y%H%M%S%f")
            fn = file_name + detected_Champions[i]+temps+'.jpg'
            image_feature.save(fn)
            image_feature = im.crop([hexes[i,0]-feature_w,hexes[i,1]+feature_h,hexes[i,0]+feature_w,hexes[i,1]+3*feature_h])
            temps = datetime.now().strftime("%m%d%Y%H%M%S%f")
            fn = file_name + detected_Champions[i]+temps+'.jpg'
            image_feature.save(fn)
            image_feature = im.crop([hexes[i,0],hexes[i,1],hexes[i,0]+2*feature_w,hexes[i,1]+2*feature_h])
            temps = datetime.now().strftime("%m%d%Y%H%M%S%f")
            fn = file_name + detected_Champions[i]+temps+'.jpg'
            image_feature.save(fn)
            image_feature = im.crop([hexes[i,0],hexes[i,1]-feature_h,hexes[i,0]+2*feature_w,hexes[i,1]+feature_h])
            temps = datetime.now().strftime("%m%d%Y%H%M%S%f")
            fn = file_name + detected_Champions[i]+temps+'.jpg'
            image_feature.save(fn)
            image_feature = im.crop([hexes[i,0]-feature_w,hexes[i,1]-feature_h,hexes[i,0]+feature_w,hexes[i,1]+feature_h])
            temps = datetime.now().strftime("%m%d%Y%H%M%S%f")
            fn = file_name + detected_Champions[i]+temps+'.jpg'
            image_feature.save(fn)
    print('Finished')

def record_lobe(im,hexes):
    detected_Champions = detect_champion_all_board(im,hexes)
    file_name = 'data/input_lobe/'
    for i in range(hexes.shape[0]):
        if detected_Champions[i] != "Empty":
            image_hex = im.crop([hexes[i,0]-hex_w,hexes[i,1]-hex_h,hexes[i,0]+hex_w,hexes[i,1]+hex_h])
            temps = datetime.now().strftime("%m%d%Y%H%M%S%f")
            fn = file_name + detected_Champions[i]+temps+'.jpg'
            image_hex.save(fn)
    print('Finished')

def detect_with_lobe(im,hexes,model):
    occupation = detect_empty_hexes(im,hexes)
    detected_Champions = []
    file_name = 'data/input_lobe/'
    for i in range(hexes.shape[0]):
        if occupation[0,i] == 1:
            img = im.crop([hexes[i,0]-hex_w,hexes[i,1]-hex_h,hexes[i,0]+hex_w,hexes[i,1]+hex_h])
            result = model.predict(img)
            print(str(i) + ': ' + result.prediction)
            detected_Champions.append(result.prediction)
            temps = datetime.now().strftime("%m%d%Y%H%M%S%f")
            fn = file_name + result.prediction +temps+'.jpg'
            img.save(fn)
            img.close()
        else:
            pass
##            img = im.crop([hexes[i,0]-hex_w,hexes[i,1]-hex_h,hexes[i,0]+hex_w,hexes[i,1]+hex_h])
##            temps = datetime.now().strftime("%m%d%Y%H%M%S%f")
##            fn = file_name + 'Empty' +temps+'.jpg'
##            img.save(fn)
##            detected_Champions.append("Empty")
##            print(str(i) + ': Empty')
##            img.close()
    return detected_Champions

def main():
##    print('begining')
##    model = ImageModel.load('Lobe/TensorFlow/')
##    print('model loaded')
    
    # Initialisation
    HexesPosition = pd.read_csv("data/csv_files/HexesPosition.csv",delimiter = ';')                         # Importation of the hex position from a CSV file              
    hexes = HexesPosition.values
    dim = initialize()
    flag = True
    while (flag == True):
        fn = datetime.now().strftime("%m%d%Y%H%M%S")
        im = ImageGrab.grab(dim)
        stage = im.crop(crop_stage)
        estage = im.crop(crop_estage)
        stage.save('data/stages/'+fn+'.jpg')
        estage.save('data/estages/'+fn+'.jpg')
        time.sleep(10)
    '''
    flag = True
    while(flag == True):
        recorded = keyboard.read_key()
        fn = datetime.now().strftime("%m%d%Y%H%M%S")
        im = ImageGrab.grab(dim)
        if recorded == '1':
            temps = datetime.now().strftime("%m%d%Y%H%M%S")
            fn = 'data/analyze_boards/'+temps+'.jpg'
            im.save(fn)
            im.close()
#            occupation = detect_empty_hexes(im,hexes)
        elif recorded == '3':
            detect_champion_all_board(im,hexes)
        elif recorded == '2':
            detect_with_lobe(im,hexes,model)
#            detect_champion_all_board_multiple_features(im,hexes)
        elif recorded == '6':
            initilize_naked_board(im,hexes)
        elif recorded == '5':
            record_all_features(im,hexes)
        elif recorded == '8':
            record_lobe(im,hexes)
        elif recorded == '4':
            fn = datetime.now().strftime("%m%d%Y%H%M%S")
            record_feature_champion(im,fn,hexes)
        elif recorded == '9':
            flag = False
            print('Exit')
        else:
            print('Aucun intérêt')
        im.close()
        time.sleep(1)
    '''
if __name__ == "__main__":
    main()




##      elif recorded == '4':
##            localize_hex(im)                # Use a 1 star lissandra out of combat  elif recorded == '5':
##            im.save('data/generated_data/whole_screenshot/'+fn+'.jpg',format='jpeg')
##            print('Whole board and bench screenshot saved')
##            extract_hexes(im,hexes,fn)          # Calls the function to extract the hexes from the image and save them


##        elif recorded == '2':
##            dt = detect_champion(im,hexes,28)
##            print('28: ' + dt)

##def extract_hexes(im,hexes,fn):
##    for i in range(hexes.shape[0]):
##        file_name = fn + '_' + str(i)
##        img = im.crop([hexes[i,0]-hex_w,hexes[i,1]-hex_h,hexes[i,0]+hex_w,hexes[i,1]+hex_h])
##        img.save('data/generated_data/hexes/'+file_name+'.jpg',format='jpeg')
##    print('Hexes screenshot saved.')

##def localize_hex(im):
##    mat1 = np.array(im)
##    im2 = Image.open('data/features_champion/Lissandra.jpg')
##    mat2 = np.array(im2)
##    result = cv.matchTemplate(mat1,mat2,4)
##    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
##    print(min_loc)
##    print(max_loc)
##    return min_loc,max_loc







