import os
import csv
import tkinter as tk
from tkinter import filedialog
import shutil

class KindleSyncApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kindle Sync App")

        # Variables for the paths
        self.books_folder_path = tk.StringVar()
        self.dest_folder_path = tk.StringVar()

        # Load paths from CSV
        self.load_paths_from_csv()

        # GUI
        self.create_widgets()

    def create_widgets(self):
        tk.Button(self.root, text="Select Books Folder", command=self.select_books_folder).pack(pady=10)
        tk.Button(self.root, text="Select Destination Folder", command=self.select_dest_folder).pack(pady=10)

        tk.Label(self.root, textvariable=self.books_folder_path).pack()
        tk.Label(self.root, textvariable=self.dest_folder_path).pack()

        tk.Button(self.root, text="Start Sync", command=self.sync_folders).pack(pady=10)

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
            # Synchronize changes from books folder to destination folder
            shutil.rmtree(dest_path)
            shutil.copytree(books_path, dest_path)

            # Synchronize changes from destination folder to books folder
            shutil.rmtree(books_path)
            shutil.copytree(dest_path, books_path)

            tk.messagebox.showinfo("Sync Completed", "Synchronization completed successfully.")

        except Exception as e:
            tk.messagebox.showerror("Sync Error", f"Error during synchronization: {e}")

    def __del__(self):
        pass

# Initialize the application
root = tk.Tk()
app = KindleSyncApp(root)
root.mainloop()
