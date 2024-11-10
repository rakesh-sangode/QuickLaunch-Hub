import customtkinter as ctk

def update_listbox_colors(app_listbox, website_listbox, listboxes_frame, button_frame):
    if ctk.get_appearance_mode() == "Dark":
        # Dark mode colors
        app_listbox.configure(
            bg='#2b2b2b',
            fg='white',
            selectbackground='#1f538d',
            selectforeground='white'
        )
        website_listbox.configure(
            bg='#2b2b2b',
            fg='white',
            selectbackground='#1f538d',
            selectforeground='white'
        )
        listboxes_frame.configure(fg_color='#2b2b2b')
        button_frame.configure(fg_color='#2b2b2b')
    else:
        # Light mode colors
        app_listbox.configure(
            bg='#e0e0e0',
            fg='black',
            selectbackground='#7eb5e8',
            selectforeground='black'
        )
        website_listbox.configure(
            bg='#e0e0e0',
            fg='black',
            selectbackground='#7eb5e8',
            selectforeground='black'
        )
        listboxes_frame.configure(fg_color='#e0e0e0')
        button_frame.configure(fg_color='#e0e0e0') 