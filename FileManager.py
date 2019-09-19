# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 14:26:55 2019

@author: Leo
"""
import Constant
import os

class FileManager():
    def __init__(self):
        print("Init FileManager")
        self.instrumentsFolderName = []
        self.notesInstrumentFileName = {}
        self.generatedNotesInstrumentFileName = {}
        for instrument_folder_name in os.listdir(Constant.baseInputVideoFolderPath):
            print(instrument_folder_name)
            self.instrumentsFolderName.append(instrument_folder_name)
            self.notesInstrumentFileName[instrument_folder_name] = []
            for note_file_name in os.listdir(Constant.baseInputVideoFolderPath+instrument_folder_name):
                self.notesInstrumentFileName[instrument_folder_name].append(note_file_name)
                # Add generated sub input video folder if not exists
                generatedFolderPath=Constant.baseInputVideoFolderPath+instrument_folder_name + "/" + Constant.generated_sub_input_video_folder_name
                if not (os.path.exists(generatedFolderPath)):
                    os.mkdir(generatedFolderPath)
                else:
                    self.addGeneratedFileName(instrument_folder_name, generatedFolderPath)
        print(self.notesInstrumentFileName)
        print(self.generatedNotesInstrumentFileName)
        
    def addGeneratedFileName(self, instrumentFolderName, generatedFolderPath):
        tmpListFileName = []
        for fileName in os.listdir(generatedFolderPath):
            tmpListFileName.append(fileName)
        self.generatedNotesInstrumentFileName[instrumentFolderName] = tmpListFileName