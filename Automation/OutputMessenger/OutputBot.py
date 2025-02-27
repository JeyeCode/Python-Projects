import pymssql
import requests
from datetime import datetime
import time
import threading


class ChatNotifier:
    def __init__(self):
        # Global list to store temperature values
        self.Temp = []
        # Define the menu list as a string
        self.menu_list = """
        1. Test
        2. Database A
        3. Database B
        4. Option C
        """

    def database(self):
        """Continuously fetch temperature data from SQL Server database"""
        while True:
            try:
                # Establish database connection using context manager
                with pymssql.connect(
                    server='DESKTOP-AGV9CJP\JEY',
                    database='Python',
                    # trusted=True  # Uncomment for Windows authentication
                ) as conn:
                    with conn.cursor() as cursor:
                        print("Connected to SQL Server successfully")
                        
                        while True:
                            # Execute query to get all data from TMP table
                            cursor.execute('SELECT * FROM TMP')
                            
                            # Clear previous data and store new results
                            self.Temp.clear()
                            self.Temp.extend(cursor.fetchall())
                            
                            # Add delay between polls (adjust as needed)
                            time.sleep(5)
            except pymssql.OperationalError as e:
                print(f"Connection error: {e}")
                print("Attempting reconnect in 10 seconds...")
                time.sleep(10)
            except Exception as e:
                print(f"Unexpected error in database function: {e}")
                time.sleep(10)  # Retry after a delay


    def notify(self, from_user, room, message, temp_data=None):
        """Helper method to send notifications."""
        api_key = "2238Y12631T8HK05QVV084LTCFCGHYY5"
        if temp_data:
            message = f"{message}: {temp_data[0]}"
        url = f"http://localhost:14125/API/notify?from={from_user}&room={room}&message={message}&color=C7EDFC&otr=0&notify=1"
        headers = {
            "API-KEY": api_key,
            "Accept": "application/json , */*",
            "host": "localhost:14125"
        }
        
        requests.post(url, headers=headers)
           
       
    def send_menu(self, username, room):
        """Send the menu to the specified user and room."""
        url = f"http://localhost:14125/API/notify?from={username}&room={room}&message=Here is the {self.menu_list}&color=C7EDFC&otr=0&notify=1"
        headers = {
            "API-KEY": "2238Y12631T8HK05QVV084LTCFCGHYY5",
            "Accept": "application/json , */*",
            "host": "localhost:14125"
        }
        requests.post(url, headers=headers)


    def UsernameAPI(self):
        """Check user chat logs via API and send notifications."""
        while True:
            try:
                API_CHAT_URL = "http://127.0.0.1:5000/api/Userchats"
                response = requests.get(API_CHAT_URL)
                if response.status_code != 200:
                    print(f"API request failed with status code {response.status_code}. Response: {response.text}")
                    time.sleep(5)
                    continue
                
                current_data = response.json()
                if not isinstance(current_data, list) or not current_data:
                    print("No new chat data available.")
                    time.sleep(5)
                    continue

                for message in current_data:
                    # Extract necessary fields
                    chats = message.get("text", "").strip()  # Message text
                    userna = message.get("username", "").strip()  # Username

                    if not chats or not userna:
                        print(f"Skipping incomplete message: {message}")
                        continue

                    # Handle admin commands
                    if userna.lower() == "admin":
                        if chats == "1":
                            self.notify("admin", "gp", "Your Current Temp is: Admin Testing ..")
                        elif chats == "2":
                            if self.Temp:
                                self.notify("admin", "gp", "Your Current Temp is", temp_data=self.Temp)
                            else:
                                print("Temperature data not available for admin.")
                        elif chats == "start":
                            self.send_menu("admin", "gp")

                    # Handle user commands
                    elif userna.lower() == "user":
                        if chats == "1":
                            self.notify("user", "gp2", "Your Current Temp is : User Testing ...")
                        elif chats == "3":
                            if self.Temp:
                                self.notify("user", "gp2", "Your Current Temp is", temp_data=self.Temp)
                            else:
                                print("Temperature data not available for user.")
                        elif chats == "start":
                            self.send_menu("user", "gp2")

            except Exception as e:
                print(f"An error occurred: {e}")
            time.sleep(5)


    def NotifEmergency(self):
        """Send emergency notifications if temperature exceeds threshold"""
        while True:
            try:
                if self.Temp and self.Temp[0][0] > 5:
                    E_temp = (f"Notification:\n"
                              f"The TEMP OF Rack 13 Is Too High!! >>>>> {self.Temp[0][0]}\n"
                              f"Calling...\n"
                              f"Sending Message...")
                    
                    url = f"http://localhost:14125/API/notify?from=admin&room=gp&message={E_temp}&color=C7EDFC&otr=0&notify=1"
                    api_key = "2238Y12631T8HK05QVV084LTCFCGHYY5"
                    headers = {
                        "API-KEY": api_key,
                        "Accept": "application/json , */*",
                        "host": "localhost:14125"
                    }
                    response = requests.post(url, headers=headers)
                    print("Emergency notification sent")
                
                # Add delay between checks
                time.sleep(10)
            
            except Exception as e:
                print(f"Error in NotifEmergency: {e}")
                time.sleep(10)


# Run the main loop if this script is executed directly
if __name__ == '__main__':
    try:
        notifier = ChatNotifier()
        threads = [
            threading.Thread(target=notifier.database),
            threading.Thread(target=notifier.UsernameAPI),
            threading.Thread(target=notifier.NotifEmergency)
        ]
        
        # Start all threads
        for thread in threads:
            thread.start()
        
        # Wait for all threads to complete (this will keep the program running)
        for thread in threads:
            thread.join()
    
    except KeyboardInterrupt:
        print("Program terminated by user")