import os
import sys
import traceback
import platform
from pytube import YouTube
from pytube import Playlist
from tkinter import filedialog as fd
from pathlib import Path, PureWindowsPath
from threading import Thread
from moviepy.video.io.VideoFileClip import VideoFileClip
import YoutubeVideoDownloadTool

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


def downloadProgress(stream=None, chunk=None, bytes_remaining=None):
    # calculate and run progress bar
    downloadProgressVar = (100 * (videoSize - bytes_remaining)) / videoSize
    w.TProgressbar1.configure(value=downloadProgressVar)
    print('{:00.0f}% downloaded of file #{:0d} of {:0d} files'.format(downloadProgressVar, videoNum, videoTotalNum))
    w.ErrorLabel.configure(
        text='{:00.0f}% downloaded of file #{:0d} of {:0d} files'.format(downloadProgressVar, videoNum, videoTotalNum))

# def convertProgress(current, n_frames):
#     # calculate and run progress bar
#     downloadProgressVar = (100 * (n_frames - current)) / n_frames
#     w.TProgressbar1.configure(value=downloadProgressVar)
#     w.ErrorLabel.configure(
#         text='{:00.0f}% Converted of file #{:0d} of {:0d} files'.format(downloadProgressVar, videoNum, videoTotalNum))

def audioConvert(stream=None, file_path=None):
    try:
        # remove extension (.mp4)
        findIn = file_path.split(".")
        mp4 = "%s.mp4" % findIn[0]
        nameSec = file_path.split('/')[-1].split('\\')
        name = nameSec[-1].split('.')
        print(name)
        out = Dloc + "/" + name[-2]
        mp3 = "%s.mp3" % out
        # ffmpeg = ('ffmpeg -i %s ' % mp4 + mp3)
        # subprocess.call(ffmpeg, shell=True)
        mp4Path = Path(mp4)
        mp3Path = Path(mp3)
        if (platform.system() == 'Windows'):
            mp4Path = str(PureWindowsPath(mp4Path))
            mp3Path = str(PureWindowsPath(mp3Path))
            print(type(mp4Path))
            print("Windows")
        print(str(mp4Path))
        video = VideoFileClip(str(mp4Path))
        print(mp3Path)
        print(type(mp4Path))
        video.audio.write_audiofile(filename=mp3Path, verbose=False, logger=None)
        # os.remove(mp4Path)
    # , progress_callback=convertProgress
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
def fileSelect():
    # clear and refill entry
    w.DownloadEntry.delete(0, tk.END)
    w.DownloadEntry.insert(0, fd.askdirectory(initialdir=str(Path.home())))


def setDefaultDir():
    return str(Path.home())


def startDownload(URL, DownloadLoc):
    # to properly manage interface and download systems
    thread = Thread(target=downloadThread, args=(URL, DownloadLoc))
    thread.start()


def downloadThread(URL, DownloadLoc):
    # disabled to prevent running infinitely many threads
    w.DownloadEntry.configure(state="disabled")
    w.URLEntry.configure(state="disabled")
    w.FileButton.configure(state="disabled")
    w.DownloadButton.configure(state="disabled")
    w.OnlyAudio.configure(state="disabled")
    w.VideoAudio.configure(state="disabled")
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
            # within try to catch invalid links
            try:
                # only mp4 streams therefore, they need to be converted to mp3 though callback
                vid = YouTube(urlTxt, on_progress_callback=downloadProgress,
                              on_complete_callback=audioConvert).streams.get_lowest_resolution()
                videoSize = vid.filesize
                vid.download(output_path=DownloadTxt)
            # within try to catch invalid links
            except Exception as e:
                print(str(e))
                traceback.print_exc() 
                w.ErrorLabel.configure(text='Error: Invalid URL: File #{0} of {1} files'.format(videoNum, videoTotalNum))
        elif "playlist" in urlTxt:
            videoTotalNum = len(Playlist(urlTxt).video_urls)
            videoNum = 0
            for videoURL in Playlist(urlTxt).video_urls:
                try:
                    videoNum += 1
                    # only mp4 streams therefore, they need to be converted to mp3 though callback
                    vid = YouTube(videoURL, on_progress_callback=downloadProgress,
                                  on_complete_callback=audioConvert).streams.get_lowest_resolution()
                    videoSize = vid.filesize
                    vid.download(output_path=DownloadTxt)
                except:
                    w.ErrorLabel.configure(text='Error: Invalid URL: File #{0} of {1} files'.format(videoNum, videoTotalNum))
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
            except Exception as e:
                print(str(e))
                w.ErrorLabel.configure(text='Error: Invalid URL: File #{0} of {1} files'.format(videoNum, videoTotalNum))
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
                    w.ErrorLabel.configure(text='Error: Invalid URL: File #{0} of {1} files'.format(videoNum, videoTotalNum))
        else:
            w.ErrorLabel.configure(text='Error: Invalid URL')
    # set to normal to allow second run
    w.DownloadEntry.configure(state="normal")
    w.URLEntry.configure(state="normal")
    w.FileButton.configure(state="normal")
    w.DownloadButton.configure(state="normal")
    w.OnlyAudio.configure(state="normal")
    w.VideoAudio.configure(state="normal")
    sys.stdout.flush()

# setup support
def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top

# allows window to be closed
def destroy_window():
    # Closes the window
    global top_level
    top_level.destroy()
    top_level = None

if __name__ == '__main__':
    # Starts the the GUI
    YoutubeVideoDownloadTool.vp_start_gui()
