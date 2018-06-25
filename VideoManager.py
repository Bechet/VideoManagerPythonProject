# -*- coding: utf-8 -*-

from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip
from ScriptManager import ScriptManager

class VideoManager():
    def __init__(self, _fullVideosFolderPath, _videoOutputPath, _scriptFilePath):
        print("VideoManager Created, extracting path information...")
        self.fileType = ".mp4"
        if (_fullVideosFolderPath == ''):
            self.fullVideosFolderPath = "./Input/"
        else:
            self.fullVideosFolderPath = _fullVideosFolderPath
        if (_videoOutputPath == ''):
            self.videoOutputPath = "./Output/output" + self.fileType
        else:
            self.videoOutputPath = _videoOutputPath
            if not (_videoOutputPath.endswith(self.fileType)):
                self.videoOutputPath = self.videoOutputPath + self.fileType
        if (_scriptFilePath == ''):
            self.scriptFilePath = "./Script/script.txt"
        else:
            self.scriptFilePath = _scriptFilePath
            if not (_scriptFilePath.endswith(".txt")):
                self.scriptFilePath = self.scriptFilePath + ".txt"
        
        self.scriptManager = ScriptManager(self.scriptFilePath)
        self.readAndSaveLocallyAllVideo()
        concatenatedVideo = self.concatVideo(self.listSlicedVideos);
        print("Concatenating done")
        print("Writting output file in path: " + self.videoOutputPath)
        print("This could take couple minutes, take a coffee break ! =)")
        concatenatedVideo.write_videofile(self.videoOutputPath, codec='libx264')
        print("Execution success!")
        return None
    
    def readAndSaveLocallyAllVideo(self):
        print("Slicing input videos from script...")
        self.listSlicedVideos = []
        while self.scriptManager.getCurrentCoupleTitleAndDuration() is not None:
            title = self.scriptManager.getCurrentTitle()
            duration = self.scriptManager.getCurrentDuration()
            print("Adding video with title: " + str(title) + " for " + str(duration)+ " seconds")
            video = VideoFileClip(self.fullVideosFolderPath + title + self.fileType).subclip(0, duration)
            self.listSlicedVideos.append(video)
            self.scriptManager.next()
        print("Slicing done")
                
    def getVideoFromFileName(self, fileName):
        for video in self.listTitleAndFullVideo:
            if video.filename == (self.fullVideosFolderPath + fileName + self.fileType):
                return video
        return None
    
    def concatVideo(self, listSlicedVideos):
        print("Concatenating sliced videos...")
        return concatenate_videoclips(listSlicedVideos)