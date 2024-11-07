import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os
import subprocess
import json

# Path to save the list of applications
APP_LIST_FILE = "applications.json"

# Known UWP apps with their package family names (PFNs)
UWP_APPS = {
    "calculator": "Microsoft.WindowsCalculator_8wekyb3d8bbwe!App",
    "microsoft.teams": "MicrosoftTeams_8wekyb3d8bbwe!Teams"
}

# Add this near the top with other constants
CONFIG_FILE = "config.json"

# Function to load the list of applications and websites
def load_applications():
    if os.path.exists(APP_LIST_FILE):
        with open(APP_LIST_FILE, "r") as file:
            return json.load(file)
    return {"apps": [], "websites": []}

# Function to save the list of applications and websites
def save_applications(data):
    with open(APP_LIST_FILE, "w") as file:
        json.dump(data, file)

# Function to add a website
def add_website():
    website_url = simpledialog.askstring("Add Website", "Enter the website URL (e.g., https://www.example.com):")
    if website_url:
        apps["websites"].append(website_url)
        save_applications(apps)
        update_app_listbox()

# Function to add an application (either .exe or UWP)
def add_application():
    add_type = messagebox.askquestion("Add Application", "Do you want to add regular .exe app? Click 'No' to add a UWP app. (like Calculator)")
    
    if add_type == 'no':
        uwp_app_name = simpledialog.askstring("Enter UWP App Name", "Enter the UWP app identifier (e.g., 'calculator' for Calculator):")
        if uwp_app_name in UWP_APPS:
            apps.append({"uwp": UWP_APPS[uwp_app_name]})
        else:
            messagebox.showerror("Error", "UWP app not recognized. Please enter a known app identifier.")
    else:
        file_path = filedialog.askopenfilename(title="Select an application", filetypes=[("Executable", "*.exe")])
        if file_path:
            apps.append(file_path)
    
    save_applications(apps)
    update_app_listbox()

# Function to remove an application from the list
def remove_application():
    selected = listbox.curselection()
    if selected:
        apps.pop(selected[0])
        save_applications(apps)
        update_app_listbox()

# Function to update the listbox with the added applications and websites
def update_app_listbox():
    listbox.delete(0, tk.END)
    for app in apps["apps"]:
        if isinstance(app, dict) and "uwp" in app:
            listbox.insert(tk.END, f"UWP: {app['uwp']}")
        else:
            listbox.insert(tk.END, app)
    for website in apps["websites"]:
        listbox.insert(tk.END, f"Website: {website}")
    listbox.configure(font=("Arial", 12))

# Function to launch all added applications and websites
def launch_applications_and_websites():
    if not apps["apps"] and not apps["websites"]:
        messagebox.showwarning("Warning", "No applications or websites added.")
        return

    for app in apps["apps"]:
        try:
            if isinstance(app, dict) and "uwp" in app:
                subprocess.Popen(["explorer.exe", f"shell:AppsFolder\\{app['uwp']}"])
            else:
                subprocess.Popen(app)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open {app}: {e}")

    for website in apps["websites"]:
        try:
            subprocess.Popen(["start", website], shell=True)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open {website}: {e}")

# Add this after the imports
def update_listbox_colors():
    if ctk.get_appearance_mode() == "Dark":
        listbox.configure(bg='#2b2b2b', fg='white', selectbackground='#1f538d')
    else:
        listbox.configure(bg='#e0e0e0', fg='black', selectbackground='#7eb5e8')

# Add these functions after the other utility functions
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    return {"first_launch": True}

def save_config(config):
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file)

# Setup main window with customtkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.title("Rakesh's SoftGenie")
root.geometry("600x400")

# Frame to manage different pages
frame1 = ctk.CTkFrame(root)
frame2 = ctk.CTkFrame(root)
frame3 = ctk.CTkFrame(root)

# Function to show a specific frame
def show_frame(frame):
    frame1.pack_forget()
    frame2.pack_forget()
    frame3.pack_forget()
    frame.pack(fill="both", expand=True)

# Page 1 - About
def setup_page1():
    container = ctk.CTkFrame(frame1, fg_color="transparent")
    container.place(relx=0.5, rely=0.5, anchor="center")
    
    label = ctk.CTkLabel(container, 
                        text="Welcome to the Rakesh's SoftGenie!\n\nThis software allows you to add and launch applications easily.", 
                        font=("Arial", 14))
    label.pack(pady=20)
    
    next_button = ctk.CTkButton(container, text="Next", command=lambda: show_frame(frame2))
    next_button.pack(pady=20)

# Page 2 - How It Helps
def setup_page2():
    container = ctk.CTkFrame(frame2, fg_color="transparent")
    container.place(relx=0.5, rely=0.5, anchor="center")
    
    label = ctk.CTkLabel(container, 
                        text="With this launcher, you can manage frequently used applications in one place.\n\nSave time and organize your workflow effectively.", 
                        font=("Arial", 14))
    label.pack(pady=20)
    
    def finish_setup():
        config = load_config()
        config["first_launch"] = False
        save_config(config)
        show_frame(frame3)
    
    next_button = ctk.CTkButton(container, text="Get Started", command=finish_setup)
    next_button.pack(pady=20)

# Page 3 - Main Application Launcher
def setup_page3():
    global apps, listbox
    apps = load_applications()

    container = ctk.CTkFrame(frame3, fg_color="transparent")
    container.pack(fill="both", expand=True, padx=20, pady=20)

    button_frame = ctk.CTkFrame(container)
    button_frame.pack(pady=10)

    add_app_button = ctk.CTkButton(button_frame, text="Add Application", command=add_application)
    add_app_button.pack(side="left", padx=5)

    add_website_button = ctk.CTkButton(button_frame, text="Add Website", command=add_website)
    add_website_button.pack(side="left", padx=5)

    remove_button = ctk.CTkButton(button_frame, text="Remove Application", command=remove_application)
    remove_button.pack(side="left", padx=5)

    launch_app_button = ctk.CTkButton(button_frame, text="Launch Apps", command=launch_applications)
    launch_app_button.pack(side="left", padx=5)

    launch_website_button = ctk.CTkButton(button_frame, text="Launch Websites", command=lambda: launch_applications_and_websites())
    launch_website_button.pack(side="left", padx=5)

    launch_both_button = ctk.CTkButton(button_frame, text="Launch Apps & Websites", command=launch_applications_and_websites)
    launch_both_button.pack(side="left", padx=5)

    listbox = tk.Listbox(container, 
                        width=60, 
                        height=15, 
                        borderwidth=1, 
                        highlightthickness=0,
                        font=("Arial", 12))
    listbox.pack(fill="both", expand=True, padx=10, pady=10)
    
    update_listbox_colors()
    root.bind("<<AppearanceModeChanged>>", lambda _: update_listbox_colors())
    update_app_listbox()

# Replace the initialization code at the bottom with this
def initialize_app():
    config = load_config()
    
    # Initialize all frames
    setup_page1()
    setup_page2()
    setup_page3()
    
    # Show appropriate frame based on whether it's first launch
    if config.get("first_launch", True):
        show_frame(frame1)
    else:
        show_frame(frame3)

# Initialize and run the app
initialize_app()
root.mainloop()
