from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import shutil
import glob
import os
import sys
import time
import platform

if platform.system() == "Windows":
    from tkinter.ttk import *
else:
    from tkinter.ttk import Progressbar
    from tkinter.ttk import Notebook
    from tkinter.ttk import Combobox

root = Tk()
version = "0.0.2"
title = "PWAATeditor v" + version
    
    
class App:
    def __init__(self, master):
        self.titleLabel = Label(text=title)
        self.titleLabel.grid(pady=10)

        frame = Frame(master)
        frame.grid(padx=20, column=0)
        
        self.inputLabel = Label(frame, text="Save:")
        self.inputLabel.grid(row=1, column=0, padx=10)
        self.inputEntry = Entry(frame)
        self.inputEntry.grid(row=1, column=1, columnspan=2)
        self.getSaveButton = Button(frame, text="...", command=self.getSaveFile)
        self.getSaveButton.grid(row=1, column=3, padx=5)
        
        end = Frame(master)
        end.grid(padx=20, column=0)

        self.openSaveButton = Button(end, text="Open", command=self.openSavePath)
        self.openSaveButton.grid(row=0, column=0, pady=10, padx=10)

        self.showHelpButton = Button(end, text="About", command=self.showAbout)
        self.showHelpButton.grid(row=0, column=1, padx=10)

        self.quitButton = Button(end, text="Quit", command=root.quit)
        self.quitButton.grid(row=0, column=2, padx=10)
       
        self.authorLabel = Label(text="This is experimental software! Always make a backup.")
        self.authorLabel.grid(pady=(0, 10))
       
        self.authorLabel = Label(text="written by emiyl")
        self.authorLabel.grid(pady=(0, 10))
        
    def getSaveFile(self):
        savePath = filedialog.askopenfilename(initialdir="./", title="Select your save file")
        if not savePath:
            return
        filename = savePath[savePath.rfind('/') - len(savePath) + 1:]
        if filename != "systemdata":
            self.showFilenameWarning()
        self.inputEntry.delete(0, END)
        self.inputEntry.insert(0, savePath)
        
    def openSavePath(self):
        savePath = self.inputEntry.get()
        if not savePath:
            noFileWarning()
            return
        OpenSave(savePath)
        
    def showAbout(self):
        AboutWindow()
        
    def showFilenameWarning(self):
        FilenameWarning()
        
class OpenSave:
    binData = 0
    path = ""

    def __init__(self, path):
        self.path = path
        
        with open(self.path, 'rb') as f:
            self.binData = f.read()
        openSaveTk = Tk()
        openSaveTk.title("Save File")
        openSaveTkTkWindow = self.createWindow(openSaveTk)
        
    def readBin(self, address):
        decimal = int(address, 16)
        binary = self.binData[decimal]
        return binary
        
    def writeBin(self, address, hex):
        pos = int(address, 16)
        val = int(hex, 16)
        val = bytes([val])
        
        with open(self.path, "r+b") as f:
            f.seek(pos)
            f.write(val)
    
    def createWindow(self, master):
        tabParent = Notebook(master)
        tabChapters = Frame(tabParent)
        tabSettings = Frame(tabParent)
        
        tabParent.add(tabChapters, text="Chapters")
        tabParent.pack(expand=1, fill="both")
        
        ChaptersTab(self, master, tabChapters)
    
