from flask import Flask, jsonify
import pandas as pd
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import threading  # Import the threading module here
from GNT import ChatNotifier  # Import the ChatNotifier class

app = Flask(__name__)

# Specify your dynamic CSV files directory here
EXCEL_DIRECTORY = r"C:\Users\Jey\Desktop\Code\Practices\1"

# Dictionary to cache file data and their modification times
file_cache = {}

# Lock to ensure thread-safe access to the cache
cache_lock = threading.Lock()

class DirectoryMonitor(FileSystemEventHandler):
    def on_any_event(self, event):
        """Handle any file system event in the monitored directory."""
        global file_cache
        if event.is_directory:
            return  # Ignore directory events
        file_path = event.src_path
        if file_path.endswith('.csv'):
            print(f"Detected change in file: {file_path}")
            try:
                with cache_lock:
                    # Update the cache for the modified file
                    update_file_in_cache(file_path)
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

def update_file_in_cache(file_path):
    """Update the cache with the latest data from the given CSV file."""
    global file_cache
    try:
        # Check if the file exists and has at least 6 columns
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            if df.shape[1] >= 6 and not df.empty:
                last_row = df.iloc[-1]
                col_4 = str(last_row.iloc[3]) if pd.notna(last_row.iloc[3]) else None
                col_6 = str(last_row.iloc[5]) if pd.notna(last_row.iloc[5]) else None
                # Store the file's modification time and extracted data in the cache
                file_cache[file_path] = {
                    "modification_time": os.path.getmtime(file_path),
                    "data": {"username": col_4, "text": col_6}
                }
                 # Check if the file has reached 5 rows
                # if len(df) >= 10:
                #     print(f"File {file_path} has reached 5 rows. Clearing the file...")
                #     clear_csv_file(file_path)
    except Exception as e:
        print(f"Error updating cache for file {file_path}: {e}")

# def clear_csv_file(file_path):
#     """Clear the contents of the specified CSV file."""
#     try:
#         # Create an empty DataFrame and save it to the file
#         pd.DataFrame().to_csv(file_path, index=False)
#         print(f"Cleared file: {file_path}")
#     except Exception as e:
#         print(f"Error clearing file {file_path}: {e}")

def initialize_cache():
    """Initialize the cache by reading all existing CSV files in the directory."""
    global file_cache
    for root, _, files in os.walk(EXCEL_DIRECTORY):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                update_file_in_cache(file_path)

@app.route('/api/users', methods=['GET'])
def list_users():
    """API endpoint to list users based on cached data."""
    try:
        users_data = []
        with cache_lock:
            for file_path, file_info in file_cache.items():
                users_data.append(file_info["data"])
        return jsonify(users_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/Userchats', methods=['GET'])
def get_user_chats():
    """API endpoint to get user chats based on cached data."""
    try:
        user_chats = []
        with cache_lock:
            for file_path, file_info in file_cache.items():
                user_chats.append(file_info["data"])
        if not user_chats:
            return jsonify({'message': 'No chat logs found.'}), 404
        return jsonify(user_chats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def start_monitoring():
    """Start monitoring the directory for changes."""
    event_handler = DirectoryMonitor()
    observer = Observer()
    observer.schedule(event_handler, path=EXCEL_DIRECTORY, recursive=True)
    observer.start()
    print("Monitoring started...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def run_chat_notifier():
    """Run the ChatNotifier methods in separate threads."""
    notifier = ChatNotifier()
    threads = [
        threading.Thread(target=notifier.database, daemon=True),
        threading.Thread(target=notifier.UsernameAPI, daemon=True),
        threading.Thread(target=notifier.NotifEmergency, daemon=True)
    ]
    for thread in threads:
        thread.start()
        time.sleep(5)
    for thread in threads:
        thread.join()
        time.sleep(5)



if __name__ == '__main__':
    # Initialize the cache with existing files
    initialize_cache()

    # Start the directory monitoring in a separate thread
    monitoring_thread = threading.Thread(target=start_monitoring, daemon=True)
    monitoring_thread.start()

    # Start the ChatNotifier methods in separate threads
    chat_notifier_thread = threading.Thread(target=run_chat_notifier, daemon=True)
    chat_notifier_thread.start()

    # Run the Flask app
    app.run(debug=True)
    
    
    
    