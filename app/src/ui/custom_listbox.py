import tkinter as tk
from PIL import Image, ImageTk

class IconListbox(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent)
        self.icons = {}  # Store icons references
        
        # Create listbox
        self.listbox = tk.Listbox(
            self,
            borderwidth=1,
            highlightthickness=0,
            font=("Arial", 12),
            activestyle='none',
            relief="solid",
            **kwargs
        )
        self.listbox.pack(side="left", fill="both", expand=True)

    def insert(self, index, text, icon=None):
        self.listbox.insert(index, f"  {text}")  # Add padding for icon alignment
        if icon:
            try:
                # Resize icon if needed
                icon = icon.resize((16, 16), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(icon)
                self.icons[text] = photo  # Keep reference
            except:
                pass

    def delete(self, first, last=None):
        self.listbox.delete(first, last)
        self.icons.clear()

    def curselection(self):
        return self.listbox.curselection()

    def get(self, index):
        return self.listbox.get(index).strip()  # Remove padding

    def configure(self, **kwargs):
        self.listbox.configure(**kwargs)

    def bind(self, sequence=None, func=None, add=None):
        self.listbox.bind(sequence, func, add)

    # Add scrolling support
    def yview(self, *args):
        self.listbox.yview(*args)

    def yview_moveto(self, fraction):
        self.listbox.yview_moveto(fraction)

    def yview_scroll(self, number, what):
        self.listbox.yview_scroll(number, what)