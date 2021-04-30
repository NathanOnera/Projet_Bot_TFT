from PIL import ImageGrab, Image, ImageTk
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
from threading import Thread
import tkinter as tk
import tkinter.ttk # separator

import players as p
import Record_data as rec

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
        if self.game.playersInitialized == False:
            self.prompt.set('Initialization failed! Please try again')
            self.button.configure(text = 'Try again!', command=self.initialize_Game)
        else:
            self.prompt.set('Game initialized!')
            self.button.configure(text = 'Show me the data!', command=self.createAllWidgets)

    def createAllWidgets(self):
        ####### FRAME CREATION #######
        # Declaration
        self.top = tk.Frame(self)
        self.topLeft = tk.Frame(self)
        self.topRight = tk.Frame(self)
        self.bottom = tk.Frame(self)

        # These lines are necessary for good usage of space within the frames
        self.top.grid_columnconfigure(0, weight=1)
        self.top.grid_rowconfigure(0, weight=1)
        self.topRight.grid_columnconfigure(0, weight=1)
        self.topLeft.grid_columnconfigure(0, weight=1)
        self.bottom.grid_columnconfigure(0, weight=1)
        self.topRight.grid_rowconfigure(0, weight=1)
        self.topLeft.grid_rowconfigure(0, weight=1)
        self.bottom.grid_rowconfigure(0, weight=1)

        ####### SEPARATORS CREATION #######
        self.separatorTopMiddle = tkinter.ttk.Separator(self, orient='horizontal')
        self.separatorTopLeftTitle = tkinter.ttk.Separator(self.topLeft, orient='horizontal')
        self.separatorTopLeftTopRight = tkinter.ttk.Separator(self, orient='vertical')
        self.separatorTopRightMenuButton = tkinter.ttk.Separator(self.topRight, orient='horizontal')
        self.separatorTopBottom = tkinter.ttk.Separator(self, orient='horizontal')
        
        ####### WIDGETS CREATION #######
        # TOP
        self.labelTitle = tk.Label(self.top, text = 'WELCOME TO TFT HELPER v0')
        
        ## TOP LEFT WINDOW
        # Title
        self.labelTopLeftTitle = tk.Label(self.topLeft, text = 'Basic game information')
        # INFO LABELS
        self.labelInfoStage = tk.Label(self.topLeft, text = 'Stage: ' + self.game.stage)
        self.labelInfoPOV = tk.Label(self.topLeft, text = 'POV: ' +  str(self.game.POV))
        self.labelInfodmgPOV = tk.Label(self.topLeft, text = 'dmg POV: ' + str(self.game.dmgPOV))
        self.labelInfoNbPlayers = tk.Label(self.topLeft, text = 'Number of players: ' + str(len(self.game.players)))
        self.labelLabelKey = tk.Label(self.topLeft, text = 'Key')
        self.labelLabelOrder = tk.Label(self.topLeft, text = 'Rank')
        # PLAYERS INFO
        self.listlabelInfoPlayersKey = []
        self.listlabelInfoPlayersOrder = []
        for player in self.game.players:
            tkimage_ = ImageTk.PhotoImage(player.img)
            labelKey = tk.Label(self.topLeft, image=tkimage_)
            labelKey.image = tkimage_
            self.listlabelInfoPlayersKey.append(labelKey)
            labelOrder = tk.Label(self.topLeft, text = str(player.order))
            self.listlabelInfoPlayersOrder.append(labelOrder)

        ## TOP RIGHT WINDOW
        # Menu button
        self.menuButtonBoards = tk.Menubutton(self.topRight, text= 'Select the player you want to scout')
        self.menuButtonBoards.menu = tk.Menu(self.menuButtonBoards,tearoff = 0)
        self.menuButtonBoards['menu'] = self.menuButtonBoards.menu
        self.playerBoardInt = tk.IntVar()
        for i in range(len(self.game.players)):
            self.menuButtonBoards.menu.add_radiobutton ( label="Player " + str(i), variable = self.playerBoardInt, value = i, command = self.displayPlayerBoard)
        # Board picture
        self.imagePlayerBoardSize = (484,303)
        self.imagePlayerBoard = ImageTk.PhotoImage(self.game.players[0].boardbench.resize(self.imagePlayerBoardSize))
        self.labelPlayerBoard = tk.Label(self.topRight, image=self.imagePlayerBoard)
        self.labelPlayerBoard.image = self.imagePlayerBoard

        ## BOTTOM PART
        ## TODO: TOTAL OF CHAMPIONS OUT OF POOL
        # ACTION BUTTON
        self.buttonUpdateData = tk.Button(self.bottom, text = 'Update the data!', command=self.playUpdateGameState)
        self.buttonReinitialize = tk.Button(self.bottom, text = 'Error in the players!', command=self.update_Players)
        self.buttonQuit = tk.Button(self.bottom, text = 'Quit', command=self.quit_Application)

        ## ONCE CREATED, CALL THEIR LAYOUT
        self.initializeMainWindow()

    def initializeMainWindow(self):
        # First thing first: remove former widgets on the self frame
        for item in self.grid_slaves():
            item.grid_forget()

        ####### FRAMES LAYOUT #######
        self.top.grid(row = 0, columnspan = 3)
        self.topLeft.grid(row = 2, column = 0, sticky = 'nsew')
        self.topRight.grid(row = 2, column = 2, sticky = 'nsew')
        self.bottom.grid(row = 4, columnspan = 3, sticky = 'ew')

        ####### FRAMES SEPARATORS LAYOUT #######
        self.separatorTopMiddle.grid(row = 1, columnspan = 3, sticky='ew')
        self.separatorTopLeftTopRight.grid(row = 2, column = 1, sticky = 'ns')
        self.separatorTopBottom.grid(row = 3, columnspan = 3, sticky = 'ew')
            
        ####### WIDGETS LAYOUT ######
        ## TOP FRAME
        self.labelTitle.grid(row = 0, columnspan = 2,sticky = 'ew')
        
        ## TOP LEFT FRAME
        # Title
        self.labelTopLeftTitle.grid(row = 0, column = 0,columnspan = 2, sticky="ew")
        self.separatorTopLeftTitle.grid(row = 1, column = 0, columnspan = 2, sticky="ew")
        # INFO LABELS
        self.labelInfoStage.grid(row = 2, sticky='w')
        self.labelInfoPOV.grid(row = 3, sticky='w')
        self.labelInfodmgPOV.grid(row = 4, sticky='w')
        self.labelInfoNbPlayers.grid(row = 5, sticky='w')
        self.labelLabelKey.grid(row = 6, column = 0, sticky = 'w')
        self.labelLabelOrder.grid(row = 6, column = 1, sticky = 'e')
        # PLAYERS INFO
        for i in range(len(self.game.players)):
            self.listlabelInfoPlayersKey[i].grid(column = 0, sticky='w')
            self.listlabelInfoPlayersOrder[i].grid(row = self.listlabelInfoPlayersKey[i].grid_info()['row'],column = 1, sticky='e')
        
        ## TOP RIGHT WINDOW
        #BOARD PICTURES AND MENU BUTTON
        self.menuButtonBoards.grid(row = 0)
