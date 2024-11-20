import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image
import os
import sys
import customtkinter as ctk
from src.ui.theme_manager import update_listbox_colors
from src.ui.listbox_manager import ListboxManager
from src.config import WINDOW_TITLE, WINDOW_SIZE, UWP_APPS
from src.ui.custom_scrollbar import ModernScrollbar
from src.ui.checkbox_listbox import CheckboxListbox
from src.utils.system_apps import SystemApps
from src.utils.file_handler import FileHandler
from src.utils.app_launcher import AppLauncher

class AppWindow:
    def __init__(self, file_handler: FileHandler, app_launcher: AppLauncher):
        self.file_handler = file_handler
        self.app_launcher = app_launcher
        self.apps = self.file_handler.load_applications()
        self.websites = self.file_handler.load_websites()
        
        # Create the main window first
        self.root = ctk.CTk()
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        
        # Get the absolute path to the assets directory and load icons
        if getattr(sys, 'frozen', False):
            # Running in PyInstaller bundle
            base_path = sys._MEIPASS
        else:
            # Running in normal Python environment
            current_dir = os.path.dirname(os.path.abspath(__file__))
            base_path = os.path.dirname(os.path.dirname(current_dir))
        
        self.assets_dir = os.path.join(base_path, "assets")
        print(f"Loading icons from: {self.assets_dir}")  # Debug print
        
        self.load_icons()
        self.setup_ui()
        self.bind_events()

    def load_icons(self):
        """Load all icons after window creation"""
        try:
            # Load and resize icons using PIL first
            add_img = Image.open(os.path.join(self.assets_dir, "add.png"))
            minus_img = Image.open(os.path.join(self.assets_dir, "minus.png"))
            select_img = Image.open(os.path.join(self.assets_dir, "select.png"))
            unselect_img = Image.open(os.path.join(self.assets_dir, "unselect.png"))
            
            # Create CTkImage objects with both light and dark mode versions
            small_icon_size = (16, 16)  # Smaller size for add/minus icons
            normal_icon_size = (24, 24)  # Original size for select/unselect icons
            
            self.add_icon = ctk.CTkImage(
                light_image=add_img,
                dark_image=add_img,
                size=small_icon_size
            )
            self.minus_icon = ctk.CTkImage(
                light_image=minus_img,
                dark_image=minus_img,
                size=small_icon_size
            )
            self.select_icon = ctk.CTkImage(
                light_image=select_img,
                dark_image=select_img,
                size=normal_icon_size
            )
            self.unselect_icon = ctk.CTkImage(
                light_image=unselect_img,
                dark_image=unselect_img,
                size=normal_icon_size
            )
            print("Icons loaded successfully")  # Debug print
        except Exception as e:
            print(f"Error loading icons: {e}")
            self.add_icon = None
            self.minus_icon = None
            self.select_icon = None
            self.unselect_icon = None

    def setup_window(self):
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)

    def setup_ui(self):
        """Setup the main user interface"""
        # Create main container
        self.container = ctk.CTkFrame(self.root)
        self.container.pack(expand=True, fill="both", padx=10, pady=10)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=1)

        # Create top button frame
        top_button_frame = ctk.CTkFrame(self.container)
        top_button_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 10))
        top_button_frame.grid_columnconfigure(0, weight=1)  # For centering

        # Create center frame for buttons
        center_frame = ctk.CTkFrame(top_button_frame)
        center_frame.grid(row=0, column=0)

        # Add launch buttons horizontally
        launch_apps_button = ctk.CTkButton(
            center_frame, 
            text="Launch Applications", 
            command=self.launch_applications,
            height=32
        )
        launch_apps_button.pack(side="left", padx=5)

        launch_websites_button = ctk.CTkButton(
            center_frame, 
            text="Launch Websites", 
            command=self.launch_websites,
            height=32
        )
        launch_websites_button.pack(side="left", padx=5)

        launch_all_button = ctk.CTkButton(
            center_frame, 
            text="Launch Apps & Websites", 
            command=self.launch_all,
            height=32
        )
        launch_all_button.pack(side="left", padx=5)

        # Add tab view
        self.tabview = ctk.CTkTabview(self.container)
        self.tabview.grid(row=1, column=0, sticky="nsew")

        # Add tabs
        self.tabview.add("All Apps")
        self.tabview.add("My Applications")
        self.tabview.add("Websites")

        # All Apps tab
        all_apps_frame = self.tabview.tab("All Apps")
        
        # Create button frame at the top
        all_apps_button_frame = ctk.CTkFrame(all_apps_frame)
        all_apps_button_frame.pack(side="top", fill="x", padx=5, pady=5)

        # Add buttons with icons
        add_to_my_apps_button = ctk.CTkButton(
            all_apps_button_frame,
            text="",
            width=28,
            height=28,
            image=self.add_icon,
            fg_color="transparent",
            hover_color=("gray75", "gray25"),
            command=self.add_from_all_apps
        )
        add_to_my_apps_button.pack(side="left", padx=2)

        remove_from_my_apps_button = ctk.CTkButton(
            all_apps_button_frame,
            text="",
            width=28,
            height=28,
            image=self.minus_icon,
            fg_color="transparent",
            hover_color=("gray75", "gray25"),
            command=self.remove_from_all_apps
        )
        remove_from_my_apps_button.pack(side="left", padx=2)

        select_all_button = ctk.CTkButton(
            all_apps_button_frame,
            text="Select All",
            image=self.select_icon,
            compound="left",
            fg_color="transparent",
            hover_color=("gray75", "gray25"),
            command=self.select_all_apps,
            width=100,
            height=32
        )
        select_all_button.pack(side="left", padx=2)

        unselect_all_button = ctk.CTkButton(
            all_apps_button_frame,
            text="Unselect All",
            image=self.unselect_icon,
            compound="left",
            fg_color="transparent",
            hover_color=("gray75", "gray25"),
            command=self.unselect_all_apps,
            width=100,
            height=32
        )
        unselect_all_button.pack(side="left", padx=2)

        # Create frame for checkbox listbox
        all_apps_list_frame = ctk.CTkFrame(all_apps_frame)
        all_apps_list_frame.pack(expand=True, fill="both", padx=5, pady=5)

        # Create and pack the checkbox listbox
        self.all_apps_listbox = CheckboxListbox(all_apps_list_frame)
        self.all_apps_listbox.pack(expand=True, fill="both")

        # My Applications tab
        app_frame = self.tabview.tab("My Applications")
        app_frame.grid_columnconfigure(0, weight=1)
        app_frame.grid_rowconfigure(1, weight=1)

        # Create frame for the list
        app_list_frame = ctk.CTkFrame(app_frame)
        app_list_frame.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="nsew")

        # Get the correct background color based on the appearance mode
        if ctk.get_appearance_mode() == "Dark":
            canvas_bg = "#2b2b2b"  # Dark theme background
        else:
            canvas_bg = "#dbdbdb"  # Light theme background

        # Create a canvas and scrollbar
        self.app_canvas = tk.Canvas(
            app_list_frame,
            borderwidth=0,
            highlightthickness=0,
            bg=canvas_bg
        )
        self.app_scrollbar = ctk.CTkScrollbar(app_list_frame, command=self.app_canvas.yview)
        self.app_scrollable_frame = ctk.CTkFrame(self.app_canvas)

        # Configure canvas
        self.app_canvas.configure(yscrollcommand=self.app_scrollbar.set)
        
        # Pack widgets
        self.app_scrollbar.pack(side="right", fill="y")
        self.app_canvas.pack(side="left", fill="both", expand=True)
        
        # Create a window in the canvas for the scrollable frame
        self.app_canvas_frame = self.app_canvas.create_window((0, 0), window=self.app_scrollable_frame, anchor="nw")
        
        # Bind events
        self.app_scrollable_frame.bind("<Configure>", lambda e: self.app_canvas.configure(scrollregion=self.app_canvas.bbox("all")))
        self.app_canvas.bind("<Configure>", lambda e: self.app_canvas.itemconfig(self.app_canvas_frame, width=e.width))

        # Bind mouse wheel
        def _on_mousewheel(event):
            self.app_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.app_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Store frames for applications
        self.app_frames = []

        # Update colors on theme change
        def update_app_colors(event=None):
            bg_color = "#2b2b2b" if ctk.get_appearance_mode() == "Dark" else "#dbdbdb"
            self.app_canvas.configure(bg=bg_color)
            for frame in self.app_frames:
                frame.configure(fg_color=bg_color)

        self.root.bind("<<ThemeChanged>>", update_app_colors)

        # Websites tab
        website_frame = self.tabview.tab("Websites")
        website_frame.grid_columnconfigure(0, weight=1)
        website_frame.grid_rowconfigure(1, weight=1)

        # Create button frame at the top
        website_button_frame = ctk.CTkFrame(website_frame)
        website_button_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        # Add buttons with icons
        add_website_button = ctk.CTkButton(
            website_button_frame,
            text="",
            width=28,
            height=28,
            image=self.add_icon,
            fg_color="transparent",
            hover_color=("gray75", "gray25"),
            command=self.add_website
        )
        add_website_button.pack(side="left", padx=2)

        remove_website_button = ctk.CTkButton(
            website_button_frame,
            text="",
            width=28,
            height=28,
            image=self.minus_icon,
            fg_color="transparent",
            hover_color=("gray75", "gray25"),
            command=self.remove_website
        )
        remove_website_button.pack(side="left", padx=2)

        # Create frame for the list
        website_list_frame = ctk.CTkFrame(website_frame)
        website_list_frame.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="nsew")

        # Get the correct background color based on the appearance mode
        if ctk.get_appearance_mode() == "Dark":
            canvas_bg = "#2b2b2b"  # Dark theme background
        else:
            canvas_bg = "#dbdbdb"  # Light theme background

        # Create a canvas and scrollbar
        self.website_canvas = tk.Canvas(
            website_list_frame,
            borderwidth=0,
            highlightthickness=0,
            bg=canvas_bg
        )
        self.website_scrollbar = ctk.CTkScrollbar(website_list_frame, command=self.website_canvas.yview)
        self.website_scrollable_frame = ctk.CTkFrame(self.website_canvas)

        # Configure canvas
        self.website_canvas.configure(yscrollcommand=self.website_scrollbar.set)
        
        # Pack widgets
        self.website_scrollbar.pack(side="right", fill="y")
        self.website_canvas.pack(side="left", fill="both", expand=True)
        
        # Create a window in the canvas for the scrollable frame
        self.website_canvas_frame = self.website_canvas.create_window((0, 0), window=self.website_scrollable_frame, anchor="nw")
        
        # Bind events
        self.website_scrollable_frame.bind("<Configure>", lambda e: self.website_canvas.configure(scrollregion=self.website_canvas.bbox("all")))
        self.website_canvas.bind("<Configure>", lambda e: self.website_canvas.itemconfig(self.website_canvas_frame, width=e.width))

        # Bind mouse wheel
        def _on_website_mousewheel(event):
            self.website_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.website_canvas.bind_all("<MouseWheel>", _on_website_mousewheel)

        # Store frames for websites
        self.website_frames = []

        # Update colors on theme change
        def update_website_colors(event=None):
            bg_color = "#2b2b2b" if ctk.get_appearance_mode() == "Dark" else "#dbdbdb"
            self.website_canvas.configure(bg=bg_color)
            for frame in self.website_frames:
                frame.configure(fg_color=bg_color)

        self.root.bind("<<ThemeChanged>>", update_website_colors)

    def bind_events(self):
        self.root.bind("<<AppearanceModeChanged>>", 
                      lambda _: update_listbox_colors(
                          self.app_listbox, 
                          self.website_listbox, 
                          self.tabview, 
                          self.button_frame
                      ))

    def update_listboxes(self):
        self.app_canvas.delete("all")
        self.app_scrollable_frame.destroy()
        self.app_scrollable_frame = ctk.CTkFrame(self.app_canvas)
        self.app_canvas_frame = self.app_canvas.create_window((0, 0), window=self.app_scrollable_frame, anchor="nw")
        self.app_scrollable_frame.bind("<Configure>", lambda e: self.app_canvas.configure(scrollregion=self.app_canvas.bbox("all")))
        self.app_canvas.bind("<Configure>", lambda e: self.app_canvas.itemconfig(self.app_canvas_frame, width=e.width))
        self.app_frames = []
        
        # Update applications with proper formatting
        for i, app in enumerate(self.apps):
            # Create frame for the application with gray background
            bg_color = "#e6e6e6" if ctk.get_appearance_mode() == "Light" else "#333333"
            app_frame = ctk.CTkFrame(self.app_scrollable_frame, fg_color=bg_color)
            app_frame.pack(fill="x", padx=10, pady=(1, 0))  # Small top padding for separation
            self.app_frames.append(app_frame)

            # Add application name
            if isinstance(app, dict):
                if "uwp" in app:
                    # Format UWP apps
                    app_name = app['uwp'].split('!')[-1]  # Get the app name part
                    display_name = f"UWP: {app_name}"
                    app_label = ctk.CTkLabel(app_frame, text=display_name, font=("Arial", 14), anchor="w", height=24)
                else:
                    # Format regular apps with their name
                    app_label = ctk.CTkLabel(app_frame, text=app['name'], font=("Arial", 14), anchor="w", height=24)
            else:
                # Format executable files
                app_name = os.path.basename(app)
                app_label = ctk.CTkLabel(app_frame, text=app_name, font=("Arial", 14), anchor="w", height=24)
            
            app_label.pack(fill="x", padx=10, pady=0)

            # No need for dividers as the gray backgrounds provide visual separation

        # Update websites
        self.website_canvas.delete("all")
        self.website_scrollable_frame.destroy()
        self.website_scrollable_frame = ctk.CTkFrame(self.website_canvas)
        self.website_canvas_frame = self.website_canvas.create_window((0, 0), window=self.website_scrollable_frame, anchor="nw")
        self.website_scrollable_frame.bind("<Configure>", lambda e: self.website_canvas.configure(scrollregion=self.website_canvas.bbox("all")))
        self.website_canvas.bind("<Configure>", lambda e: self.website_canvas.itemconfig(self.website_canvas_frame, width=e.width))
        self.website_frames = []
        
        # Update websites with proper formatting
        for i, website in enumerate(self.websites):
            # Create frame for the website with gray background
            bg_color = "#e6e6e6" if ctk.get_appearance_mode() == "Light" else "#333333"
            website_frame = ctk.CTkFrame(self.website_scrollable_frame, fg_color=bg_color)
            website_frame.pack(fill="x", padx=10, pady=(1, 0))  # Small top padding for separation
            self.website_frames.append(website_frame)

            # Add website name
            website_label = ctk.CTkLabel(website_frame, text=website, font=("Arial", 14), anchor="w", height=24)
            website_label.pack(fill="x", padx=10, pady=0)

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
        website = simpledialog.askstring("Add Website", "Enter website URL:")
        if website:
            if not website.startswith(('http://', 'https://')):
                website = 'https://' + website
            self.websites.append(website)
            self.file_handler.save_websites(self.websites)
            self.update_listboxes()

    def remove_application(self):
        """Remove application from My Applications"""
        selected_indices = []
        for i, frame in enumerate(self.app_frames):
            if frame.cget("fg_color") == "#90EE90":
                selected_indices.append(i)

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
        # Get the index of the clicked website frame
        selected_frame = None
        for i, frame in enumerate(self.website_frames):
            if frame.winfo_containing(
                frame.winfo_pointerx() - frame.winfo_rootx(),
                frame.winfo_pointery() - frame.winfo_rooty()
            ):
                selected_frame = i
                break

        if selected_frame is not None:
            website = self.websites[selected_frame]
            if messagebox.askyesno("Remove Website", f"Are you sure you want to remove {website}?"):
                self.websites.pop(selected_frame)
                self.file_handler.save_websites(self.websites)
                self.update_listboxes()
                messagebox.showinfo("Success", f"Removed {website}")

    def launch_applications(self):
        """Launch all applications in My Applications tab"""
        selected_apps = []
        for i, app in enumerate(self.apps):
            if isinstance(app, dict) and "exe_path" in app:
                selected_apps.append(app["exe_path"])
            elif isinstance(app, dict) and "uwp" in app:
                selected_apps.append(app)  # Pass the entire UWP app info
        
        if selected_apps:
            self.app_launcher.launch_applications(selected_apps)
        else:
            messagebox.showinfo("Info", "No applications to launch")

    def launch_websites(self):
        if not self.websites:
            messagebox.showinfo("No Websites", "No websites to launch.")
            return
        
        for website in self.websites:
            self.app_launcher.launch_website(website)
        
        messagebox.showinfo("Success", f"Launched {len(self.websites)} website(s)")

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