import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from src.ui.theme_manager import update_listbox_colors
from src.ui.listbox_manager import ListboxManager
from src.config import WINDOW_TITLE, WINDOW_SIZE, UWP_APPS
from src.ui.custom_scrollbar import ModernScrollbar
from src.ui.checkbox_listbox import CheckboxListbox
from src.utils.system_apps import SystemApps
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
        all_apps_frame.grid_rowconfigure(1, weight=1)

        # Create button frame for All Apps tab
        all_apps_button_frame = ctk.CTkFrame(all_apps_frame)
        all_apps_button_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")

        # Add buttons
        add_to_my_apps_button = ctk.CTkButton(
            all_apps_button_frame,
            text="Add Selected to My Applications",
            command=self.add_from_all_apps
        )
        add_to_my_apps_button.pack(side="left", padx=5, pady=5)

        remove_from_my_apps_button = ctk.CTkButton(
            all_apps_button_frame,
            text="Remove Selected from My Applications",
            command=self.remove_from_all_apps
        )
        remove_from_my_apps_button.pack(side="left", padx=5, pady=5)

        select_all_button = ctk.CTkButton(
            all_apps_button_frame,
            text="Select All",
            command=self.select_all_apps
        )
        select_all_button.pack(side="left", padx=5, pady=5)

        unselect_all_button = ctk.CTkButton(
            all_apps_button_frame,
            text="Unselect All",
            command=self.unselect_all_apps
        )
        unselect_all_button.pack(side="left", padx=5, pady=5)

        # Create frame for checkbox listbox
        all_apps_list_frame = ctk.CTkFrame(all_apps_frame)
        all_apps_list_frame.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="nsew")

        # Create and pack the checkbox listbox
        self.all_apps_listbox = CheckboxListbox(all_apps_list_frame)
        self.all_apps_listbox.pack(fill="both", expand=True)

        # My Applications tab
        app_frame = self.tabview.tab("My Applications")
        app_frame.grid_columnconfigure(0, weight=1)
        app_frame.grid_rowconfigure(0, weight=1)

        app_list_frame = ctk.CTkFrame(app_frame)
        app_list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.app_listbox = tk.Listbox(
            app_list_frame,
            borderwidth=1,
            highlightthickness=0,
            font=("Arial", 12),
            activestyle='none',
            relief="solid"
        )
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
            if isinstance(app, dict):
                if "uwp" in app:
                    self.app_listbox.insert(tk.END, f"UWP: {app['uwp']}")
                else:
                    self.app_listbox.insert(tk.END, app['name'])
            else:
                app_name = os.path.basename(app)
                self.app_listbox.insert(tk.END, app_name)

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
        """Remove application from My Applications"""
        selected_indices = self.app_listbox.curselection()
        if not selected_indices:
            messagebox.showinfo("Info", "Please select an application to remove")
            return

        removed_count = 0
        for index in reversed(selected_indices):
            app = self.apps[index]
            app_name = app.get("name") or app.get("uwp_name", "Unknown")
            self.apps.pop(index)
            removed_count += 1
            # Reset background and uncheck in All Apps tab
            self.all_apps_listbox.reset_item_background(app_name)

        if removed_count > 0:
            self.file_handler.save_applications(self.apps)
            self.update_listboxes()
            messagebox.showinfo("Success", f"Removed {removed_count} application(s)")

    def remove_website(self):
        selected = self.website_listbox.curselection()
        if selected:
            self.websites.pop(selected[0])
            self.file_handler.save_websites(self.websites)
            self.update_listboxes()

    def launch_applications(self):
        """Launch all applications in My Applications tab"""
        selected_apps = []
        for i in range(self.app_listbox.size()):
            app_info = self.apps[i]
            if isinstance(app_info, dict) and "exe_path" in app_info:
                selected_apps.append(app_info["exe_path"])
            elif isinstance(app_info, dict) and "uwp" in app_info:
                selected_apps.append(app_info)  # Pass the entire UWP app info
        
        if selected_apps:
            self.app_launcher.launch_applications(selected_apps)
        else:
            messagebox.showinfo("Info", "No applications to launch")

    def launch_websites(self):
        """Launch all websites in Websites tab"""
        if self.websites:
            self.app_launcher.launch_websites(self.websites)
        else:
            messagebox.showinfo("Info", "No websites to launch")

    def launch_all(self):
        """Launch both applications and websites"""
        self.launch_applications()
        self.launch_websites()

    def update_all_apps_list(self):
        """Update the All Apps list with checkboxes"""
        # Clear existing items
        self.all_apps_listbox.clear()
        
        # Get the list of installed applications
        installed_apps = SystemApps.get_installed_apps()
        
        # Convert UWP_APPS to list of dictionaries
        uwp_apps = [{"uwp_name": name, "uwp": app_id} for name, app_id in UWP_APPS.items()]
        installed_apps.extend(uwp_apps)
        
        # Get names of applications in My Applications
        my_apps_names = set()
        for app in self.apps:
            if isinstance(app, dict):
                if "name" in app:
                    my_apps_names.add(app["name"])
                elif "uwp_name" in app:
                    my_apps_names.add(app["uwp_name"])
        
        # Add each application to the listbox
        for i, app in enumerate(installed_apps):
            if isinstance(app, dict):
                app_name = app.get("name") or app.get("uwp_name", "Unknown")
            else:
                app_name = str(app)
            
            # If app is in My Applications, set selected background
            is_selected = app_name in my_apps_names
            self.all_apps_listbox.insert(i, app_name, selected=is_selected)

    def add_from_all_apps(self):
        """Add selected applications from All Apps to My Applications"""
        checked_items = self.all_apps_listbox.get_checked_items()
        if not checked_items:
            messagebox.showinfo("Info", "No applications selected")
            return
        
        added_count = 0
        installed_apps = SystemApps.get_installed_apps()
        uwp_apps = [{"uwp_name": name, "uwp": app_id} for name, app_id in UWP_APPS.items()]
        installed_apps.extend(uwp_apps)
        
        for item in checked_items:
            # Check if app is already in My Applications
            if not any(app.get("name") == item or app.get("uwp_name") == item for app in self.apps):
                # Find the app info from the installed apps
                app_info = None
                for app in installed_apps:
                    if isinstance(app, dict):
                        if app.get("name") == item or app.get("uwp_name") == item:
                            app_info = app
                            break
                    elif str(app) == item:
                        app_info = {"name": str(app)}
                        break
                
                if app_info:
                    self.apps.append(app_info)
                    added_count += 1
                    # Set selected background in All Apps
                    self.all_apps_listbox.set_item_background(item, self.all_apps_listbox.selected_bg)
        
        if added_count > 0:
            self.file_handler.save_applications(self.apps)
            self.update_listboxes()
            messagebox.showinfo("Success", f"Added {added_count} application(s) to My Applications")
        else:
            messagebox.showinfo("Info", "Selected applications are already in My Applications")

    def remove_from_all_apps(self):
        """Remove selected applications from My Applications"""
        checked_items = self.all_apps_listbox.get_checked_items()
        if not checked_items:
            messagebox.showinfo("Info", "No applications selected")
            return
        
        removed_count = 0
        for item in checked_items:
            # Find and remove the app from My Applications
            for app in self.apps[:]:
                if app.get("name") == item or app.get("uwp_name") == item:
                    self.apps.remove(app)
                    removed_count += 1
                    # Reset background and uncheck in All Apps
                    self.all_apps_listbox.reset_item_background(item)
                    break
        
        if removed_count > 0:
            self.file_handler.save_applications(self.apps)
            self.update_listboxes()
            messagebox.showinfo("Success", f"Removed {removed_count} application(s) from My Applications")
        else:
            messagebox.showinfo("Info", "Selected applications are not in My Applications")

    def select_all_apps(self):
        """Select all applications in the list"""
        self.all_apps_listbox.select_all()

    def unselect_all_apps(self):
        """Unselect all applications in the list"""
        self.all_apps_listbox.unselect_all()