# -*- coding: utf-8 -*-

from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip
from ScriptManager import ScriptManager
import Constant
import os
import psutil
import gc

class VideoManager():
    def __init__(self, _selectedInstrumentFolder, _boolConcatAtEnd, _boolOnlyGenerateSubFile, _boolUseGeneratedSubFile, _outputFolderName):
        print("VideoManager Created, extracting path information...")
        self.boolConcatAtEnd=_boolConcatAtEnd
        self.boolOnlyGenerateSubFile = _boolOnlyGenerateSubFile
        self.boolUseGeneratedSubFile = _boolUseGeneratedSubFile
        self.listDuration = []
        print("Concat at end: ", self.boolConcatAtEnd)
        self.outputFolderName = _outputFolderName
        print("outputFolderName: ", self.outputFolderName)
        self.selectedInstrumentFolder = _selectedInstrumentFolder
        self.tmpOutputFolderPath=Constant.output_video_folder_name+self.outputFolderName
    
    def extecute(self):
        print("Execution...")
        self.scriptManager = ScriptManager()
        
        print("Generating tmp output folder in path: ", self.tmpOutputFolderPath)
        os.mkdir(self.tmpOutputFolderPath)
        print("Generating tmp output folder...ok")
        
        print("Generating sub file...")
        self.checkAndGenerateSubVideoFile()
        print("Generating sub file... ok")
    
        if not (self.boolOnlyGenerateSubFile):
            print("Generating concatenated sub file...")
            self.readAndSaveAllVideoBis()
            print("Generating concatenated sub file...")
            self.listSlicedVideos = []
            gc.collect()
            print("Concat at end: ", self.boolConcatAtEnd)
            if (self.boolConcatAtEnd): 
                counter = 0
                for file_name in (os.listdir(self.tmpOutputFolderPath)):
                    duration = self.listDuration[counter]
                    video = VideoFileClip(self.tmpOutputFolderPath + "/" + file_name)
                    video = self.changeVideoSetting(video, duration, 60)
                    self.listSlicedVideos.append(video)
                    del video
                    counter = counter + 1
                if (len(self.listSlicedVideos) > 1):
                    self.concatVideoAndSave(self.listSlicedVideos, self.tmpOutputFolderPath + "/" + Constant.output_file_name)
                del self.listSlicedVideos
        gc.collect()
        print("Execution success!")
        
    def checkAndGenerateSubVideoFile(self):
        noteCounter=1
        self.scriptManager.reInitPointer()
        while self.scriptManager.getCurrentCoupleTitleAndDuration() is not None:
            print("")
            print("Dealing note number : ", noteCounter)
            title = self.scriptManager.getCurrentTitle()
            duration = self.scriptManager.getCurrentDuration()
            generatedFilePath=Constant.baseInputVideoFolderPath+ self.selectedInstrumentFolder + "/" + Constant.generated_sub_input_video_folder_name + "/" + title + "-" + str(duration) + Constant.mp4suffix
            print("Adding video with title: " + str(title) + " for " + str(duration)+ " seconds")
            if not os.path.exists(generatedFilePath):
                print("File not generated yet, generating into path :" + generatedFilePath)
                video = VideoFileClip(Constant.baseInputVideoFolderPath + self.selectedInstrumentFolder + "/" + title + Constant.mp4suffix)
                video = self.changeVideoSetting(video, duration, 60)
                self.saveVideoIntoFile(video, generatedFilePath)
                print("End of generating file")
                video.close()
                del video
                gc.collect()
            noteCounter = noteCounter + 1
            self.scriptManager.next()
        
    def readAndSaveAllVideoBis(self):
        self.scriptManager.reInitPointer()
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
            video = None
            if hashmapFileName_File.__contains__(generatedFilePath):
                video = hashmapFileName_File[generatedFilePath]
                video = self.changeVideoSetting(video, duration, 60)
            else:
                video = None
                if self.boolUseGeneratedSubFile:
                    video = VideoFileClip(generatedFilePath)
                    video = self.changeVideoSetting(video, duration, 60)
                else:
                    print("Not using generated sub file... spliting file...")
                    video = VideoFileClip(Constant.baseInputVideoFolderPath + self.selectedInstrumentFolder + "/" + title + Constant.mp4suffix)
                    video = self.changeVideoSetting(video, duration, 60)
                hashmapFileName_File[generatedFilePath]=video
            self.listSlicedVideos.append(video)
            del video
            gc.collect()

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
                memoryLimit=psutil.virtual_memory()[2] + (Constant.max_memory_percentage-psutil.virtual_memory()[2])/2
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
                del video
        self.listSlicedVideos = []
        #close all
        for key in hashmapFileName_File:
            print("Closing video: ", hashmapFileName_File[key])
            hashmapFileName_File[key].close()
            hashmapFileName_File[key] = None
        hashmapFileName_File={}
        del hashmapFileName_File
        gc.collect()
        
    def concatVideo(self, listSlicedVideos):
        print("Concatenating sliced videos...")
        return concatenate_videoclips(listSlicedVideos)
    
    def concatVideoAndSave(self, listSlicedVideos, path):
        print("Concatenating sliced videos...")
        duration = self.getDuration(listSlicedVideos)
        concatenatedVideo=concatenate_videoclips(listSlicedVideos)
        print(concatenatedVideo.duration)
        print("Saving...")
        self.saveVideoIntoFile(concatenatedVideo, path)
        self.listDuration.append(duration)
        concatenatedVideo.close()
        del concatenatedVideo
        gc.collect()
        
    def saveVideoIntoFile(self, video, path):
        video = video.subclip(0.0, video.duration - Constant.exceedTime)
        video.write_videofile(path, codec=Constant.codec, fps=60)
        
    def changeVideoSetting(self, video, duration, fps):
        nframes = int(duration)*60
        print("##############Before###############")
        print("duration", video.duration)
        print("frames:", (video.fps * video.duration))
        print("nbFrames:", video.reader.nframes)
        print("nbFrames:", video.reader.ffmpeg_duration)
        print("nbFrames:", video.reader.duration)
        print("nbFrames:", video.reader.fps)
        video = video.subclip(0.0, duration)
        video.duration=duration
        video.set_fps(fps)
        video.reader.duration=duration
        video.reader.ffmpeg_duration=duration
        video.reader.nframes=nframes
        video.reader.fps=fps
        print("duration", video.duration)
        print("frames:", (video.fps * video.duration))
        print("nbFrames:", video.reader.nframes)
        print("ffmpeg_duration:", video.reader.ffmpeg_duration)
        print("reader.duration:", video.reader.duration)
        print("reader.fps:", video.reader.fps)
        return video
    
    def getDuration(self, listVideos):
        duration = 0.0
        for video in listVideos:
            duration = duration + video.duration
        return duration
        