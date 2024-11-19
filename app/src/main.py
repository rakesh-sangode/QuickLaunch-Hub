import os
import sys
import customtkinter as ctk

# Add the app directory to sys.path
app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

from src.ui.app_window import AppWindow
from src.utils.app_launcher import AppLauncher
from src.utils.file_handler import FileHandler


def main():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    
    # Initialize data handlers
    file_handler = FileHandler()
    app_launcher = AppLauncher()
    
    # Create and run the main window
    app = AppWindow(file_handler, app_launcher)
    app.root.mainloop()

if __name__ == "__main__":
    main()