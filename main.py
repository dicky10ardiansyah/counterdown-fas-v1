import tkinter as tk
from tkinter import messagebox
import pygame
import threading
import sys
import os

# Inisialisasi pygame mixer untuk memainkan file audio
pygame.mixer.init()

# Cek apakah aplikasi dijalankan dalam mode standalone (bundle dengan PyInstaller)
if getattr(sys, 'frozen', False):
    # Jika aplikasi dijalankan sebagai executable (PyInstaller)
    application_path = sys._MEIPASS
else:
    # Jika aplikasi dijalankan sebagai skrip Python biasa
    application_path = os.path.abspath(".")

# Membuat jalur lengkap untuk file audio
beep_path = os.path.join(application_path, "beep.mp3")
buzzer_path = os.path.join(application_path, "buzzer.mp3")

def start_countdown():
    try:
        # Menghilangkan teks "Waktu Habis" saat mulai countdown baru
        time_up_label.config(text="")

        # Ambil waktu dari entry
        minutes = int(minutes_entry.get())
        seconds = int(seconds_entry.get())
        total_seconds = minutes * 60 + seconds
        countdown(total_seconds)
    except ValueError:
        messagebox.showerror("Error", "Masukkan waktu dengan benar.")

def countdown(total_seconds):
    if total_seconds > 0:
        minutes, seconds = divmod(total_seconds, 60)
        time_display = f"{minutes:02}:{seconds:02}"
        timer_label.config(text=time_display)

        # Ubah warna teks menjadi merah jika sisa waktu 10 detik atau kurang
        if total_seconds <= 10:
            timer_label.config(fg="red")
            # Putar suara beep di thread terpisah
            threading.Thread(target=play_beep).start()
        else:
            timer_label.config(fg="#212529")  # Warna default (hitam)

        root.after(1000, countdown, total_seconds - 1)
    else:
        timer_label.config(text="00:00")
        # Jangan mengubah teks time_up_label, atau biarkan tetap kosong
        # time_up_label.config(text="Waktu Habis", fg="red")  # Hapus atau komentari baris ini
        # Putar suara buzzer di thread terpisah ketika waktu habis
        threading.Thread(target=play_buzzer).start()

# Fungsi untuk memutar suara beep
def play_beep():
    pygame.mixer.music.load(beep_path)  # Gunakan jalur yang benar
    pygame.mixer.music.play()

# Fungsi untuk memutar suara buzzer
def play_buzzer():
    pygame.mixer.music.load(buzzer_path)  # Gunakan jalur yang benar
    pygame.mixer.music.play()

# Fungsi untuk memvalidasi input angka saja
def validate_input(P):
    if P == "" or P.isdigit():  # Izinkan string kosong atau hanya angka
        return True
    else:
        return False

# Membuat GUI
root = tk.Tk()
root.title("(FAS) Festival Anak Sholeh 2024")  # Title bar tetap ada
root.geometry("600x600")  # Ukuran awal layar
root.configure(bg="#f8f9fa")

# Menambahkan judul dengan background hitam
title_label = tk.Label(root, text="(FAS) Festival Anak Sholeh 2024", font=("Helvetica", 24, "bold"), bg="black", fg="white", pady=20)
title_label.pack(fill=tk.X)

# Fungsi untuk membuat frame dengan sudut melengkung menggunakan canvas
def create_rounded_frame(parent, width, height, bg_color, corner_radius):
    canvas = tk.Canvas(parent, width=width, height=height, bg=bg_color, bd=0, highlightthickness=0)
    canvas.pack_propagate(False)
    
    # Membuat latar belakang dengan sudut melengkung
    canvas.create_rectangle(
        corner_radius, 0, width - corner_radius, height, fill=bg_color, outline=bg_color
    )
    canvas.create_rectangle(
        0, corner_radius, width, height - corner_radius, fill=bg_color, outline=bg_color
    )
    canvas.create_oval(
        0, 0, corner_radius * 2, corner_radius * 2, fill=bg_color, outline=bg_color
    )
    canvas.create_oval(
        width - corner_radius * 2, 0, width, corner_radius * 2, fill=bg_color, outline=bg_color
    )
    canvas.create_oval(
        0, height - corner_radius * 2, corner_radius * 2, height, fill=bg_color, outline=bg_color
    )
    canvas.create_oval(
        width - corner_radius * 2, height - corner_radius * 2, width, height, fill=bg_color, outline=bg_color
    )
    
    return canvas