##        self.separatorTopRightMenuButton.grid(row = 1,  sticky ='ew')
        self.labelPlayerBoard.grid(row =2)
      
        ## BOTTOM SECTION
        # ACTION BUTTONS
        self.buttonUpdateData.grid(column = 0,sticky = 'e')
        self.buttonReinitialize.grid(row = self.buttonUpdateData.grid_info()['row'], column = 1)
        self.buttonQuit.grid(row = self.buttonUpdateData.grid_info()['row'], column = 2, sticky = 'e')


    def menu_Button(self):
        self.remove_Widgets()
        # Trying a menu button
        self.menu_button = tk.Menubutton(self, text= 'Here is a choice for you')
        self.menu_button.grid()
        
    def displayPlayerBoard(self):
        self.imagePlayerBoard = ImageTk.PhotoImage(self.game.players[self.playerBoardInt.get()].boardbench.resize(self.imagePlayerBoardSize))
        self.labelPlayerBoard.configure(image=self.imagePlayerBoard)
        self.labelPlayerBoard.image = self.imagePlayerBoard

    def update_Players(self):
        self.game.playersInitialized = False
        self.game.update(ImageGrab.grab(self.dim))
        self.game_Info_Widgets()

    def threadUpdateGameState(self):
        self.flagAutoUpdate = True
        while self.flagAutoUpdate:
            while self._pause:
                pass
            self.game.update(ImageGrab.grab(self.dim))
            self.label_stage.configure(text = 'Current stage: ' + self.game.stage)
            self.label_POV.configure(text = 'Current POV: ' +  str(self.game.POV))
            self.label_dmgPOV.configure(text = 'Current dmg POV: ' + str(self.game.dmgPOV))
            for lab in self.labelListPlayers:
                print(lab)
                lab.configure(text = 'Current rank: ' + str(player.order))
            time.sleep(0.1)

    def playUpdateGameState(self):
        if self._thread is None:
            self._stop = False
            self._thread = Thread(target = self.threadUpdateGameState)
            self._thread.start()
        self._pause = False
        self.button_update.configure(text = 'Pause the update!', command = self.pauseUpdateGameState)

    def pauseUpdateGameState(self):
        self._pause = True
        self.button_update.configure(text = 'Update the data!', command = self.playUpdateGameState)
        
        
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
    
