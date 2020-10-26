

import os
import threading
import time
from tkinter.messagebox import *
from tkinter import *
from tkinter.filedialog import *
import pygame

from tkinter import ttk
from ttkthemes import themed_tk as tk

from mutagen.mp3 import MP3
from pygame import mixer

scroll_thread = None
counter_thread = None
color = '#A8C1B4'
root = tk.ThemedTk()
print(root.get_themes())
root.minsize(width=750, height=550)
root.maxsize(width=750, height=550)
root.title("My Music Player")
try:
    root.set_theme("scidpurple")  # scidpurple alt vista
except:
    root.set_theme("alt")
root.configure(bg=color)
statusbar = ttk.Label(root, text="Welcome to My Music Player", relief=SUNKEN, anchor=W, font='Times 10 italic')
statusbar.pack(side=BOTTOM, fill=X)
pygame.mixer.init()
songName = StringVar()
# ============================================================
playlist = []
count = []  # for using only FileHandling
list = []  # for using only file handling
playlist2 = []  # for using only for filehandling in same name but diff. loc


def load_Music():
    global count, playlist, listbox, list, playlist2
    del list[0:]
    listbox.delete(0, END)
    del playlist[0:]
    del count[0:]
    try:
        file = open("MyPlayer_Data2.txt", "r")
        for value in file:
            if value in count:
                # print(value)
                continue
            else:
                count.append(value)
        # print(count)
        for x in count:
            a = x[0:-1]
            list.append(a)
            filename = os.path.basename(a)
            listbox.insert(0, filename)
            playlist.insert(0, a)
    except FileNotFoundError:
        return
    root.update()


def select_folder():
    global playlist, playlist2
    chooseDirPath = askdirectory(parent=root,
                                 title="Select Directory contains .Mp3 files", )
    print("select:", chooseDirPath)
    if len(chooseDirPath) == 0:
        return

    a = os.chdir(chooseDirPath)
    b = os.listdir()
    # b = set(b)
    # print(b)
    os.chdir("c:\\users\\hp\\pycharmProjects\\music_Player")
    # print("A = ", a)
    # print("B = ", b)
    # path = "\MyPlayer_Data2.txt"
    f = open("MyPlayer_Data2.txt", "a")
    for file in b:
        file2 = chooseDirPath + "/" + file
        # print("file",file)
        # print("playsit",playlist)
        if file2 in playlist:
            print(file)
        else:
            f.write(file2 + "\n")
    f.close()
    load_Music()

    # for files in filenames:
    # print(files)


def __addMusic():
    global playlist, listbox, playlist2
    try:
        filespath = askopenfilenames(defaultextension=".mp3",
                                     filetypes=[("mp3", ".mp3"), ("wev", ".wev*")])
        if filespath == "":
            filespath = None
        else:
            # filespath = root.tk.splitlist(filespath)
            try:
                f = open("MyPlayer_Data2.txt", "a")

                for path in filespath:
                    playlist2.append(os.path.basename(path))
                    # print("A",a)
                    # print("playlist2",playlist2)

                    if path in playlist:
                        continue
                    else:
                        for li in playlist2:
                            # print("li",li)
                            # print("listbox",listbox)
                            if li in listbox.get(0, END):
                                continue
                            else:
                                f.write(path + "\n")

                f.close()
                load_Music()
                # root.update()
            except:
                pass

    except:
        return


def delete_music2():
    global playlist, listbox, r
    file1 = open("MyPlayer_Data2.txt", "r")
    file2 = open("temp.txt", "w")
    lines = file1.readlines()
    for line in lines:
        if r not in line:
            file2.write(line)
    file1.close()
    file2.close()
    os.remove("MyPlayer_Data2.txt")
    os.rename("temp.txt", "MyPlayer_Data2.txt")
    stop_music()


r = ""


def __delMusic():
    global playlist, listbox, r
    if playlist:
        remove = listbox.curselection()
        r = str((listbox.get(ACTIVE)))
        # print(r)
        if remove:
            ask = askyesno("Confirm", "Are u sure want to Remove selected Music")
            if ask == YES:
                # a = int(listbox.size())
                # print(a)
                if listbox.size() == 1:
                    state_Disabled()
                    listbox.delete(remove[0])
                    playlist.pop(remove[0])
                    delete_music2()

                else:
                    listbox.delete(remove[0])
                    playlist.pop(remove[0])
                    delete_music2()
            else:
                pass

        else:
            showwarning("Warning", "Please select any Music")
        # print(playlist)
    else:
        showwarning("Warning", "Playlist is already Empty")


