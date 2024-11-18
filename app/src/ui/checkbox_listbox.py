import tkinter as tk
import customtkinter as ctk

class CheckboxListbox(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
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
        widget.bind("<MouseWheel>", self.on_mouse_wheel)
        for child in widget.winfo_children():
            self.bind_mouse_wheel(child)

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