# Timer tanpa Card (Pindahkan posisi ke atas)
timer_label = tk.Label(root, text="00:00", font=("Helvetica", 180, "bold"), bg="#f8f9fa", fg="#212529", pady=40)
timer_label.pack(pady=30)  # Padding lebih kecil agar timer di atas card

# Card Input (Rounded Frame)
input_card = create_rounded_frame(root, width=400, height=150, bg_color="white", corner_radius=20)
input_card.pack(pady=40)  # Padding lebih besar agar ada jarak antara card dan timer

# Masukkan elemen ke dalam card
inner_frame = tk.Frame(input_card, bg="white")
inner_frame.place(x=0, y=0, width=400, height=150)

tk.Label(inner_frame, text="Masukkan Waktu", font=("Helvetica", 14, "bold"), bg="white", fg="#495057").pack(pady=10)

input_frame = tk.Frame(inner_frame, bg="white")
input_frame.pack()

tk.Label(input_frame, text="Menit:", font=("Helvetica", 12), bg="white", fg="#495057").pack(side=tk.LEFT, padx=5)

# Mendaftarkan validatecommand untuk validasi input
vcmd = root.register(validate_input)

minutes_entry = tk.Entry(input_frame, width=5, font=("Helvetica", 12), justify="center", validate="key", validatecommand=(vcmd, "%P"))
minutes_entry.pack(side=tk.LEFT, padx=5)

tk.Label(input_frame, text="Detik:", font=("Helvetica", 12), bg="white", fg="#495057").pack(side=tk.LEFT, padx=5)
seconds_entry = tk.Entry(input_frame, width=5, font=("Helvetica", 12), justify="center", validate="key", validatecommand=(vcmd, "%P"))
seconds_entry.pack(side=tk.LEFT, padx=5)

# Tombol
start_button = tk.Button(inner_frame, text="Mulai", command=start_countdown, font=("Helvetica", 12), bg="#007bff", fg="white", 
                         activebackground="#0056b3", activeforeground="white", relief="flat", padx=20, pady=5)
start_button.pack(pady=15)

# Label "Waktu Habis"
time_up_label = tk.Label(root, text="", font=("Helvetica", 24, "bold"), bg="#f8f9fa", fg="red")
time_up_label.pack(pady=10)

# Footer
footer = tk.Label(root, text="© 2024 Countdown Timer", font=("Helvetica", 10), bg="#f8f9fa", fg="#adb5bd", pady=10)
footer.pack(side=tk.BOTTOM, fill=tk.X)

# Fungsi untuk fullscreen in (maksimalkan layar)
def fullscreen_in(event=None):
    root.attributes('-fullscreen', True)  # Mengaktifkan fullscreen
    root.bind("<Escape>", fullscreen_out)  # Mengikat tombol Escape untuk keluar fullscreen

# Fungsi untuk fullscreen out (keluar dari fullscreen)
def fullscreen_out(event=None):
    root.attributes('-fullscreen', False)  # Menonaktifkan fullscreen
    root.geometry("600x600")  # Mengembalikan ukuran semula
    root.bind("<Double-1>", fullscreen_in)  # Mengikat double-click untuk fullscreen in

# Mengikat double-click untuk fullscreen in
root.bind("<Double-1>", fullscreen_in)

# Menjalankan loop utama tkinter
root.mainloop()
