import speech_recognition as sr
import subprocess
import pyautogui
import time
import psutil

recognizer = sr.Recognizer()

def open_app_with_search(app_name):
    try:
        pyautogui.hotkey("win")
        pyautogui.typewrite(app_name)
        pyautogui.press("enter")
        print(f"\033[92mSearching for and opening {app_name}...\033[0m")

    except Exception as e:
        print(f"\033[31mError opening the app: {e}\033[0m")

def close_app(app_name):
    try:
        for process in psutil.process_iter(attrs=['pid', 'name']):
            if app_name.lower() in process.info['name'].lower():
                pid = process.info['pid']
                process = psutil.Process(pid)
                process.terminate()
                print(f"\033[33mClosing {app_name}...\033[0m")
                time.sleep(1) 

        print(f"\033[31mClosed all instances of {app_name}.\033[0m")

    except Exception as e:
        print(f"Error closing the app: {e}")

def listen_for_commands():
    with sr.Microphone() as source:
        print("Listening for commands...")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print("\033[34mYou said:", command + "\033[0m")

        if command.startswith("open "):
            app_name = command.split("open ")[1]
            open_app_with_search(app_name)
        elif command.startswith("close "):
            app_name = command.split("close ")[1]
            close_app(app_name)
        elif command == "stop listening":
            print("\033[31mGoodbye!\033[0m")
            exit()

    except sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        print(f"Could not request results; {e}")

if __name__ == "__main__":
    subprocess.call("cls", shell=True)
    while True:
        listen_for_commands()