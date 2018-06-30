# -*- coding: utf-8 -*-

from music21 import converter

class MidiManager():
    def __init__(self, _path, _generatedScriptName):
        self.hashMap = self.initHashMap()
        self.fileType = '.mid'
        if _path == '':
            self.path = "./Midi/midi.mid"
        else:
            if not _path.endswith(self.fileType):
                self.path = _path + self.fileType
        if _generatedScriptName =='':
            self.scriptPath = "./Script/script.txt"
        else:
            self.scriptPath = './Script/' + _generatedScriptName
            if not _generatedScriptName.endswith(".txt"):
                self.scriptPath = self.scriptPath + '.txt'
        self.streamScore=converter.parse(self.path)
        self.listOfNotesAndRests = self.getListOfNotesAndRests()
        
    def initHashMap(self):
        hashMap = {}
        print("Initializing mapper from file in path : ./Mapper/mapper.txt")
        file = open("./Mapper/mapper.txt", "r")
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
        if (self.hashMap.get(str(note.pitch))) is None:
            print("####### Careful #######")
            print("There is not file mapped with :" + str(note.pitch))
        if (note.isNote):
            return self.hashMap.get(str(note.pitch))
        else:   #Rest
            return "Rest"
    
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
        script = self.getScript()
        file = open(self.scriptPath, "w")
        file.write(script)
        print("Done")
        print("Script generated at: " + self.scriptPath)
        file.close()
