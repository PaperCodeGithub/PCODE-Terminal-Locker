import os
import sys
import time
import keyboard
import colorama
import psutil
from colorama import Fore, Style, Back
import smtplib, ssl
import secrets
import json
import base64
import ctypes
import string
from dotenv import load_dotenv

load_dotenv("bin\\setup.env")
EMAIL = os.getenv('EMAIL_ADDRESS')
PASSWORD = os.getenv('APP_PASSWORD')

colorama.init(autoreset=True)

LOCKED_USB_NAME = None
PHASE_CLEARED = 0
def load_data(filename="config\\config.json"):

    if not os.path.exists(filename):
        print(Fore.RED + "❌ Failed to load data. File not found." + Style.RESET_ALL)
        return {}
    
    with open(filename, 'r') as file:
        encoded_data = file.read()
        decoded_data = base64.b64decode(encoded_data.encode()).decode()
        return json.loads(decoded_data)
    
data =  load_data()

def lock_system():
    karnel32 = ctypes.WinDLL('kernel32')
    user32 = ctypes.WinDLL('user32')
    SW_MAXIMIZE = 3
    hWnd = karnel32.GetConsoleWindow()
    user32.ShowWindow(hWnd, SW_MAXIMIZE)
    lock_keyboard_all()    

def banner():
    print(Fore.GREEN + Style.BRIGHT)
    print("=" * 80)
    print(" " * 28 + "🛡️ SYSTEM LOCKED BY PCODE 🛡️\n")
    print("=" * 80 + Style.RESET_ALL)

def listen_for_unlock_usb():
    LOCKED_USB_NAME = data.get('authorized_drive', 'Not set')
    for part in psutil.disk_partitions(all=False):
        if LOCKED_USB_NAME.lower() in part.device.lower() or LOCKED_USB_NAME.lower() in part.mountpoint.lower():
            return True
    return False

def lock_keyboard_all():
   for key_code in range(150):
       try:
            keyboard.block_key(key_code)
       except Exception as e:
            print(Fore.RED + f"❌ Failed to block key {key_code}: {e}" + Style.RESET_ALL)

def lock_keyboard():
    # Lock the keyboard input
    keys = ['alt', 'tab', 'windows', 'ctrl', 'f4']
    for key in keys:
        try:
            keyboard.block_key(key)
        except:
            pass

def unlock_keyboard():
    keyboard.unhook_all()

def check_device_connected():
    
    if data.get('authorized_drive', None) is None:
        print(Fore.RED + "❌ Authorized USB drive not set in configuration. Please set your authorized USB drive in config.json." + Style.RESET_ALL)
        print(Fore.RED + "Exiting..." + Style.RESET_ALL)
        unlock_keyboard()
        sys.exit(1)
    else:
        while True:
            if listen_for_unlock_usb():
                break

def ask_for_password():
    if data.get('unique_code', None) is None:
        print(Fore.RED + "❌ Unique code not set in configuration. Please set your unique code in config.json." + Style.RESET_ALL)
        print(Fore.RED + "Exiting..." + Style.RESET_ALL)
        unlock_keyboard()
        sys.exit(1)
    else:
        print(Fore.YELLOW + "Please enter the password:" + Style.RESET_ALL)
        password = input("Password: ")
        if password == f"{data.get('unique_code', 'Not set')}":
            return True
        else:
            print(Fore.RED + "❌ Incorrect password. Device Reset.." + Style.RESET_ALL)
            return False
    
    
def send_email_notification(code):
    print(Fore.YELLOW + "Collecting data..." + Style.RESET_ALL)
    sender_email = EMAIL  # Replace with your email address
    password = PASSWORD  # Replace with your app password
    subject = "Unlock Verification"
    body = f"Your 6-digit unlock code is: {code}\n\nDo not share this code."

    message = f"Subject: {subject}\n\n{body}"

    print(Fore.YELLOW + "Sending Request..." + Style.RESET_ALL)
    context = ssl.create_default_context()

    try:
        print(Fore.YELLOW + "Connecting to server..." + Style.RESET_ALL)
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            print(Fore.YELLOW + "Logging in..." + Style.RESET_ALL)
            server.login(sender_email, password)
            print(Fore.YELLOW + "Sending Details..." + Style.RESET_ALL)
            if data.get('email', None) is None:
                print(Fore.RED + "❌ Email not set in configuration. Please set your email in config.json." + Style.RESET_ALL)
                print(Fore.RED + "Exiting..." + Style.RESET_ALL)
                unlock_keyboard()
                sys.exit(1)
            else:
                server.sendmail(sender_email, f"{data.get('email', 'Not set')}", message)
                return True
    except Exception as e:
        print(Fore.RED + f"❌ Failed to send email: {e}" + Style.RESET_ALL)
        return False

if __name__ == "__main__":

    lock_system()    
    while True:
        if keyboard.is_pressed('esc'):
            print(Fore.RED + "\nExiting USB Locker..." + Style.RESET_ALL)
            unlock_keyboard()
            sys.exit(0)

        try:
            os.system('cls' if os.name == 'nt' else 'clear')
            os.system('mode con: cols=120 lines=30')
            banner()
            if(PHASE_CLEARED == 0):
                check_device_connected()
                print(Fore.YELLOW + "\n✅ Authorize Device Detected. Unlocking Layer 1/3..." + Style.RESET_ALL)
                print(Fore.YELLOW + "🔓 Unlocking Keyboard..." + Style.RESET_ALL)
                unlock_keyboard()
                lock_keyboard()
                time.sleep(1)
                print(Fore.GREEN + "🔓 Keyboard Unlocked. You can now use your keyboard." + Style.RESET_ALL)
                PHASE_CLEARED = 1
            
            if(PHASE_CLEARED == 1):
                check = ask_for_password()
                if check:
                    print(Fore.GREEN + "✅ Password Correct. Unlocking Layer 2/3..." + Style.RESET_ALL)
                    PHASE_CLEARED = 2
                        
                else:
                    print(Fore.RED + "❌ Incorrect Password. Locking Keyboard again." + Style.RESET_ALL)
                    lock_keyboard()
                    time.sleep(1)
                    PHASE_CLEARED = 0
                    check_device_connected()

            if(PHASE_CLEARED == 2):
                code = secrets.token_urlsafe(6)
                check = send_email_notification(code)
                
                if check:
                    user_code = input(Fore.YELLOW + f"🔑 Enter Code: " + Style.RESET_ALL)
                    if user_code == code:
                        print(Fore.GREEN + "✅ Code Verified. Unlocking Layer 3/3..." + Style.RESET_ALL)
                        PHASE_CLEARED = 3
                    else:
                        print(Fore.RED + "❌ Incorrect Code. Locking Keyboard again." + Style.RESET_ALL)
                        lock_keyboard()
                        time.sleep(1)
                        PHASE_CLEARED = 0
                        check_device_connected()
                else:
                    print(Fore.RED + "❌ Email Sending Failed. Unlocking System." + Style.RESET_ALL)
                    time.sleep(2)
                    sys.exit(1)

            if(PHASE_CLEARED == 3):
                unlock_keyboard()
                print(Fore.GREEN + "🔓 Unlocking System. You can now use your computer." + Style.RESET_ALL)
                time.sleep(3)
                break

        except KeyboardInterrupt:
            unlock_keyboard()
            print(Fore.RED + "\nExiting Lockdown manually" + Style.RESET_ALL)