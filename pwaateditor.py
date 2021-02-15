from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Notebook
from tkinter.ttk import Combobox
import platform
import sys
import os
import re

if platform.system() == 'Windows':
    from tkinter.ttk import *

version = '0.3.0'
title = 'PWAATeditor v' + version
args = sys.argv[1:]

class App:
    saveLabelString        = 'Save:'
    selectSaveButtonString = '...'
    openSaveButtonString   = 'Open'
    aboutPageButtonString  = 'About'
    quitAppButtonString    = 'Quit'
    experimentalString     = 'This is experimental software! Always make a backup.'
    authorCreditsString    = 'written by emiyl'
    fileDialogueString     = 'Select your save file'

    def __init__(self):
        root = Tk()
        root.title(title)
        self.savePath = ''
        self.createWindow(root)
        root.mainloop()
    
    def createWindow(self, root):
        if self.getArgs(root) < 1:
            window = self.displayWindow(root)
            
    def getArgs(self, root):
        success = 0
        for i in range(0,len(args)):
            self.savePath = args[i]
            val = self.openSavePath(root)
            if success == 0:
                success = val
        return success
    
    def displayWindow(self, master):
        titleLabel = Label(text=title)
        titleLabel.grid(pady=10)

        frame = Frame(master)
        frame.grid(padx=20, column=0)

        inputLabel = Label(frame, text=self.saveLabelString)
        inputLabel.grid(row=1, column=0, padx=10)
        
        self.inputEntry = Entry(frame)
        self.inputEntry.grid(row=1, column=1, columnspan=2)
        
        getSaveButton = Button(frame, text=self.selectSaveButtonString, command=self.getSaveFile)
        getSaveButton.grid(row=1, column=3, padx=5)

        end = Frame(master)
        end.grid(padx=20, column=0)

        openSaveButton = Button(end, text=self.openSaveButtonString, command=self.openSaveButton)
        openSaveButton.grid(row=0, column=0, pady=10, padx=10)

        showHelpButton = Button(end, text=self.aboutPageButtonString, command=self.showAbout)
        showHelpButton.grid(row=0, column=1, padx=10)

        quitButton = Button(end, text=self.quitAppButtonString, command=master.quit)
        quitButton.grid(row=0, column=2, padx=10)

        authorLabel = Label(text=self.experimentalString)
        authorLabel.grid(pady=(0, 10))

        authorLabel = Label(text=self.authorCreditsString)
        authorLabel.grid(pady=(0, 10))

    def getSaveFile(self):
        savePath = filedialog.askopenfilename(initialdir='./', title=self.fileDialogueString)
        if not savePath:
            return
        filename = savePath[savePath.rfind('/') - len(savePath) + 1:]
        if filename != 'systemdata':
            FilenameWarning()
        self.inputEntry.delete(0, END)
        self.inputEntry.insert(0, savePath)
        
    def openSaveButton(self):
        self.savePath = self.inputEntry.get()
        self.openSavePath(0)

    def openSavePath(self, root):
        if self.savePath:
            OpenSave(root, self.savePath)
            return 1
        return 0

    def showAbout(self):
        AboutWindow()


class OpenSave:
    binData = 0

    def __init__(self, root, path):
        self.path = path
        with open(self.path, 'rb') as f:
            self.binData = f.read()
        if root == 0:
            openSaveTk = Tk()
            openSaveTk.title("Save File")
            openSaveTkWindow = self.createWindow(openSaveTk)
        else:
            root.title("Save File")
            openSaveTkWindow = self.createWindow(root)
            

    def readBin(self, address, length):
        v = []
        if length == 1:
            v.append(self.binData[address])
        else:
            for i in range(0, length):
                loopAddr = address + i
                loopHexa = self.binData[loopAddr]
                v.append(loopHexa)
        return bytes(v)

    def writeBin(self, address, byte):
        with open(self.path, 'r+b') as f:
            f.seek(address)
            f.write(byte)

    def createWindow(self, master):
        tabParent = Notebook(master)
        settingsTab = Frame(tabParent)
        
        saveSlotTab = []
        saveCount = 7
        for i in range(0,saveCount):
            saveSlotTab.append(Frame(tabParent))
        
        tabParent.add(settingsTab, text="Settings")
        #for i in range(0,saveCount):
        #    title = "Slot {0}".format(i+1)
        #    tabParent.add(saveSlotTab[i], text=title)
            
        tabParent.pack(expand=1, fill="both")
        
        SettingsEditor(master, self, settingsTab)
        #for i in range(0,saveCount):
        #    SaveSlot(master, self, saveSlotTab[i], i)
        
