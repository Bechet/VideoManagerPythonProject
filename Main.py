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
        self.checkButtonOnlyGenerateSubFileValue = BooleanVar()
        self.checkButtonOnlyGenerateSubFileValue.set(Constant.defaultOnlyGenerateSubFile)
        checkButtonOnlyGenerateSubFile=ttk.Checkbutton(self.root, text="Only generate sub note files ?", var=self.checkButtonOnlyGenerateSubFileValue)
        self.checkButtonUseGeneratedSubFileValue = BooleanVar()
        self.checkButtonUseGeneratedSubFileValue.set(Constant.defaultUseGeneratedSubFile)
        checkButtonUseGeneratedSubFile=ttk.Checkbutton(self.root, text="Use generated sub note files ?", var=self.checkButtonUseGeneratedSubFileValue)
        
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
        
        rowIndex = rowIndex + 1 
        checkButtonOnlyGenerateSubFile.grid(column=0, row=rowIndex)
        
        rowIndex = rowIndex + 1 
        checkButtonUseGeneratedSubFile.grid(column=0, row=rowIndex)
        
        #rowIndex = rowIndex + 1 
        #testButton.grid(row=rowIndex)
        
        self.root.mainloop()
    
    def run(self):
        print("executing")
        selectedInstrumentFolderName = self.comboboxSelectedInstrument.get()
        outputFolderName = self.entryVideoOutputFolderName.get().split(".")[0]
        print(outputFolderName)
        print("Selected Instrument folder:" + selectedInstrumentFolderName)
        self.root.destroy()
        videoManager = VideoManager(selectedInstrumentFolderName, self.checkButtonConcatValue.get(), self.checkButtonOnlyGenerateSubFileValue.get(), self.checkButtonUseGeneratedSubFileValue.get(), outputFolderName)
        videoManager.extecute()   
        del videoManager
        gc.collect()
                   
    def generateScript(self):
        midiManager = MidiManager(self.comboboxSelectedMidi.get())
        midiManager.saveScriptIntoFile()
        
    def test(self):
        listt = []
        listt.append(1)
        listt.append(2)
        listt.append(3)
        listt.append(4)
        print(listt[0])
        
        
myinstance = Main()
