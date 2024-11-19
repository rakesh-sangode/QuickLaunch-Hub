import tkinter as tk
import customtkinter as ctk
import time
import os

class CheckboxListbox(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Get the absolute path to the assets directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), "assets")
        
        # Load custom icons with absolute paths
        self.select_icon = tk.PhotoImage(file=os.path.join(assets_dir, "select.png"))
        self.unselect_icon = tk.PhotoImage(file=os.path.join(assets_dir, "unselect.png"))
        self.add_icon = tk.PhotoImage(file=os.path.join(assets_dir, "add.png"))
        self.minus_icon = tk.PhotoImage(file=os.path.join(assets_dir, "minus.png"))
        
        # Get the correct background color based on the appearance mode
        if ctk.get_appearance_mode() == "Dark":
            canvas_bg = "#2b2b2b"  # Dark theme background
            self.selected_bg = "#1f4d1f"  # Dark green for dark mode
        else:
            canvas_bg = "#dbdbdb"  # Light theme background
            self.selected_bg = "#90EE90"  # Light green for light mode

        # Create a canvas and scrollbar
        self.canvas = tk.Canvas(
            self,
            borderwidth=0,
            highlightthickness=0,
            bg=canvas_bg
        )
        self.scrollbar = ctk.CTkScrollbar(self, command=self.canvas.yview)
        self.scrollable_frame = ctk.CTkFrame(self.canvas)

        # Configure canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack widgets
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Create a window in the canvas for the scrollable frame
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Bind events
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.bind_mouse_wheel(self)
        
        # Initialize variables
        self.checkboxes = []
        self.checkbox_vars = []
        self._command = None
        self.items_data = {}  # Store additional data for items
        self._scroll_speed = 2.5  # Increased scroll speed
        self._last_scroll_time = 0
        self._smooth_scroll_after = None  # For handling smooth scroll animation

        # Bind theme change event
        self.master.bind("<<ThemeChanged>>", self.update_colors)

    def update_colors(self, event=None):
        """Update colors when theme changes"""
        if ctk.get_appearance_mode() == "Dark":
            self.canvas.configure(bg="#2b2b2b")
            self.selected_bg = "#1f4d1f"  # Dark green for dark mode
        else:
            self.canvas.configure(bg="#dbdbdb")
            self.selected_bg = "#90EE90"  # Light green for light mode
        
        # Update existing items
        for item, data in self.items_data.items():
            if data["selected"]:
                self.set_item_background(item, self.selected_bg)

    def bind_mouse_wheel(self, widget):
        """Bind mouse wheel to scroll"""
        def _on_mousewheel(event):
            current_time = time.time()
            if current_time - self._last_scroll_time < 0.016:  # ~60fps
                return "break"
            
            self._last_scroll_time = current_time
            
            # Fix scroll direction: event.delta > 0 means scroll up
            delta = 1 if event.delta > 0 else -1
            self._smooth_scroll(delta * self._scroll_speed)
            
            return "break"

        # Bind to the widget and all its children
        widget.bind("<MouseWheel>", _on_mousewheel)
        widget.bind("<Enter>", lambda e: widget.bind_all("<MouseWheel>", _on_mousewheel))
        widget.bind("<Leave>", lambda e: widget.unbind_all("<MouseWheel>"))
        
        for child in widget.winfo_children():
            self.bind_mouse_wheel(child)

    def _smooth_scroll(self, delta):
        """Implement smooth scrolling animation"""
        if self._smooth_scroll_after:
            self.after_cancel(self._smooth_scroll_after)
        
        current_pos = self.canvas.yview()[0]
        target_pos = current_pos - (delta / 80.0)  # Adjusted for faster scrolling
        target_pos = max(0, min(1, target_pos))
        
        def _animate_scroll():
            current = self.canvas.yview()[0]
            diff = target_pos - current
            
            # If we're close enough to the target, stop animating
            if abs(diff) < 0.001:
                self.canvas.yview_moveto(target_pos)
                self._smooth_scroll_after = None
                return
            
            # Move a larger fraction of the remaining distance for faster animation
            move_amount = diff * 0.4  # Increased from 0.3 for faster animation
            self.canvas.yview_moveto(current + move_amount)
            
            # Schedule the next animation frame
            self._smooth_scroll_after = self.after(16, _animate_scroll)
        
        _animate_scroll()

    def on_mouse_wheel(self, event):
        """Handle mouse wheel scrolling"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        return "break"

    def on_frame_configure(self, event=None):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        """Update the width of the frame to fill the canvas"""
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

    def insert(self, index, item, text_color=None, selected=False):
        """Insert a new item with checkbox and optional color"""
        # Convert tk.END to actual index
        if index == tk.END:
            index = len(self.checkboxes)
        
        # Create a frame for the checkbox (for background color)
        item_frame = ctk.CTkFrame(self.scrollable_frame)
        item_frame.pack(fill="x", padx=2, pady=1)
        
        var = tk.BooleanVar(value=selected)
        checkbox = ctk.CTkCheckBox(
            item_frame,
            text=item,
            variable=var,
            command=lambda: self._on_checkbox_click(var)
        )
        checkbox.pack(fill="x", padx=5, pady=2)
        
        if text_color:
            checkbox.configure(text_color=text_color)
        
        if selected:
            item_frame.configure(fg_color=self.selected_bg)
        
        self.checkboxes.insert(index, checkbox)
        self.checkbox_vars.insert(index, var)
        self.items_data[item] = {
            "checkbox": checkbox,
            "frame": item_frame,
            "selected": selected,
            "variable": var  # Store the variable separately
        }

    def set_item_background(self, item, color):
        """Set the background color of a specific item"""
        if item in self.items_data:
            self.items_data[item]["frame"].configure(fg_color=color)
            self.items_data[item]["selected"] = (color == self.selected_bg)

    def reset_item_background(self, item):
        """Reset the background color of a specific item and uncheck it"""
        if item in self.items_data:
            self.items_data[item]["frame"].configure(fg_color="transparent")
            self.items_data[item]["selected"] = False
            # Uncheck the checkbox using the stored variable
            self.items_data[item]["variable"].set(False)

    def set_item_checked(self, item, checked):
        """Set whether an item is checked or not"""
        if item in self.items_data:
            if checked:
                self.items_data[item]["variable"].set(True)
            else:
                self.items_data[item]["variable"].set(False)

    def delete(self, first, last=None):
        """Delete items from the listbox"""
        if last is None:
            last = first
        
        for checkbox in self.checkboxes[first:last+1]:
            checkbox.destroy()
        
        del self.checkboxes[first:last+1]
        del self.checkbox_vars[first:last+1]
        for item in self.checkboxes[first:last+1]:
            del self.items_data[item.cget("text")]

    def clear(self):
        """Clear all items from the listbox"""
        for item_data in self.items_data.values():
            item_data["frame"].destroy()
        self.checkboxes.clear()
        self.checkbox_vars.clear()
        self.items_data.clear()

    def get_checked_items(self):
        """Return a list of checked items"""
        return [checkbox.cget("text") for var, checkbox in zip(self.checkbox_vars, self.checkboxes) if var.get()]

    def get_checked_indices(self):
        """Return a list of checked indices"""
        return [i for i, var in enumerate(self.checkbox_vars) if var.get()]

    def bind_checkbox_click(self, command):
        """Bind a command to checkbox clicks"""
        self._command = command

    def _on_checkbox_click(self, var):
        """Internal checkbox click handler"""
        if self._command:
            self._command()

    def select_all(self):
        """Select all checkboxes"""
        for var in self.checkbox_vars:
            var.set(True)
        if self._command:
            self._command()

    def unselect_all(self):
        """Unselect all checkboxes"""
        for var in self.checkbox_vars:
            var.set(False)
        if self._command:
            self._command()

    def add_item(self, text, data=None):
        """Add a new item to the listbox"""
        var = tk.BooleanVar()
        checkbox = ctk.CTkCheckBox(
            self.scrollable_frame,
            text=text,
            variable=var,
            command=lambda: self._on_checkbox_click(checkbox),
            image=self.unselect_icon,
            selectimage=self.select_icon,
            width=32,
            height=32
        )
        checkbox.pack(fill="x", padx=5, pady=2)
        
        self.checkboxes.append(checkbox)
        self.checkbox_vars.append(var)
        
        if data is not None:
            self.items_data[checkbox] = data
        
        return checkbox

    def _on_checkbox_click(self, checkbox):
        """Handle checkbox click event"""
        is_checked = checkbox.get()
        checkbox.configure(
            image=self.select_icon if is_checked else self.unselect_icon
        )
        if self._command:
            self._command()
