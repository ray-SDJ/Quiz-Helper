import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from ttkthemes import ThemedTk
from src.ui.styles import AppStyles
from src.api.grok_client import GrokClient
from src.utils.web_scraper import WebScraper
import threading
from src.app import QuizHelperApp  # Add this import

class MainWindow:
    def __init__(self, api_key: str):
        self.root = ThemedTk(theme="arc")
        self.styles = AppStyles()
        self.grok_client = GrokClient(api_key)
        self.web_scraper = WebScraper()
        
        self.setup_window()
        self.create_widgets()
        self.setup_styles()
        
        self.app = QuizHelperApp()
        self.threads = []  # Track threads
        
        # Add window close handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_window(self):
        self.root.title("Quiz Helper")
        self.root.geometry("800x600")
    
    def setup_styles(self):
        """Configure the application styles"""
        self.root.configure(bg=self.styles.bg_color)
        self.styles.apply_styles(self.root)
    
    def start_screenshot(self):
        """Start the screenshot selection process"""
        self.root.iconify()  # Minimize main window
        self.screenshot_selector.overlay.deiconify()  # Show selection overlay
        
    def process_screenshot(self, screenshot):
        """Handle the captured screenshot"""
        self.root.deiconify()  # Restore main window
        # Process screenshot with OCR etc...

    def create_widgets(self):
        # Main container
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Title
        title = ttk.Label(self.main_frame, 
                         text="Quiz Helper", 
                         style="Title.TLabel")
        title.grid(row=0, column=0, pady=(0, 20))
        
        # URL Entry
        url_frame = ttk.Frame(self.main_frame)
        url_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        url_label = ttk.Label(url_frame, text="Quiz URL:")
        url_label.grid(row=0, column=0, padx=(0, 10))
        
        self.url_entry = ttk.Entry(url_frame, width=50)
        self.url_entry.grid(row=0, column=1)
        
        # Analyze Button
        self.analyze_btn = ttk.Button(
            url_frame,
            text="Analyze Quiz",
            command=self.analyze_url,
            style="Custom.TButton"
        )
        self.analyze_btn.grid(row=0, column=2, padx=(10, 0))
        
        # Results Area
        self.result_text = scrolledtext.ScrolledText(
            self.main_frame, 
            height=20, 
            width=60)
        self.result_text.grid(row=2, column=0, pady=10)
    
    def analyze_url(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("No URL", "Please enter a quiz URL")
            return
            
        self.analyze_btn.config(state='disabled')
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Analyzing quiz...\n\n")
        
        thread = threading.Thread(target=self._process_url, args=(url,))
        thread.daemon = True
        thread.start()
    
    def _process_url(self, url):
        try:
            # Scrape content
            content = self.web_scraper.scrape_quiz_content(url)
            
            # Analyze with Grok
            response = self.grok_client.analyze_question(
                f"""Context: This is from the webpage {url}
                
                Content found:
                {content['question']}
                
                Please analyze this content and provide:
                1. The likely quiz question
                2. The correct answer
                3. A brief explanation
                """
            )
            
            # Update UI
            self.root.after(0, self._update_results, response)
            
        except Exception as e:
            self.root.after(0, self._show_error, str(e))
        finally:
            self.root.after(0, lambda: self.analyze_btn.config(state='normal'))
    
    def _update_results(self, response):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, response['choices'][0]['message']['content'])
    
    def _show_error(self, error_msg):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"Error: {error_msg}")
    
    def start_screenshot_thread(self):
        thread = threading.Thread(target=self.app.process_screenshot)
        self.threads.append(thread)
        thread.start()
    
    def capture_screenshot(self, event=None):
        """Handle screenshot capture request"""
        self.start_screenshot_thread()
    
    def on_closing(self):
        """Clean up threads before closing"""
        # Join all threads
        for thread in self.threads:
            if thread.is_alive():
                thread.join()
        self.root.destroy()
    
    def cleanup_thread(self, thread):
        """Remove completed thread from tracking list"""
        if thread in self.threads:
            self.threads.remove(thread)