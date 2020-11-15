from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import platform

if platform.system() == 'Windows':
    from tkinter.ttk import *
else:
    from tkinter.ttk import Notebook
    from tkinter.ttk import Combobox

root = Tk()
version = '0.1.1'
title = 'PWAATeditor v' + version
    
    
class App:
    def __init__(self, master):
        self.titleLabel = Label(text=title)
        self.titleLabel.grid(pady=10)

        frame = Frame(master)
        frame.grid(padx=20, column=0)
        
        self.inputLabel = Label(frame, text='Save:')
        self.inputLabel.grid(row=1, column=0, padx=10)
        self.inputEntry = Entry(frame)
        self.inputEntry.grid(row=1, column=1, columnspan=2)
        self.getSaveButton = Button(frame, text='...', command=self.getSaveFile)
        self.getSaveButton.grid(row=1, column=3, padx=5)
        
        end = Frame(master)
        end.grid(padx=20, column=0)

        self.openSaveButton = Button(end, text='Open', command=self.openSavePath)
        self.openSaveButton.grid(row=0, column=0, pady=10, padx=10)

        self.showHelpButton = Button(end, text='About', command=self.showAbout)
        self.showHelpButton.grid(row=0, column=1, padx=10)

        self.quitButton = Button(end, text='Quit', command=root.quit)
        self.quitButton.grid(row=0, column=2, padx=10)
       
        self.authorLabel = Label(text='This is experimental software! Always make a backup.')
        self.authorLabel.grid(pady=(0, 10))
       
        self.authorLabel = Label(text='written by emiyl')
        self.authorLabel.grid(pady=(0, 10))
        
    def getSaveFile(self):
        savePath = filedialog.askopenfilename(initialdir='./', title='Select your save file')
        if not savePath:
            return
        filename = savePath[savePath.rfind('/') - len(savePath) + 1:]
        if filename != 'systemdata':
            FilenameWarning()
        self.inputEntry.delete(0, END)
        self.inputEntry.insert(0, savePath)
        
    def openSavePath(self):
        savePath = self.inputEntry.get()
        if not savePath:
            NoFileError()
            return
        OpenSave(savePath)
        
    def showAbout(self):
        AboutWindow()
        
        
class OpenSave:
    binData = 0
    path = ''

    def __init__(self, path):
        self.path = path
        
        with open(self.path, 'rb') as f:
            self.binData = f.read()
        openSaveTk = Tk()
        openSaveTk.title('Save File')
        openSaveTkTkWindow = self.createWindow(openSaveTk)
        
    def readBin(self, address):
        decimal = int(address, 16)
        hexa = self.binData[decimal]
        return hexa
        
    def writeBin(self, address, hexa):
        pos = int(address, 16)
        val = int(hexa, 16)
        val = bytes([val])
        
        with open(self.path, 'r+b') as f:
            f.seek(pos)
            f.write(val)
    
    def createWindow(self, master):
        tabParent = Notebook(master)
        tabSettings = Frame(tabParent)
        
        tabParent.add(tabSettings, text='Settings')
        tabParent.pack(expand=1, fill='both')
        
        SettingsTab(self, master, tabSettings)
    
