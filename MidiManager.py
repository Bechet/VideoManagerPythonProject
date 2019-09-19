# -*- coding: utf-8 -*-

from music21 import converter
import Constant

class MidiManager():
    def __init__(self):
        self.hashMap = self.initHashMap()
        self.streamScore=converter.parse(Constant.midi_path_name)
        self.listOfNotesAndRests = self.getListOfNotesAndRests()
        
    def initHashMap(self):
        hashMap = {}
        print("Initializing mapper from file in path :"+ Constant.mapper_file_path_name)
        file = open(Constant.mapper_file_path_name, "r")
        content = file.read().replace('\n','')
        splitContent = content.split(',')
        for noteSignAndTitle in splitContent:
            couple = noteSignAndTitle.split(':')
            hashMap[couple[0]] = couple[1]
            print("Mapping : " + couple[0] + "\twith " + couple[1])
        print("Initializing mapper ... Done")
        return hashMap
        
    def getListOfNotesAndRests(self):
        part = self.streamScore.parts[0]
        return [noteAndRest for noteAndRest in part.notesAndRests]
            
    def getFileNameFromNote(self, note):
        if not note.isNote:
            return "Rest"
        else:
            if (self.hashMap.get(str(note.pitch))) is None:
                print("####### Careful #######")
                print("There is not file mapped with :" + str(note.pitch))
            if (note.isNote):
                return self.hashMap.get(str(note.pitch))
    
    def getDurationFromNoteOrRest(self, note):
        return note.duration.quarterLength
    
    def getScriptFromNoteOrRest(self, note):
        return self.getFileNameFromNote(note) + '-' + str(self.getDurationFromNoteOrRest(note))
                
    def getScript(self):
        strRes = ''
        for i in range(len(self.listOfNotesAndRests)):
            strRes = strRes + str(self.getScriptFromNoteOrRest(self.listOfNotesAndRests[i]))
            if len(self.listOfNotesAndRests) > i+1:
                strRes = strRes + ','
        return strRes
    
    def saveScriptIntoFile(self):
        print("Saving script into file...")
        script = self.getScript()
        file = open(Constant.script_path_name, "w")
        file.write(script)
        print("Done")
        print("Script generated at: " + Constant.script_path_name)
        file.close()
