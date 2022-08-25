import os
import time
import cozmo #Install the Cozmo SDK http://cozmosdk.anki.com/docs/initial.html#installation
import subprocess
import tkinter.filedialog
from PIL import Image #pip install Pillow
from shutil import rmtree #This function removes directories. Run this script with unused folder "frames"

print("Make sure Cozmo is connected to your phone and SDK enabled")

#Ask user for video file
video = tkinter.filedialog.askopenfilename(title="Choose a video",filetypes=(('', '*.mp4'),('', '*.avi')))

if not len(video) == 0: #Check if video is empty before running
    if os.path.isdir("frames") == True: #Remake directory if it exists
        rmtree("frames")
        os.mkdir("frames")
    else:
        os.mkdir("frames")

    #Split the video into frames (ffmpeg required)
    subprocess.call("ffmpeg -i "+'"'+video+'"'+" frames/thumb%04d.jpg -hide_banner", shell=True)

    #Use the frames directory
    directories = os.listdir("frames")

    #Resize all the frames to Cozmo's screen resolution
    for file in directories:
        Image.open("frames/"+file).resize(cozmo.oled_face.dimensions(),Image.NEAREST).save("frames/"+file)
    
    frame_rate=20 #Higher framerates will cause more framedrops (Default: 20)
    remove_frames_after_program_is_done=True #(Default: True)

    #Make sure Cozmo is connected to your phone and SDK enabled
    def cozmo_program(robot: cozmo.robot.Robot):
        time.sleep(1) #Prevent beginning of the video from cutoff
        for file in sorted(directories):
            robot.display_oled_face_image(cozmo.oled_face.convert_image_to_screen_data(Image.open("frames/"+file),
                #Brightness controls
                invert_image=False, #(Default: False)
                pixel_threshold=127 #(Default: 127)
            ),1000/frame_rate)
            time.sleep(1/frame_rate)
        if remove_frames_after_program_is_done:
            rmtree("frames")

    cozmo.run_program(cozmo_program)