total_length = 0
timeformat = ''


def show_details(play_song):
    global total_length, counter_thread, scroll_thread, timeformat
    file_data = os.path.splitext(play_song)
    # print("1")
    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
        # print("2")

    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()
        # print(total_length)
        # print("3")

    # div - total_length/60, mod - total_length % 60
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel['text'] = timeformat
    # showinfo('details :',total_length)
    # root.update()
    # print("4")
    counter_thread = threading.Thread(target=start_count, daemon=True, args=(total_length,))
    counter_thread.start()


paused = TRUE
current_time = 0
ct = True


def start_count(t):
    import math
    global paused
    global start_from
    global current_time, total_length
    mixer.music.get_busy()
    current_time = 0
    pv = t / 100

    timeS = (current_time / pv) * 100

    progressbar['value'] = timeS

    while current_time <= t and mixer.music.get_busy() and ct == True:
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            # print("min=",mins,"sec=",secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelabel['text'] = timeformat
            time.sleep(1)

            current_time += 1

            if current_time % math.ceil(pv) == 0 and ct == True:
                a = pv * 100
                timeS = (current_time / a) * 100

                # print("current time ", timeS , current_time , a)
                progressbar['value'] = timeS
                # progressbar['value'] = v
                # print(v)

    '''if current_time >=t:
        mixer.music.fadeout(2000)
        next_Song()'''


start_from = 0
t1 = 0
resetFlag = 0


def state_Change2():
    stopBtn.configure(state=NORMAL)
    forwardBtn.configure(state=NORMAL)
    backwordBtn.configure(state=NORMAL)


def state_Change(*event):
    playBtn.configure(state=NORMAL)
    # stopBtn.configure(state=NORMAL)
    previousBtn.configure(state=NORMAL)
    nextBtn.configure(state=NORMAL)
    # forwardBtn.configure(state=NORMAL)
    # backwordBtn.configure(state=NORMAL)
    volumeBtn.configure(state=NORMAL)
    # scale.configure(state=NORMAL)


def state_Disabled():
    playBtn.configure(state=DISABLED)
    stopBtn.configure(state=DISABLED)
    previousBtn.configure(state=DISABLED)
    nextBtn.configure(state=DISABLED)
    forwardBtn.configure(state=DISABLED)
    backwordBtn.configure(state=DISABLED)
    volumeBtn.configure(state=DISABLED)


selected_song = 0


def selectForList(*event, j=0):
    global paused, ct, st, selected_song
    global start_from, playPhoto, pausePhoto
    global counter_thread, scroll_thread, flag, current_time
    state_Change2()
    stop_music()
    # songName.set("Song Name :- ")
    ct = True
    st = True
    # current_time = start_from
    try:
        playBtn["image"] = pausePhoto
        paused = FALSE
        # mixer.music.stop()
        # stop_music()
        time.sleep(1)
        selected_song = int(listbox.curselection()[0])
        # selected_song = int(selected_song[0])
        play_it = playlist[selected_song]
        mixer.music.load(play_it)
        statusbar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
        scroll_thread = threading.Thread(target=scrollingName, daemon=True, args=(os.path.basename(play_it),))
        scroll_thread.start()
        flag = 0
        show_details(play_it)
        mixer.music.play(0, start_from)
    except Exception as e:
        showerror('error ', e)


def play_music(*event):
    global paused, ct, st, selected_song
    global start_from, playPhoto, pausePhoto
    global counter_thread, scroll_thread, flag
    ct = True
    st = True

    if flag == 0:
        if paused:
            playBtn["image"] = pausePhoto
            mixer.music.unpause()
            statusbar['text'] = "Music Resumed"
            paused = FALSE


        else:
            playBtn["image"] = playPhoto
            __pauseMusic()


    else:
        stop_music()
        selectForList(j=selected_song)

        # paused = TRUE
        flag = 0


st = True


def scrollingName(play_it):
    global st
    while progressbar['value'] <= 100 and st == True:
        songName.set(play_it)
        play_it = play_it[1:] + play_it[0]
        time.sleep(0.5)


flag = 1


def __pauseMusic(*event):
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music Paused"


def stop_music():
    global start_from, paused, st, ct, resetFlag, timeformat, songName, flag
    mixer.music.stop()
    # mixer.music.fadeout(1000)
    statusbar['text'] = "Music Stopped"
    start_from = 1
    progressbar['value'] = 100
    currenttimelabel['text'] = timeformat
    songName.set("Song Name :- ")
    paused = True
    st = False
    ct = False
    playBtn["image"] = playPhoto
    flag = 1