class SaveSlot:
    saveButtonString     = 'Save'
    resetButtonString    = 'Reset'
    quitButtonString     = 'Quit'
    
    dateTimeLabelString  = ['Date', 'Time']
    setDateTimeBtnString = ['Set Date', 'Set Time']
    dividerChar          = ['/', ':']
    
    def getSaveAddr(self, address):
        address = address + self.slot * 0x30
        return address
        
    def getInfo(self):
        # Date and time
        self.timeValue = []
        for i in range(0, self.timeStringCount):
            byteList = self.master.readBin(self.timeAddr[i], self.timeStringLength[i])
            v = bytes(byteList).decode('utf-8')
            self.timeValue.append(v)
        
    def setAddr(self):
        self.timeStringCount  = 6
        self.timeStringLength = [4,2,2,2,2,2]
        self.timeAddr = []
        
        for i in range(0, self.timeStringCount):
            if i == 0:
                previousAddr = self.dateAndTimeAddr
                previousLength = 0
            else:
                previousAddr = self.timeAddr[i-1]
                previousLength = self.timeStringLength[i-1] + 1
            self.timeAddr.append(previousAddr + previousLength)

    def __init__(self, window, master, tab, slot):
        self.master = master
        self.slot = slot
        
        self.dateAndTimeAddr = self.getSaveAddr(0x1E4)
        self.chapterPartAddr = self.getSaveAddr(0x210)
        self.setAddr()
        
        self.getInfo()
        
        self.createWindow(window, tab)
       
    def createWindow(self, window, tab):
        pady = 10
        padx = 20

        frame = Frame(tab)
        frame.grid(padx=padx, pady=pady)
        
        self.timeEntry = []
        
        for i in range(0,2):
            inputLabel = Label(frame, text=self.dateTimeLabelString[i] + ':')
            inputLabel.grid(row=i, column=0, padx=padx)
        
        for x in range(0,3):
            for y in range(0,2):
                i = x + (y * 3)
                boxWidth = 2
                if i == 0:
                    boxWidth = 4
                
                timeEntry = Entry(frame, width=boxWidth)
                timeEntry.grid(row=y, column=(x*2)+1)
                timeEntry.insert(y, self.timeValue[i])
                self.timeEntry.append(timeEntry)
            
        for x in range(0,2):
            for y in range(0,2):
                dividerLabel = Label(frame, text=self.dividerChar[y])
                dividerLabel.grid(row=y, column=(x*2)+2)
            
        setDateBtn = Button(frame, text=self.setDateTimeBtnString[0], command=window.destroy)
        setDateBtn.grid(row=0, column=7, pady=pady, padx=padx, columnspan=3)
            
        setTimeBtn = Button(frame, text=self.setDateTimeBtnString[1], command=window.destroy)
        setTimeBtn.grid(row=1, column=7, pady=pady, padx=padx, columnspan=3)

        end = Frame(tab)
        end.grid(padx=padx)
        pady += 10

        showHelpButton = Button(end, text=self.saveButtonString, command=window.destroy)
        showHelpButton.grid(row=0, column=0, padx=padx, pady=pady)

        showHelpButton = Button(end, text=self.resetButtonString, command=window.destroy)
        showHelpButton.grid(row=0, column=1, padx=padx, pady=pady)

        showHelpButton = Button(end, text=self.quitButtonString, command=window.destroy)
        showHelpButton.grid(row=0, column=2, padx=padx, pady=pady)

