from src.app import QuizHelperApp  # Imports the main app class that handles core functionality
from src.ui.main_window import MainWindow  # Imports the GUI window class for the user interface
import os  # For accessing environment variables and file paths
from dotenv import load_dotenv  # For loading API keys securely from .env files

def main():
    """Main entry point of the Quiz Helper application.
    
    The application flow:
    1. Shows initial setup instructions for first-time users
    2. Loads the Grok API key from environment variables
    3. Creates and runs the main application window
    
    Required Setup:
    - Python packages: pillow, pytesseract, pyautogui, pynput, requests, etc.
    - Tesseract OCR engine for image-to-text conversion
    - Grok API key for AI analysis capabilities
    
    The app allows users to:
    1. Capture screenshots of quiz questions (F1 hotkey)
    2. Paste text directly from clipboard
    3. Have quiz questions analyzed by Grok AI
    4. Get explanations and answers
    """
    
    # Display setup requirements for first-time users
    print("Quiz Helper App")
    print("===============")
    print("SETUP REQUIRED:")
    # List required packages that must be installed via pip
    print("1. Install required packages: pip install pillow pytesseract pyautogui pynput requests python-dotenv ttkthemes")
    print("2. Install Tesseract OCR:")  # Required for converting screenshots to text
    print("3. Get Grok API key from https://x.ai")  # Required for AI analysis
    print("\nStarting application...")
    
    # Load API key from .env.local file for security
    # This prevents exposing sensitive keys in source code
    load_dotenv('.env.local')  # Load environment variables
    api_key = os.getenv('GROK_API')  # Get API key from environment
    
    # Create and start the main application window
    window = MainWindow(api_key)  # Initialize GUI with API key
    window.root.mainloop()  # Start the event loop (blocks until window closed)

# Standard Python idiom to run main() when script is executed directly
# This won't run if the file is imported as a module
if __name__ == "__main__":
    main()