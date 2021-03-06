from PIL import ImageGrab, Image, ImageTk
from win32 import win32gui              # import win32gui if not working
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
from threading import Thread
import tkinter as tk
import tkinter.ttk # separator

import players as p
#import Record_data as rec

def normalize_array(arr):
    return arr/np.linalg.norm(arr)

class Application(tk.Tk):
    def __init__(self):
        print('Visual platform initialization')
        tk.Tk.__init__(self)
        self.grid_columnconfigure(0, weight=1)
        self.prompt = tk.StringVar()
        self.prompt.set('Click OK to initialize the program')
        self.initial_Widgets()
        self._thread, self._pause, self._stop = None, False, True

    def initial_Widgets(self):
        self.label = tk.Label(self, textvariable = self.prompt)
        self.button = tk.Button(self, text = 'OK', command=self.initialize_Application)
        self.label.grid()
        self.button.grid()
        
    def initialize_Application(self):
        try:
##            dim = win32gui.GetWindowRect(win32gui.FindWindow(None, 'League of Legends (TM) Client'))
##            self.dim = dim
            self.prompt.set('Click OK to start recording data')
            self.button.configure(text = 'OK', command=self.initialize_Game)
        except win32gui.error:
            print('Localization failed!')
            self.prompt.set('Localization failed! Try again!')
            self.button.configure(text = 'Try again!', command=self.initialize_Application)
        
    def initialize_Game(self):
