from VideoManager import VideoManager
from functools import partial
from tkinter import Tk, Label, Entry, Button
from MidiManager import MidiManager

class Main():
    def __init__(self, ):
        print("Init main")
        self.initIHM()
        
    def initIHM(self):
        root = Tk()
        labelVideoFolderPath = Label(root, text='Video Folder Path: (ex: D:/folderName/) (default: ./Input/)')
        labelVideoOutput = Label(root, text='Video Output File (Path+) Name: ')
        labelScriptFilePath = Label(root, text='Script File Path: (default: ./Script/script.txt)')
        labelMidiFilePath = Label(root, text="MidiFilePath: (ex: ./Midi/midiFile) (defalt: ./Midi/midi.mid)")
        labelGeneratedScriptName = Label(root, text="Script generated Name: (ex: Script123) (default: ./Script/script.txt)")
        self.entryVideoFolderPath = Entry(root)
        self.entryVideoOutput = Entry(root)
        self.entryScriptFilePath = Entry(root)
        self.entryMidiFilePath = Entry(root)
        self.entryGeneratedScriptName= Entry(root)
        executeButton = Button(root, text="execute", command=partial(self.run))
        generateScriptButton = Button(root, text="generateScript", command=partial(self.generateScript))
        labelVideoFolderPath.grid(column=0, row=0)
        labelVideoOutput.grid(column=0, row=1)
        labelScriptFilePath.grid(column=0, row=2)
        self.entryVideoFolderPath.grid(column=1, row=0)
        self.entryVideoOutput.grid(column=1, row=1)
        self.entryScriptFilePath.grid(column=1, row=2)
        executeButton.grid(row = 3)
        labelMidiFilePath.grid(column = 0, row = 4)
        self.entryMidiFilePath.grid(column=1, row=4)
        labelGeneratedScriptName.grid(column = 0, row=5)
        self.entryGeneratedScriptName.grid(column=1, row=5)
        generateScriptButton.grid(row=6)
        root.mainloop()
    
    def run(self):
        print("executing")
        print(self.entryVideoFolderPath.get())
        print(self.entryVideoOutput.get())
        videoManager = VideoManager(self.entryVideoFolderPath.get(), self.entryVideoOutput.get(), self.entryScriptFilePath.get())
                           
    def generateScript(self):
        print("generating Script from midi file: " + self.entryMidiFilePath.get())
        midiManager = MidiManager(self.entryMidiFilePath.get(), self.entryGeneratedScriptName.get())
        midiManager.saveScriptIntoFile()

myinstance = Main()
