from pytube import YouTube

fileName = input("Enter the Location and file name of TXT file where you have stored Youtube URLs")
file = open(fileName, "r")
for line in file:
    YouTube(line).streams.get_highest_resolution().download()
# yt = YouTube('http://youtube.com/watch?v=9bZkp7q19f0')
# print(yt.streams.all())


from pytube import Playlist
playlist = Playlist("https://www.youtube.com/playlist?list=PLynhp4cZEpTbRs_PYISQ8v_uwO0_mDg_X")
for video in playlist:
    video.streams.get_highest_resolution().download()