##        self.game = p.game(ImageGrab.grab(self.dim))
        self.game = p.game(Image.open('data/analyze_boards/01.jpg'))
        if self.game.initialized == False:
            self.prompt.set('Initialization failed! Please try again')
            self.button.configure(text = 'Try again!', command=self.initialize_Game)
        else:
            self.prompt.set('Game initialized!')
            self.button.configure(text = 'Show me the data!', command=self.createAllWidgets)

    def createAllWidgets(self):
        ####### FRAME CREATION #######
        # Declaration
        self.top = tk.Frame(self)
        self.generalGameInfo = tk.Frame(self)
        self.playersBoard = tk.Frame(self)
        self.championsOut = tk.Frame(self)
        self.bottomMenu = tk.Frame(self)

        # These lines are necessary for good usage of space within the frames
        for i in range(2):
            self.top.grid_columnconfigure(i, weight=1)
            self.playersBoard.grid_columnconfigure(i, weight=1)
            self.bottomMenu.grid_columnconfigure(i, weight=1)
            self.top.grid_rowconfigure(i, weight=1)
            self.playersBoard.grid_rowconfigure(i, weight=1)
            self.bottomMenu.grid_rowconfigure(i, weight=1)
        for i in range(10):
            self.championsOut.grid_columnconfigure(i, weight=1)
            self.championsOut.grid_rowconfigure(i, weight=1)

        for i in range(6):
            self.generalGameInfo.grid_rowconfigure(i, weight=1)
            self.generalGameInfo.grid_columnconfigure(i, weight=1)
            

        ####### SEPARATORS CREATION #######
        self.separatorTopMiddle = tkinter.ttk.Separator(self, orient='horizontal')
        self.separatorgeneralGameInfoTitle = tkinter.ttk.Separator(self.generalGameInfo, orient='horizontal')
        self.separatorgeneralGameInfoplayersBoard = tkinter.ttk.Separator(self, orient='vertical')
        self.separatorplayersBoardMenuButton = tkinter.ttk.Separator(self.playersBoard, orient='horizontal')
        self.separatorchampionsOut = tkinter.ttk.Separator(self, orient='horizontal')
        self.separatorbottomMenu = tkinter.ttk.Separator(self, orient='horizontal')
        
        ####### WIDGETS CREATION #######
        # TOP
        self.labelTitle = tk.Label(self.top, text = 'WELCOME TO TFT HELPER v0')
        
        ## TOP LEFT WINDOW
        # Title
        self.labelgeneralGameInfoTitle = tk.Label(self.generalGameInfo, text = 'Basic game information')
        # INFO LABELS
        self.labelInfoStage = tk.Label(self.generalGameInfo, text = 'Stage: ' + str(self.game.stage))
        self.labelInfoPhase = tk.Label(self.generalGameInfo, text = 'Phase: ' + str(self.game.phase))
        self.labelInfoPOV = tk.Label(self.generalGameInfo, text = 'ownPointOfView: ' +  str(self.game.ownPointOfView))
        self.labelInfodmgPOV = tk.Label(self.generalGameInfo, text = 'playersVisible: ' + str(self.game.playersVisible))
        self.labelInfoNbPlayers = tk.Label(self.generalGameInfo, text = 'Number of players: ' + str(len(self.game.players)))
        self.labelLabelKey = tk.Label(self.generalGameInfo, text = 'Key')
        self.labelLabelOrder = tk.Label(self.generalGameInfo, text = 'Rank')
        self.labelLabelCurrentMinimapPosition = tk.Label(self.generalGameInfo, text = 'Current minimap position')
        self.labelLabelLittleLegend = tk.Label(self.generalGameInfo, text = 'Little Legend')
        self.labelLabelItemList= tk.Label(self.generalGameInfo, text = 'Item list')
        self.labelLabelMinimapEmpty = tk.Label(self.generalGameInfo, text = 'Minimap Empty')
        # PLAYERS INFO
        self.listlabelInfoPlayersKey = []
        self.listlabelInfoPlayersLittleLegend = []
        self.listlabelInfoPlayersOrder = []
        self.listlabelInfoPlayersMinimapCurrentPosition = []
        self.listlabelInfoPlayersItemList = []
        self.listlabelInfoPlayersMinimapEmpty = []
        for player in self.game.players:
            tkimage_ = ImageTk.PhotoImage(player.imgKey)
            labelKey = tk.Label(self.generalGameInfo, image=tkimage_)
            labelKey.image = tkimage_
            self.listlabelInfoPlayersKey.append(labelKey)
            
            tkimage_ = ImageTk.PhotoImage(player.imgLittleLegendMinimap)
            labelLittleLegend = tk.Label(self.generalGameInfo, image=tkimage_)
            labelLittleLegend.image = tkimage_
            self.listlabelInfoPlayersLittleLegend.append(labelLittleLegend)
            
            labelOrder = tk.Label(self.generalGameInfo, text = str(player.rank))
            self.listlabelInfoPlayersOrder.append(labelOrder)
            
            labelMinimapCurrentPosition = tk.Label(self.generalGameInfo, text = str(player.minimapCurrentPosition))
            self.listlabelInfoPlayersMinimapCurrentPosition.append(labelMinimapCurrentPosition)
            
            labelMinimapEmpty = tk.Label(self.generalGameInfo, text = str(player.minimapEmpty))
            self.listlabelInfoPlayersMinimapEmpty.append(labelMinimapEmpty)
            
            #labelItemList = tk.Label(self.generalGameInfo, text = ' '.join(player.itemList))
            #self.listlabelInfoPlayersItemList.append(labelItemList)

            tkimage_ = ImageTk.PhotoImage(player.imgItemList)
            labelItemList = tk.Label(self.generalGameInfo, image=tkimage_)
            labelItemList.image = tkimage_
            self.listlabelInfoPlayersItemList.append(labelItemList)




        ## TOP RIGHT WINDOW
        # Menu button
        self.menuButtonBoards = tk.Menubutton(self.playersBoard, text= 'Whole image')
        self.menuButtonBoards.menu = tk.Menu(self.menuButtonBoards,tearoff = 0)
        self.menuButtonBoards['menu'] = self.menuButtonBoards.menu
        self.playerBoardInt = tk.IntVar()
        self.playerBoardInt.set(8)
        self.menuButtonBoards.menu.add_radiobutton ( label="Whole image", variable = self.playerBoardInt, value = 8, command = self.displayPlayerBoard)
        for i in range(len(self.game.players)):
            self.menuButtonBoards.menu.add_radiobutton ( label="Player " + str(i), variable = self.playerBoardInt, value = i, command = self.displayPlayerBoard)
        # Board picture
        self.imagePlayerBoardSize = (484,303)
        self.imagePlayerBoard = ImageTk.PhotoImage(self.game.players[0].boardbench.resize(self.imagePlayerBoardSize))
        self.labelPlayerBoard = tk.Label(self.playersBoard, image=self.imagePlayerBoard)
        self.labelPlayerBoard.image = self.imagePlayerBoard
        self.displayPlayerBoard()

        ## championsOut
        s = tk.ttk.Style(self)
        
        s.theme_use("default")
        s.layout("LabeledProgressbar",
         [('LabeledProgressbar.trough',
           {'children': [('LabeledProgressbar.pbar',
                          {'side': 'left', 'sticky': 'nsew'}),
                         ("LabeledProgressbar.label",   # label inside the bar
                          {"sticky": ""})],
           'sticky': 'nswe'})])
        s.configure("LabeledProgressbar", thickness=1, foreground='red', background='red')
        self.createProgressBarChampions(p.championsList)
        
        ## BOTTOM PART
        ## TODO: TOTAL OF CHAMPIONS OUT OF POOL
        # ACTION BUTTON
        self.buttonUpdateData = tk.Button(self.bottomMenu, text = 'Update the data!', command=self.playUpdateGameState)
        self.buttonReinitialize = tk.Button(self.bottomMenu, text = 'Error in the players!', command=self.update_Players)
        self.buttonQuit = tk.Button(self.bottomMenu, text = 'Quit', command=self.quit_Application)

        ## ONCE CREATED, CALL THEIR LAYOUT
        self.layoutMainWindow()

    def layoutMainWindow(self):
        # First thing first: remove former widgets on the self frame
        for item in self.grid_slaves():
            item.grid_forget()

        ####### FRAMES LAYOUT #######
        self.top.grid(row = 0, columnspan = 3)
        self.generalGameInfo.grid(row = 2, column = 0, sticky = 'nsew')
        self.playersBoard.grid(row = 2, column = 2, sticky = 'nsew')
        self.championsOut.grid(row = 4, columnspan = 3, sticky = 'ew')
        self.bottomMenu.grid(row = 6, columnspan = 3, sticky = 'ew')

        ####### FRAMES SEPARATORS LAYOUT #######
        self.separatorTopMiddle.grid(row = 1, columnspan = 3, sticky='ew')
        self.separatorgeneralGameInfoplayersBoard.grid(row = 2, column = 1, sticky = 'ns')
        self.separatorchampionsOut.grid(row = 3, columnspan = 3, sticky = 'ew')
        self.separatorbottomMenu.grid(row = 5, columnspan = 3, sticky = 'ew')
            
        ####### WIDGETS LAYOUT ######
        ## TOP FRAME
        self.labelTitle.grid(row = 0, columnspan = 2,sticky = 'ew')
        
        ## TOP LEFT FRAME
        # Title
        self.labelgeneralGameInfoTitle.grid(row = 0, column = 0,columnspan = 2, sticky="ew")
        self.separatorgeneralGameInfoTitle.grid(row = 1, column = 0, columnspan = 2, sticky="ew")
        # INFO LABELS
        self.labelInfoStage.grid(row = 2, sticky='w')
        self.labelInfoPhase.grid(row = 3, sticky='w')
        self.labelInfoPOV.grid(row = 4, sticky='w')
        self.labelInfodmgPOV.grid(row = 5, sticky='w')
        self.labelInfoNbPlayers.grid(row = 6, sticky='w')
        self.labelLabelKey.grid(row = 7, column = 0, sticky = 'w')
        self.labelLabelLittleLegend.grid(row = 7, column = 1, sticky = '')
        self.labelLabelOrder.grid(row = 7, column = 2, sticky = 'e')
        self.labelLabelCurrentMinimapPosition.grid(row = 7, column = 3, sticky = 'e')
        self.labelLabelMinimapEmpty.grid(row = 7, column = 4, sticky = 'e')
        self.labelLabelItemList.grid(row = 7, column = 5, sticky = 'e')
        # PLAYERS INFO
        for i in range(len(self.game.players)):
            self.listlabelInfoPlayersKey[i].grid(column = 0, sticky='w')
            self.listlabelInfoPlayersLittleLegend[i].grid(row = self.listlabelInfoPlayersKey[i].grid_info()['row'], column = 1, sticky='')
            self.listlabelInfoPlayersOrder[i].grid(row = self.listlabelInfoPlayersKey[i].grid_info()['row'],column = 2, sticky='e')
            self.listlabelInfoPlayersMinimapCurrentPosition[i].grid(row = self.listlabelInfoPlayersKey[i].grid_info()['row'],column = 3, sticky='e')
            self.listlabelInfoPlayersMinimapEmpty[i].grid(row = self.listlabelInfoPlayersKey[i].grid_info()['row'],column = 4, sticky='e')
            self.listlabelInfoPlayersItemList[i].grid(row = self.listlabelInfoPlayersKey[i].grid_info()['row'],column = 5, sticky='e')
        
        ## TOP RIGHT WINDOW
        #BOARD PICTURES AND MENU BUTTON
        self.menuButtonBoards.grid(row = 0)
