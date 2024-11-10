import tkinter as tk
import customtkinter as ctk

class ModernScrollbar(tk.Canvas):
    def __init__(self, parent, width=8, **kwargs):
        super().__init__(parent, width=width, highlightthickness=0, **kwargs)
        self.thumb_color = "#666666"  # Default color
        self._thumb = None
        self._thumb_pos = 0
        self._timer = None
        self._command = None
        
        # Set background color based on appearance mode
        if ctk.get_appearance_mode() == "Dark":
            self.bg_color = "#2b2b2b"  # Dark mode background
        else:
            self.bg_color = "#e0e0e0"  # Light mode background
            
        # Bind mouse events
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<B1-Motion>", self.on_motion)
        
        self.hide()  # Initially hidden

    def set(self, first, last):
        if float(first) <= 0 and float(last) >= 1:
            self.hide()  # Hide when no scrolling needed
            return
        
        self.show()
        height = self.winfo_height()
        thumb_height = max(height * float(last), 30)  # Minimum thumb size
        thumb_pos = height * float(first)

        # Update or create thumb
        if self._thumb is None:
            self._thumb = self.create_rectangle(
                0, thumb_pos, self.winfo_width(), thumb_pos + thumb_height,
                fill=self.thumb_color, outline=self.thumb_color, tags="thumb"
            )
        else:
            self.coords(
                self._thumb,
                0, thumb_pos, self.winfo_width(), thumb_pos + thumb_height
            )

        self._thumb_pos = thumb_pos
        self.start_fade_timer()

    def configure(self, **kwargs):
        if "command" in kwargs:
            self._command = kwargs.pop("command")
        super().configure(**kwargs)

    def on_press(self, event):
        if self._command is not None:
            # Calculate relative position
            relative_pos = event.y / self.winfo_height()
            self._command("moveto", relative_pos)

    def on_motion(self, event):
        if self._command is not None:
            # Calculate relative movement
            relative_pos = event.y / self.winfo_height()
            self._command("moveto", relative_pos)

    def show(self):
        if ctk.get_appearance_mode() == "Dark":
            self.configure(bg="#333333")  # Dark mode scrollbar
        else:
            self.configure(bg="#c1c1c1")  # Light mode scrollbar

    def hide(self):
        self.configure(bg=self.bg_color)  # Use fixed background color
        if self._thumb is not None:
            self.delete(self._thumb)
            self._thumb = None

    def start_fade_timer(self):
        if self._timer is not None:
            self.after_cancel(self._timer)
        self._timer = self.after(1000, self.hide)  # Hide after 1 second

    def update_colors(self):
        # Update colors when theme changes
        if ctk.get_appearance_mode() == "Dark":
            self.bg_color = "#2b2b2b"
        else:
            self.bg_color = "#e0e0e0"
        self.hide()