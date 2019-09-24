# -*- coding: utf-8 -*-

from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip
from ScriptManager import ScriptManager
import Constant
import os
import psutil
import gc

class VideoManager():
    def __init__(self, _selectedInstrumentFolder, _boolConcatAtEnd, _outputFolderName):
        print("VideoManager Created, extracting path information...")
        self.boolConcatAtEnd=_boolConcatAtEnd
        print("Concat at end: ", self.boolConcatAtEnd)
        self.outputFolderName = _outputFolderName
        print("outputFolderName: ", self.outputFolderName)
        self.selectedInstrumentFolder = _selectedInstrumentFolder
        self.tmpOutputFolderPath=Constant.output_video_folder_name+self.outputFolderName
    
    def extecute(self):
        print("Execution...")
        print("Generating tmp output folder in path: ", self.tmpOutputFolderPath)
        os.mkdir(self.tmpOutputFolderPath)
        print("Generating tmp output folder...ok")
        self.scriptManager = ScriptManager()
        print("Spliting into sub file... This could take couple minutes, take a coffee break ! =)")
        self.readAndSaveAllVideoBis()
        print("Spliting... ok")
        self.listSlicedVideos = []
        gc.collect()
        print("Concat at end: ", self.boolConcatAtEnd)
        if (self.boolConcatAtEnd): 
            for file_name in (os.listdir(self.tmpOutputFolderPath)):
                self.listSlicedVideos.append(VideoFileClip(self.tmpOutputFolderPath + "/" + file_name))
            if (len(self.listSlicedVideos) > 1):
                self.concatVideoAndSave(self.listSlicedVideos, self.tmpOutputFolderPath + "/" + Constant.output_file_name)
            del self.listSlicedVideos
            gc.collect()
        print("Execution success!")
        
    def readAndSaveLocallyAllVideo(self):
        print("Slicing input videos from script...")
        self.listSlicedVideos = []
        while self.scriptManager.getCurrentCoupleTitleAndDuration() is not None:
            title = self.scriptManager.getCurrentTitle()
            duration = self.scriptManager.getCurrentDuration()
            print("Adding video with title: " + str(title) + " for " + str(duration)+ " seconds")
            video = VideoFileClip(Constant.baseInputVideoFolderPath + self.selectedInstrumentFolder + "/" + title + Constant.mp4suffix).subclip(0, duration)
            self.listSlicedVideos.append(video)
            self.scriptManager.next()
        print("Slicing done")
        
    def readAndSaveAllVideoBis(self):
        hashmapFileName_File={}
        tmpFileConter=0
        noteCounter=1
        print("Slicing input videos from script...")
        self.listSlicedVideos = []
        print("Initial memory usage" + str(psutil.virtual_memory()))
        memoryLimit=psutil.virtual_memory()[2] + (Constant.max_memory_percentage-psutil.virtual_memory()[2])/2
        while self.scriptManager.getCurrentCoupleTitleAndDuration() is not None:
            print("")
            print("Dealing note number : ", noteCounter)
            title = self.scriptManager.getCurrentTitle()
            duration = self.scriptManager.getCurrentDuration()
            generatedFilePath=Constant.baseInputVideoFolderPath+ self.selectedInstrumentFolder + "/" + Constant.generated_sub_input_video_folder_name + "/" + title + "-" + str(duration) + Constant.mp4suffix
            print("Adding video with title: " + str(title) + " for " + str(duration)+ " seconds")
            
            if not os.path.exists(generatedFilePath):
                print("File not generated yet, generating into path :" + generatedFilePath)
                print("############################test#############################")
                print(duration-Constant.exceedTime)
                print("############################end#############################")
                video = VideoFileClip(Constant.baseInputVideoFolderPath + self.selectedInstrumentFolder + "/" + title + Constant.mp4suffix).subclip(0, duration-Constant.exceedTime)
                
                self.saveVideoIntoFile(video, generatedFilePath)
                print("End of generating file")
                self.listSlicedVideos.append(video)
                hashmapFileName_File[generatedFilePath]=video
            else:
                if hashmapFileName_File.__contains__(generatedFilePath):
                    self.listSlicedVideos.append(hashmapFileName_File[generatedFilePath])
                else:
                    video = VideoFileClip(generatedFilePath)
                    self.listSlicedVideos.append(video)
                    hashmapFileName_File[generatedFilePath]=video
            # Memory check
            if (psutil.virtual_memory()[2] > memoryLimit or len(self.listSlicedVideos) is Constant.split_length):
                print("Exceeding memory / split_length limit, saving into tmp video file")
                print("Memory limit, current memory:", psutil.virtual_memory()[2])
                tmpFilePath=self.tmpOutputFolderPath + "/" + Constant.defaultSubFilePrefix + str(tmpFileConter) + Constant.mp4suffix
                tmpFileConter = tmpFileConter + 1
                print("Saving sub video in tmp folder, path: ", tmpFilePath)
                self.concatVideoAndSave(self.listSlicedVideos, tmpFilePath)
                self.listSlicedVideos=[]
                gc.collect()
            self.scriptManager.next()
            print("Current memory usage percentage: ", psutil.virtual_memory()[2])
            noteCounter = noteCounter + 1

        if len(self.listSlicedVideos) > 0:
            if len(self.listSlicedVideos) == 1:
                self.saveVideoIntoFile(self.listSlicedVideos[0], self.tmpOutputFolderPath + "/" + Constant.defaultSubFilePrefix + str(tmpFileConter) + Constant.mp4suffix)
            else:
                self.concatVideoAndSave(self.listSlicedVideos, self.tmpOutputFolderPath + "/" + Constant.defaultSubFilePrefix + str(tmpFileConter) + Constant.mp4suffix)    
            for video in self.listSlicedVideos:
                video.close()
        #close all
        for key in hashmapFileName_File:
            hashmapFileName_File[key].close()
        hashmapFileName_File={}
        gc.collect()
        
    def concatVideo(self, listSlicedVideos):
        print("Concatenating sliced videos...")
        return concatenate_videoclips(listSlicedVideos)
    
    def concatVideoAndSave(self, listSlicedVideos, path):
        print("Concatenating sliced videos...")
        concatenatedVideo=concatenate_videoclips(listSlicedVideos)
        print("Saving...")
        self.saveVideoIntoFile(concatenatedVideo, path)
        concatenatedVideo.close()
        del concatenatedVideo
        gc.collect()
        
    def saveVideoIntoFile(self, video, path):
        print(video)
        print(path)
        video.write_videofile(path, codec=Constant.codec)