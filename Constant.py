# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 22:11:55 2019

@author: Leo
"""

input_video_folder_name="./Input/"
output_video_folder_name="./Output/"
midi_folder_name="./Midi/"
script_folder_name="./Script/"
output_tmp_folder_name="tmp"
output_tmp_folder_path_name=output_video_folder_name + output_tmp_folder_name + "/"

midi_file_name="midi.mid"
script_file_name="script.txt"
output_file_name="output.mp4"
output_tmp_file_name="tmpVideoClip"

midi_path_name=midi_folder_name + midi_file_name
script_path_name=script_folder_name +  script_file_name
output_video_path_name=output_video_folder_name + output_file_name
output_tmp_video_path_name=output_tmp_folder_path_name + output_tmp_file_name

baseInputVideoFolderPath= "./InputVideoFolder/"
mapper_file_path_name="./Mapper/mapper.txt"

generated_sub_input_video_folder_name="generated"

mp4suffix=".mp4"

codecMpeg4='mpeg4'
codecLibx264='libx264'














codec=codecLibx264
# Split into tmp video file each "split_length" notes
split_length=20
max_memory_percentage=90