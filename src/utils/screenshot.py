from PIL import ImageGrab
import tkinter as tk
from typing import Tuple, Optional

class ScreenshotTool:
    def __init__(self):
        self.start_pos = None
        self.end_pos = None
        self.overlay_window = None

    def take_screenshot(self, bbox: Optional[Tuple[int, int, int, int]] = None):
        return ImageGrab.grab(bbox=bbox)

class ScreenshotSelector:
    def __init__(self, parent):
        self.parent = parent
        self.start_x = None
        self.start_y = None
        self.current_rect = None
        
        # Create transparent fullscreen window
        self.overlay = tk.Toplevel(parent)
        self.overlay.attributes('-alpha', 0.3, '-topmost', True)
        self.overlay.attributes('-fullscreen', True)
        
        # Configure overlay
        self.overlay.configure(bg='grey')
        self.canvas = tk.Canvas(self.overlay, cursor="cross")
        self.canvas.pack(fill="both", expand=True)
        
        # Bind mouse events
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        
        # Hide the overlay initially
        self.overlay.withdraw()
    
    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        
    def on_drag(self, event):
        if self.current_rect:
            self.canvas.delete(self.current_rect)
            
        self.current_rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, event.x, event.y,
            outline='red', width=2
        )
    
    def on_release(self, event):
        x1 = min(self.start_x, event.x)
        y1 = min(self.start_y, event.y)
        x2 = max(self.start_x, event.x)
        y2 = max(self.start_y, event.y)
        
        # Capture the selected region
        screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        self.overlay.withdraw()
        
        # Pass screenshot back to main app
        self.parent.process_screenshot(screenshot)