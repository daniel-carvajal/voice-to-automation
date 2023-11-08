import subprocess

def focusOnApp(application_name):
    cmd = f'osascript -e \'activate application "{application_name}"\''
    subprocess.call(cmd, shell=True)

def isAppFocused(application_name):
    # AppleScript to get the title of the focused application
    script = '''
    global frontAppName
    tell application "System Events"
        set frontApp to first application process whose frontmost is true
        set frontAppName to name of frontApp
    end tell
    return frontAppName
    '''

    # Run the AppleScript
    proc = subprocess.Popen(['osascript', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    stdout, stderr = proc.communicate(script)

    # Check if 'application_name' is the focused application
    is_app_focused = application_name == stdout.strip()
    print(f"Is {application_name} focused: {is_app_focused}")
    return is_app_focused

# isAppFocused("Live")