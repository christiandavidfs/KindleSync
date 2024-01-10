import os
import csv
import tkinter as tk
from tkinter import filedialog
import threading
import shutil
import time

class KindleSyncApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kindle Sync App")
        self.root.geometry("400x400")  # Set an initial fixed size

        # Variables for the paths
        self.books_folder_path = tk.StringVar()
        self.dest_folder_path = tk.StringVar()

        # Load paths from CSV
        self.load_paths_from_csv()

        # Flag to indicate synchronization thread status
        self.sync_thread_running = False

        # Last displayed synchronization status
        self.last_sync_status = ""

        # GUI
        self.create_widgets()

    def create_widgets(self):
        self.root.pack_propagate(False)  # Prevent automatic resizing

        tk.Button(self.root, text="Select Books Folder", command=self.select_books_folder).pack(pady=10)
        tk.Button(self.root, text="Select Destination Folder", command=self.select_dest_folder).pack(pady=10)

        tk.Label(self.root, textvariable=self.books_folder_path).pack()
        tk.Label(self.root, textvariable=self.dest_folder_path).pack()

        tk.Button(self.root, text="Start Sync", command=self.start_sync_thread).pack(pady=10)

        # Text widget to display synchronization status
        self.sync_status_text = tk.Text(self.root, height=10, width=40, wrap="word")
        self.sync_status_text.pack(pady=10)

    def select_books_folder(self):
        folder_path = filedialog.askdirectory()
        self.books_folder_path.set(folder_path)

    def select_dest_folder(self):
        folder_path = filedialog.askdirectory()
        self.dest_folder_path.set(folder_path)

    def load_paths_from_csv(self):
        if os.path.exists("paths.csv"):
            with open("paths.csv", "r") as csv_file:
                csv_reader = csv.reader(csv_file)
                rows = list(csv_reader)
                if len(rows) == 2:
                    self.books_folder_path.set(rows[0][0])
                    self.dest_folder_path.set(rows[1][0])

    def save_paths_to_csv(self):
        with open("paths.csv", "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([self.books_folder_path.get()])
            csv_writer.writerow([self.dest_folder_path.get()])

    def sync_folders(self):
        books_path = self.books_folder_path.get()
        dest_path = self.dest_folder_path.get()

        try:
            self.update_sync_status("Copying from Books to Destination")
            # Synchronize changes from books folder to destination folder
            shutil.rmtree(dest_path)
            shutil.copytree(books_path, dest_path)

            self.update_sync_status("Copying from Destination to Books")
            # Synchronize changes from destination folder to books folder
            shutil.rmtree(books_path)
            shutil.copytree(dest_path, books_path)

            self.update_sync_status("Sync Completed")

        except Exception as e:
            self.update_sync_status(f"Sync Error - {e}")

    def sync_thread(self):
        while self.sync_thread_running:
            dest_path = self.dest_folder_path.get()
            if os.path.exists(dest_path):
                self.sync_folders()
                break
            else:
                self.update_sync_status("Waiting for Destination Folder...")
                time.sleep(1)

        self.sync_thread_running = False

    def start_sync_thread(self):
        if not self.sync_thread_running:
            # Start a new thread for synchronization
            self.sync_thread_running = True
            sync_thread = threading.Thread(target=self.sync_thread)
            sync_thread.start()

    def update_sync_status(self, message):
        if message != self.last_sync_status:
            current_status = self.sync_status_text.get("1.0", tk.END).strip()
            new_status = f"{current_status}\n{message}"
            self.sync_status_text.delete("1.0", tk.END)
            self.sync_status_text.insert(tk.END, new_status)
            self.last_sync_status = message

# Initialize the application
root = tk.Tk()
app = KindleSyncApp(root)
root.mainloop()
