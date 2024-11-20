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
        all_apps_frame.grid_columnconfigure(0, weight=1)
        all_apps_frame.grid_rowconfigure(1, weight=1)

        # Create button frame at the top
        all_apps_button_frame = ctk.CTkFrame(all_apps_frame)
        all_apps_button_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

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

        # Create frame for the list
        all_apps_list_frame = ctk.CTkFrame(all_apps_frame)
        all_apps_list_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        # Create scrollable canvas
        bg_color = "#2b2b2b" if ctk.get_appearance_mode() == "Dark" else "#dbdbdb"
        self.all_apps_canvas = tk.Canvas(
            all_apps_list_frame,
            borderwidth=0,
            highlightthickness=0,
            bg=bg_color
        )
        self.all_apps_scrollbar = ctk.CTkScrollbar(all_apps_list_frame, command=self.all_apps_canvas.yview)
        self.all_apps_scrollable_frame = ctk.CTkFrame(self.all_apps_canvas)

        # Configure canvas
        self.all_apps_canvas.configure(yscrollcommand=self.all_apps_scrollbar.set)
        self.all_apps_scrollbar.pack(side="right", fill="y")
        self.all_apps_canvas.pack(side="left", fill="both", expand=True)

        # Create window for scrollable frame
        self.all_apps_canvas_frame = self.all_apps_canvas.create_window(
            (0, 0),
            window=self.all_apps_scrollable_frame,
            anchor="nw"
        )

        # Configure scrolling
        self.all_apps_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.all_apps_canvas.configure(scrollregion=self.all_apps_canvas.bbox("all"))
        )
        self.all_apps_canvas.bind(
            "<Configure>",
            lambda e: self.all_apps_canvas.itemconfig(self.all_apps_canvas_frame, width=e.width)
        )

        # Initialize all apps frames list
        self.all_apps_frames = []

        # My Applications tab
        my_apps_frame = self.tabview.tab("My Applications")
        my_apps_frame.grid_columnconfigure(0, weight=1)
        my_apps_frame.grid_rowconfigure(1, weight=1)

        # Create button frame at the top
        my_apps_button_frame = ctk.CTkFrame(my_apps_frame)
        my_apps_button_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        # Add buttons with icons
        add_app_button = ctk.CTkButton(
            my_apps_button_frame,
            text="",
            width=28,
            height=28,
            image=self.add_icon,
            fg_color="transparent",
            hover_color=("gray75", "gray25"),
            command=self.add_application
        )
        add_app_button.pack(side="left", padx=2)

        remove_app_button = ctk.CTkButton(
            my_apps_button_frame,
            text="",
            width=28,
            height=28,
            image=self.minus_icon,
            fg_color="transparent",
            hover_color=("gray75", "gray25"),
            command=self.remove_application
        )
        remove_app_button.pack(side="left", padx=2)

        # Create frame for applications list
        my_apps_list_frame = ctk.CTkFrame(my_apps_frame)
        my_apps_list_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        # Create scrollable canvas
        bg_color = "#2b2b2b" if ctk.get_appearance_mode() == "Dark" else "#dbdbdb"
        self.my_apps_canvas = tk.Canvas(
            my_apps_list_frame,
            borderwidth=0,
            highlightthickness=0,
            bg=bg_color
        )
        self.my_apps_scrollbar = ctk.CTkScrollbar(my_apps_list_frame, command=self.my_apps_canvas.yview)
        self.my_apps_scrollable_frame = ctk.CTkFrame(self.my_apps_canvas)

        # Configure canvas
        self.my_apps_canvas.configure(yscrollcommand=self.my_apps_scrollbar.set)
        self.my_apps_scrollbar.pack(side="right", fill="y")
        self.my_apps_canvas.pack(side="left", fill="both", expand=True)

        # Create window for scrollable frame
        self.my_apps_canvas_frame = self.my_apps_canvas.create_window(
            (0, 0),
            window=self.my_apps_scrollable_frame,
            anchor="nw"
        )

        # Configure scrolling
        self.my_apps_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.my_apps_canvas.configure(scrollregion=self.my_apps_canvas.bbox("all"))
        )
        self.my_apps_canvas.bind(
            "<Configure>",
            lambda e: self.my_apps_canvas.itemconfig(self.my_apps_canvas_frame, width=e.width)
        )

        # Initialize app frames list
        self.app_frames = []

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

        # Create frame for websites list
        website_list_frame = ctk.CTkFrame(website_frame)
        website_list_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        # Create scrollable canvas
        bg_color = "#2b2b2b" if ctk.get_appearance_mode() == "Dark" else "#dbdbdb"
        self.website_canvas = tk.Canvas(
            website_list_frame,
            borderwidth=0,
            highlightthickness=0,
            bg=bg_color
        )
        self.website_scrollbar = ctk.CTkScrollbar(website_list_frame, command=self.website_canvas.yview)
        self.website_scrollable_frame = ctk.CTkFrame(self.website_canvas)

        # Configure canvas
        self.website_canvas.configure(yscrollcommand=self.website_scrollbar.set)
        self.website_scrollbar.pack(side="right", fill="y")
        self.website_canvas.pack(side="left", fill="both", expand=True)

        # Create window for scrollable frame
        self.website_canvas_frame = self.website_canvas.create_window(
            (0, 0),
            window=self.website_scrollable_frame,
            anchor="nw"
        )

        # Configure scrolling
        self.website_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.website_canvas.configure(scrollregion=self.website_canvas.bbox("all"))
        )
        self.website_canvas.bind(
            "<Configure>",
            lambda e: self.website_canvas.itemconfig(self.website_canvas_frame, width=e.width)
        )

        # Initialize website frames list
        self.website_frames = []

        # Update initial content
        self.update_all_apps_list()
        self.update_listboxes()

    def bind_events(self):
        self.root.bind("<<AppearanceModeChanged>>", 
                      lambda _: update_listbox_colors(
                          self.app_listbox, 
                          self.website_frames,  # Pass website frames instead of listbox
                          self.tabview, 
                          self.button_frame
                      ))

    def update_listboxes(self):
        self.my_apps_canvas.delete("all")
        self.my_apps_scrollable_frame.destroy()
        self.my_apps_scrollable_frame = ctk.CTkFrame(self.my_apps_canvas)
        self.my_apps_canvas_frame = self.my_apps_canvas.create_window((0, 0), window=self.my_apps_scrollable_frame, anchor="nw")
        self.my_apps_scrollable_frame.bind("<Configure>", lambda e: self.my_apps_canvas.configure(scrollregion=self.my_apps_canvas.bbox("all")))
        self.my_apps_canvas.bind("<Configure>", lambda e: self.my_apps_canvas.itemconfig(self.my_apps_canvas_frame, width=e.width))
        self.app_frames = []
        
        # Update applications with proper formatting
        for idx, app in enumerate(self.apps, 1):
            # Create frame for each application
            bg_color = "#e6e6e6" if ctk.get_appearance_mode() == "Light" else "#333333"
            app_frame = ctk.CTkFrame(
                self.my_apps_scrollable_frame,
                fg_color=bg_color,
                corner_radius=10
            )
            app_frame.pack(fill="x", padx=10, pady=(5 if idx == 1 else 2))
            self.app_frames.append(app_frame)
            
            # Create left frame for index
            index_frame = ctk.CTkFrame(
                app_frame,
                fg_color="#007AFF",  # Blue accent color
                width=30,
                height=32,
                corner_radius=10
            )
            index_frame.pack(side="left", padx=(0, 10))
            index_frame.pack_propagate(False)
            
            # Add index number
            index_label = ctk.CTkLabel(
                index_frame,
                text=str(idx),
                font=("Arial Bold", 14),
                text_color="white"
            )
            index_label.place(relx=0.5, rely=0.5, anchor="center")
            
            # Create right frame for app content
            content_frame = ctk.CTkFrame(
                app_frame,
                fg_color="transparent"
            )
            content_frame.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=3)
            
            # Add app name and path
            if isinstance(app, dict):
                app_name = app.get('name', 'Unknown')
                app_path = app.get('path', 'Unknown')
            else:
                app_name = app
                app_path = app
            
            app_label = ctk.CTkLabel(
                content_frame,
                text=app_name,
                font=("Arial", 14),
                anchor="w"
            )
            app_label.pack(side="left", fill="x", expand=True)
            
            # Add launch button
            launch_button = ctk.CTkButton(
                content_frame,
                text="Launch",
                width=70,
                height=24,
                font=("Arial", 12),
                fg_color="#28a745",  # Green color
                hover_color="#218838",  # Darker green
                command=lambda app=app: self.launch_application(app)
            )
            launch_button.pack(side="right", padx=5)

        # Update websites
        for frame in self.website_frames:
            frame.destroy()
        self.website_frames.clear()
        
        for idx, website in enumerate(self.websites, 1):
            # Create frame for each website
            bg_color = "#e6e6e6" if ctk.get_appearance_mode() == "Light" else "#333333"
            website_frame = ctk.CTkFrame(
                self.website_scrollable_frame,
                fg_color=bg_color,
                corner_radius=10
            )
            website_frame.pack(fill="x", padx=10, pady=(5 if idx == 1 else 2))
            self.website_frames.append(website_frame)
            
            # Create left frame for index
            index_frame = ctk.CTkFrame(
                website_frame,
                fg_color="#007AFF",  # Blue accent color
                width=30,
                height=32,
                corner_radius=10
            )
            index_frame.pack(side="left", padx=(0, 10))
            index_frame.pack_propagate(False)
            
            # Add index number
            index_label = ctk.CTkLabel(
                index_frame,
                text=str(idx),
                font=("Arial Bold", 14),
                text_color="white"
            )
            index_label.place(relx=0.5, rely=0.5, anchor="center")
            
            # Create right frame for website content
            content_frame = ctk.CTkFrame(
                website_frame,
                fg_color="transparent"
            )
            content_frame.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=3)
            
            # Add website name
            website_label = ctk.CTkLabel(
                content_frame,
                text=website,
                font=("Arial", 14),
                anchor="w"
            )
            website_label.pack(side="left", fill="x", expand=True)
            
            # Add launch button
            launch_button = ctk.CTkButton(
                content_frame,
                text="Launch",
                width=70,
                height=24,
                font=("Arial", 12),
                fg_color="#28a745",  # Green color
                hover_color="#218838",  # Darker green
                command=lambda url=website: self.launch_website(url)
            )
            launch_button.pack(side="right", padx=5)

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
        selected = self.website_listbox.curselection()
        if selected:
            self.websites.pop(selected[0])
            self.file_handler.save_websites(self.websites)
            self.update_listboxes()

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
        # Clear existing frames
        for frame in self.all_apps_frames:
            frame.destroy()
        self.all_apps_frames.clear()

        # Get all installed apps
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
        
        # Update the list with proper formatting
        for idx, app in enumerate(installed_apps, 1):
            # Create frame for each app
            bg_color = "#e6e6e6" if ctk.get_appearance_mode() == "Light" else "#333333"
            app_frame = ctk.CTkFrame(
                self.all_apps_scrollable_frame,
                fg_color=bg_color,
                corner_radius=10
            )
            app_frame.pack(fill="x", padx=10, pady=(5 if idx == 1 else 2))
            self.all_apps_frames.append(app_frame)
            
            # Create left frame for index
            index_frame = ctk.CTkFrame(
                app_frame,
                fg_color="#007AFF",  # Blue accent color
                width=30,
                height=32,
                corner_radius=10
            )
            index_frame.pack(side="left", padx=(0, 10))
            index_frame.pack_propagate(False)
            
            # Add index number
            index_label = ctk.CTkLabel(
                index_frame,
                text=str(idx),
                font=("Arial Bold", 14),
                text_color="white"
            )
            index_label.place(relx=0.5, rely=0.5, anchor="center")

            # Create checkbox frame
            checkbox_frame = ctk.CTkFrame(
                app_frame,
                fg_color="transparent"
            )
            checkbox_frame.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=3)

            # Format app name based on type
            if isinstance(app, dict):
                if "uwp" in app:
                    app_name = app["uwp_name"]
                    display_name = f"UWP: {app_name}"
                else:
                    app_name = app["name"]
                    display_name = app_name
            else:
                app_name = os.path.basename(app)
                display_name = app_name

            # Add checkbox with app name
            checkbox_var = tk.BooleanVar(value=app_name in my_apps_names)
            checkbox = ctk.CTkCheckBox(
                checkbox_frame,
                text=display_name,
                variable=checkbox_var,
                font=("Arial", 14),
                text_color="white" if ctk.get_appearance_mode() == "Dark" else "black",
                width=20,
                height=20,
                corner_radius=4,
                border_width=2
            )
            checkbox.pack(side="left", fill="x", expand=True)

    def add_from_all_apps(self):
        """Add selected applications from All Apps to My Applications"""
        checked_items = []
        for frame in self.all_apps_frames:
            checkbox = None
            for child in frame.winfo_children():
                if isinstance(child, ctk.CTkFrame) and child.winfo_children():
                    for grandchild in child.winfo_children():
                        if isinstance(grandchild, ctk.CTkCheckBox) and grandchild.get():
                            checked_items.append(grandchild.cget("text"))
                            break

        if not checked_items:
            messagebox.showinfo("Info", "No applications selected")
            return

        added_count = 0
        installed_apps = SystemApps.get_installed_apps()

        for item in checked_items:
            # Handle UWP apps
            if item.startswith("UWP: "):
                app_name = item.replace("UWP: ", "")
                if app_name in UWP_APPS:
                    if not any(app.get("uwp_name") == app_name for app in self.apps):
                        self.apps.append({"uwp_name": app_name, "uwp": UWP_APPS[app_name]})
                        added_count += 1
            else:
                # Handle regular apps
                if not any(app.get("name") == item for app in self.apps):
                    # Find the app in installed apps
                    for app_info in installed_apps:
                        if app_info.get("name") == item:
                            self.apps.append({
                                "name": item,
                                "path": app_info.get("exe_path", "")
                            })
                            added_count += 1
                            break

        if added_count > 0:
            # Save the updated apps list
            self.file_handler.save_applications(self.apps)
            # Update both listboxes
            self.update_listboxes()
            messagebox.showinfo("Success", f"Added {added_count} application(s) to My Applications")
        else:
            messagebox.showinfo("Info", "No new applications were added")

    def remove_from_all_apps(self):
        """Remove selected applications from My Applications"""
        checked_items = []
        for frame in self.all_apps_frames:
            checkbox = None
            for child in frame.winfo_children():
                if isinstance(child, ctk.CTkFrame) and child.winfo_children():
                    for grandchild in child.winfo_children():
                        if isinstance(grandchild, ctk.CTkCheckBox) and grandchild.get():
                            checked_items.append(grandchild.cget("text").replace("UWP: ", ""))
                            break

        if not checked_items:
            messagebox.showinfo("Info", "No applications selected")
            return

        removed_count = 0
        for item in checked_items:
            # Remove from My Applications if present
            for app in self.apps[:]:
                if (app.get("name") == item) or (app.get("uwp_name") == item):
                    self.apps.remove(app)
                    removed_count += 1

        if removed_count > 0:
            # Save the updated apps list
            self.file_handler.save_applications(self.apps)
            # Update both listboxes
            self.update_listboxes()
            messagebox.showinfo("Success", f"Removed {removed_count} application(s) from My Applications")
        else:
            messagebox.showinfo("Info", "No applications were removed")

    def select_all_apps(self):
        """Select all applications in the All Apps tab"""
        for frame in self.all_apps_frames:
            for child in frame.winfo_children():
                if isinstance(child, ctk.CTkFrame) and child.winfo_children():
                    for grandchild in child.winfo_children():
                        if isinstance(grandchild, ctk.CTkCheckBox):
                            grandchild.select()

    def unselect_all_apps(self):
        """Unselect all applications in the All Apps tab"""
        for frame in self.all_apps_frames:
            for child in frame.winfo_children():
                if isinstance(child, ctk.CTkFrame) and child.winfo_children():
                    for grandchild in child.winfo_children():
                        if isinstance(grandchild, ctk.CTkCheckBox):
                            grandchild.deselect()

def update_listbox_colors(app_listbox, website_listbox, tabview, button_frame):
    appearance_mode = ctk.get_appearance_mode().lower()
    
    # Update app listbox colors
    if appearance_mode == "dark":
        app_listbox.configure(bg="#2b2b2b", fg="white")
    else:
        app_listbox.configure(bg="#dbdbdb", fg="black")
    
    # Update tabview colors
    if appearance_mode == "dark":
        tabview.configure(fg_color="#333333")
        button_frame.configure(fg_color="#333333")
    else:
        tabview.configure(fg_color="#ebebeb")
        button_frame.configure(fg_color="#ebebeb")
    
    # Update website frames colors
    for frame in website_listbox:
        if appearance_mode == "dark":
            frame.configure(fg_color="#333333")
        else:
            frame.configure(fg_color="#ebebeb")