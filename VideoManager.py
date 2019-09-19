# -*- coding: utf-8 -*-

from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip
from ScriptManager import ScriptManager
import Constant
import os
import psutil
import gc

class VideoManager():
    def __init__(self, _selectedInstrumentFolder):
        print("VideoManager Created, extracting path information...")
        self.selectedInstrumentFolder = _selectedInstrumentFolder
    
    def extecute(self):
        print("Execution...")
        self.scriptManager = ScriptManager()
        print("Spliting into sub file... This could take couple minutes, take a coffee break ! =)")
        self.readAndSaveAllVideoBis()
        
        self.listSlicedVideos = []
        for file_name in (os.listdir(Constant.output_tmp_folder_path_name)):
            self.listSlicedVideos.append(VideoFileClip(Constant.output_tmp_folder_path_name + file_name))
        if (len(self.listSlicedVideos) > 0):
            self.concatVideoAndSave(self.listSlicedVideos, Constant.output_video_path_name)
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
        tmpFileConter=0
        print("Slicing input videos from script...")
        self.hashmapFileName_File = {}
        self.listSlicedVideos = []
        print("Initial memory usage" + str(psutil.virtual_memory()))
        memoryLimit=psutil.virtual_memory()[2] + (Constant.max_memory_percentage-psutil.virtual_memory()[2])/2
        while self.scriptManager.getCurrentCoupleTitleAndDuration() is not None:
            title = self.scriptManager.getCurrentTitle()
            duration = self.scriptManager.getCurrentDuration()
            # TODO print("Checking existance of file" + fileName)
            generatedFilePath=Constant.baseInputVideoFolderPath+ self.selectedInstrumentFolder + "/" + Constant.generated_sub_input_video_folder_name + "/" + title + "-" + str(duration) + Constant.mp4suffix
            print("Adding video with title: " + str(title) + " for " + str(duration)+ " seconds")
            if not os.path.exists(generatedFilePath):
                print("File not generated yet, generating into path :" + generatedFilePath)
                video = VideoFileClip(Constant.baseInputVideoFolderPath + self.selectedInstrumentFolder + "/" + title + Constant.mp4suffix).subclip(0, duration)
                self.saveVideoIntoFile(video, generatedFilePath)
                print("End of generating file")
                self.listSlicedVideos.append(video)
                self.hashmapFileName_File[generatedFilePath]=video
            else:
                if self.hashmapFileName_File.__contains__(generatedFilePath):
                    self.listSlicedVideos.append(self.hashmapFileName_File[generatedFilePath])
                else:
                    video = VideoFileClip(generatedFilePath)
                    self.listSlicedVideos.append(video)
            # Memory check
            if (psutil.virtual_memory()[2] > memoryLimit):
                print("Memory limit, current memory:", psutil.virtual_memory()[2])
                tmpFilePath=Constant.output_tmp_video_path_name + str(tmpFileConter) + Constant.mp4suffix
                tmpFileConter = tmpFileConter + 1
                print("Saving sub video in tmp folder, path: ", tmpFilePath)
                self.concatVideoAndSave(self.listSlicedVideos, tmpFilePath)
                #Reset
                self.listSlicedVideos=[]
                gc.collect()
                
            self.scriptManager.next()
            print("Current memory usage percentage: ", psutil.virtual_memory()[2])
            
        self.concatVideoAndSave(self.listSlicedVideos, Constant.output_tmp_video_path_name + str(tmpFileConter) + Constant.mp4suffix)    

    
    def concatVideo(self, listSlicedVideos):
        print("Concatenating sliced videos...")
        return concatenate_videoclips(listSlicedVideos)
    
    def concatVideoAndSave(self, listSlicedVideos, path):
        print("Concatenating sliced videos...")
        concatenatedVideo=concatenate_videoclips(listSlicedVideos)
        print("Saving...")
        self.saveVideoIntoFile(concatenatedVideo, path)
        del concatenatedVideo
        gc.collect()
        
    
    def saveVideoIntoFile(self, video, path):
        video.write_videofile(path, codec='libx264')