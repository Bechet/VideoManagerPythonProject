# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

from moviepy.editor import VideoFileClip

# UKULELE CLIP, OBTAINED BY CUTTING AND CROPPING
# RAW FOOTAGE

#class VideoManagerClass():
#    listTitleAndFullVideo = []
#    def __init__(self, ):
#        print("VideoManager Created")
#        return None
#    def test():
#        print("test")
#
#videoManager = VideoManagerClass()
#videoManager.test()



class Main():
    def __init__(self,):
        self.test();
    
    def test(self):
#        w,h = Avideo.size
#        print(Avideo)
#        print(w)
#        print(h)


#Avideo.write_videofile("D:/test.mp4")

#Bvideo = VideoFileClip("D:/VideoMakerProject/VideosForderName/B.mp4", audio=False)
#w,h = Bvideo.size
#
#print(w)
#print(h)
#
## THE TEXT CLIP IS ANIMATED.
## I am *NOT* explaining the formula, understands who can/want.
#txt_mov = txt_col.set_pos( lambda t: (max(w/30,int(w-0.5*w*t)),
#                                  max(5*h/6,int(100*t))) )
#
#final = CompositeVideoClip(([Avideo,txt_mov,Bvideo])
#final.subclip(0,5).write_videofile("D:/VideoMakerProject/AB.mp4",fps=24,codec='libx264')

main = Main()

Avideo = VideoFileClip("D:/VideoMakerProject/VideosForderName/A.mp4", audio=False).subclip(0,5);