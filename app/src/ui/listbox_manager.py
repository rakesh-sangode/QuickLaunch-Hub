import tkinter as tk
from config import FONT_FAMILY, FONT_SIZE

class ListboxManager:
    @staticmethod
    def create_listbox(parent, **kwargs):
        return tk.Listbox(
            parent,
            borderwidth=1,
            highlightthickness=0,
            font=(FONT_FAMILY, FONT_SIZE),
            activestyle='none',
            relief="solid",
            **kwargs
        )

    @staticmethod
    def update_app_listbox(listbox, apps):
        listbox.delete(0, tk.END)
        for app in apps:
            if isinstance(app, dict) and "uwp" in app:
                listbox.insert(tk.END, f"UWP: {app['uwp']}")
            else:
                listbox.insert(tk.END, app)

    @staticmethod
    def update_website_listbox(listbox, websites):
        listbox.delete(0, tk.END)
        for website in websites:
            listbox.insert(tk.END, website) 