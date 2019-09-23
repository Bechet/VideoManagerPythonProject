from VideoManager import VideoManager
from functools import partial
from tkinter import Tk, Label, ttk, Button, BooleanVar, Entry
from MidiManager import MidiManager
from FileManager import FileManager
import gc, sys
import psutil
import Constant
import os

class Main():
    def __init__(self, ):
        print("Init main")
        self.initVariable()
        self.initIHM()
        print("Memory check ", psutil.virtual_memory())
        gc.collect()
        
    
    def initVariable(self):
        self.fileManager = FileManager()
        
    def initIHM(self):
        self.root = Tk()
        
        labelInstrument = Label(self.root, text='Instrument; ')
        labelMidi = Label(self.root, text='Midi file: ')
        labelVideoOutputFolderName=Label(self.root, text="OutputFolderName: ")
        self.comboboxSelectedInstrument= ttk.Combobox(self.root, values=self.fileManager.instrumentsFolderName)
        self.comboboxSelectedMidi= ttk.Combobox(self.root, values=self.fileManager.midiFileName)
        executeButton = Button(self.root, text="execute", command=partial(self.run))
        generateScriptButton = Button(self.root, text="generateScript", command=partial(self.generateScript))
        testButton = Button(self.root, text="test", command=partial(self.test))
        self.checkButtonConcatValue = BooleanVar()
        self.checkButtonConcatValue.set(Constant.defaultConcatAtEnd)
        checkButtonConcat=ttk.Checkbutton(self.root, text="Concatenate at end ?", var=self.checkButtonConcatValue)
        self.entryVideoOutputFolderName=Entry(self.root)
        
        rowIndex = 0
        
        self.comboboxSelectedInstrument.current(0)
        self.comboboxSelectedMidi.current(0) 
        
        labelInstrument.grid(column=0, row=rowIndex)
        self.comboboxSelectedInstrument.grid(column=1, row=rowIndex)
        
        rowIndex = rowIndex + 1 
        
        labelMidi.grid(column=0, row=1)
        self.comboboxSelectedMidi.grid(column=1, row=rowIndex)
        
        rowIndex = rowIndex + 1 
        
        labelVideoOutputFolderName.grid(column=0, row=rowIndex)
        self.entryVideoOutputFolderName.grid(column=1, row=rowIndex)
        
        rowIndex = rowIndex + 1 
        
        generateScriptButton.grid(column=0, row=rowIndex)
        executeButton.grid(column=1, row=rowIndex)
        
        rowIndex = rowIndex + 1 
        
        checkButtonConcat.grid(column=0, row=rowIndex)
        #testButton.grid(row=4)
        
        self.root.mainloop()
    
    def run(self):
        print("executing")
        selectedInstrumentFolderName = self.comboboxSelectedInstrument.get()
        outputFolderName = self.entryVideoOutputFolderName.get().split(".")[0]
        print(outputFolderName)
        print("Selected Instrument folder:" + selectedInstrumentFolderName)
        self.root.destroy()
        videoManager = VideoManager(selectedInstrumentFolderName, self.checkButtonConcatValue.get(), outputFolderName)
        videoManager.extecute()   
        del videoManager
        gc.collect()
                   
    def generateScript(self):
        midiManager = MidiManager(self.comboboxSelectedMidi.get())
        midiManager.saveScriptIntoFile()
        
    def test(self):
        for file_name in (os.listdir(Constant.output_tmp_folder_path_name)):
            print(file_name)
        test = {}
        test["test"]="test"
        test["test2"]="test2"
        print(test)
        
myinstance = Main()
