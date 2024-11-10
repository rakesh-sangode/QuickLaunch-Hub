import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from src.ui.theme_manager import update_listbox_colors
from src.ui.listbox_manager import ListboxManager
from src.config import WINDOW_TITLE, WINDOW_SIZE, UWP_APPS
from src.ui.custom_scrollbar import ModernScrollbar
from src.utils.system_apps import SystemApps
from PIL import ImageTk
from src.ui.custom_listbox import IconListbox
import os

class AppWindow:
    def __init__(self, file_handler, app_launcher):
        self.file_handler = file_handler
        self.app_launcher = app_launcher
        self.apps = self.file_handler.load_applications()
        self.websites = self.file_handler.load_websites()
        
        self.setup_window()
        self.setup_ui()
        self.bind_events()

    def setup_window(self):
        self.root = ctk.CTk()
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)

    def setup_ui(self):
        # Main container with grid layout
        self.container = ctk.CTkFrame(self.root)
        self.container.pack(fill="both", expand=True, padx=20, pady=20)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        # Left sidebar for buttons
        self.setup_sidebar()
        
        # Right side tabview
        self.setup_tabview()

    def setup_sidebar(self):
        # Button frame on the left
        self.button_frame = ctk.CTkFrame(self.container)
        self.button_frame.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="nsew")

        # Add buttons vertically
        add_app_button = ctk.CTkButton(self.button_frame, text="Add Application", command=self.add_application)
        add_app_button.pack(padx=10, pady=5, fill="x")

        add_website_button = ctk.CTkButton(self.button_frame, text="Add Website", command=self.add_website)
        add_website_button.pack(padx=10, pady=5, fill="x")

        remove_app_button = ctk.CTkButton(self.button_frame, text="Remove Application", command=self.remove_application)
        remove_app_button.pack(padx=10, pady=5, fill="x")

        remove_website_button = ctk.CTkButton(self.button_frame, text="Remove Website", command=self.remove_website)
        remove_website_button.pack(padx=10, pady=5, fill="x")

        launch_apps_button = ctk.CTkButton(self.button_frame, text="Launch Applications", command=self.launch_applications)
        launch_apps_button.pack(padx=10, pady=5, fill="x")

        launch_websites_button = ctk.CTkButton(self.button_frame, text="Launch Websites", command=self.launch_websites)
        launch_websites_button.pack(padx=10, pady=5, fill="x")

        launch_all_button = ctk.CTkButton(self.button_frame, text="Launch Apps & Websites", command=self.launch_all)
        launch_all_button.pack(padx=10, pady=5, fill="x")

    def setup_tabview(self):
        # Create tabview
        self.tabview = ctk.CTkTabview(self.container)
        self.tabview.grid(row=0, column=1, sticky="nsew")

        # Create tabs in new order
        self.tabview.add("All Apps")
        self.tabview.add("My Applications")
        self.tabview.add("Websites")

        # Set All Apps as default
        self.tabview.set("All Apps")

        # All Apps tab
        all_apps_frame = self.tabview.tab("All Apps")
        all_apps_frame.grid_columnconfigure(0, weight=1)
        all_apps_frame.grid_rowconfigure(0, weight=1)

        # Create frame for listbox and scrollbar
        all_apps_list_frame = ctk.CTkFrame(all_apps_frame)
        all_apps_list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create and pack the all apps listbox
        self.all_apps_listbox = IconListbox(all_apps_list_frame)
        self.all_apps_listbox.pack(side="left", fill="both", expand=True)

        # Create and pack the modern scrollbar
        all_apps_scrollbar = ModernScrollbar(all_apps_list_frame)
        all_apps_scrollbar.pack(side="right", fill="y", padx=(2, 0))

        # Connect listbox and scrollbar
        self.all_apps_listbox.configure(yscrollcommand=all_apps_scrollbar.set)
        all_apps_scrollbar.configure(command=self.all_apps_listbox.yview)

        # My Applications tab
        app_frame = self.tabview.tab("My Applications")
        app_frame.grid_columnconfigure(0, weight=1)
        app_frame.grid_rowconfigure(0, weight=1)

        app_list_frame = ctk.CTkFrame(app_frame)
        app_list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.app_listbox = IconListbox(app_list_frame)
        self.app_listbox.pack(side="left", fill="both", expand=True)

        # Create and pack the scrollbar
        app_scrollbar = ModernScrollbar(app_list_frame)
        app_scrollbar.pack(side="right", fill="y", padx=(2, 0))

        # Connect listbox and scrollbar
        self.app_listbox.configure(yscrollcommand=app_scrollbar.set)
        app_scrollbar.configure(command=self.app_listbox.yview)

        # Websites tab
        website_frame = self.tabview.tab("Websites")
        website_frame.grid_columnconfigure(0, weight=1)
        website_frame.grid_rowconfigure(0, weight=1)

        # Create frame for listbox and scrollbar
        website_list_frame = ctk.CTkFrame(website_frame)
        website_list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create and pack the website listbox
        self.website_listbox = tk.Listbox(
            website_list_frame,
            borderwidth=1,
            highlightthickness=0,
            font=("Arial", 12),
            activestyle='none',
            relief="solid"
        )
        self.website_listbox.pack(side="left", fill="both", expand=True)

        # Create and pack the scrollbar
        website_scrollbar = ModernScrollbar(website_list_frame)
        website_scrollbar.pack(side="right", fill="y", padx=(2, 0))

        # Connect listbox and scrollbar
        self.website_listbox.configure(yscrollcommand=website_scrollbar.set)
        website_scrollbar.configure(command=self.website_listbox.yview)

        # Update initial content
        self.update_all_apps_list()
        self.update_listboxes()

    def bind_events(self):
        self.root.bind("<<AppearanceModeChanged>>", 
                      lambda _: update_listbox_colors(
                          self.app_listbox, 
                          self.website_listbox, 
                          self.tabview, 
                          self.button_frame
                      ))

    def update_listboxes(self):
        self.app_listbox.delete(0, tk.END)
        self.website_listbox.delete(0, tk.END)
        
        # Update applications
        for app in self.apps:
            if isinstance(app, dict) and "uwp" in app:
                self.app_listbox.insert(tk.END, f"UWP: {app['uwp']}")
            else:
                app_name = os.path.basename(app)
                icon = SystemApps.get_app_icon(app)
                self.app_listbox.insert(tk.END, app_name, icon)

        # Update websites
        for website in self.websites:
            self.website_listbox.insert(tk.END, website)

    def add_application(self):
        add_type = messagebox.askquestion("Add Application", 
                                        "Do you want to add a regular .exe app? Click 'No' to add a UWP app (e.g., Calculator)")
        if add_type == 'no':
            uwp_app_name = simpledialog.askstring("Enter UWP App Name", 
                                                "Enter the UWP app identifier (e.g., 'calculator' for Calculator):")
            if uwp_app_name in UWP_APPS:
                self.apps.append({"uwp": UWP_APPS[uwp_app_name]})
            else:
                messagebox.showerror("Error", "UWP app not recognized. Please enter a known app identifier.")
        else:
            file_path = filedialog.askopenfilename(title="Select an application", 
                                                 filetypes=[("Executable", "*.exe")])
            if file_path:
                self.apps.append(file_path)
        
        self.file_handler.save_applications(self.apps)
        self.update_listboxes()

    def add_website(self):
        website_url = simpledialog.askstring("Add Website", "Enter the website URL:")
        if website_url:
            self.websites.append(website_url)
            self.file_handler.save_websites(self.websites)
            self.update_listboxes()

    def remove_application(self):
        selected = self.app_listbox.curselection()
        if selected:
            self.apps.pop(selected[0])
            self.file_handler.save_applications(self.apps)
            self.update_listboxes()

    def remove_website(self):
        selected = self.website_listbox.curselection()
        if selected:
            self.websites.pop(selected[0])
            self.file_handler.save_websites(self.websites)
            self.update_listboxes()

    def launch_applications(self):
        self.app_launcher.launch_applications(self.apps)

    def launch_websites(self):
        self.app_launcher.launch_websites(self.websites)

    def launch_all(self):
        self.app_launcher.launch_all(self.apps, self.websites) 

    def update_all_apps_list(self):
        self.all_apps_listbox.delete(0, tk.END)
        installed_apps = SystemApps.get_installed_apps()
        
        for app in installed_apps:
            self.all_apps_listbox.insert(tk.END, app['name'], app['icon'])

    def show_all_apps_menu(self, event):
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Add to My Applications", 
                        command=lambda: self.add_from_all_apps())
        menu.post(event.x_root, event.y_root)

    def add_from_all_apps(self):
        selection = self.all_apps_listbox.curselection()
        if selection:
            selected_name = self.all_apps_listbox.get(selection[0])
            installed_apps = SystemApps.get_installed_apps()
            
            # Find the selected app in our list
            selected_app = next((app for app in installed_apps if app['name'] == selected_name), None)
            
            if selected_app and selected_app['path'] not in [a.get('path', a) for a in self.apps]:
                if selected_app['path'].startswith("UWP:"):
                    self.apps.append({"uwp": selected_app['path'].split(":")[1]})
                else:
                    self.apps.append(selected_app['path'])
                self.file_handler.save_applications(self.apps)
                self.update_listboxes() 