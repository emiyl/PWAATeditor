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
version = '0.2.0'
title = 'PWAATeditor v' + version

class App:
    def __init__(self, master):
        titleLabel = Label(text=title)
        titleLabel.grid(pady=10)

        frame = Frame(master)
        frame.grid(padx=20, column=0)

        inputLabel = Label(frame, text='Save:')
        inputLabel.grid(row=1, column=0, padx=10)
        self.inputEntry = Entry(frame)
        self.inputEntry.grid(row=1, column=1, columnspan=2)
        getSaveButton = Button(frame, text='...', command=self.getSaveFile)
        getSaveButton.grid(row=1, column=3, padx=5)

        end = Frame(master)
        end.grid(padx=20, column=0)

        openSaveButton = Button(end, text='Open', command=self.openSavePath)
        openSaveButton.grid(row=0, column=0, pady=10, padx=10)

        showHelpButton = Button(end, text='About', command=self.showAbout)
        showHelpButton.grid(row=0, column=1, padx=10)

        quitButton = Button(end, text='Quit', command=root.quit)
        quitButton.grid(row=0, column=2, padx=10)

        authorLabel = Label(text='This is experimental software! Always make a backup.')
        authorLabel.grid(pady=(0, 10))

        authorLabel = Label(text='written by emiyl')
        authorLabel.grid(pady=(0, 10))

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

    def __init__(self, path):
        self.path = path
        with open(self.path, 'rb') as f:
            self.binData = f.read()
        self.createWindow()

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

    def createWindow(self):
        EditorGUI(self)

class EditorGUI:
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

    titleList = ['Ace Attorney', 'Justice For All', 'Trials and Tribulations', 'Background Music', 'Sound Effects', 'Text Skip', 'Screen Shake', 'Vibration', 'Text Box Transparency', 'Language', 'Fullscreen (PC)', 'Vertical Sync (PC)']
    addressList = [gameOneAddress, gameTwoAddress, gameThreeAddress, backgroundMusicVolumeAddress, soundEffectsVolumeAddress, textSkipAddress, screenShakeAddress, vibrationAddress, textBoxTransparencyAddress, languageAddress, fullscreenAddress, verticalSyncAddress]
    textList = [chapterList, chapterList, chapterList, backgroundMusicVolumeText, SoundEffectsVolumeText, textSkipText, screenShakeText, vibrationText, textBoxTransparencyText, languageText, fullScreenText, verticalSyncText]

    values = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    elementCount = len(addressList)

    hexValues = []
    comboBoxes = []

    # Separate to other settings
    resolutionWidthAddress   = ['12D8', '12D9']
    resolutionHeightAddress  = ['12DC', '12DD']
    resolutionAddress        = [resolutionWidthAddress, resolutionHeightAddress]

    resolutionWidthText      = 'Resolution Width:'
    resolutionHeightText     = 'Resolution Height:'
    resolutionText           = [resolutionWidthText, resolutionHeightText]

    resolutionWidthValue     = 1280
    resolutionHeightValue    = 720
    resolutionValue          = [resolutionWidthValue, resolutionHeightValue]

    resolutionHexValue       = []
    resolutionEntry          = []
    setResolutionButton      = []

    def __init__(self, master):
        self.master = master
        if self.getInfo() < 0:
            InvalidSaveFileError()
        else:
            editorGUITk = Tk()
            editorGUITk.title('Save Editor')
            editorGUITkWindow = self.createWindow(editorGUITk)

    def createWindow(self, master):
        pady = 10
        padx = 20

        frame = Frame(master)
        frame.grid(padx=padx, pady=pady)

        rowCount = int(self.elementCount / 4) + 1

        for y in range(0, rowCount):
            for x in range(0,4):
                try:
                    titleLabel = Label(frame, text=self.titleList[x+y*4])
                    titleLabel.grid(row=y*2, column=x, padx=padx, pady=pady)

                    textList = self.textList[x+y*4]
                    comboBox = Combobox(frame, values = textList)
                    comboBox.set(textList[self.values[x+y*4]])
                    comboBox.grid(row=(y*2)+1, column=x, padx=padx)
                    self.comboBoxes.append(comboBox)
                except:
                    continue

        resolutionFrame = Frame(master)
        resolutionFrame.grid(padx=padx, pady=pady)

        # Resolution
        for i in range(0,2):
            label = Label(resolutionFrame, text=self.resolutionText[i])
            label.grid(row=0, column=i*3, padx=10)

            entry = Entry(resolutionFrame)
            entry.grid(row=0, column=(i*3)+1, padx=10)
            entry.insert(0, self.resolutionValue[i])
            self.resolutionEntry.append(entry)

        button = Button(resolutionFrame, text='Set', command=lambda: self.setResolution(0))
        button.grid(row=0, column=(0*3)+2, padx=5)
        self.setResolutionButton.append(button)

        button = Button(resolutionFrame, text='Set', command=lambda: self.setResolution(1))
        button.grid(row=0, column=(1*3)+2, padx=5)
        self.setResolutionButton.append(button)

        end = Frame(master)
        end.grid(padx=padx)
        pady += 10

        showHelpButton = Button(end, text='Save', command=self.saveChanges)
        showHelpButton.grid(row=0, column=0, padx=padx, pady=pady)

        showHelpButton = Button(end, text='Reset', command=self.resetInfo)
        showHelpButton.grid(row=0, column=1, padx=padx, pady=pady)

        showHelpButton = Button(end, text='Quit', command=master.destroy)
        showHelpButton.grid(row=0, column=2, padx=padx, pady=pady)

    def resetInfo(self):
        for i in range(0, self.elementCount):
            self.comboBoxes[i].set(self.textList[i][self.values[i]])

        for i in range(0,2):
            self.resolutionEntry[i].delete(0, END)
            self.resolutionEntry[i].insert(0, self.resolutionValue[i])

    def setResolution(self, d): # d is dimension
        ratio = []

        if d == 0:
            ratio.append(16)
            ratio.append(9)
            o = 1

        if d == 1:
            ratio.append(9)
            ratio.append(16)
            o = 0

        # dres = dimension res, the resolution of the dimension specified
        dres = int(self.resolutionEntry[d].get())
        dres = ratio[0] * round(dres / ratio[0])
        self.resolutionEntry[d].delete(0, END)
        self.resolutionEntry[d].insert(0, str(dres))

        # ores = other res, the resolution of the other dimension
        ores = str(int((dres / ratio[0]) * ratio[1]))
        self.resolutionEntry[o].delete(0, END)
        self.resolutionEntry[o].insert(0, ores)

    def getInfo(self):
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

            # Resolution
            for dimension in range (0,2):
                hexValList = []
                for i in range (0,2):
                    decVal = self.master.readBin(self.resolutionAddress[dimension][i])
                    hexVal = str(hex(decVal)[2:])
                    if len(hexVal) < 2:
                        hexVal = '0' + hexVal
                    hexValList.append(hexVal)
                self.resolutionHexValue.append(hexValList[1] + hexValList[0])

            self.resolutionValue[0] = int(self.resolutionHexValue[0], 16)
            self.resolutionValue[1] = int(self.resolutionHexValue[1], 16)

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

        for d in range(0,2):
            self.resolutionValue[d] = int(self.resolutionEntry[d].get())

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

        # Resolution
        for d in range(0,2):
            res = self.resolutionValue[d]
            res = hex(res)[2:]
            while len(res) < 4:
                res = '0' + res
            bytes = [res[2:], res[:2]]
            for i in range(0,2):
                self.master.writeBin(self.resolutionAddress[d][i], bytes[i])

