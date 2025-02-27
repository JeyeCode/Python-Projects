import os
import time
import threading
from instagrapi import Client, exceptions
import tkinter as tk
from tkinter import filedialog, messagebox, font
import signal
import sys


class InstagramBot:
    def __init__(self):
        self.cl = Client()
        self.last_message_texts = {}
        self.database = []
        self.message_text = ""
        self.username = ""
        self.password = ""
        self.running = False

    def login(self, username, password):
        """Log in to Instagram."""
        self.username = username
        self.password = password

        try:
            self.cl.login(username, password)
            print("Logged Successfully...")
            return True
        except Exception as e:
            print(f"User And Password is Incurrect ...")
            return False

    def send_photo_reply(self, thread_id):
        """Send a photo in response to a message."""
        try:
            time.sleep(3)
            self.cl.direct_send_photo(image_path_entry.get(), thread_ids=[thread_id])
            print("All Photoes Succesfully Shared ...")
        except Exception as e:
            print(f"Error sending photo: {str(e)}")

    def reply_to_message(self, thread_id):
        """Send text replies to a message using the database."""
        try:
            for data in self.database:
                self.cl.direct_answer(thread_id, data)
            print(f"All Data Succesfully Shared ...")
        except Exception as e:
            print(f"Error sending reply: {str(e)}")

    def check_messages(self):
        """Fetch all direct threads and process messages."""
        while self.running:
            try:
                threads = self.cl.direct_threads()
                if not threads:
                    print("No threads found.")
                    time.sleep(5)
                    continue

                for index, thread in enumerate(threads, start=1):
                    last_message = thread.messages[0] if thread.messages else None

                    if last_message is not None:
                        self.message_text = last_message.text

                        if index not in self.last_message_texts:
                            self.last_message_texts[index] = ""

                        if self.message_text and self.message_text.strip():
                            if self.message_text != self.last_message_texts[index]:
                                self.last_message_texts[index] = self.message_text

                                if self.message_text.lower() == "yo":
                                    reply_thread = threading.Thread(target=self.reply_to_message,
                                                                    args=(last_message.thread_id,))
                                    photo_thread = threading.Thread(target=self.send_photo_reply,
                                                                    args=(last_message.thread_id,))

                                    reply_thread.start()
                                    reply_thread.join()

                                    time.sleep(1)
                                    photo_thread.start()
                                    photo_thread.join()
                    else:
                        print("Bot is Waiting For New Messege ...")
            except exceptions.LoginRequired:
                print("Login required. Attempting to log in again.\n Check Your Phone To Login Again To Continue ...")
                self.login(self.username, self.password)

            except Exception as e:
                print(f"Error in message checking: {str(e)}")
                time.sleep(5)


def start_bot():
    global bot
    username = username_entry.get()
    password = password_entry.get()

    bot = InstagramBot()

    story_path = story_path_entry.get().strip()
    audio_path = audio_path_entry.get().strip()
    video_path = video_path_entry.get().strip()

    bot.database.append(story_path)
    bot.database.append(audio_path)
    bot.database.append(video_path)

    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password.")
        return

    try:
        if bot.login(username, password):
            messagebox.showinfo("Success", "Logged in successfully.")
            bot.running = True
            status_label.config(text="Connecting...", fg="blue")
            threading.Thread(target=bot.check_messages, daemon=True).start()
            status_label.config(text="Connected", fg="green")
    except Exception as e:
        messagebox.showerror("Login Failed", str(e))


def stop_bot():
    global bot
    if bot:
        bot.running = False
        status_label.config(text="Disconnected", fg="red")
        print("Bot stopped.")
        os.kill(os.getpid(), signal.SIGINT)  # Simulate Ctrl+C  


def browse_file(entry_widget):
    """Open a file dialog and insert the selected file path into the entry widget."""
    filename = filedialog.askopenfilename(title="Select a file")
    if filename:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, filename)

    # Custom class to redirect stdout and stderr to the Text widget


class TextRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert(tk.END, text)
        self.widget.see(tk.END)  # Auto-scroll to the end

    def flush(self):
        pass


