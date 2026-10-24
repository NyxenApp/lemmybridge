import os
import plistlib

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.plist")


def load_instance():
    with open(CONFIG_PATH, "rb") as f:
        data = plistlib.load(f)
    return data.get("lemmyInstance", "https://lemmy.world").rstrip("/")
