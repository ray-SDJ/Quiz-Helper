import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import pyautogui
import pytesseract
from PIL import Image, ImageTk
import threading
import requests
import json
import os
from datetime import datetime
import pynput
from pynput import mouse, keyboard
import time
from dotenv import load_dotenv

# Load environment variables from .env.local
load_dotenv('.env.local')

class QuizHelperApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Quiz Helper - Screenshot & Text Analysis")
        self.root.geometry("800x600")
        
        # Variables
        self.screenshot_mode = False
        self.start_pos = None
        self.end_pos = None
        self.overlay_window = None
        self.threads = []  # Keep track of created threads
        
        # Load API key from .env.local
        self.api_key = os.getenv('GROK_API')
        self.api_url = "https://api.x.ai/v1/chat/completions"
        
        self.create_widgets()
        self.setup_hotkeys()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Quiz Helper", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # API Key section
        api_frame = ttk.LabelFrame(main_frame, text="API Configuration", padding="10")
        api_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(api_frame, text="Claude API Key:").grid(row=0, column=0, sticky=tk.W)
        self.api_key_entry = ttk.Entry(api_frame, width=50, show="*")
        self.api_key_entry.grid(row=0, column=1, padx=(10, 0))
        self.api_key_entry.bind('<KeyRelease>', self.update_api_key)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.screenshot_btn = ttk.Button(button_frame, text="Take Screenshot (F1)", 
                                       command=self.start_screenshot)
        self.screenshot_btn.pack(side=tk.LEFT, padx=5)
        
        self.paste_btn = ttk.Button(button_frame, text="Paste Text (Ctrl+V)", 
                                  command=self.paste_text)
        self.paste_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = ttk.Button(button_frame, text="Clear", 
                                  command=self.clear_all)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Input text area
        input_frame = ttk.LabelFrame(main_frame, text="Question Text", padding="10")
        input_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.input_text = scrolledtext.ScrolledText(input_frame, height=8, wrap=tk.WORD)
        self.input_text.pack(fill=tk.BOTH, expand=True)
        
        # Analyze button
        self.analyze_btn = ttk.Button(main_frame, text="Analyze Question", 
                                    command=self.analyze_question)
        self.analyze_btn.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Output area
        output_frame = ttk.LabelFrame(main_frame, text="Answer & Explanation", padding="10")
        output_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=12, wrap=tk.WORD)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        main_frame.rowconfigure(5, weight=2)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Press F1 for screenshot or paste text directly")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
    
    def setup_hotkeys(self):
        """Setup global hotkeys"""
        try:
            # F1 for screenshot
            keyboard.add_hotkey('f1', self.start_screenshot)
            self.status_var.set("Hotkeys active - F1 for screenshot")
        except:
            self.status_var.set("Hotkeys unavailable - use buttons instead")
    
    def update_api_key(self, event=None):
        """Update API key from entry field"""
        self.api_key = self.api_key_entry.get()
    
    def start_screenshot(self):
        """Start screenshot selection mode"""
        self.status_var.set("Click and drag to select area...")
        self.root.withdraw()  # Hide main window
        time.sleep(0.5)  # Give time for window to hide
        
        # Create transparent overlay
        self.create_overlay()
        
    def create_overlay(self):
        """Create transparent overlay for screenshot selection"""
        self.overlay_window = tk.Toplevel()
        self.overlay_window.attributes('-fullscreen', True)
        self.overlay_window.attributes('-alpha', 0.3)
        self.overlay_window.configure(bg='gray')
        self.overlay_window.attributes('-topmost', True)
        
        # Canvas for drawing selection rectangle
        self.canvas = tk.Canvas(self.overlay_window, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Bind mouse events
        self.canvas.bind('<Button-1>', self.on_click)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)
        
        # Bind escape key to cancel
        self.overlay_window.bind('<Escape>', self.cancel_screenshot)
        self.overlay_window.focus_set()
    
    def on_click(self, event):
        """Handle mouse click start"""
        self.start_pos = (event.x_root, event.y_root)
    
    def on_drag(self, event):
        """Handle mouse drag"""
        if self.start_pos:
            # Clear previous rectangle
            self.canvas.delete("selection")
            # Draw new rectangle
            x1, y1 = self.canvas.canvasx(self.start_pos[0]), self.canvas.canvasy(self.start_pos[1])
            x2, y2 = self.canvas.canvasx(event.x_root), self.canvas.canvasy(event.y_root)
            self.canvas.create_rectangle(x1, y1, x2, y2, outline='red', width=2, tags="selection")
    
    def on_release(self, event):
        """Handle mouse release - take screenshot"""
        if self.start_pos:
            self.end_pos = (event.x_root, event.y_root)
            self.take_screenshot()
    
    def cancel_screenshot(self, event=None):
        """Cancel screenshot mode"""
        if self.overlay_window:
            self.overlay_window.destroy()
        self.root.deiconify()
        self.status_var.set("Screenshot cancelled")
    
    def take_screenshot(self):
        """Take screenshot of selected area and extract text"""
        try:
            # Close overlay
            if self.overlay_window:
                self.overlay_window.destroy()
            
            # Calculate screenshot area
            x1 = min(self.start_pos[0], self.end_pos[0])
            y1 = min(self.start_pos[1], self.end_pos[1])
            x2 = max(self.start_pos[0], self.end_pos[0])
            y2 = max(self.start_pos[1], self.end_pos[1])
            
            # Take screenshot
            screenshot = pyautogui.screenshot(region=(x1, y1, x2-x1, y2-y1))
            
            # Save screenshot
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"screenshot_{timestamp}.png"
            screenshot.save(screenshot_path)
            
            # Extract text using OCR
            self.status_var.set("Extracting text from screenshot...")
            extracted_text = pytesseract.image_to_string(screenshot)
            
            # Display extracted text
            self.input_text.delete(1.0, tk.END)
            self.input_text.insert(1.0, extracted_text.strip())
            
            self.status_var.set(f"Screenshot saved as {screenshot_path} - Text extracted")
            
        except Exception as e:
            messagebox.showerror("Screenshot Error", f"Error taking screenshot: {str(e)}")
            self.status_var.set("Screenshot failed")
        finally:
            self.root.deiconify()
    
    def paste_text(self):
        """Paste text from clipboard"""
        try:
            clipboard_text = self.root.clipboard_get()
            self.input_text.delete(1.0, tk.END)
            self.input_text.insert(1.0, clipboard_text)
            self.status_var.set("Text pasted from clipboard")
        except:
            messagebox.showwarning("Paste Error", "No text found in clipboard")
    
    def clear_all(self):
        """Clear all text areas"""
        self.input_text.delete(1.0, tk.END)
        self.output_text.delete(1.0, tk.END)
        self.status_var.set("Cleared all text")
    
    def analyze_question(self):
        """Analyze the question using Grok API"""
        question_text = self.input_text.get(1.0, tk.END).strip()
        
        if not question_text:
            messagebox.showwarning("No Question", "Please enter or capture a question first")
            return
        
        if not self.api_key:
            messagebox.showwarning("No API Key", "Please enter your Grok API key")
            return
        
        # Show loading
        self.status_var.set("Analyzing question...")
        self.analyze_btn.config(state='disabled')
        
        # Run analysis in separate thread to avoid blocking UI
        thread = threading.Thread(target=self.call_grok_api, args=(question_text,))
        thread.daemon = True
        thread.start()
        
        # Add a cleanup handler when the window closes
        self.root.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(thread))

    def on_closing(self, thread):
        """Handle window closing event"""
        if thread and thread.is_alive():
            thread.join(timeout=1.0)  # Wait up to 1 second for thread to finish
        self.root.destroy()
    
    def call_grok_api(self, question_text):
        """Call Grok API to analyze the question"""
        try:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.api_key}'
            }
            
            data = {
                'messages': [
                    {
                        'role': 'system',
                        'content': 'You are a helpful quiz assistant. Provide clear, accurate answers with brief explanations.'
                    },
                    {
                        'role': 'user',
                        'content': f"""Please help me answer this quiz question:

{question_text}

Format your response as:
ANSWER: [Your answer]
EXPLANATION: [Brief explanation of why this is correct]"""
                    }
                ],
                'model': 'grok-3-latest',
                'stream': False,
                'temperature': 0.7
            }
            
            response = requests.post(self.api_url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                answer = result['choices'][0]['message']['content']
                self.display_answer(answer)
            else:
                error_msg = f"API Error {response.status_code}: {response.text}"
                self.display_error(error_msg)
                
        except requests.exceptions.RequestException as e:
            self.display_error(f"Network error: {str(e)}")
        except Exception as e:
            self.display_error(f"Error: {str(e)}")
    
    def display_answer(self, answer):
        """Display the answer in the output area"""
        self.root.after(0, lambda: self._update_output(answer, "Analysis complete"))
    
    def display_error(self, error_msg):
        """Display error message"""
        self.root.after(0, lambda: self._update_output(f"Error: {error_msg}", "Analysis failed"))
    
    def _update_output(self, text, status):
        """Update output text and status (must be called from main thread)"""
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(1.0, text)
        self.status_var.set(status)
        self.analyze_btn.config(state='normal')
    
    def process_screenshot(self):
        thread = threading.Thread(target=self._process_screenshot_thread)
        self.threads.append(thread)
        thread.start()
    
    def cleanup(self):
        # Join all running threads before closing
        for thread in self.threads:
            thread.join()
        # ...existing code...
    
    def _process_screenshot_thread(self):
        try:
            # ...existing screenshot processing code...
            pass
        finally:
            # Remove thread from tracking list when done
            if threading.current_thread() in self.threads:
                self.threads.remove(threading.current_thread())
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    """Main function with setup instructions"""
    print("Quiz Helper App")
    print("===============")
    print("SETUP REQUIRED:")
    print("1. Install required packages: pip install pillow pytesseract pyautogui pynput requests")
    print("2. Install Tesseract OCR:")
    print("   - Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki")
    print("   - Mac: brew install tesseract")
    print("   - Linux: sudo apt-get install tesseract-ocr")
    print("3. Get Claude API key from https://console.anthropic.com/")
    print("\nStarting application...")
    
    try:
        app = QuizHelperApp()
        app.run()
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Please install required packages with:")
        print("pip install pillow pytesseract pyautogui pynput requests")
    except Exception as e:
        print(f"Error starting application: {e}")

if __name__ == "__main__":
    main()