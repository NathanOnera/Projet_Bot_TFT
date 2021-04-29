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

import players as p
import Record_data as rec

def normalize_array(arr):
    return arr/np.linalg.norm(arr)

class Application(tk.Tk):
    def __init__(self):
        print('Visual platform initialization')
        tk.Tk.__init__(self)
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
            dim = win32gui.GetWindowRect(win32gui.FindWindow(None, 'League of Legends (TM) Client'))
            self.dim = dim
            self.prompt.set('Click OK to start recording data')
            self.button.configure(text = 'OK', command=self.initialize_Game)
        except win32gui.error:
            print('Localization failed!')
            self.prompt.set('Localization failed! Try again!')
            self.button.configure(text = 'Try again!', command=self.initialize_Application)
        
    def initialize_Game(self):
        self.game = p.game(ImageGrab.grab(self.dim))
        if self.game.playersInitialized == False:
            self.prompt.set('Initialization failed! Please try again')
            self.button.configure(text = 'Try again!', command=self.initialize_Game)
        else:
            self.prompt.set('Game initialized!')
            self.button.configure(text = 'Show me the data!', command=self.menu_Button)

    def menu_Button(self):
        self.remove_Widgets()
        # Trying a menu button
        self.menu_button = tk.Menubutton(self, text= 'Here is a choice for you')
        self.menu_button.grid()
        self.menu_button.menu = tk.Menu(self.menu_button,tearoff = 0)
        self.menu_button["menu"] = self.menu_button.menu
        self.playerVar = tk.IntVar()
        self.playerVar.set(1000)
        self.menu_button.menu.add_radiobutton ( label="General game info", variable = self.playerVar, value = 1000, command = self.game_Info_Widgets)
        self.menu_button.menu.add_separator()
        for i in range(len(self.game.players)):
            self.menu_button.menu.add_radiobutton ( label="Player " + str(i)+ " info", variable = self.playerVar, value = i, command = self.display_player_info)
##        self.menu_button.menu.add_cascade(label='Choix

    def display_player_info(self):
        for item in self.grid_slaves():
            item.grid_forget()
        self.menu_button.grid()
##        self.remove_Widgets()
        image_ = self.game.players[self.playerVar.get()].boardbench
##        self.menu_Button()
        tkimage_ = ImageTk.PhotoImage(image_)
        label_ = tk.Label(self, image=tkimage_)
        label_.image = tkimage_
        label_.grid()

    def game_Info_Widgets(self):
        self.remove_Widgets()
        self.menu_Button()
        self.label_stage = tk.Label(self, text = 'Current stage: ' + self.game.stage)
        self.label_POV = tk.Label(self, text = 'Current POV: ' +  str(self.game.POV))
        self.label_dmgPOV = tk.Label(self, text = 'Current dmg POV: ' + str(self.game.dmgPOV))
        self.button_update = tk.Button(self, text = 'Update the data!', command=self.playUpdateGameState)
        self.button_update_players = tk.Button(self, text = 'Error in the players!', command=self.update_Players)
        self.button_quit = tk.Button(self, text = 'Quit', command=self.quit_Application)
        self.label_stage.grid()
        self.label_POV.grid()
        self.label_dmgPOV.grid()
##        tk.Label(self, text = 'There are ' + str(self.game.nbPlayers) + 'players.')
        self.ReserveImages = []
        for player in self.game.players:
            image_ = player.img
            tkimage_ = ImageTk.PhotoImage(image_)
            label_ = tk.Label(self, image=tkimage_)
            label_.image = tkimage_
            label_.grid(column = 0)
            lab = tk.Label(self, text = 'Current rank: ' + str(player.order)).grid(row = label_.grid_info()['row'],column = 1)
        self.button_update_players.grid(column = 0)
        self.button_update.grid(row = self.button_update_players.grid_info()['row'], column = 1)
        self.button_quit.grid(row = self.button_update_players.grid_info()['row'], column = 2)

    def remove_Widgets(self):
        list_widgets = self.grid_slaves()
        for item in list_widgets:
            item.destroy()

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
##            for lab in self.labelListPlayers:
##                print(lab)
##                lab.configure(text = 'Current rank: ' + str(player.order))
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
    
