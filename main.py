import os
import pygame
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import ttk

# Get the current script directory to build the full path to the "Music" folder
current_directory = os.path.dirname(os.path.abspath(__file__))
music_directory = os.path.join(current_directory, "Music")

# Initialize mixer
pygame.mixer.init()

def choose_songs():
    temp_songs = filedialog.askopenfilenames(initialdir=music_directory, title="Choose songs",
                                            filetypes=(("mp3 Files", "*.mp3"),))
    for s in temp_songs:
        s = os.path.basename(s)
        if s not in songs_list.get(0, END):
            songs_list.insert(END, s)

def remove_song():
    curr_song = songs_list.curselection()
    if not curr_song:
        return
    songs_list.delete(curr_song[0])

def play():
    if not songs_list.curselection():
        messagebox.showwarning("Warning", "Please select a song.")
        return

    song = songs_list.get(ACTIVE)
    pygame.mixer.music.load(os.path.join(music_directory, song))
    pygame.mixer.music.play()
    update_status("Playing")
    update_current_song(song)

def pause():
    pygame.mixer.music.pause()
    update_status("Paused")

def stop():
    pygame.mixer.music.stop()
    songs_list.selection_clear(ACTIVE)
    update_status("Stopped")
    update_current_song("")

def resume():
    pygame.mixer.music.unpause()
    update_status("Playing")

def previous():
    songs_list.selection_clear(ACTIVE)
    previous_one = songs_list.curselection()
    if not previous_one:
        return
    previous_one = previous_one[0] - 1
    if previous_one < 0:
        previous_one = songs_list.size() - 1
    songs_list.activate(previous_one)
    play()

def next_song():
    songs_list.selection_clear(ACTIVE)
    next_one = songs_list.curselection()
    if not next_one:
        return
    next_one = next_one[0] + 1
    if next_one >= songs_list.size():
        next_one = 0
    songs_list.activate(next_one)
    play()

def set_volume(val):
    volume = int(float(val)) / 100  # Convert to float and then to int
    pygame.mixer.music.set_volume(volume)
    volume_label.config(text=f"Volume: {volume*100:.1f}%")

def update_status(status):
    status_label.config(text=f"Status: {status}")

def update_current_song(song):
    current_song_label.config(text=f"Current Song: {song}")

def on_song_end():
    next_song()

# Creating the root window
root = Tk()
root.title('Python MP3 Music Player')

# Creating the listbox to contain songs
songs_list = Listbox(root, selectmode=SINGLE, bg="black", fg="white", font=('arial', 15),
                     height=12, width=47, selectbackground="gray", selectforeground="black")
songs_list.grid(columnspan=9)

# Adding scrollbar to the listbox
scrollbar = Scrollbar(root, orient=VERTICAL, command=songs_list.yview)
scrollbar.grid(row=0, column=9, rowspan=10, sticky="ns")
songs_list.configure(yscrollcommand=scrollbar.set)

# Buttons
play_button = ttk.Button(root, text="Play", command=play)
play_button.grid(row=1, column=0)

pause_button = ttk.Button(root, text="Pause", command=pause)
pause_button.grid(row=1, column=1)

stop_button = ttk.Button(root, text="Stop", command=stop)
stop_button.grid(row=1, column=2)

resume_button = ttk.Button(root, text="Resume", command=resume)
resume_button.grid(row=1, column=3)

previous_button = ttk.Button(root, text="Prev", command=previous)
previous_button.grid(row=1, column=4)

next_button = ttk.Button(root, text="Next", command=next_song)
next_button.grid(row=1, column=5)

# Menu
my_menu = Menu(root)
root.config(menu=my_menu)
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Menu", menu=add_song_menu)
add_song_menu.add_command(label="Add songs", command=choose_songs)
add_song_menu.add_command(label="Remove song", command=remove_song)

# Volume control
volume_label = ttk.Label(root, text="Volume: 70")
volume_label.grid(row=2, column=0, sticky="w", padx=5)

volume_scale = ttk.Scale(root, from_=0, to=100, orient=HORIZONTAL, command=set_volume, length=150)
volume_scale.set(70)  # Set initial volume to 70
volume_scale.grid(row=2, column=1, columnspan=3, sticky="w", padx=5)

# Status bar
status_label = ttk.Label(root, text="Status: Stopped", anchor=W)
status_label.grid(row=3, column=0, columnspan=5, sticky="w", padx=5)

# Current song label
current_song_label = ttk.Label(root, text="Current Song: None", anchor=W)
current_song_label.grid(row=4, column=0, columnspan=5, sticky="w", padx=5)

# Bind keyboard shortcuts
root.bind("<space>", lambda event: pause() if pygame.mixer.music.get_busy() else play())
root.bind("<Left>", lambda event: previous())
root.bind("<Right>", lambda event: next_song())

# Handle end of song event
pygame.mixer.music.set_endevent(pygame.USEREVENT)
root.bind(pygame.USEREVENT, lambda event: on_song_end())

# Styling
style = ttk.Style()
style.configure("TScale", sliderthickness=10, troughcolor="gray", sliderrelief="flat", sliderlength=25, troughrelief="flat")

mainloop()
