#JeyCode
import pyautogui
import webbrowser
from time import sleep
import pyperclip

# Define the phone number and message
numero = "+981111111111"
texto = "Salam Chetori?" / "How r u?!"
rango = 1

# Open WhatsApp Web
webbrowser.open("https://web.whatsapp.com/" + numero)
sleep(15)  # Wait for WhatsApp Web to load (increase if necessary)

# Ensure the browser is in focus
print("Please make sure the browser window is active.")
sleep(5)  # Give you time to click on the browser

# Send a message
for i in range(rango):
    pyautogui.typewrite(texto)
    pyautogui.press("enter")
    print("Success Connected To WhatsApp Web")

# Wait for a moment before retrieving the last message
sleep(5)

# Click on the chat with the specified number (you may need to adjust this)
# You can use pyautogui's position function to get coordinates if needed
pyautogui.click(x=369, y=328)  # Adjust x and y coordinates as needed

# Wait for the chat to load
sleep(2)

# # Scroll up to ensure we can see previous messages (optional)
# pyautogui.scroll(-300)  # Scroll up to see previous messages

# # Wait a moment for messages to load
# sleep(2)

# Use pyautogui to select the last message (adjust coordinates)
pyautogui.moveTo(x=831, y=948)  # Adjust x and y coordinates to point to the last message
pyautogui.click()  # Click on the last message to select it

# Wait a moment for selection
sleep(1)

# Copy the selected message
pyautogui.hotkey('ctrl', 'c')  # Copy the selected message
sleep(1)

# Retrieve the copied text
last_message = pyperclip.paste()  # Use pyperclip to get the copied text

print("Last Message:", last_message)