class SettingsTab:
    gameOneAddress               = '12C4'
    gameTwoAddress               = '12C5'
    gameThreeAddress             = '12C6'
    backgroundMusicVolumeAddress = '12C8'
    soundEffectsVolumeAddress    = '12CA'
    textSkipAddress              = '12CC'
    screenShakeAddress           = '12CE'
    vibrationAddress             = '12D0'
    textBoxTransparencyAddress   = '12D2'
    languageAddress              = '12D4'
    fullscreenAddress            = '12D6'
    verticalSyncAddress          = '12E0'
    
    titleList = ['Ace Attorney', 'Justice For All', 'Trials and Tribulations', 'Background Music', 'Sound Effects', 'Text Skip', 'Screen Shake', 'Vibration', 'Text Box Transparency', 'Language', 'Fullscreen (PC)', 'Vertical Sync (PC)']
    chapterList = ['Chapter 1', 'Chapter 2', 'Chapter 3', 'Chapter 4', 'Chapter 5']
    backgroundMusicVolumeText = ['0', '1', '2', '3', '4']
    SoundEffectsVolumeText = ['0', '1', '2', '3', '4']
    textSkipText = ['Off', 'Single Box Skip', 'Full Auto-Skip']
    screenShakeText = ['Off', 'On']
    vibrationText = ['Off', 'On']
    textBoxTransparencyText = ['Off', 'Low', 'High']
    languageText = ['Japanese', 'English', 'French', 'German', 'Korean', 'Chinese (Simplified)', 'Chinese (Traditional)']
    fullScreenText = ['Windowed', 'Fullscreen']
    verticalSyncText = ['Off', 'On']
    
    addressList = [gameOneAddress, gameTwoAddress, gameThreeAddress, backgroundMusicVolumeAddress, soundEffectsVolumeAddress, textSkipAddress, screenShakeAddress, vibrationAddress, textBoxTransparencyAddress, languageAddress, fullscreenAddress, verticalSyncAddress]
    textList = [chapterList, chapterList, chapterList, backgroundMusicVolumeText, SoundEffectsVolumeText, textSkipText, screenShakeText, vibrationText, textBoxTransparencyText, languageText, fullScreenText, verticalSyncText]
    
    values = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    hexValues = []
    elementCount = len(addressList)
    comboBoxes = []
    master = ''
    
    def __init__(self, master, window, tab):
        self.master = master
        if self.getInfo() < 0:
            InvalidSaveFileError()
        else:
            self.createWindow(self, window, tab)
        
    def createWindow(self, master, window, tab):
        pady = 10
        padx = 20
        
        frame = Frame(tab)
        frame.grid(padx=padx, pady=pady)
        
        rowCount = int(self.elementCount / 4) + 1
        
        for y in range(0, rowCount):
            for x in range(0,4):
                try:
                    self.titleLabel = Label(frame, text=self.titleList[x+y*4])
                    self.titleLabel.grid(row=y*2, column=x, padx=padx, pady=pady)
                    
                    textList = self.textList[x+y*4]
                    comboBox = Combobox(frame, values = textList)
                    comboBox.set(textList[self.values[x+y*4]])
                    comboBox.grid(row=(y*2)+1, column=x, padx=padx)
                    self.comboBoxes.append(comboBox)
                except:
                    continue
        
        end = Frame(tab)
        end.grid(padx=padx)
        
        self.showHelpButton = Button(end, text='Save', command=lambda: self.saveChanges())
        self.showHelpButton.grid(row=0, column=0, padx=padx, pady=pady)
        
        self.showHelpButton = Button(end, text='Quit', command=window.destroy)
        self.showHelpButton.grid(row=0, column=1, padx=padx, pady=pady)
        
    def getInfo(self):
        self.hexValues = []
        
        try:
            # Grab hex values from save file
            for i in range (0,self.elementCount):
                decVal = self.master.readBin(self.addressList[i])
                hexVal = hex(decVal)[2:]
                self.hexValues.append(hexVal)
            
            # Chapters
            for i in range (0,3):
                self.values[i] = int(self.hexValues[i][:1]) - 1

            # Sound Volume
            for i in range (3,5):
                self.values[i] = int(self.hexValues[i]) - 1
            
            # Rest of the settings
            for i in range (5,self.elementCount):
                self.values[i] = int(self.hexValues[i])
                
            return 1
        except:
            return -1
        
    def saveChanges(self):
        # Grab hex values from tkinter comboboxes
        for element in range(0,self.elementCount):
            settingCount = len(self.textList[element])
            for setting in range(0,settingCount):
                if self.comboBoxes[element].get() == self.textList[element][setting]:
                    self.values[element] = setting
    
        # Chapters
        for i in range(0,3):
            hexa = str(self.values[i] + 1) + "0"
            self.hexValues[i] = hexa
        
        # Sound Volume
        for i in range(3,5):
            hexa = str(self.values[i] + 1)
            self.hexValues[i] = hexa
        
        # Rest of the settings
        for i in range(5,self.elementCount):
            hexa = str(self.values[i])
            self.hexValues[i] = hexa
        
        for i in range(0,self.elementCount):
            self.master.writeBin(self.addressList[i], self.hexValues[i])
                