currentVol = 0


def mute_unmute():
    global currentVol

    if scale.get() == 0:
        volumeBtn["image"] = volumePhoto
        scale.set(currentVol)
        mixer.music.set_volume(scale.get() * 0.01)
    else:
        volumeBtn["image"] = mutePhoto
        currentVol = scale.get()
        scale.set(0)
        mixer.music.set_volume(scale.get() * 0.01)


def set_vol(*event):
    vol = scale.get()
    mixer.music.set_volume(vol * 0.01)
    if vol == 0:
        volumeBtn["image"] = mutePhoto
    else:
        volumeBtn["image"] = volumePhoto


def next_Song():
    global selected_song
    if listbox.size() == 0:
        showwarning('warning', 'NO Song in Your PlayList')
        return

    stop_music()
    # s = listbox.curselection()
    # print(s)
    # if len(s) != 0:
    if selected_song:
        # print("1",selected_song)
        # print(s[0])
        # if s[0] < listbox.size() - 1:
        if selected_song < listbox.size() - 1:
            listbox.selection_clear(0, END)
            # listbox.selection_set(s[0] + 1)
            listbox.selection_set(selected_song + 1)
            # print("2nd",selected_song)
        else:
            listbox.selection_clear(0, END)
            listbox.selection_set(0)
            # print("3rd",selected_song)
    else:
        listbox.selection_clear(0, END)
        if listbox.size() == 1:
            listbox.selection_set(0)
        else:
            listbox.selection_set(selected_song + 1)
        # print("4th",selected_song)

    global paused
    paused = FALSE
    play_music()


def prev_song():
    global selected_song
    # previousBtn.configure(state=NORMAL)
    if listbox.size() == 0:
        showwarning('warning', 'NO Song in Your PlayList')
        return

    stop_music()
    if selected_song:
        if selected_song < listbox.size():
            listbox.selection_clear(0, END)
            listbox.selection_set(selected_song - 1)
        else:

            listbox.selection_clear(0, END)
            listbox.selection_set(0)
    else:
        a = int(listbox.size())
        listbox.selection_clear(0, END)
        listbox.selection_set(a - 1)

    global paused
    paused = FALSE
    play_music()
    # print(s)


def forward():
    global start_from, total_length, selected_song
    if mixer.music.get_busy():
        start_from2 = start_from
        stop_music()
        start_from = start_from2
        if start_from < total_length - 10:
            start_from += 10
            selectForList(j=selected_song)
            # play_music()


def backward():
    global start_from, total_length, selected_song
    if mixer.music.get_busy():
        start_from1 = start_from
        stop_music()
        start_from = start_from1
        if start_from + 10 < total_length:
            start_from -= 10
            selectForList(j=selected_song)


def progreesbarValue(*event):
    global start_from, total_length, selected_song, progressbar
    if mixer.music.get_busy():
        """start_from2 = start_from
        #stop_music()
        start_from = start_from2
        if start_from < total_length - 10:
            start_from += 1
            selectForList(j=selected_song)"""

        vol = round(progressbar.get())
        print(vol)
        if vol == 0:
            start_from2 = start_from
            print("st",start_from2)
            stop_music()
            start_from2 += start_from
            start_from2 += vol

            print("Value",start_from2)
            selectForList(j=selected_song)
        else:
            pass

            # volumeBtn["image"] = mutePhoto



# ============================================================
# ======================================
# Create the menubar
# ==========================
# Styling
style = ttk.Style()
style.configure("TFrame", background=color)
style2 = ttk.Style()
style2.configure("TLabel", background=color)
style3 = ttk.Style()
style3.configure("TScale", background=color)
style4 = ttk.Style()
style4.configure("TButton", background="red")
prog = ttk.Style()
prog.configure("red.Horizontal.TProgressbar", foreground='red', background='red')
# ===========================
menubar = Menu(root)
root.config(menu=menubar)

# Create the submenu
subMenu = Menu(menubar, tearoff=0)
subMenu.add_command(label="open file", command=__addMusic)
subMenu.add_command(label="open folder", command=select_folder)
menubar.add_cascade(label="file", menu=subMenu)

listframe = ttk.Frame(root, style="TFrame")
listframe.pack(pady=10)
listboxframe = ttk.Frame(listframe)
listboxframe.pack()
y = Scrollbar(listboxframe, orient=VERTICAL)
y.pack(side=RIGHT, fill=Y)
listbox = Listbox(listboxframe, yscrollcommand=y.set, selectmode=EXTENDED, width=80, bg="Aqua", fg="blue",
                  selectbackground="Red", highlightcolor="yellow", activestyle='none')
