from ttkthemes import ThemedTk
from tkinter import ttk

class AppStyles:
    def __init__(self):
        self.bg_color = "#f0f0f0"
        self.accent_color = "#2196f3"
        self.font_main = ("Segoe UI", 10)
        self.font_title = ("Segoe UI", 24, "bold")

    def apply_styles(self, root: ThemedTk):
        style = ttk.Style()
        
        # Configure common styles
        style.configure("Custom.TButton",
            padding=10,
            font=self.font_main,
            background=self.accent_color)
            
        style.configure("Custom.TLabelframe",
            background=self.bg_color,
            padding=15)
            
        style.configure("Title.TLabel",
            font=self.font_title,
            foreground=self.accent_color)