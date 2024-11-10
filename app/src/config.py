import os
import json

# Get the base directory path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configuration constants with absolute paths
APP_LIST_FILE = os.path.join(BASE_DIR, "data", "applications.json")
WEBSITE_FILE = os.path.join(BASE_DIR, "data", "websites.json")
CONFIG_FILE = os.path.join(BASE_DIR, "data", "config.json")

# Window settings
WINDOW_TITLE = "SoftGenie"
WINDOW_SIZE = "800x600"

# Font settings
FONT_FAMILY = "Arial"
FONT_SIZE = 12

# UWP apps configuration
UWP_APPS = {
    "calculator": "Microsoft.WindowsCalculator_8wekyb3d8bbwe!App",
    "microsoft.teams": "MicrosoftTeams_8wekyb3d8bbwe!Teams"
}

# Theme colors
DARK_MODE = {
    "bg": "#2b2b2b",
    "fg": "white",
    "selectbg": "#1f538d",
    "selectfg": "white"
}

LIGHT_MODE = {
    "bg": "#e0e0e0",
    "fg": "black",
    "selectbg": "#7eb5e8",
    "selectfg": "black"
}

# Create data directory if it doesn't exist
os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)

# Create config file if it doesn't exist
if not os.path.exists(CONFIG_FILE):
    default_config = {
        "first_launch": True,
        "theme": "System",
        "window_size": WINDOW_SIZE
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(default_config, f, indent=4) 