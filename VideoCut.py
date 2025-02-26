# -*- coding= utf-8 -*-
import subprocess
import shutil
import os

#ffmpeg -i /data/video_1.mp4 -f image2  -vf fps=fps=1/60 -qscale:v 2 /data/mp4-%05d.jpg
#將影片進行分解成圖像序列，並放在一個文件夾裡面
def videocut(FileName):
    ffmpegCmd = "C://ffmpeg//bin//ffmpeg.exe"
    frameDir = "C://xampp//htdocs//AndroidUpload//upload//pic//"  #存放图像序列路径
    videoDir="C://xampp//htdocs//AndroidUpload//upload"            #存放视频路径
    clear_all_file()
    videoFiles=os.listdir(videoDir)
    for video in videoFiles:
        sinVideoDir=os.path.join(videoDir,video)
        if (sinVideoDir.endswith("video.mp4")):
            videoName=os.path.basename(sinVideoDir)
            videoBaseName=videoName.rsplit('.')
            curVideoFrameOut=frameDir+videoBaseName[0]+"_%04d.jpg"

            video2framesCmd = ffmpegCmd + " -i " + sinVideoDir + " -f image2 -vf fps=fps=5 -qscale:v 2 " +curVideoFrameOut
            subprocess.call(video2framesCmd, shell=True)


def clear_all_file():
    shutil.rmtree("C://xampp//htdocs//AndroidUpload//upload//pic//") 
    os.mkdir("C://xampp//htdocs//AndroidUpload//upload//pic//")


# if __name__ == "__main__":
    # ffmpegCmd = "C://ffmpeg//bin//ffmpeg.exe"
    # frameDir = "C://xampp//htdocs//AndroidUpload//upload//pic5//"  #存放图像序列路径
    # videoDir="C://xampp//htdocs//AndroidUpload//upload"     #存放视频路径
    # videoFileName(videoDir,frameDir,ffmpegCmd)