# -*- coding: utf-8 -*-

class ScriptManager():
    def __init__(self, scriptFilePath):
        self.pointerIndex = 0
        self.scriptFilePath = scriptFilePath
        self.scriptFileContent = self.getScript(self.scriptFilePath).rstrip()
        self.listOfTitleAndDuration = self.getListOfTitleAndDuration(self.scriptFileContent)
        
    def getScript(self, scriptFilePath):
        print("getting script")
        file = open(scriptFilePath,'r')
        return file.read()
    
    def getListOfTitleAndDuration(self, scriptFileContent):
        res = []
        listTitleAndDuration = scriptFileContent.split(',')
        for titleAndDuration in listTitleAndDuration:
            res.append(titleAndDuration.split('-'))
        return res
    
    def next(self):
        self.pointerIndex+=1
        
    def getCurrentTitle(self):
        if len(self.listOfTitleAndDuration) > self.pointerIndex:
            return self.listOfTitleAndDuration[self.pointerIndex][0]
        else:
            return None
        
    def getCurrentDuration(self):
        if len(self.listOfTitleAndDuration) > self.pointerIndex:
            return float(self.listOfTitleAndDuration[self.pointerIndex][1])
        else:
            return None
        
    def getCurrentCoupleTitleAndDuration(self):
        if len(self.listOfTitleAndDuration) > self.pointerIndex:
            return self.listOfTitleAndDuration[self.pointerIndex]
        else:
            return None
        
    def showCurrentCoupe(self):
        if len(self.listOfTitleAndDuration) > self.pointerIndex:
            print(self.listOfTitleAndDuration[self.pointerIndex])
        else:
            print('None')