##        self.separatorTopRightMenuButton.grid(row = 1,  sticky ='ew')
        self.labelPlayerBoard.grid(row =2)

        ## championsOut
        self.layoutProgressBarChampions()
        
        ## BOTTOM SECTION
        # ACTION BUTTONS
        self.buttonUpdateData.grid(column = 0,sticky = 'w')
        self.buttonReinitialize.grid(row = self.buttonUpdateData.grid_info()['row'], column = 1, sticky = 'w')
        self.buttonQuit.grid(row = self.buttonUpdateData.grid_info()['row'], column = 2, sticky = 'e')

    def createProgressBarChampions(self,l):
        self.listChampionsProgressBar = []
        self.listChampionsLabelsw = []
        self.listChampionsLabelse = []
        for i in range(len(l)):
            tempLabelw = tk.Label(self.championsOut, text = l.values[i,0])
            tempLabele = tk.Label(self.championsOut, text = str(l.values[i,3]) +  '/' + str(l.values[i,2]))
            tempProgressBar = tk.ttk.Progressbar(self.championsOut,style="LabeledProgressbar", maximum = l.values[i,2])
            self.listChampionsProgressBar.append(tempProgressBar)
            self.listChampionsLabelsw.append(tempLabelw)
            self.listChampionsLabelse.append(tempLabele)
            
    def layoutProgressBarChampions(self):
        for i in range(len(self.listChampionsProgressBar)):
            self.listChampionsLabelsw[i].grid(row = 2*p.championsList.values[i,4], column=2*(p.championsList.values[i,1]-1), sticky = 'w', padx = 2)
            self.listChampionsLabelse[i].grid(row = 2*p.championsList.values[i,4], column=2*(p.championsList.values[i,1]-1)+1, sticky = 'e', padx = 2)
            self.listChampionsProgressBar[i].grid(row = 2*p.championsList.values[i,4]+1, column=2*(p.championsList.values[i,1]-1), columnspan = 2, sticky = 'ew', padx = 2)

    def updateAllWidgets(self):
        # INFO LABELS
        self.labelInfoStage.configure(text = 'Stage: ' + str(self.game.stage))
        self.labelInfoPhase.configure(text = 'Phase: ' + str(self.game.phase))
        self.labelInfoPOV.configure(text = 'ownPointOfView: ' +  str(self.game.ownPointOfView))
        self.labelInfodmgPOV.configure(text = 'playersVisible: ' + str(self.game.playersVisible))
        self.labelInfoNbPlayers.configure(text = 'Number of players: ' + str(len(self.game.players)))
        
        # PLAYERS INFO
        for i in range(len(self.game.players)):
            self.listlabelInfoPlayersOrder[i].configure(text = str(self.game.players[i].rank))
            
            tkimage_ = ImageTk.PhotoImage(self.game.players[i].imgItemList)
            self.listlabelInfoPlayersItemList[i].configure(image=tkimage_)
            self.listlabelInfoPlayersItemList[i].image = tkimage_
            #self.listlabelInfoPlayersItemList[i].configure(text = '-'.join(self.game.players[i].itemList))
            
            self.listlabelInfoPlayersMinimapEmpty[i].configure(text = str(self.game.players[i].minimapEmpty))
            self.listlabelInfoPlayersMinimapCurrentPosition[i].configure(text = str(self.game.players[i].minimapCurrentPosition))
        
        self.displayPlayerBoard()
        self.updateProgressBarChampions(self.game.championsList)

    def updateProgressBarChampions(self,l):
        for i in range(len(l)):
            self.listChampionsLabelse[i].configure(text = str(l.values[i,3]) +  '/' + str(l.values[i,2]))
            self.listChampionsProgressBar[i]['value'] = l.values[i,3]

    def displayPlayerBoard(self):
        if self.playerBoardInt.get() == 8:
            self.imagePlayerBoard = ImageTk.PhotoImage(self.game.im.resize(self.imagePlayerBoardSize))
            self.labelPlayerBoard.configure(image=self.imagePlayerBoard)
            self.labelPlayerBoard.image = self.imagePlayerBoard
        else:
            self.imagePlayerBoard = ImageTk.PhotoImage(self.game.players[self.playerBoardInt.get()].boardbench.resize(self.imagePlayerBoardSize))
            self.labelPlayerBoard.configure(image=self.imagePlayerBoard)
            self.labelPlayerBoard.image = self.imagePlayerBoard

    def update_Players(self):
        self.game.initialized = False
        self.game.update(ImageGrab.grab(self.dim))
        self.game_Info_Widgets()

    def threadUpdateGameState(self):
        self.flagAutoUpdate = True
        list_item = glob.glob('data/analyze_boards/*.jpg')
        k = 1
        while self.flagAutoUpdate:
            while self._pause:
                pass
            keyboard.wait('7')
            self.game.update(Image.open(list_item[k]))
            for i in range(len(self.game.championsList)):
                self.game.championsList.loc[i,'Out'] = i % (self.game.championsList.loc[i,'Copies']+1)
            self.updateAllWidgets()
#            time.sleep(4)
            k = k+1
            
    def playUpdateGameState(self):
        if self._thread is None:
            self._stop = False
            self._thread = Thread(target = self.threadUpdateGameState)
            self._thread.start()
        self._pause = False
        self.buttonUpdateData.configure(text = 'Pause the update!', command = self.pauseUpdateGameState)

    def pauseUpdateGameState(self):
        self._pause = True
        self.buttonUpdateData.configure(text = 'Update the data!', command = self.playUpdateGameState)
        
        
##    def main_loop(self):
##        self.game_Info_Widgets()

    def quit_Application(self): 
        self.destroy()

def main():
    App = Application()
    App.mainloop()

if __name__ == "__main__":
    FlagMain = True
    if FlagMain:
        main()
    