class FilenameWarning:
    def __init__(self):
        filenameTk = Tk()
        filenameTk.title('Warning')
        filenameTkWindow = self.createWindow(filenameTk)

    def createWindow(self, master):
        frame = Frame(master)
        frame.grid(padx=20, pady=10)

        introLabel = Label(frame, text='Save files are usually named "systemdata". Please ensure you have selected the right file before proceeding.', anchor=E, justify=LEFT, wraplength=400)
        introLabel.grid(row=1, column=0, sticky='W')

        end = Frame(master)
        end.grid(padx=20, column=0)

        showHelpButton = Button(end, text='OK', command=master.destroy)
        showHelpButton.grid(row=0, column=1, padx=10, pady=10)

class NoFileError:
    def __init__(self):
        noFileErrorTk = Tk()
        noFileErrorTk.title('Error')
        noFileErrorTkWindow = self.createWindow(noFileErrorTk)

    def createWindow(self, master):
        frame = Frame(master)
        frame.grid(padx=20, pady=20)

        introLabel = Label(frame, text='You must select a save file first!', anchor=E, justify=LEFT, wraplength=400)
        introLabel.grid(row=1, column=0, sticky='W')

        end = Frame(master)
        end.grid(padx=20, column=0)

        showHelpButton = Button(end, text='OK', command=master.destroy)
        showHelpButton.grid(row=0, column=1, padx=10, pady=10)

class InvalidSaveFileError:
    def __init__(self):
        invalidSaveFileErrorTk = Tk()
        invalidSaveFileErrorTk.title('Error')
        invalidSaveFileErrorTkWindow = self.createWindow(invalidSaveFileErrorTk)

    def createWindow(self, master):
        frame = Frame(master)
        frame.grid(padx=20, pady=20)

        introLabel = Label(frame, text='Not a valid save file!', anchor=E, justify=LEFT, wraplength=400)
        introLabel.grid(row=1, column=0, sticky='W')

        end = Frame(master)
        end.grid(padx=20, column=0)

        showHelpButton = Button(end, text='OK', command=master.destroy)
        showHelpButton.grid(row=0, column=1, padx=10, pady=10)

class AboutWindow:
    def __init__(self):
        aboutTk = Tk()
        aboutTk.title('About PWAATeditor')
        aboutTkWin = self.createWindow(aboutTk)

    def createWindow(self, master):
        frame = Frame(master)
        frame.grid(padx=20, pady=10)

        label = Label(frame, text='This tool was developed by emiyl and works for the Phoenix Wright Ace Attorney Trilogy.', anchor=E, justify=LEFT, wraplength=400)
        label.grid(row=1, column=0, sticky='W')

        label = Label(frame, text='The editor has been tested for PC and Nintendo Switch. If you want, you can try to use it on other consoles and send me the results.', anchor=E, justify=LEFT, wraplength=400)
        label.grid(row=2, column=0, sticky='W')

        label = Label(frame, text='Always make a backup before editing your save! I am not responsible for any lost progress.', anchor=E, justify=LEFT, wraplength=400)
        label.grid(row=3, column=0, sticky='W')

        label = Label(frame, text='Thank you to summertriangle-dev and Amy While for helping me with the project.', anchor=E, justify=LEFT, wraplength=400)
        label.grid(row=4, column=0, sticky='W')

        end = Frame(master)
        end.grid(padx=20, column=0)

        showHelpButton = Button(end, text='OK', command=master.destroy)
        showHelpButton.grid(row=0, column=1, padx=10, pady=10)

app = App(root)
root.title(title)
root.mainloop()