class SettingsEditor:
    # UI Elements
    resolutionButtonString = 'Set'
    saveButtonString       = 'Save'
    resetButtonString      = 'Reset'
    quitButtonString       = 'Quit'
    
    gameChapterText = ['Chapter 1', 'Chapter 2', 'Chapter 3', 'Chapter 4', 'Chapter 5']
    volumeText      = ['0', '1', '2', '3', '4']
    textSkipText    = ['Off', 'Single Box Skip', 'Full Auto-Skip']
    booleanText     = ['Off', 'On']
    textBoxText     = ['Off', 'Low', 'High']
    languageText    = ['Japanese', 'English', 'French', 'German', 'Korean', 'Chinese (Simplified)', 'Chinese (Traditional)']
    fullScreenText  = ['Windowed', 'Fullscreen']
    titleList       = [
        'Ace Attorney',
        'Justice For All',
        'Trials and Tribulations',
        'Background Music',
        'Sound Effects',
        'Text Skip',
        'Screen Shake',
        'Vibration',
        'Text Box Transparency',
        'Language',
        'Fullscreen (PC)',
        'Vertical Sync (PC)'
    ]
    resolutionText   = [
        'Resolution Width:',
        'Resolution Height:'
    ]

    # Savedata elements
    gameOneAddr          = 0x12C4
    gameTwoAddr          = 0x12C5
    gameThreeAddr        = 0x12C6
    backgroundMusicAddr  = 0x12C8
    soundEffectsAddr     = 0x12CA
    textSkipAddr         = 0x12CC
    screenShakeAddr      = 0x12CE
    vibrationAddr        = 0x12D0
    textBoxAddr          = 0x12D2
    languageAddr         = 0x12D4
    fullscreenAddr       = 0x12D6
    verticalSyncAddr     = 0x12E0
    resolutionWidthAddr  = 0x12D8
    resolutionHeightAddr = 0x12DC

    addressList = [
        gameOneAddr,
        gameTwoAddr,
        gameThreeAddr,
        backgroundMusicAddr,
        soundEffectsAddr,
        textSkipAddr,
        screenShakeAddr,
        vibrationAddr,
        textBoxAddr,
        languageAddr,
        fullscreenAddr,
        verticalSyncAddr
    ]
    elementCount = len(addressList)
    
    resolutionAddr = [
        resolutionWidthAddr,
        resolutionHeightAddr
    ]
    
    textList = [
        gameChapterText,
        gameChapterText[:-1],
        gameChapterText,
        volumeText,
        volumeText,
        textSkipText,
        booleanText,
        booleanText,
        textBoxText,
        languageText,
        fullScreenText,
        booleanText
    ]
    
    console      = 0
    comboState   = ['readonly', 'disabled']

    values              = []
    resolutionValue     = []
    
    comboBoxes          = []
    resolutionEntry     = []
    setResolutionButton = []

    def __init__(self, window, master, tab):
        self.master = master
        
        if self.getInfo() < 0:
            InvalidSaveFileError()
        else:
            self.createWindow(window, tab)

    def createWindow(self, window, tab):
        pady = 10
        padx = 20

        frame = Frame(tab)
        frame.grid(padx=padx, pady=pady)

        rowCount = int(self.elementCount / 4) + 1

        for y in range(0, rowCount):
            for x in range(0,4):
                try:
                    i = x+y*4
                    
                    titleLabel = Label(frame, text=self.titleList[i])
                    titleLabel.grid(row=y*2, column=x, padx=padx, pady=pady)

                    state = self.comboState[0]
                    if self.addressList[i] == self.fullscreenAddr or self.addressList[i] == self.verticalSyncAddr:
                        state = self.comboState[self.console]
                    
                    textList = self.textList[i]
                    comboBox = Combobox(frame, values=textList, state=state)
                    comboBox.set(textList[self.values[i]])
                    comboBox.grid(row=(y*2)+1, column=x, padx=padx)
                    self.comboBoxes.append(comboBox)
                except:
                    continue
                    
        if self.console == 0:
            resolutionFrame = Frame(tab)
            resolutionFrame.grid(padx=padx, pady=pady)

            # Resolution
            for i in range(0,2):
                label = Label(resolutionFrame, text=self.resolutionText[i])
                label.grid(row=0, column=i*3, padx=10)

                entry = Entry(resolutionFrame)
                entry.grid(row=0, column=(i*3)+1, padx=10)
                entry.insert(0, self.resolutionValue[i])
                self.resolutionEntry.append(entry)

            button = Button(resolutionFrame, text=self.resolutionButtonString, command=lambda: self.setResolution(0))
            button.grid(row=0, column=(0*3)+2, padx=5)
            self.setResolutionButton.append(button)

            button = Button(resolutionFrame, text=self.resolutionButtonString, command=lambda: self.setResolution(1))
            button.grid(row=0, column=(1*3)+2, padx=5)
            self.setResolutionButton.append(button)

        end = Frame(tab)
        end.grid(padx=padx)
        pady += 10

        showHelpButton = Button(end, text=self.saveButtonString, command=self.saveChanges)
        showHelpButton.grid(row=0, column=0, padx=padx, pady=pady)

        showHelpButton = Button(end, text=self.resetButtonString, command=self.resetInfo)
        showHelpButton.grid(row=0, column=1, padx=padx, pady=pady)

        showHelpButton = Button(end, text=self.quitButtonString, command=window.destroy)
        showHelpButton.grid(row=0, column=2, padx=padx, pady=pady)

    def resetInfo(self):
        for i in range(0, self.elementCount):
            self.comboBoxes[i].set(self.textList[i][self.values[i]])

        for i in range(0,2):
            self.resolutionEntry[i].delete(0, END)
            self.resolutionEntry[i].insert(0, self.resolutionValue[i])

    def setResolution(self, d): # d is dimension
        ratio = []

        if d == 0: # If we are setting width
            ratio.append(16)
            ratio.append(9)
            o = 1

        if d == 1: # If we are setting height
            ratio.append(9)
            ratio.append(16)
            o = 0

        # dRes = dimension res, the resolution of the dimension specified
        dRes = int(self.resolutionEntry[d].get())       # Grab resolution entered in box
        dRes = ratio[0] * round(dRes / ratio[0])        # Rounds to nearest 16:9 aspect ratio
        self.resolutionEntry[d].delete(0, END)          # Delete value previously in box
        self.resolutionEntry[d].insert(0, str(dRes))    # Enter new one
        self.resolutionValue[d] = dRes

        # oRes = other res, the resolution of the other dimension
        oRes = dRes / ratio[0]
        oRes = oRes * ratio[1]                          # Rounds to nearest 16:9 aspect ratio
        oRes = int(oRes)                                # Must be whole number
        self.resolutionEntry[o].delete(0, END)          # Delete value previously in box
        self.resolutionEntry[o].insert(0, str(oRes))    # Enter new one
        self.resolutionValue[o] = oRes

    def getInfo(self):
        for i in range (0,self.elementCount):
            v = self.master.readBin(self.addressList[i], 1)
            v = int.from_bytes(v, byteorder='big')

            if i < 3:
                v /= 16         # Chapters are unlocked when the value is increased by 0x10, which is 16 in decimal
                v = int(v)      # Ensure that v is a whole number
            if i < 5:
                v -= 1          # Chapters and volume are stored as starting at 1; We need to change this as arrays start at 0

            self.values.append(v)

        # Resolution
        for d in range (0,2):                       # d is dimension
            addr = self.resolutionAddr[d]           # Grab the address at which the resolution is stored
            byteList = self.master.readBin(addr, 2) # Resolution is stored as a 16-bit integer, so it has a length of 2 bytes
            byteList = [byteList[1], byteList[0]]   # Bytes are flipped in the savedata for some reason
            resolution = int.from_bytes(byteList, byteorder='big')
            self.resolutionValue.append(resolution)
            
        # Disable boxes if not a PC save
        if self.resolutionValue[0] == 0:
            self.console = 1
        
        return 1

    def saveChanges(self):
        # Grab values from tkinter comboboxes
        for element in range(0,self.elementCount):
            settingCount = len(self.textList[element])
            for setting in range(0,settingCount):
                if self.comboBoxes[element].get() == self.textList[element][setting]:
                    self.values[element] = setting
            
        # Convert data to hexadecimal to put back into the save file
        for i in range(0,self.elementCount):
            v = self.values[i]
            if i < 5:       # Chapters and volume start at 01, rather than 00
                v += 1      # To make this work with our arrays, we'll subtract 1 so they start at 00
            if i < 3:
                v *= 16
                
            self.master.writeBin(self.addressList[i], bytes([v]))

        for d in range(0,2):                            # d for dimension
            res = self.resolutionValue[d]               # Don't need to grab it from the UI because the 'Set' button handles that for us
            byteList = res.to_bytes(2, byteorder='big') # Convert 16-bit integer to 2 bytes
            byteList = [byteList[1], byteList[0]]       # Byte flip time!
            for i in range(0,2):
                byte = bytes([byteList[i]])
                address = self.resolutionAddr[d]        # Grab the address
                address = address + i                   # Since we're writing two bytes we need two addresses
                self.master.writeBin(address, byte)