class ChaptersTab:
    addressList = ["12C4", "12C5", "12C6"]
    gameTitleList = ["Ace Attorney", "Justice For All", "Trials and Tribulations"]
    chapterNameList = ["Chapter 1", "Chapter 2", "Chapter 3", "Chapter 4", "Chapter 5"]
    unknownChapterStr = "Unknown chapter"
        
    currentChapterIntList = []
    chapterBox = []
    
    master = " "
    
    def __init__(self, master, window, tab):
        self.master = master
        
        frame = Frame(tab)
        frame.grid(padx=20, pady=10)
            
        x = 20
        y = 10
        
        for i in range(0,3):
            # Game Titles
            self.gameLabel = Label(frame, text=self.gameTitleList[i])
            self.gameLabel.grid(row=0, column=i, pady=y)
            self.currentChapterIntList.append(self.getChapterInt(i))
            
            # Select Chapter
            comboBox = Combobox(frame, values = self.chapterNameList)
            chapInt = self.currentChapterIntList[i]
            comboBox.set(self.getChapterName(chapInt))
            comboBox.grid(row=1, column=i, padx=x, pady=y)
            self.chapterBox.append(comboBox)
        
        end = Frame(tab)
        end.grid(padx=20, column=0)
        
        self.showHelpButton = Button(end, text="Save", command=self.saveChanges)
        self.showHelpButton.grid(row=0, column=0, padx=10, pady=10)
        
        self.showHelpButton = Button(end, text="Quit", command=window.destroy)
        self.showHelpButton.grid(row=0, column=1, padx=10, pady=10)
            
    def saveChanges(self):
        chapInt = []
        
        # Grab chapter number from boxes
        for game in range(0,3):
            string = self.chapterBox[game].get()
            if string == self.unknownChapterStr:
                chapInt.append(-1)
            for chapter in range(0,5):
                if string == self.chapterNameList[chapter]:
                    chapInt.append(chapter)
            chapInt[game] += 1
        
        # Now write them back to the save
        for game in range(0,3):
            hex = str(chapInt[game]) + "0"
            self.master.writeBin(self.addressList[game], hex)
        
    def getChapterInt(self, game):
        i = self.master.readBin(self.addressList[game])
        i = hex(i)[2:-1] # This prints the first digit of the address
        try:
            i = int(i) - 1
        except:
            i = " "
        return i
        
    def getChapterName(self, i):
        try:
            chapter = self.chapterNameList[i]
        except:
            chapter = self.unknownChapterStr
        return chapter
        
                
class FilenameWarning:
    def __init__(self):
        filenameTk = Tk()
        filenameTk.title("Warning")
        filenameTkWindow = self.createWindow(filenameTk)
    
    def createWindow(self, master):
        frame = Frame(master)
        frame.grid(padx=20, pady=10)
       
        self.introLabel = Label(frame, text="Save files are usually named \"systemdata\". Please ensure you have selected the right file before proceeding.", anchor=E, justify=LEFT, wraplength=400)
        self.introLabel.grid(row=1, column=0, sticky="W")
        
        end = Frame(master)
        end.grid(padx=20, column=0)

        self.showHelpButton = Button(end, text="OK", command=master.destroy)
        self.showHelpButton.grid(row=0, column=1, padx=10, pady=10)
        
class noFileWarning:
    def __init__(self):
        noFileWarningTk = Tk()
        noFileWarningTk.title("Error")
        noFileWarningTkWindow = self.createWindow(noFileWarningTk)
    
    def createWindow(self, master):
        frame = Frame(master)
        frame.grid(padx=20, pady=20)
       
        self.introLabel = Label(frame, text="You must select a save file first!", anchor=E, justify=LEFT, wraplength=400)
        self.introLabel.grid(row=1, column=0, sticky="W")
        
        end = Frame(master)
        end.grid(padx=20, column=0)

        self.showHelpButton = Button(end, text="OK", command=master.destroy)
        self.showHelpButton.grid(row=0, column=1, padx=10, pady=10)
        
class AboutWindow:
    def __init__(self):
        aboutTk = Tk()
        aboutTk.title("About PWAATeditor")
        aboutTkWin = self.createWindow(aboutTk)
    
    def createWindow(self, master):
        frame = Frame(master)
        frame.grid(padx=20, pady=10)
       
        self.label = Label(frame, text="This tool was developed by emiyl and works for the Phoenix Wright Ace Attorney Trilogy.", anchor=E, justify=LEFT, wraplength=400)
        self.label.grid(row=1, column=0, sticky="W")
        
        self.label = Label(frame, text="The editor has been tested for PC and Nintendo Switch. If you want, you can try to use it on other consoles and send me the results.", anchor=E, justify=LEFT, wraplength=400)
        self.label.grid(row=2, column=0, sticky="W")
        
        self.label = Label(frame, text="Always make a backup before editing your save! I am not responsible for any lost progress.", anchor=E, justify=LEFT, wraplength=400)
        self.label.grid(row=3, column=0, sticky="W")
        
        self.label = Label(frame, text="Thank you to summertriangle-dev and Amy While for helping me with the project.", anchor=E, justify=LEFT, wraplength=400)
        self.label.grid(row=4, column=0, sticky="W")
        
        end = Frame(master)
        end.grid(padx=20, column=0)

        self.showHelpButton = Button(end, text="OK", command=master.destroy)
        self.showHelpButton.grid(row=0, column=1, padx=10, pady=10)

app = App(root)
root.title(title)
root.mainloop()
