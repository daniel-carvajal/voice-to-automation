import rumps
import threading

import os
from pathlib import Path
import configparser
from dotenv import load_dotenv
load_dotenv('.env')

from rhino_demo_mic import main as rhino_main

CONTEXT_PATH = './Ableton_en_mac_v3_0_0.rhn' 
ACCESS_KEY = os.getenv('ACCESS_KEY')  


class PomodoroApp(object):
    def __init__(self):
        self.settings = self.load_settings()  # Load settings first
        print("here! ", self.settings)

        self.config = {
            "app_name": "Pomodoro",
            "start": "Start Timer",
            "pause": "Pause Timer",
            "continue": "Continue Timer",
            "stop": "Stop Timer",
            "break_message": "Time is up! Take a break :)",
            "interval": self.settings.get('interval', 1500)  # Use settings value or default
            # "interval": 1500
        }
        self.app = rumps.App(self.config["app_name"])
        self.timer = rumps.Timer(self.on_tick, 1)
        self.interval = self.config["interval"]
        self.set_up_menu()
        
        # self.start_pause_button = rumps.MenuItem(
        #     title=self.config["start"], callback=self.start_timer)
        # self.stop_button = rumps.MenuItem(
        #     title=self.config["stop"], callback=self.stop_timer)
        self.microphone_button = rumps.MenuItem(title="Microphone On", callback=self.toggle_microphone)

        # self.app.menu = [self.start_pause_button, self.stop_button, self.microphone_button]
        self.app.menu = [self.microphone_button]
        self.microphone_event = threading.Event()  # Initialize the threading event here

    def get_data_path(self, filename):
        home_dir = Path.home()
        settings_dir = home_dir / '.pomodoro_app'
        settings_dir.mkdir(exist_ok=True)
        return settings_dir / filename

    def load_settings(self):
        settings_path = self.get_data_path('settings.ini')
        print(f"Looking for settings.ini at: {settings_path}")  # Debug print

        if not settings_path.exists():
            print("Settings file not found, creating from default settings.")
            local_dir = Path(os.path.dirname(os.path.abspath(__file__)))
            default_settings_path = local_dir / 'default_settings.ini'
            print(f"Looking for default_settings.ini at: {default_settings_path}")  # Debug print

            # Make sure the default settings file exists
            if not default_settings_path.exists():
                print("Default settings file not found.")
                return {}
            with open(default_settings_path, 'r') as default_settings, open(settings_path, 'w') as settings:
                settings.write(default_settings.read())
                print(f"Created settings.ini from default_settings.ini at: {settings_path}")  # Debug print


        config = configparser.ConfigParser()
        config.read(settings_path)

        # Here you can define the expected settings and their types
        settings_to_validate = {
            'General': {
                'interval': int,  # Add 'interval' to the 'General' section
            },
        }

        # Initialize an empty dictionary to hold settings
        validated_settings = {}

        # Validate and assign settings
        for section, settings in settings_to_validate.items():
            for setting, value_type in settings.items():
                if value_type == int:
                    validated_settings[setting] = config.getint(section, setting, fallback=0)
                elif value_type == float:
                    validated_settings[setting] = config.getfloat(section, setting, fallback=0.0)
                # Add more types if needed
        
        return validated_settings


    def set_up_menu(self):
        self.timer.stop()
        self.timer.count = 0
        self.app.title = "🍅"

    def toggle_microphone(self, sender):
        if sender.title == "Microphone On":
            sender.title = "Microphone Off"
            self.microphone_event.clear()  # Clear the event to allow the microphone thread to run
            self.microphone_thread = threading.Thread(target=rhino_main, args=(ACCESS_KEY, CONTEXT_PATH, self.microphone_event))
            self.microphone_thread.start()
        else:
            sender.title = "Microphone On"
            self.microphone_event.set()  # Set the event to signal the microphone thread to stop
            self.microphone_thread.join()  # Wait for the thread to finish
            print("Microphone stopped.")

    def on_tick(self, sender):
        time_left = sender.end - sender.count
        mins = time_left // 60 if time_left >= 0 else time_left // 60 + 1
        secs = time_left % 60 if time_left >= 0 else (-1 * time_left) % 60
        if mins == 0 and time_left < 0:
            rumps.notification(
                title=self.config["app_name"],
                subtitle=self.config["break_message"],
                message='')
            self.stop_timer()
            self.stop_button.set_callback(None)
        else:
            self.stop_button.set_callback(self.stop_timer)
            self.app.title = '{:2d}:{:02d}'.format(mins, secs)
        sender.count += 1

    def start_timer(self, sender):
        if sender.title.lower().startswith(("start", "continue")):
            if sender.title == self.config["start"]:
                self.timer.count = 0
                self.timer.end = self.interval
            sender.title = self.config["pause"]
            self.timer.start()
        else:
            sender.title = self.config["continue"]
            self.timer.stop()

    def stop_timer(self, sender):
        self.set_up_menu()
        self.stop_button.set_callback(None)
        self.start_pause_button.title = self.config["start"]

    def run(self):
        self.app.run()


if __name__ == '__main__':
    app = PomodoroApp()
    app.run()