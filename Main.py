from VideoManager import VideoManager
from functools import partial
from tkinter import Tk, Label, ttk, Button
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
        print("Memory check ", psutil.virtual_memory()[2])
        sys.exit(0)
        
    
    def initVariable(self):
        self.fileManager = FileManager()
        
    def initIHM(self):
        self.root = Tk()
        labelInstrument = Label(self.root, text='Instrument')
        self.comboboxSelectedInstrument= ttk.Combobox(self.root, values=self.fileManager.instrumentsFolderName)
        self.comboboxSelectedInstrument.current(0)
        executeButton = Button(self.root, text="execute", command=partial(self.run))
        generateScriptButton = Button(self.root, text="generateScript", command=partial(self.generateScript))
        testButton = Button(self.root, text="test", command=partial(self.test))
        
        labelInstrument.grid(column=0, row=0)
        self.comboboxSelectedInstrument.grid(column=1, row=0)
        generateScriptButton.grid(row=1)
        executeButton.grid(row = 2)
        testButton.grid(row=3)
        self.root.mainloop()
    
    def run(self):
        print("executing")
        selectedInstrumentFolderName = self.comboboxSelectedInstrument.get()
        print("Selected Instrument folder:" + selectedInstrumentFolderName)
        videoManager = VideoManager(selectedInstrumentFolderName)
        videoManager.extecute()   
        self.root.destroy()
        gc.collect()
        sys.exit(0)
        
                   
    def generateScript(self):
        midiManager = MidiManager()
        midiManager.saveScriptIntoFile()
        
    def test(self):
        for file_name in (os.listdir(Constant.output_tmp_folder_path_name)):
            print(file_name)
        
myinstance = Main()
