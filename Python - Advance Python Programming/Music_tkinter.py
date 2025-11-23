import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import mysql.connector
import os
import subprocess
import platform

# ---------------------------
# DATABASE CONNECTION
# ---------------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",     
        password="",      
        database="musicbox_db"
    )

# ---------------------------
# OPEN SONG (CROSS-PLATFORM)
# ---------------------------
def open_song(filepath):
    """Open the song file with the system's default music player"""
    try:
        if platform.system() == "Windows":
            os.startfile(filepath)
        elif platform.system() == "Darwin":  
            subprocess.Popen(["open", filepath])
        else:  # Linux
            subprocess.Popen(["xdg-open", filepath])
    except Exception as e:
        messagebox.showerror("Error", f"Could not open file:\n{e}")

# ---------------------------
# MAIN APP CLASS
# ---------------------------
class MusicBoxApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎶 MusicBox Playlist Manager")
        self.root.geometry("800x550")
        self.root.config(bg="#f4f4f4")

        # ---------- HEADER ----------
        tk.Label(root, text="🎶 MusicBox Playlist Manager",
                 font=("Segoe UI", 18, "bold"), bg="#f4f4f4", fg="#222").pack(pady=10)

        # ---------- CREATE PLAYLIST ----------
        create_frame = tk.Frame(root, bg="#f4f4f4")
        create_frame.pack(pady=5)

        tk.Label(create_frame, text="Playlist Name:", bg="#f4f4f4",
                 font=("Segoe UI", 11)).grid(row=0, column=0, sticky="e", padx=5)
        self.name_entry = tk.Entry(create_frame, width=30, font=("Segoe UI", 11))
        self.name_entry.grid(row=0, column=1, padx=5)

        tk.Button(create_frame, text="📁 Add Songs", command=self.add_songs,
                  bg="#4CAF50", fg="white", relief="flat", padx=10).grid(row=0, column=2, padx=10)

        self.song_list = tk.Listbox(root, width=70, height=6, font=("Consolas", 10),
                                    selectbackground="#cce5ff", activestyle="none")
        self.song_list.pack(pady=5)

        tk.Button(root, text="💾 Save Playlist", command=self.save_playlist,
                  bg="#2196F3", fg="white", relief="flat", padx=15).pack(pady=5)

        ttk.Separator(root, orient='horizontal').pack(fill='x', pady=15)

        # ---------- VIEW PLAYLISTS ----------
        main_frame = tk.Frame(root, bg="#f4f4f4")
        main_frame.pack(pady=5)

        # LEFT
        left_frame = tk.Frame(main_frame, bg="#f4f4f4")
        left_frame.pack(side="left", padx=20)

        tk.Label(left_frame, text="Existing Playlists:",
                 bg="#f4f4f4", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        self.playlist_box = tk.Listbox(left_frame, width=30, height=10, font=("Consolas", 10),
                                       selectbackground="#cce5ff", activestyle="none")
        self.playlist_box.pack(pady=5)
        self.playlist_box.bind("<<ListboxSelect>>", self.load_songs)  

        # RIGHT
        right_frame = tk.Frame(main_frame, bg="#f4f4f4")
        right_frame.pack(side="left", padx=20)

        tk.Label(right_frame, text="Songs in Playlist:",
                 bg="#f4f4f4", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        self.song_box = tk.Listbox(right_frame, width=50, height=10, font=("Consolas", 10),
                                   selectbackground="#cce5ff", selectmode=tk.SINGLE, activestyle="none")
        self.song_box.pack(pady=5)

        # ---------- CRUD BUTTONS ----------
        btn_frame = tk.Frame(root, bg="#f4f4f4")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="▶ Play Song", command=self.play_selected_song,
                  bg="#009688", fg="white", width=12, relief="flat").grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="➕ Add Song", command=self.add_song_to_existing,
                  bg="#4CAF50", fg="white", width=12, relief="flat").grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="❌ Delete Song", command=self.delete_song,
                  bg="#E91E63", fg="white", width=12, relief="flat").grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="🗑 Delete Playlist", command=self.delete_playlist,
                  bg="#9C27B0", fg="white", width=14, relief="flat").grid(row=0, column=3, padx=5)

        # ---------- STATE VARIABLES ----------
        self.selected_files = []
        self.current_songs = []
        self.current_playlist_id = None

        self.load_playlists()

    # ---------------- ADD SONGS ----------------
    def add_songs(self):
        files = filedialog.askopenfilenames(title="Select Songs",
            filetypes=[("Audio Files", "*.mp3 *.wav *.ogg *.flac")])
        if files:
            self.selected_files = list(files)
            self.song_list.delete(0, tk.END)
            for f in self.selected_files:
                self.song_list.insert(tk.END, os.path.basename(f))

    # ---------------- SAVE PLAYLIST ----------------
    def save_playlist(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter a playlist name.")
            return
        if not self.selected_files:
            messagebox.showerror("Error", "No songs selected.")
            return

        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT id FROM playlists WHERE name=%s", (name,))
            if cur.fetchone():
                messagebox.showerror("Error", "Playlist already exists!")
                conn.close()
                return

            cur.execute("INSERT INTO playlists (name) VALUES (%s)", (name,))
            pid = cur.lastrowid
            for path in self.selected_files:
                cur.execute(
                    "INSERT INTO songs (playlist_id, title, filepath) VALUES (%s, %s, %s)",
                    (pid, os.path.basename(path), path)
                )
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Playlist '{name}' saved!")
            self.song_list.delete(0, tk.END)
            self.name_entry.delete(0, tk.END)
            self.selected_files = []
            self.load_playlists()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))

    # ---------------- LOAD PLAYLISTS ----------------
    def load_playlists(self, event=None):
        self.playlist_box.delete(0, tk.END)
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT name FROM playlists ORDER BY id DESC")
        for (name,) in cur.fetchall():
            self.playlist_box.insert(tk.END, name)
        conn.close()

    # ---------------- LOAD SONGS ----------------
    def load_songs(self, event=None):
        """Load songs of selected playlist (only if changed)"""
        sel = self.playlist_box.curselection()
        if not sel:
            return

        # Get the name of the selected playlist
        name = self.playlist_box.get(sel[0])

        # Prevent reloading if same playlist clicked again
        if hasattr(self, "last_selected_playlist") and self.last_selected_playlist == name:
            return
        self.last_selected_playlist = name  
        self.song_box.delete(0, tk.END)

        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT id FROM playlists WHERE name=%s", (name,))
            result = cur.fetchone()
            if not result:
                return
            pid = result[0]
            cur.execute("SELECT title, filepath FROM songs WHERE playlist_id=%s", (pid,))
            self.current_songs = cur.fetchall()
            conn.close()

            for title, _ in self.current_songs:
                self.song_box.insert(tk.END, title)
            self.current_playlist_id = pid
        except Exception as e:
            messagebox.showerror("Error", str(e))


    # ---------------- PLAY SONG ----------------
    def play_selected_song(self):
        """Play selected song from the listbox."""
        selection = self.song_box.curselection()
        if not selection:
            messagebox.showwarning("Select Song", "Please select a song to play.")
            return
        index = selection[0]
        title, path = self.current_songs[index]
        if os.path.exists(path):
            open_song(path)
        else:
            messagebox.showerror("Error", f"File not found:\n{path}")

    # ---------------- ADD SONG ----------------
    def add_song_to_existing(self):
        if not self.current_playlist_id:
            messagebox.showerror("Error", "Select a playlist first.")
            return
        files = filedialog.askopenfilenames(title="Add Songs")
        if not files:
            return
        conn = get_connection()
        cur = conn.cursor()
        for path in files:
            cur.execute(
                "INSERT INTO songs (playlist_id, title, filepath) VALUES (%s, %s, %s)",
                (self.current_playlist_id, os.path.basename(path), path)
            )
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Songs added!")
        self.load_songs(None)

    # ---------------- DELETE SONG ----------------
    def delete_song(self):
        sel = self.song_box.curselection()
        if not sel:
            messagebox.showerror("Error", "Select a song to delete.")
            return
        title, _ = self.current_songs[sel[0]]
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM songs WHERE title=%s AND playlist_id=%s",
                    (title, self.current_playlist_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Deleted", f"Song '{title}' removed.")
        self.load_songs(None)

    # ---------------- DELETE PLAYLIST ----------------
    def delete_playlist(self):
        sel = self.playlist_box.curselection()
        if not sel:
            messagebox.showerror("Error", "Select a playlist to delete.")
            return
        name = self.playlist_box.get(sel[0])
        if not messagebox.askyesno("Confirm", f"Delete playlist '{name}'?"):
            return
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM playlists WHERE name=%s", (name,))
        pid = cur.fetchone()[0]
        cur.execute("DELETE FROM songs WHERE playlist_id=%s", (pid,))
        cur.execute("DELETE FROM playlists WHERE id=%s", (pid,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Deleted", f"Playlist '{name}' deleted.")
        self.song_box.delete(0, tk.END)
        self.load_playlists()



# RUN APP

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicBoxApp(root)
    root.mainloop()
