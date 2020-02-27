import os
import sys
from pytube import YouTube
from pytube import Playlist
from tkinter import filedialog as fd
from pathlib import Path
from threading import Thread
import subprocess

# TODO Check/Install FFMPEG

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk

    py3 = False
except ImportError:
    import tkinter.ttk as ttk

    py3 = True


def set_Tk_var():
    global selectedButton
    selectedButton = tk.IntVar(0)


def downloadProgress(stream=None, chunk=None, file_handle=None, remaining=None):
    downloadProgressVar = (100 * (videoSize - remaining)) / videoSize
    w.TProgressbar1.configure(value=downloadProgressVar)
    w.ErrorLabel.configure(
        text='{:00.0f}% downloaded of file #{:0d} of {:0d} files'.format(downloadProgressVar, videoNum, videoTotalNum))


def audioConvert(stream=None, file_path=None):
    filePath = file_path.name
    #remove extension (.mp4)
    fineIn = filePath.split(".")
    mp4 = "'%s'.mp4" % fineIn[0]
    nameSec = filePath.split('/')
    name = nameSec[-1].split('.')
    out = Dloc + "/" + name[0]
    mp3 = "'%s'.mp3" % out
    ffmpeg = ('ffmpeg -i %s ' % mp4 + mp3)
    subprocess.call(ffmpeg, shell=True)
    os.remove(mp4)


def fileSelect():
    w.DownloadEntry.delete(0, tk.END)
    w.DownloadEntry.insert(0, fd.askdirectory())


def setDefaultDir():
    return str(Path.home())


def startDownload(URL, DownloadLoc):
    thread = Thread(target=downloadThread, args=(URL, DownloadLoc))
    thread.start()


def downloadThread(URL, DownloadLoc):
    # Progressbar needs to start at 0
    w.TProgressbar1["value"] = 0
    # unable to pass due to lib configuration
    global videoSize
    global videoTotalNum
    global videoNum
    global Dloc
    # Get string object from entry object
    urlTxt = URL.get()
    DownloadTxt = DownloadLoc.get()
    Dloc = DownloadTxt
    # Only audio if true or video & audio if false
    if selectedButton.get():
        DownloadTxt = os.path.join(os.getcwd(), r'tempVidStorage')
        # removes files from tempVidStorage file
        for root, dirs, files in os.walk(DownloadTxt):
            for file in files:
                os.remove(os.path.join(root, file))
        # determines if URL is to playlist or video
        if "watch" in urlTxt:
            videoNum = 1
            videoTotalNum = 1
            #within try to catch invalid links
            try:
                # only mp4 streams therefore, they need to be converted to mp3 though callback
                vid = YouTube(urlTxt, on_progress_callback=downloadProgress,
                              on_complete_callback=audioConvert).streams.filter(only_audio=True).first()
                videoSize = vid.filesize
                vid.download(output_path=DownloadTxt)
            # within try to catch invalid links
            except:
                w.ErrorLabel.configure(text='Error: Invalid URL: File #{0}'.format(videoNum))
        elif "playlist" in urlTxt:
            videoTotalNum = len(Playlist(urlTxt).video_urls)
            videoNum = 0
            for videoURL in Playlist(urlTxt).video_urls:
                try:
                    videoNum += 1
                    # only mp4 streams therefore, they need to be converted to mp3 though callback
                    vid = YouTube(videoURL, on_progress_callback=downloadProgress,
                                  on_complete_callback=audioConvert).streams.filter(only_audio=True).first()
                    videoSize = vid.filesize
                    vid.download(output_path=DownloadTxt)
                except:
                    w.ErrorLabel.configure(text='Error: Invalid URL: File #{0}'.format(videoNum))
        else:
            w.ErrorLabel.configure(text='Error: Invalid URL')
    else:
        # determines if URL is to playlist or video
        if "watch" in urlTxt:
            videoNum = 1
            videoTotalNum = 1
            #within try to catch invalid links
            try:
                vid = YouTube(urlTxt, on_progress_callback=downloadProgress).streams.get_highest_resolution()
                videoSize = vid.filesize
                vid.download(output_path=DownloadTxt)
            except:
                w.ErrorLabel.configure(text='Error: Invalid URL: File #{0}'.format(videoNum))
        elif "playlist" in urlTxt:
            videoTotalNum = len(Playlist(urlTxt).video_urls)
            videoNum = 0
            for videoURL in Playlist(urlTxt).video_urls:
                # within try to catch invalid links
                try:
                    videoNum += 1
                    vid = YouTube(videoURL, on_progress_callback=downloadProgress).streams.get_highest_resolution()
                    videoSize = vid.filesize
                    vid.download(output_path=DownloadTxt)
                except:
                    w.ErrorLabel.configure(text='Error: Invalid URL: File #{0}'.format(videoNum))
        else:
            w.ErrorLabel.configure(text='Error: Invalid URL')
    sys.stdout.flush()


def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top


def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None


if __name__ == '__main__':
    import YoutubeVideoDownloadTool

    YoutubeVideoDownloadTool.vp_start_gui()