listbox.pack()
Bframe = ttk.Frame(listframe)
Bframe.pack(fill=X, expand=YES, anchor=CENTER, pady=0)

addButton = ttk.Button(Bframe, style="TButton", text='+Add to Playlist', command=__addMusic)
addButton.grid(row=0, column=0, padx=100, pady=20)

delButton = ttk.Button(Bframe, text='Delete to Playlist', command=__delMusic)
delButton.grid(row=0, column=1, pady=20)

rightframe = ttk.Frame(root, style="TFrame")
rightframe.pack(padx=30)

topframe = ttk.Frame(rightframe, style="TFrame")
topframe.pack(fill=X, expand=YES)
played = ttk.Label(topframe, textvariable=songName, style="TLabel", font=("MV Boli", 15))
played.pack(pady=20)
songName.set("Song Name :- ")

lframe = LabelFrame(topframe, bd=1, bg=color)
lframe.pack(fill=X, expand=YES, anchor=CENTER)

currenttimelabel = ttk.Label(lframe, text='--:--', style="TLabel", font=('corbel', 20))
currenttimelabel.grid(row=0, column=1, padx=160)
lengthlabel = ttk.Label(lframe, text='--:--', style="TLabel", font=('corbel', 20))
lengthlabel.grid(row=0, column=2, padx=10)

progressbar = ttk.Scale(topframe, style="TScale", from_=0, to=100, orient=HORIZONTAL)
progressbar.pack(fill=X, expand=YES)

middleframe = Frame(rightframe)
middleframe.pack(pady=30, padx=30)

labelFrame = LabelFrame(middleframe, bd=5, bg=color)
labelFrame.pack(fill=X, expand=YES, anchor=W, side=BOTTOM)

playPhoto = PhotoImage(file='icons/play.png')
playBtn = ttk.Button(labelFrame, image=playPhoto, command=play_music)
playBtn.grid(row=0, column=0, padx=10)

stopPhoto = PhotoImage(file='icons/stop.png')
stopBtn = ttk.Button(labelFrame, image=stopPhoto, command=stop_music)
stopBtn.grid(row=0, column=1, padx=10)

pausePhoto = PhotoImage(file='icons/pause.png')

previousPhoto = PhotoImage(file='icons/previous.png')
previousBtn = ttk.Button(labelFrame, image=previousPhoto, command=prev_song)
previousBtn.grid(row=0, column=3, padx=10)

backwordPhoto = PhotoImage(file='icons/backward.png')
backwordBtn = ttk.Button(labelFrame, image=backwordPhoto, command=backward)
backwordBtn.grid(row=0, column=4, padx=10)

forwardPhoto = PhotoImage(file='icons/forward.png')
forwardBtn = ttk.Button(labelFrame, image=forwardPhoto, command=forward)
forwardBtn.grid(row=0, column=5, padx=10)

nextPhoto = PhotoImage(file='icons/next.png')
nextBtn = ttk.Button(labelFrame, image=nextPhoto, command=next_Song)
nextBtn.grid(row=0, column=6, padx=10)

mutePhoto = PhotoImage(file='icons/mute.png')
volumePhoto = PhotoImage(file='icons/speaker.png')
volumeBtn = ttk.Button(labelFrame, image=volumePhoto, command=mute_unmute)
volumeBtn.grid(row=0, column=7)

scale = ttk.Scale(labelFrame, style="TScale", from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(70)  # implement the default value of scale when music player starts
# mixer.music.set_volume(0.7)
scale.grid(row=0, column=8, pady=15, padx=30)

# Binding Double-clic event to play music -
listbox.bind("<Double-Button>", selectForList)
listbox.bind('<<ListboxSelect>>', state_Change)


def on_closing(*event):
    stop_music()
    state_Disabled()
    root.destroy()


# popup Menu Design
popup_menu = Menu(root, tearoff=0)


def showPopup(event):
    popup_menu.post(event.x_root, event.y_root)


popup_menu.add_command(label="play", command=selectForList)
popup_menu.add_command(label="pause", command=play_music)
popup_menu.add_separator()

popup_menu.add_command(label="Delete")
popup_menu.add_separator()
popup_menu.add_command(label="Select All")

# ============================================================
listbox.bind("<Button-3>", showPopup)
root.bind("<space>", play_music)
progressbar.bind("<Button-1>", progreesbarValue)
# root.bind("<Destroy>",on_closing)
load_Music()
state_Disabled()
root.mainloop()