# Create the main window
root = tk.Tk()
root.title("JEYCODE IB")
root.geometry("500x700")
root.configure(bg="#f0f0f0")

# Center the window on the screen  
window_width = 500
window_height = 700
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Create a custom font  
custom_font = font.Font(family="Helvetica", size=12)

# Create and style the labels and entries  
tk.Label(root, text="Username", bg="#f0f0f0", font=custom_font).grid(row=0, column=0, pady=10, padx=10)
username_entry = tk.Entry(root, font=custom_font, width=30)
username_entry.grid(row=0, column=1, pady=10, padx=10)

tk.Label(root, text="Password", bg="#f0f0f0", font=custom_font).grid(row=1, column=0, pady=10, padx=10)
password_entry = tk.Entry(root, show='*', font=custom_font, width=30)
password_entry.grid(row=1, column=1, pady=10, padx=10)

# Add "Connect" and "Disconnect" buttons  
button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.grid(row=2, column=0, columnspan=3, pady=20)

connect_button = tk.Button(button_frame, text="Connect", command=start_bot, font=custom_font, bg="#5cb85c", fg="white")
connect_button.pack(side=tk.LEFT, padx=10)

disconnect_button = tk.Button(button_frame, text="Disconnect", command=stop_bot, font=custom_font, bg="#d9534f",
                              fg="white")
disconnect_button.pack(side=tk.LEFT, padx=10)

# Image Path  
tk.Label(root, text="Image Path", bg="#f0f0f0", font=custom_font).grid(row=3, column=0, pady=10, padx=10)
image_path_entry = tk.Entry(root, font=custom_font, width=30)
image_path_entry.grid(row=3, column=1, pady=10, padx=10)
tk.Button(root, text="Browse", command=lambda: browse_file(image_path_entry), font=custom_font).grid(row=3, column=2,
                                                                                                     pady=10)

# Story Path  
tk.Label(root, text="Story Path", bg="#f0f0f0", font=custom_font).grid(row=4, column=0, pady=10, padx=10)
story_path_entry = tk.Entry(root, font=custom_font, width=30)
story_path_entry.grid(row=4, column=1, pady=10, padx=10)
tk.Button(root, text="Browse", command=lambda: browse_file(story_path_entry), font=custom_font).grid(row=4, column=2,
                                                                                                     pady=10)

# Post Path  
tk.Label(root, text="Post Path", bg="#f0f0f0", font=custom_font).grid(row=5, column=0, pady=10, padx=10)
audio_path_entry = tk.Entry(root, font=custom_font, width=30)
audio_path_entry.grid(row=5, column=1, pady=10, padx=10)
tk.Button(root, text="Browse", command=lambda: browse_file(audio_path_entry), font=custom_font).grid(row=5, column=2,
                                                                                                     pady=10)

# Video Path  
tk.Label(root, text="Video Path", bg="#f0f0f0", font=custom_font).grid(row=6, column=0, pady=10, padx=10)
video_path_entry = tk.Entry(root, font=custom_font, width=30)
video_path_entry.grid(row=6, column=1, pady=10, padx=10)
tk.Button(root, text="Browse", command=lambda: browse_file(video_path_entry), font=custom_font).grid(row=6, column=2,
                                                                                                     pady=10)

# Add status label  
status_label = tk.Label(root, text="Not Connected", bg="#f0f0f0", font=custom_font, fg="red")
status_label.grid(row=7, columnspan=3, pady=10)

# Add a Text widget for terminal output  
terminal_label = tk.Label(root, bg="#f0f0f0", font=custom_font)
terminal_label.grid(row=8, column=0, columnspan=3, pady=10)

terminal_output = tk.Text(root, wrap=tk.WORD, height=10, width=50)
terminal_output.grid(row=9, column=0, columnspan=3, padx=10, pady=10)

# Redirect stdout and stderr to the Text widget  
sys.stdout = TextRedirector(terminal_output)
sys.stderr = TextRedirector(terminal_output)

# Start the Tkinter event loop  
root.mainloop()
