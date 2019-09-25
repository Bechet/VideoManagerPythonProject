# -*- coding: utf-8 -*-
import Constant

class ScriptManager():
    def __init__(self):
        self.pointerIndex = 0
        self.scriptFileContent = self.getScript().rstrip()
        self.listOfTitleAndDuration = self.getListOfTitleAndDuration(self.scriptFileContent)
        
    def getScript(self):
        print("getting script")
        file = open(Constant.script_path_name,'r')
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
            return eval(self.listOfTitleAndDuration[self.pointerIndex][1])
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

    def reInitPointer(self):
        self.pointerIndex = 0