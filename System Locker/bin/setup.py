import psutil
import os
import json, base64
from colorama import Fore, Style, Back
import time

def usb_authorization():
    while True:
        input("Press Enter to continue...")
        check_connected_drives()
        print("Please enter the drive letter of the USB drive you want to use for authorization.")
        print(Fore.YELLOW + "Example: If your USB drive is D:, enter 'D:' without quotes." + Style.RESET_ALL)
        print(Fore.GREEN + "Note: The drive letter is case-sensitive, so use uppercase letters only." + Style.RESET_ALL)
        print(Fore.RED + "Do not use the drive letter of your system drive (usually C:) or any other drive that is not a USB drive." + Style.RESET_ALL)
        print(Fore.YELLOW + "Press 'Enter' to recheck connected drives." + Style.RESET_ALL)
        user_data = input("Enter the drive letter (e.g., E:): ")
        if user_data.strip() == "":
            continue
        else:
            drive = user_data
            if not drive.endswith(':'):
                print(Fore.RED + "❌ Invalid drive letter format. Please ensure it ends with a colon (e.g., E:)." + Style.RESET_ALL)
            else:
                check = check_usb_drive(drive)
                if check:
                    print(Fore.YELLOW + "Please kindly remove the USB drive." + Style.RESET_ALL)
                    while True:
                        if not check_usb_drive(drive):
                            break
                    print(Fore.GREEN + f"✅ USB drive {drive} is now authorized and will be use as verification key." + Style.RESET_ALL)
                    data = {
                        "authorized_drive": drive,
                    }
                    save_data(data)
                    break
                else:
                    print(Fore.RED + f"❌ Failed! USB drive {drive} is not connected. Please connect the USB drive and try again." + Style.RESET_ALL)

def email_password_setup():
    email = ""
    while True:
        email = input(Fore.YELLOW + "Email: " + Style.RESET_ALL)
        
        # Check if the email is valid (Advanced check)
        if "@" not in email or "." not in email.split("@")[-1]:
            print(Fore.RED + "❌ Invalid email format. Please enter a valid email address." + Style.RESET_ALL)
            continue
        else:
            break
    
    data = {
            "email": email,
        }
        
    save_data(data)
    print(Fore.GREEN + "✅ Email configuration saved successfully." + Style.RESET_ALL)

def get_unique_code(length=4):
    while True:
        pin = input("Press Enter a 4 digit pin: ")
        if len(pin) != length or not pin.isdigit():
            print(Fore.RED + "❌ Invalid input. Please enter a 4-digit number." + Style.RESET_ALL)
            continue
        else:
            data = {
                "unique_code": pin
            }
            save_data(data)
            print(Fore.GREEN + "✅ Unique code saved successfully." + Style.RESET_ALL)
            break


def load_data(filename="config\\config.json"):
    """
    Load data from a file in base64 encoded format.
    """
    if not os.path.exists(filename):
        print(Fore.RED + "❌ Failed to load data. File not found." + Style.RESET_ALL)
        return {}
    
    with open(filename, 'r') as file:
        encoded_data = file.read()
        decoded_data = base64.b64decode(encoded_data.encode()).decode()
        return json.loads(decoded_data)
    
def save_data(new_data, filename="config\\config.json"):
    """
    Save data to a file in base64 encoded format.
    If the file exists, update it with new data.
    """
    data = {}
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as file:
                encoded_data = file.read()
                decoded_data = base64.b64decode(encoded_data.encode()).decode()
                data = json.loads(decoded_data)
        except:
            data = {}
    
    # Merge new_data into existing data
    data.update(new_data)

    with open(filename, 'w') as file:
        encoded_data = base64.b64encode(json.dumps(data).encode()).decode()
        file.write(encoded_data)


def check_usb_drive(drive_letter):
    """
    Check if the specified USB drive is connected.
    """
    drive_letter = drive_letter + "\\"
    for part in psutil.disk_partitions(all=False):
        if part.device.lower() == drive_letter.lower():
            return True
    return False
def check_connected_drives():
    print("📦 Connected Drives:")
    for part in psutil.disk_partitions(all=False):
        print(Fore.YELLOW + "Device: " + Style.RESET_ALL + f"{part.device}")
        print(Fore.YELLOW + "Mountpoint: " + Style.RESET_ALL + f"{part.mountpoint}")
        print(Fore.YELLOW + "Filesystem: " + Style.RESET_ALL + f"{part.fstype}")
        print("-" * 30)

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.GREEN + "🔒 System Locker Setup" + Style.RESET_ALL)
    print(Fore.YELLOW + "System Locker uses a USB drive for verification layer 1" + Style.RESET_ALL)
    usb_authorization()
    print(Fore.YELLOW + "System Locker uses Email for verification layer 2" + Style.RESET_ALL)
    email_password_setup()
    print(Fore.YELLOW + "System Locker uses a 4 digit pin for verification layer 3" + Style.RESET_ALL)
    get_unique_code()
    print(Fore.GREEN + "✅ Setup completed successfully!" + Style.RESET_ALL)
    time.sleep(2)
    data = load_data()
    print(Fore.YELLOW + "Configuration Summary:" + Style.RESET_ALL)
    print(Fore.YELLOW + f"Authorized USB Drive: {data.get('authorized_drive', 'Not set')}" + Style.RESET_ALL)
    print(Fore.YELLOW + f"Email: {data.get('email', 'Not set')}" + Style.RESET_ALL)
    print(Fore.YELLOW + f"Unique Code: {data.get('unique_code', 'Not set')}" + Style.RESET_ALL)
    print(Fore.GREEN + "You can now run the locker.py script to use the system locker." + Style.RESET_ALL)
    print(Fore.YELLOW + "Thank you for using System Locker!" + Style.RESET_ALL)
    print(Fore.RED + "Exiting setup..." + Style.RESET_ALL)
    input("Press Enter to exit...")
    time.sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')

                                
            
       
                
    
