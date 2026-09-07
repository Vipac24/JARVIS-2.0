import subprocess
import datetime
import json

def run_cmd(cmd, timeout=10):
    try:
        return subprocess.check_output(
            cmd, text=True, stderr=subprocess.STDOUT, timeout=timeout
        ).strip()
    except Exception as e:
        return str(e)

def get_time():
    return datetime.datetime.now().strftime("%I:%M %p")

def get_date():
    return datetime.datetime.now().strftime("%d %B %Y")

def battery():
    return run_cmd(["termux-battery-status"])

def flashlight(state):
    if state == "on":
        subprocess.run(["termux-torch", "on"], timeout=10)
        return "Flashlight turned on."
    if state == "off":
        subprocess.run(["termux-torch", "off"], timeout=10)
        return "Flashlight turned off."
    return "Invalid flashlight state."

def volume_up():
    subprocess.run(["termux-volume", "music", "raise"], timeout=10)
    return "Volume increased."

def volume_down():
    subprocess.run(["termux-volume", "music", "lower"], timeout=10)
    return "Volume decreased."

def mute():
    subprocess.run(["termux-volume", "music", "0"], timeout=10)
    return "Media volume muted."

def vibrate():
    subprocess.run(["termux-vibrate", "-d", "500"], timeout=10)
    return "Phone vibrated."

def device_info():
    return run_cmd(["termux-telephony-deviceinfo"])

def wifi_status():
    return run_cmd(["termux-wifi-connectioninfo"])

def bluetooth_status():
    return run_cmd(["termux-bluetooth-enable", "false"])

def notify(title, message):
    subprocess.run(
        ["termux-notification", "--title", title, "--content", message],
        timeout=10
    )
    return "Notification sent."

def speak(text):
    subprocess.run(["termux-tts-speak", text], timeout=15)
    return "Spoken."

def execute_tool(name, value=None):
    tools = {
        "time": lambda: get_time(),
        "date": lambda: get_date(),
        "battery": lambda: battery(),
        "volume_up": volume_up,
        "volume_down": volume_down,
        "mute": mute,
        "vibrate": vibrate,
        "device_info": device_info,
        "wifi_status": wifi_status,
        "bluetooth_status": bluetooth_status,
    }

    if name == "flashlight_on":
        return flashlight("on")

    if name == "flashlight_off":
        return flashlight("off")

    if name == "notify":
        return notify("JARVIS", value or "JARVIS notification")

    if name == "speak":
        return speak(value or "")

    if name in tools:
        return tools[name]()

    return "Tool not found."

def camera_photo(camera_id=0):
    import os
    path = os.path.expanduser("~/JARVIS-2.0/vision/latest.jpg")
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        subprocess.run(
            ["termux-camera-photo", "-c", str(camera_id), path],
            timeout=30,
            check=True
        )
        if os.path.exists(path):
            return f"Photo captured successfully: {path}"
        return "Camera capture failed."
    except Exception as e:
        return f"Camera error: {e}"
