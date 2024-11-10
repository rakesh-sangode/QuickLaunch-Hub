import customtkinter as ctk
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ui.app_window import AppWindow
from src.utils.file_handler import FileHandler
from src.utils.app_launcher import AppLauncher

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