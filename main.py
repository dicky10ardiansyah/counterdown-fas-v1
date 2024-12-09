import tkinter as tk
from tkinter import messagebox
import pygame
import datetime
import os
import sys

# Initialize pygame mixer for playing audio
pygame.mixer.init()

# Global variables for countdown management
is_counting_down = False
total_seconds = 0

def get_resource_path(relative_path):
    """Return the absolute path to a resource, works for development and PyInstaller bundle."""
    try:
        # PyInstaller creates a temp folder and stores the path in _MEIPASS
        if getattr(sys, 'frozen', False):
            # If running as a bundled app, use _MEIPASS
            base_path = sys._MEIPASS
        else:
            # If running in a normal Python environment, use the current directory
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    except Exception as e:
        print(f"Error getting resource path: {e}")
        return relative_path  # Return relative path if there's an issue

def play_beep():
    beep_path = get_resource_path("beep.mp3")
    pygame.mixer.music.load(beep_path)
    pygame.mixer.music.play()

def play_buzzer():
    buzzer_path = get_resource_path("buzzer.mp3")
    pygame.mixer.music.load(buzzer_path)
    pygame.mixer.music.play()

def start_countdown():
    global is_counting_down, total_seconds
    try:
        time_up_label.config(text="")
        minutes = int(minutes_entry.get())
        seconds = int(seconds_entry.get())
        total_seconds = minutes * 60 + seconds
        is_counting_down = True
        countdown()  # Start countdown
    except ValueError:
        messagebox.showerror("Error", "Masukkan waktu dengan benar.")

def countdown():
    global total_seconds, is_counting_down
    if total_seconds > 0 and is_counting_down:
        minutes, seconds = divmod(total_seconds, 60)
        time_display = f"{minutes:02}:{seconds:02}"
        timer_label.config(text=time_display)

        if total_seconds <= 10:
            timer_label.config(fg="red")
            play_beep()  # Play beep sound if less than 10 seconds
        else:
            timer_label.config(fg="#212529")  # Default color

        total_seconds -= 1
        root.after(1000, countdown)  # Call countdown every second
    elif total_seconds == 0:
        timer_label.config(text="00:00")
        play_buzzer()  # Play buzzer when time is up

def stop_countdown():
    global is_counting_down
    is_counting_down = False

def reset_countdown():
    global is_counting_down, total_seconds
    is_counting_down = False
    total_seconds = 0
    timer_label.config(text="00:00")
    time_up_label.config(text="")
    pygame.mixer.music.stop()  # Stop any sound

def validate_input(P):
    return P == "" or P.isdigit()  # Validate input is a number or empty

def continue_countdown():
    global is_counting_down
    if not is_counting_down and total_seconds > 0:
        is_counting_down = True
        countdown()  # Resume countdown from where it stopped

root = tk.Tk()
root.title(f"(FAS) Festival Anak Sholeh {datetime.datetime.now().year}")  # Use current year here
root.geometry("600x600")
root.configure(bg="#f8f9fa")

title_label = tk.Label(root, text=f"(FAS) Festival Anak Sholeh {datetime.datetime.now().year}", font=("Helvetica", 24, "bold"), bg="black", fg="white", pady=20)
title_label.pack(fill=tk.X)

timer_label = tk.Label(root, text="00:00", font=("Helvetica", 180, "bold"), bg="#f8f9fa", fg="#212529", pady=40)
timer_label.pack(pady=30)

# Removed card style, directly place inputs here
tk.Label(root, text="Masukkan Waktu", font=("Helvetica", 14, "bold"), bg="white", fg="#495057").pack(pady=10)

input_frame = tk.Frame(root, bg="white")
input_frame.pack()

tk.Label(input_frame, text="Menit:", font=("Helvetica", 12), bg="white", fg="#495057").pack(side=tk.LEFT, padx=5)

vcmd = root.register(validate_input)

minutes_entry = tk.Entry(input_frame, width=5, font=("Helvetica", 12), justify="center", validate="key", validatecommand=(vcmd, "%P"))
minutes_entry.pack(side=tk.LEFT, padx=5)

tk.Label(input_frame, text="Detik:", font=("Helvetica", 12), bg="white", fg="#495057").pack(side=tk.LEFT, padx=5)
seconds_entry = tk.Entry(input_frame, width=5, font=("Helvetica", 12), justify="center", validate="key", validatecommand=(vcmd, "%P"))
seconds_entry.pack(side=tk.LEFT, padx=5)

# Control Buttons
button_frame = tk.Frame(root, bg="white")
button_frame.pack(pady=20)

start_button = tk.Button(button_frame, text="Mulai", command=start_countdown, font=("Helvetica", 12), bg="#007bff", fg="white", activebackground="#0056b3", activeforeground="white", relief="flat", padx=20, pady=5)
start_button.grid(row=0, column=0, padx=10)

stop_button = tk.Button(button_frame, text="Stop", command=stop_countdown, font=("Helvetica", 12), bg="#dc3545", fg="white", activebackground="#c82333", activeforeground="white", relief="flat", padx=20, pady=5)
stop_button.grid(row=0, column=1, padx=10)

reset_button = tk.Button(button_frame, text="Reset", command=reset_countdown, font=("Helvetica", 12), bg="#28a745", fg="white", activebackground="#218838", activeforeground="white", relief="flat", padx=20, pady=5)
reset_button.grid(row=0, column=2, padx=10)

continue_button = tk.Button(button_frame, text="Lanjutkan", command=continue_countdown, font=("Helvetica", 12), bg="#ffc107", fg="white", activebackground="#e0a800", activeforeground="white", relief="flat", padx=20, pady=5)
continue_button.grid(row=0, column=3, padx=10)

time_up_label = tk.Label(root, text="", font=("Helvetica", 24, "bold"), bg="#f8f9fa", fg="red")
time_up_label.pack(pady=10)

# Dynamically update the year in the footer
current_year = datetime.datetime.now().year
footer = tk.Label(root, text=f"© {current_year} Countdown Timer", font=("Helvetica", 10), bg="#f8f9fa", fg="#adb5bd", pady=10)
footer.pack(side=tk.BOTTOM, fill=tk.X)

def fullscreen_in(event=None):
    root.attributes('-fullscreen', True)
    root.bind("<Escape>", fullscreen_out)

def fullscreen_out(event=None):
    root.attributes('-fullscreen', False)
    root.geometry("600x600")
    root.bind("<Double-1>", fullscreen_in)

root.bind("<Double-1>", fullscreen_in)

root.mainloop()
