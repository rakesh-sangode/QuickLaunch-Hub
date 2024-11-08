import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os
import subprocess
import json
import webbrowser

# Paths for saving application and website lists
APP_LIST_FILE = "applications.json"
WEBSITE_LIST_FILE = "websites.json"

# Known UWP apps with their package family names (PFNs)
UWP_APPS = {
    "calculator": "Microsoft.WindowsCalculator_8wekyb3d8bbwe!App",
    "microsoft.teams": "MicrosoftTeams_8wekyb3d8bbwe!Teams"
}

# Function to load the list of applications
def load_applications():
    if os.path.exists(APP_LIST_FILE):
        with open(APP_LIST_FILE, "r") as file:
            return json.load(file)
    return []

# Function to save the list of applications
def save_applications(applications):
    with open(APP_LIST_FILE, "w") as file:
        json.dump(applications, file)

# Function to load the list of websites
def load_websites():
    if os.path.exists(WEBSITE_LIST_FILE):
        with open(WEBSITE_LIST_FILE, "r") as file:
            return json.load(file)
    return []

# Function to save the list of websites
def save_websites(websites):
    with open(WEBSITE_LIST_FILE, "w") as file:
        json.dump(websites, file)

# Function to add an application (either .exe or UWP)
def add_application():
    add_type = messagebox.askquestion("Add Application", "Do you want to add a regular .exe app? Click 'No' to add a UWP app (e.g., Calculator)")
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

# Function to add a website
def add_website():
    website_url = simpledialog.askstring("Add Website", "Enter the website URL:")
    if website_url:
        websites.append(website_url)
        save_websites(websites)
        update_website_listbox()

# Function to remove an application from the list
def remove_application():
    selected = app_listbox.curselection()
    if selected:
        apps.pop(selected[0])
        save_applications(apps)
        update_app_listbox()

# Function to remove a website from the list
def remove_website():
    selected = website_listbox.curselection()
    if selected:
        websites.pop(selected[0])
        save_websites(websites)
        update_website_listbox()

# Function to update the application listbox
def update_app_listbox():
    app_listbox.delete(0, tk.END)
    for app in apps:
        if isinstance(app, dict) and "uwp" in app:
            app_listbox.insert(tk.END, f"UWP: {app['uwp']}")
        else:
            app_listbox.insert(tk.END, app)
    app_listbox.configure(font=("Arial", 12))

# Function to update the website listbox
def update_website_listbox():
    website_listbox.delete(0, tk.END)
    for website in websites:
        website_listbox.insert(tk.END, website)
    website_listbox.configure(font=("Arial", 12))

# Function to launch all applications
def launch_applications():
    for app in apps:
        try:
            if isinstance(app, dict) and "uwp" in app:
                subprocess.Popen(["explorer.exe", f"shell:AppsFolder\\{app['uwp']}"])
            else:
                subprocess.Popen(app)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open {app}: {e}")

# Function to launch all websites
def launch_websites():
    for website in websites:
        try:
            webbrowser.open(website)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open {website}: {e}")

# Function to launch both applications and websites
def launch_apps_and_websites():
    launch_applications()
    launch_websites()

# Setup main window with customtkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.title("Rakesh's SoftGenie")
root.geometry("700x500")

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

# Main Application Launcher Page
def setup_page3():
    global apps, websites, app_listbox, website_listbox
    apps = load_applications()
    websites = load_websites()

    container = ctk.CTkFrame(frame3, fg_color="transparent")
    container.pack(fill="both", expand=True, padx=20, pady=20)

    # Buttons Frame arranged in two rows
    button_frame = ctk.CTkFrame(container)
    button_frame.pack(pady=10)

    # First Row of Buttons
    add_app_button = ctk.CTkButton(button_frame, text="Add Application", command=add_application)
    add_app_button.grid(row=0, column=0, padx=5, pady=5)

    add_website_button = ctk.CTkButton(button_frame, text="Add Website", command=add_website)
    add_website_button.grid(row=0, column=1, padx=5, pady=5)

    remove_app_button = ctk.CTkButton(button_frame, text="Remove Application", command=remove_application)
    remove_app_button.grid(row=0, column=2, padx=5, pady=5)

    # Second Row of Buttons
    remove_website_button = ctk.CTkButton(button_frame, text="Remove Website", command=remove_website)
    remove_website_button.grid(row=1, column=0, padx=5, pady=5)

    launch_apps_button = ctk.CTkButton(button_frame, text="Launch Applications", command=launch_applications)
    launch_apps_button.grid(row=1, column=1, padx=5, pady=5)

    launch_websites_button = ctk.CTkButton(button_frame, text="Launch Websites", command=launch_websites)
    launch_websites_button.grid(row=1, column=2, padx=5, pady=5)

    # Launch both Apps and Websites button
    launch_apps_websites_button = ctk.CTkButton(button_frame, text="Launch Apps & Websites", command=launch_apps_and_websites)
    launch_apps_websites_button.grid(row=1, column=3, padx=5, pady=5)

    # Listboxes Frame
    listboxes_frame = ctk.CTkFrame(container)
    listboxes_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Application Listbox
    app_listbox_label = ctk.CTkLabel(listboxes_frame, text="Applications", font=("Arial", 12))
    app_listbox_label.pack(anchor="w")
    app_listbox = tk.Listbox(listboxes_frame, width=60, height=8, borderwidth=1, highlightthickness=0, font=("Arial", 12))
    app_listbox.pack(fill="x", padx=10, pady=5)
    update_app_listbox()

    # Website Listbox
    website_listbox_label = ctk.CTkLabel(listboxes_frame, text="Websites", font=("Arial", 12))
    website_listbox_label.pack(anchor="w")
    website_listbox = tk.Listbox(listboxes_frame, width=60, height=8, borderwidth=1, highlightthickness=0, font=("Arial", 12))
    website_listbox.pack(fill="x", padx=10, pady=5)
    update_website_listbox()

# Initialize all frames and show the main frame
setup_page3()
show_frame(frame3)

# Start the application
root.mainloop()
