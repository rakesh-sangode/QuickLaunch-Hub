import subprocess
import webbrowser
from tkinter import messagebox

class AppLauncher:
    @staticmethod
    def launch_applications(apps):
        for app in apps:
            try:
                if isinstance(app, dict) and "uwp" in app:
                    subprocess.Popen(["explorer.exe", f"shell:AppsFolder\\{app['uwp']}"])
                else:
                    subprocess.Popen(app)
            except Exception as e:
                messagebox.showerror("Error", f"Could not open {app}: {e}")

    @staticmethod
    def launch_websites(websites):
        for website in websites:
            try:
                webbrowser.open(website)
            except Exception as e:
                messagebox.showerror("Error", f"Could not open {website}: {e}")

    @staticmethod
    def launch_all(apps, websites):
        AppLauncher.launch_applications(apps)
        AppLauncher.launch_websites(websites) 