class FilenameWarning:
    def __init__(self):
        filenameTk = Tk()
        filenameTk.title('Warning')
        filenameTkWindow = self.createWindow(filenameTk)
    
    def createWindow(self, master):
        frame = Frame(master)
        frame.grid(padx=20, pady=10)
       
        self.introLabel = Label(frame, text='Save files are usually named "systemdata". Please ensure you have selected the right file before proceeding.', anchor=E, justify=LEFT, wraplength=400)
        self.introLabel.grid(row=1, column=0, sticky='W')
        
        end = Frame(master)
        end.grid(padx=20, column=0)

        self.showHelpButton = Button(end, text='OK', command=master.destroy)
        self.showHelpButton.grid(row=0, column=1, padx=10, pady=10)
        
class NoFileError:
    def __init__(self):
        noFileErrorTk = Tk()
        noFileErrorTk.title('Error')
        noFileErrorTkWindow = self.createWindow(noFileErrorTk)
    
    def createWindow(self, master):
        frame = Frame(master)
        frame.grid(padx=20, pady=20)
       
        self.introLabel = Label(frame, text='You must select a save file first!', anchor=E, justify=LEFT, wraplength=400)
        self.introLabel.grid(row=1, column=0, sticky='W')
        
        end = Frame(master)
        end.grid(padx=20, column=0)

        self.showHelpButton = Button(end, text='OK', command=master.destroy)
        self.showHelpButton.grid(row=0, column=1, padx=10, pady=10)
        
class InvalidSaveFileError:
    def __init__(self):
        invalidSaveFileErrorTk = Tk()
        invalidSaveFileErrorTk.title('Error')
        invalidSaveFileErrorTkWindow = self.createWindow(invalidSaveFileErrorTk)
    
    def createWindow(self, master):
        frame = Frame(master)
        frame.grid(padx=20, pady=20)
       
        self.introLabel = Label(frame, text='Not a valid save file!', anchor=E, justify=LEFT, wraplength=400)
        self.introLabel.grid(row=1, column=0, sticky='W')
        
        end = Frame(master)
        end.grid(padx=20, column=0)

        self.showHelpButton = Button(end, text='OK', command=master.destroy)
        self.showHelpButton.grid(row=0, column=1, padx=10, pady=10)
        
class AboutWindow:
    def __init__(self):
        aboutTk = Tk()
        aboutTk.title('About PWAATeditor')
        aboutTkWin = self.createWindow(aboutTk)
    
    def createWindow(self, master):
        frame = Frame(master)
        frame.grid(padx=20, pady=10)
       
        self.label = Label(frame, text='This tool was developed by emiyl and works for the Phoenix Wright Ace Attorney Trilogy.', anchor=E, justify=LEFT, wraplength=400)
        self.label.grid(row=1, column=0, sticky='W')
        
        self.label = Label(frame, text='The editor has been tested for PC and Nintendo Switch. If you want, you can try to use it on other consoles and send me the results.', anchor=E, justify=LEFT, wraplength=400)
        self.label.grid(row=2, column=0, sticky='W')
        
        self.label = Label(frame, text='Always make a backup before editing your save! I am not responsible for any lost progress.', anchor=E, justify=LEFT, wraplength=400)
        self.label.grid(row=3, column=0, sticky='W')
        
        self.label = Label(frame, text='Thank you to summertriangle-dev and Amy While for helping me with the project.', anchor=E, justify=LEFT, wraplength=400)
        self.label.grid(row=4, column=0, sticky='W')
        
        end = Frame(master)
        end.grid(padx=20, column=0)

        self.showHelpButton = Button(end, text='OK', command=master.destroy)
        self.showHelpButton.grid(row=0, column=1, padx=10, pady=10)

app = App(root)
root.title(title)
root.mainloop()
