# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 21:27:40 2023

@author: user
"""
import sys
from PySide2 import QtCore#, QtGui 
from PySide2 import QtWidgets
from PySide2.QtUiTools import QUiLoader

from pytube import YouTube

if not QtWidgets.QApplication.instance():
    app = QtWidgets.QApplication(sys.argv)
else:
    app = QtWidgets.QApplication.instance()

#app = QtWidgets.QApplication([])

loader = QUiLoader()

# if not QtWidgets.QApplication.instance():
#     app = QtWidgets.QApplication(sys.argv)
#     app.setQuitOnLastWindowClosed(True)
# else:
#     app = QtWidgets.QApplication.instance()
#     app.setQuitOnLastWindowClosed(True)

window = loader.load("main.ui", None)

def InfoYoutube():
    link = window.leVideoLink.text()
    yt = YouTube(link)
    
    formats = []
    
    for item in yt.vid_info:
        if item == 'streamingData':
            d = yt.vid_info[item]
            for item in d['formats']:
                if 'video/mp4' in item['mimeType']:
                    # yt.title
                    k1 = str(item['qualityLabel'])
                    if k1 in formats:
                        pass
                    else:
                        formats.append(item['qualityLabel'])
            for item in d['adaptiveFormats']:
                if 'video/mp4' in item['mimeType']:
                    k1 = str(item['qualityLabel'])
                    if k1 in formats:
                        pass
                    else:
                        formats.append(item['qualityLabel']+'(адаптивная)')
                    
    window.cbVersions.addItems(formats)

    window.lName.setText(yt.title)
    #window.bDownload.setEnabled = True


window.bGetVers.clicked.connect(InfoYoutube)

def DownYoutube():
    try:
        video = window.cbVersions.currentText()
        
        link = window.leVideoLink.text()
        yt = YouTube(link)
    except:
        QtWidgets.QMessageBox.warning(window, "Не могу получить видео", 
        "Не указана ссылка на YouTube.com или доступ блокирует сетевой экран.")
        return None
    
    #print(file)
    def DownloadAdaptive():
        import moviepy.editor as mpe
        import os

        vname = file + "/clip.mp4"
        aname = file + "/audio.mp3"
        
        video = window.cbVersions.currentText()
        # Download video and rename
        video = video.replace('(адаптивная)', '')
        # print(video)
        video = YouTube(link).streams.filter(subtype='mp4', 
                                                    res=video).first().download()
        #print(video, vname)
        try:
            os.rename(video, vname)
        except FileExistsError:
            import os.path
            from random import randint
            f1 = randint(0, 300)
            if os.path.exists(vname):
                vname = file + f"/clip{f1}.mp4"
                os.rename(video, vname)
                               
        
        # Download audio and rename
        audio = YouTube(link).streams.filter(only_audio=True).first().download()
        try:
            os.rename(audio, aname)
        except FileExistsError:
            import os.path
            from random import randint
            f1 = randint(0, 300)
            if os.path.exists(aname):
                aname = file + f"/audio{f1}.mp4"
                os.rename(audio, aname)
                
                
        # Setting the audio to the video
        video = mpe.VideoFileClip(vname)
        audio = mpe.AudioFileClip(aname)
        final = video.set_audio(audio)
        try:
            final.write_videofile(yt.title + ".mp4", fps=video.fps)
        except TypeError:
            os.remove(vname)
            os.remove(aname)
        
        # try:
        #     # Output result
        #     final.write_videofile(yt.title + ".mp4")
        # except:
        #     QtWidgets.QMessageBox.warning(window, "Не могу сохранить видео", 
        #     "Не получилось сохранить видео. Попробуйте другую версию. Проблема может быть связана с отсутствием доступа на запись или с кодеком ffmpeg.")
        
        # Delete video and audio to keep the result
        os.remove(vname)
        os.remove(aname)
    
    # Куда сохранить
    file = str(QtWidgets.QFileDialog.getExistingDirectory(window, 
                     "Укажите каталог для сохрнения видео"))
    if file == False or file == None:
        return None
    
    if '(адаптивная)' in video:
        DownloadAdaptive()
    else:
        #print(video)
        try:
            yt.streams.filter(progressive=True,
                              res=video).order_by('resolution').first().download(file)
            QtWidgets.QMessageBox.information(window, 
                                              "Загрузка завершена", 
                                              f"Видео было загружено в папку {file}.")
        except AttributeError:
            #print(video)
            video = video.replace('p60', 'p')
            yt.streams.filter(res=video).order_by('resolution').first().download(file)
            QtWidgets.QMessageBox.information(window, 
                                              "Загрузка завершена", 
                                              f"Видео было загружено в папку {file}.")

window.bDownload.clicked.connect(DownYoutube)
#window.bDownload.setEnabled = False

window.show()
sys.exit(app.exec_())