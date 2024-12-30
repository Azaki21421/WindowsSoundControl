import json
import os
import threading
import time
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from comtypes import CoInitialize, CoUninitialize
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import tkinter as tk
from tkinter import messagebox, simpledialog


CONFIG_FILE = "volume_settings.json"
DEFAULT_VOLUME = 3.0


def load_settings():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}


def save_settings(settings):
    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4, ensure_ascii=False)


def get_current_volumes():
    volumes = {}
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        app_name = session.Process.name() if session.Process else "System Sounds"
        volumes[app_name] = volume.GetMasterVolume() * 100
    return volumes


def apply_volumes(settings):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        app_name = session.Process.name() if session.Process else "System Sounds"
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if app_name == "System Sounds":
            volume.SetMasterVolume(0.01, None)
        elif app_name in settings:
            volume.SetMasterVolume(settings[app_name] / 100, None)
        else:
            volume.SetMasterVolume(DEFAULT_VOLUME / 100, None)


def monitor_volumes(settings):
    CoInitialize()
    try:
        while True:
            current_volumes = get_current_volumes()
            updated = False

            for app_name, volume in current_volumes.items():
                if app_name == "System Sounds":
                    if volume != 1.0:
                        sessions = AudioUtilities.GetAllSessions()
                        for session in sessions:
                            if session.Process is None:
                                vol = session._ctl.QueryInterface(ISimpleAudioVolume)
                                vol.SetMasterVolume(0.01, None)
                                break
                elif app_name not in settings:
                    settings[app_name] = DEFAULT_VOLUME
                    updated = True
                elif settings[app_name] != volume:
                    settings[app_name] = volume
                    updated = True

            if updated:
                save_settings(settings)

            time.sleep(2)
    finally:
        CoUninitialize()


def create_icon_image():
    # Create a basic icon image
    icon_size = 64
    image = Image.new("RGBA", (icon_size, icon_size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    draw.ellipse((0, 0, icon_size, icon_size), fill="blue", outline="white")
    return image


def show_volumes():
    volumes = get_current_volumes()
    message = "\n".join([f"{app}: {volume:.2f}%" for app, volume in volumes.items()])
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Current Volumes", message)


def save_current_volumes(settings):
    volumes = get_current_volumes()
    save_settings(volumes)
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Save Volumes", "Current volumes have been saved to file.")


def apply_volume_settings(settings):
    apply_volumes(settings)
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Apply Settings", "Volumes have been applied from settings.")


def add_or_update_volume(settings):
    root = tk.Tk()
    root.withdraw()
    app_name = simpledialog.askstring("App Name", "Enter the application name:")
    if app_name:
        volume_level = simpledialog.askfloat("Volume Level", "Enter volume level (0-100):")
        if volume_level is not None and 0 <= volume_level <= 100:
            settings[app_name] = volume_level
            save_settings(settings)
            apply_volumes(settings)
            messagebox.showinfo("Update Volume", f"Volume for {app_name} has been updated.")
        else:
            messagebox.showerror("Error", "Volume level must be between 0 and 100.")


def main():
    settings = load_settings()

    monitor_thread = threading.Thread(target=monitor_volumes, args=(settings,), daemon=True)
    monitor_thread.start()

    icon = Icon("Volume Manager", create_icon_image(), menu=Menu(
        MenuItem("Show Current Volumes", show_volumes),
        MenuItem("Save Current Volumes", lambda: save_current_volumes(settings)),
        MenuItem("Apply Volume Settings", lambda: apply_volume_settings(settings)),
        MenuItem("Add/Update Volume", lambda: add_or_update_volume(settings)),
        MenuItem("Exit", lambda: icon.stop())
    ))
    icon.run()


if __name__ == "__main__":
    main()