class FilenameWarning:
    titleString  = 'Warning'
    errorString  = 'Save files are usually named "systemdata". Please ensure you have selected the right file before proceeding.'
    buttonString = 'OK'
    
    def __init__(self):
        filenameTk = Tk()
        filenameTk.title(self.titleString)
        filenameTkWindow = self.createWindow(filenameTk)

    def createWindow(self, master):
        frame = Frame(master)
        frame.grid(padx=20, pady=10)

        introLabel = Label(frame, text=self.errorString, anchor=E, justify=LEFT, wraplength=400)
        introLabel.grid(row=1, column=0, sticky='W')

        end = Frame(master)
        end.grid(padx=20, column=0)

        showHelpButton = Button(end, text=self.buttonString, command=master.destroy)
        showHelpButton.grid(row=0, column=1, padx=10, pady=10)
        
class InvalidSaveFileError:
    titleString  = 'Error'
    errorString  = 'Not a valid save file!'
    buttonString = 'OK'

    def __init__(self):
        invalidSaveFileErrorTk = Tk()
        invalidSaveFileErrorTk.title(self.titleString)
        invalidSaveFileErrorTkWindow = self.createWindow(invalidSaveFileErrorTk)

    def createWindow(self, master):
        frame = Frame(master)
        frame.grid(padx=20, pady=20)

        introLabel = Label(frame, text=self.errorString, anchor=E, justify=LEFT, wraplength=400)
        introLabel.grid(row=1, column=0, sticky='W')

        end = Frame(master)
        end.grid(padx=20, column=0)

        showHelpButton = Button(end, text=self.buttonString, command=master.destroy)
        showHelpButton.grid(row=0, column=1, padx=10, pady=10)

class AboutWindow:
    titleString = 'About PWAATeditor'
    windowStrings = [
        'This tool was developed by emiyl and works for the Phoenix Wright Ace Attorney Trilogy.',
        'The save editor has been tested for PC and Nintendo Switch. If you want, you can try to use it on other consoles and send me the results.',
        'Always make a backup before editing your save! I am not responsible for any lost progress.',
        'Thank you to summertriangle-dev and Amy While for helping me with the project.',
    ]
    buttonString = 'OK'
        
    def __init__(self):
        aboutTk = Tk()
        aboutTk.title(self.titleString)
        aboutTkWin = self.createWindow(aboutTk)

    def createWindow(self, master):
        frame = Frame(master)
        frame.grid(padx=20, pady=10)

        for i in range(0,4):
            label = Label(frame, text=self.windowStrings[i], anchor=E, justify=LEFT, wraplength=400)
            label.grid(row=i, column=0, sticky='W')

        end = Frame(master)
        end.grid(padx=20, column=0)

        showHelpButton = Button(end, text=self.buttonString, command=master.destroy)
        showHelpButton.grid(row=0, column=1, padx=10, pady=10)

app = App()


