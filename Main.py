from VideoManager import VideoManager
from functools import partial
from tkinter import Tk, Label, Entry, Button

class Main():
    def __init__(self, ):
#        self.videoManager = VideoManager()
        self.initIHM()
        
    def initIHM(self):
        root = Tk()
        labelVideoFolderPath = Label(root, text='Video Folder Path: (ex: D:/folderName/) (default: ./Input/)')
        labelVideoOutput = Label(root, text='Video Output File (Path+) Name: ')
        labelScriptFilePath = Label(root, text='Script File Path: (default: ./Script/script.txt)')
        self.entryVideoFolderPath = Entry(root)
        self.entryVideoOutput = Entry(root)
        self.entryScriptFilePath = Entry(root)
        executeButton = Button(root, text="execute", command=partial(self.run))
        labelVideoFolderPath.grid(column=0, row=0)
        labelVideoOutput.grid(column=0, row=1)
        labelScriptFilePath.grid(column=0, row=2)
        self.entryVideoFolderPath.grid(column=1, row=0)
        self.entryVideoOutput.grid(column=1, row=1)
        self.entryScriptFilePath.grid(column=1, row=2)
        executeButton.grid(column = 0, row = 3)
        root.mainloop()
    
    def run(self):
        print("executing")
        print(self.entryVideoFolderPath.get())
        print(self.entryVideoOutput.get())
        videoManager = VideoManager(self.entryVideoFolderPath.get(), self.entryVideoOutput.get(), self.entryScriptFilePath.get())
                           

myinstance = Main()
