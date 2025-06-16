# Quiz Helper Application

A powerful Python desktop application that assists with quiz questions through screenshot capture, OCR text extraction, web scraping, and AI-powered analysis using Grok AI.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## 🚀 Features

- **📸 Screenshot Capture**: Take screenshots of quiz questions with interactive area selection
- **🔍 OCR Text Extraction**: Convert images to text using Tesseract OCR
- **🤖 AI Analysis**: Get answers and explanations using Grok AI
- **🌐 Web Scraping**: Analyze quiz content directly from URLs
- **⌨️ Hotkey Support**: Quick screenshot capture with F1 key
- **📋 Clipboard Integration**: Paste text directly from clipboard
- **🎨 Modern UI**: Clean, themed interface with responsive design

## 📋 Prerequisites

Before installing the application, ensure you have:

- **Python 3.8+** installed on your system
- **Tesseract OCR** engine
- **Grok API key** from [x.ai](https://x.ai)

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/quiz-helper.git
cd quiz-helper
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Tesseract OCR

#### Windows
1. Download from [GitHub releases](https://github.com/UB-Mannheim/tesseract/wiki)
2. Install and add to PATH
3. Default installation path: `C:\Program Files\Tesseract-OCR\tesseract.exe`

#### macOS
```bash
brew install tesseract
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

### 4. Configure API Key

Create a `.env.local` file in the project root:

```env
GROK_API=your_grok_api_key_here
```

**Get your Grok API key:**
1. Visit [x.ai](https://x.ai)
2. Sign up/login to your account
3. Navigate to API settings
4. Generate a new API key
5. Copy the key to your `.env.local` file

## 🚀 Usage

### Starting the Application

```bash
python main.py
```

The application will display setup instructions and launch the GUI.

### Main Features

#### 📸 Screenshot Capture
1. **Method 1**: Press `F1` key globally
2. **Method 2**: Click "Take Screenshot (F1)" button
3. Click and drag to select the area containing the quiz question
4. Text will be automatically extracted and displayed

#### 📝 Text Input
1. **Paste from clipboard**: Click "Paste Text (Ctrl+V)"
2. **Manual entry**: Type directly in the "Question Text" area

#### 🌐 URL Analysis
1. Enter a quiz website URL in the URL field
2. Click "Analyze Quiz" to scrape and analyze content

#### 🤖 AI Analysis
1. Ensure question text is in the input area
2. Click "Analyze Question"
3. View AI-generated answer and explanation in the output area

## 📁 Project Structure

```
quiz-helper/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── .env.local             # API keys (create this file)
├── .gitignore             # Git ignore rules
├── README.md              # This file
└── src/
    ├── __init__.py
    ├── app.py             # Core application logic
    ├── api/
    │   └── grok_client.py # Grok API integration
    ├── ui/
    │   ├── main_window.py # Main GUI window
    │   └── styles.py      # UI styling
    └── utils/
        ├── screenshot.py  # Screenshot utilities
        └── web_scraper.py # Web scraping tools
```

## ⚙️ Configuration

### Environment Variables

Create a `.env.local` file with the following variables:

```env
# Required
GROK_API=your_grok_api_key_here

# Optional Tesseract configuration (if not in PATH)
TESSERACT_PATH=/path/to/tesseract/executable
```

### Tesseract Configuration

If Tesseract is not in your system PATH, you can configure it in your Python code:

```python
import pytesseract

# Windows example
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# macOS/Linux example
pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'
```

## 🔑 Hotkeys

| Key | Action |
|-----|--------|
| `F1` | Take screenshot |
| `Ctrl+V` | Paste text (when paste button is focused) |
| `Escape` | Cancel screenshot selection |

## 🐛 Troubleshooting

### Common Issues

#### "Tesseract not found"
- Ensure Tesseract is installed and in your system PATH
- On Windows, add `C:\Program Files\Tesseract-OCR` to your PATH
- Verify installation: `tesseract --version`

#### "API key not found"
- Check that `.env.local` file exists in the project root
- Verify the API key is correctly formatted: `GROK_API=your_key_here`
- Ensure no extra spaces or quotes around the key

#### "Hotkeys not working"
- Run the application as administrator (Windows)
- Check for conflicting global hotkeys
- Use the GUI buttons as an alternative

#### "Screenshot overlay not appearing"
- Try waiting a moment after clicking the screenshot button
- Check if the overlay is behind other windows
- Press `Escape` to cancel and try again

### Performance Tips

- **Large screenshots**: Crop to the relevant area to improve OCR accuracy
- **Poor OCR results**: Ensure good image quality and contrast
- **Slow API responses**: Check your internet connection and API rate limits

## 🔒 Security

- **API keys**: Never commit `.env.local` to version control
- **Screenshots**: Automatically saved with timestamps (excluded from git)
- **Data privacy**: No data is stored permanently; screenshots can be deleted manually

## 🛠️ Development

### Setting Up Development Environment

```bash
# Clone repository
git clone https://github.com/yourusername/quiz-helper.git
cd quiz-helper

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8
```

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
# Format code
black src/

# Check code style
flake8 src/
```

## 📄 Dependencies

### Core Dependencies
- `pillow>=10.0.0` - Image processing
- `pytesseract>=0.3.10` - OCR text extraction
- `pyautogui>=0.9.54` - Screenshot capture
- `pynput>=1.7.6` - Global hotkey detection
- `requests>=2.31.0` - HTTP requests
- `python-dotenv>=1.0.0` - Environment variable management
- `ttkthemes>=3.2.2` - Modern UI themes
- `beautifulsoup4>=4.12.2` - HTML parsing

### Development Dependencies
- `pytest>=7.4.0` - Testing framework
- `pytest-cov>=4.1.0` - Coverage reporting
- `black>=23.3.0` - Code formatting
- `flake8>=6.0.0` - Code linting

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

If you encounter any issues or have questions:

1. Check the [troubleshooting section](#-troubleshooting)
2. Search existing [GitHub issues](https://github.com/yourusername/quiz-helper/issues)
3. Create a new issue with detailed information

## 🙏 Acknowledgments

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) - OCR engine
- [Grok AI](https://x.ai) - AI analysis capabilities
- [Python Imaging Library (PIL)](https://pillow.readthedocs.io/) - Image processing
- [Tkinter](https://docs.python.org/3/library/tkinter.html) - GUI framework

## 📊 Roadmap

- [ ] Support for multiple AI providers (Claude, GPT-4, etc.)
- [ ] Batch processing of multiple screenshots
- [ ] Export results to various formats (PDF, CSV, etc.)
- [ ] Custom OCR training for specific quiz formats
- [ ] Plugin system for quiz website scrapers
- [ ] Mobile app companion

---

**Made with ❤️ for students and educators**
