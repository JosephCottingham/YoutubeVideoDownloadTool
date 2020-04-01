import sys
from functools import partial
from threading import Thread

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

import YoutubeVideoDownloadTool_support


def vp_start_gui():
    global val, w, root
    root = tk.Tk()
    YoutubeVideoDownloadTool_support.set_Tk_var()
    top = Toplevel1(root)
    YoutubeVideoDownloadTool_support.init(root, top)
    root.mainloop()


w = None


def create_Toplevel1(root, *args, **kwargs):
    global w, w_win, rt
    rt = root
    # w stores the gui
    w = tk.Toplevel(root)
    YoutubeVideoDownloadTool_support.set_Tk_var()
    top = Toplevel1(w)
    YoutubeVideoDownloadTool_support.init(w, top, *args, **kwargs)
    return (w, top)


def destroy_Toplevel1():
    global w
    w.destroy()
    w = None


class Toplevel1:
    def __init__(self, top=None):
        # class configures and populates the toplevel window
        _bgcolor = '#000000'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#1c1c1c'  # X11 color: 'gray85'
        _ana1color = '#1c1c1c'  # X11 color: 'gray85'
        _ana2color = '#ececec'  # Closest X11 color: 'gray92'
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.', background=_bgcolor)
        self.style.configure('.', foreground=_fgcolor)
        self.style.configure('.', font="TkDefaultFont")
        self.style.map('.', background=[('selected', _compcolor), ('active', _ana2color)])

        top.geometry("1333x459")
        top.minsize(1, 1)
        top.maxsize(3825, 2130)
        top.resizable(0, 0)
        top.title("YouTube Video Download Tool")
        top.configure(highlightcolor="black")
        top.configure(background="#1c1c1c")

        self.URLEntry = ttk.Entry(top)
        self.URLEntry.place(relx=0.143, rely=0.065, relheight=0.144, relwidth=0.851)
        self.URLEntry.configure(takefocus="")
        self.URLEntry.configure(cursor="xterm")
        self.URLEntry.configure(font=("TkDefaultFont", 16, 'bold'))

        self.URLLabel = ttk.Label(top)
        self.URLLabel.place(relx=0.0, rely=0.065, height=74, width=160)
        self.URLLabel.configure(background="#1c1c1c")
        self.URLLabel.configure(foreground="#000000")
        self.URLLabel.configure(font=("TkDefaultFont", 16, 'bold'))
        self.URLLabel.configure(foreground="white")
        self.URLLabel.configure(relief="flat")
        self.URLLabel.configure(text='''Youtube URL:''')


        self.DownloadLocLabel = ttk.Label(top)
        self.DownloadLocLabel.place(relx=0.0, rely=0.305, height=74, width=400)
        self.DownloadLocLabel.configure(background="#1c1c1c")
        self.DownloadLocLabel.configure(foreground="#000000")
        self.DownloadLocLabel.configure(font=("TkDefaultFont", 16, 'bold'))
        self.DownloadLocLabel.configure(foreground="white")
        self.DownloadLocLabel.configure(relief="flat")
        self.DownloadLocLabel.configure(text='''Download Location(Video is Default):''')

        self.DownloadEntry = ttk.Entry(top)
        self.DownloadEntry.place(relx=0.315, rely=0.305, relheight=0.144, relwidth=0.678)
        self.DownloadEntry.delete(0, tk.END)
        self.DownloadEntry.insert(0, YoutubeVideoDownloadTool_support.setDefaultDir())
        self.DownloadEntry.configure(takefocus="")
        self.DownloadEntry.configure(cursor="xterm")
        self.DownloadEntry.configure(font=("TkDefaultFont", 16, 'bold'))

        # style = ttk.Style()
        # style.theme_use('clam')
        # style.configure("TRadiobutton", background=[('selected', '#1c1c1c'), ('active', '#ffffff')], foreground=[('selected', '#ffffff'), ('active', '#1c1c1c')])
        self.style.map('TRadiobutton', background=[('selected', _compcolor), ('active', _compcolor)], foreground=[('selected', _compcolor), ('active', _compcolor)])
        self.VideoAudio = ttk.Radiobutton(top)
        self.VideoAudio.place(relx=0.438, rely=0.516, relwidth=0.155, relheight=0.0, height=36)
        self.VideoAudio.configure(value=0)
        self.VideoAudio.configure(variable=YoutubeVideoDownloadTool_support.selectedButton)
        self.VideoAudio.configure(text='''Video & Audio''')
        self.VideoAudio.configure(style="TRadiobutton")

        self.OnlyAudio = ttk.Radiobutton(top)
        self.OnlyAudio.place(relx=0.438, rely=0.621, relwidth=0.155, relheight=0.0, height=36)
        self.OnlyAudio.configure(value=1)
        self.OnlyAudio.configure(variable=YoutubeVideoDownloadTool_support.selectedButton)
        self.OnlyAudio.configure(text='''Only Audio''')

        downloadWithArg = partial(YoutubeVideoDownloadTool_support.startDownload, URL=self.URLEntry,
                                  DownloadLoc=self.DownloadEntry)
        self.DownloadButton = ttk.Button(top)
        self.DownloadButton.place(relx=0.69, rely=0.538, height=73, width=244)
        self.DownloadButton.configure(command=downloadWithArg)
        self.DownloadButton.configure(takefocus="")
        self.DownloadButton.configure(text='''Download Videos or Audio Files''')

        self.FileButton = ttk.Button(top)
        self.FileButton.place(relx=0.075, rely=0.538, height=73, width=360)
        self.FileButton.configure(command=YoutubeVideoDownloadTool_support.fileSelect)
        self.FileButton.configure(takefocus="")
        self.FileButton.configure(text='''Select Download Location''')

        TROUGH_COLOR = 'white'
        BAR_COLOR = 'green'
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("green.Horizontal.TProgressbar", troughcolor=TROUGH_COLOR, bordercolor=TROUGH_COLOR,
                        background=BAR_COLOR, lightcolor=BAR_COLOR, darkcolor=BAR_COLOR)

        self.TProgressbar1 = ttk.Progressbar(top)
        self.TProgressbar1.place(relx=0.008, rely=0.763, relwidth=0.983, relheight=0.0, height=40)
        self.TProgressbar1.configure(orient="horizontal", length=100, mode="determinate",
                                     style="green.Horizontal.TProgressbar")

        self.ErrorLabel = ttk.Label(top)
        self.ErrorLabel.place(relx=0.75, rely=0.893, height=34, width=881, anchor="center")
        self.ErrorLabel.configure(background="#1c1c1c")
        self.ErrorLabel.configure(foreground="#000000")
        self.ErrorLabel.configure(font=("TkDefaultFont", 16, 'bold'))
        self.ErrorLabel.configure(foreground="red")
        self.ErrorLabel.configure(relief="flat")
        self.ErrorLabel.configure(justify='center')
        self.ErrorLabel.configure(text='''No Current Errors''')


if __name__ == '__main__':

    thread = Thread(target=vp_start_gui)
    thread.start()
