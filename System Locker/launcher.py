#check for first run
import os
import sys
import subprocess

CONFIG_FILE = "config/config.json"

def is_setup_done():
    return os.path.exists(CONFIG_FILE)

def run_setup():
    subprocess.call(["python", "bin\\setup.py"])

def run_lock():
    subprocess.call(["python", "bin\\locker.py"])

def main():
    if not os.path.exists("config"):
        os.makedirs("config")

    if is_setup_done():
        run_lock()
    else:
        run_setup()


if __name__  == "__main__":
    main()