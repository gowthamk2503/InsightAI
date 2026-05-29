# AI Smart Text Summarizer

An advanced AI-powered text summarization tool with a modern GUI, built using Python and CustomTkinter. Features multiple summarization algorithms, keyword analysis, charts, history management, and more.

## ✅ Features

- **Modern Dashboard Interface**: Clean, professional UI with sidebar navigation and dark/light themes
- **Multiple Summarization Algorithms**: LSA, TextRank, and LexRank algorithms
- **Real-time Word Counter**: Live character and word count as you type
- **Advanced Keyword Analysis**: Extract keywords with frequency charts using matplotlib
- **Compression Ratio Display**: Shows percentage reduction between original and summary
- **Reading Time Estimator**: Estimates reading time for original text and summary
- **Sentence Highlighting**: Highlights important sentences in the original text
- **Drag & Drop Support**: Drag files directly into the application
- **History Management**: Save and reload previous summaries
- **Copy to Clipboard**: Instantly copy generated summaries
- **File Upload**: Support for .txt and PDF files
- **Tabbed Results**: Organized display with Summary, Keywords, and Analysis tabs
- **Threaded Processing**: Non-blocking UI during summarization

## 🧩 Project Structure

```
AI_Text_Summarizer/
│
├── main.py                 # Application entry point
├── ui.py                   # Modern GUI with dashboard interface
├── summarizer.py           # Multi-algorithm text summarization
├── pdf_reader.py           # PDF text extraction
├── keyword_extractor.py    # Keyword extraction with frequencies
├── charts.py               # Matplotlib chart generation
├── history_manager.py      # Summary history management
├── utils.py                # Utility functions for text processing
├── assets/                 # Icons and styling assets
│   ├── icons/
│   └── styles/
├── requirements.txt        # Python dependencies
└── README.md
```

## 🛠️ Technologies Used

- **Python 3.8+**
- **CustomTkinter**: Modern GUI framework
- **Sumy**: Multi-algorithm text summarization
- **Matplotlib**: Chart generation for keyword visualization
- **PyPDF2**: PDF text extraction
- **Pillow**: Image processing for icons
- **Pyperclip**: Clipboard operations
- **NLTK**: Natural language processing

## 🚀 Getting Started

### 1) Prerequisites

- Python 3.8 or higher
- pip package manager

### 2) Install Dependencies

Open a terminal in the project folder and run:

```bash
pip install -r requirements.txt
```

> 💡 On Windows, you may need: `python -m pip install -r requirements.txt`

### 3) Download NLTK Data

The first time you run the app, NLTK will download required data automatically. If needed, you can run:

```python
import nltk
nltk.download('punkt')
```

### 4) Run the Application

```bash
python main.py
```

## 📄 How to Use

### Basic Usage

1. **Enter Text**: Type or paste text in the input area
2. **Upload File**: Click "📎 Upload" or drag & drop .txt/.pdf files
3. **Choose Algorithm**: Select from LSA, TextRank, or LexRank
4. **Set Length**: Choose short, medium, or long summary
5. **Generate**: Click "🚀 Generate" to create the summary

### Advanced Features

- **Real-time Counter**: Watch word/character count update as you type
- **Theme Toggle**: Switch between dark and light modes
- **Tabbed Results**:
  - **Summary Tab**: View, copy, and save the generated summary
  - **Keywords Tab**: See extracted keywords and frequency chart
  - **Analysis Tab**: View highlighted sentences and detailed statistics
- **History Panel**: Access previous summaries from the sidebar

## 📊 Algorithm Comparison

| Algorithm | Description | Best For |
|-----------|-------------|----------|
| **LSA** | Latent Semantic Analysis | General purpose, balanced results |
| **TextRank** | Graph-based ranking | Extractive summaries, maintaining context |
| **LexRank** | Lexical centrality | Coherent summaries, sentence similarity |

## 🖼️ UI Overview

### Main Dashboard
- **Sidebar Navigation**: Quick access to Summarize and History
- **Theme Toggle**: Switch between dark/light modes
- **Control Panel**: Algorithm and length selection
- **Input Area**: Text input with live word counter
- **Results Tabs**: Organized display of summary, keywords, and analysis

### Key Features
- **Responsive Design**: Adapts to different window sizes
- **Modern Styling**: Rounded buttons, cards, and clean typography
- **Loading States**: Visual feedback during processing
- **Error Handling**: User-friendly error messages

## 📈 Example Usage

**Input Text:**
> Artificial Intelligence (AI) is intelligence demonstrated by machines, as opposed to the natural intelligence displayed by humans and animals. Leading AI textbooks define the field as the study of 'intelligent agents': any device that perceives its environment and takes actions that maximize its chance of successfully achieving its goals. Colloquially, the term "artificial intelligence" is often used to describe machines (or computers) that mimic "cognitive" functions that humans associate with the human mind, such as "learning" and "problem solving".

**Generated Summary (TextRank, Medium):**
> Artificial Intelligence (AI) is intelligence demonstrated by machines. Leading AI textbooks define the field as the study of 'intelligent agents'. Colloquially, the term "artificial intelligence" is often used to describe machines that mimic cognitive functions.

**Statistics:**
- Original: 148 words (0.7 min reading time)
- Summary: 42 words (0.2 min reading time)
- Compression: 71.6%

**Keywords:** artificial, intelligence, machines, agents, cognitive, functions

## 🔧 Customization

### Adding New Algorithms

To add a new summarization algorithm:

1. Install the required library in `requirements.txt`
2. Add the algorithm to `summarizer.py` in the `__init__` method
3. Update the UI dropdown in `ui.py`

### Custom Themes

Modify themes by updating the `ctk.set_appearance_mode()` calls in `ui.py`.

## 🧠 Technical Details

- **Threading**: Summarization runs in background threads to prevent UI freezing
- **Memory Management**: History limited to 50 entries to prevent memory issues
- **File Handling**: Supports UTF-8 encoding for international text
- **Chart Generation**: Matplotlib figures embedded in Tkinter canvas

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

---

## 🧠 Notes for Students

- The summarization uses extractive techniques (selecting important sentences)
- Keywords are extracted using frequency analysis with stop word filtering
- PDF text extraction quality depends on the PDF structure
- The app supports English text primarily (algorithms can be extended for other languages)
- Threading prevents UI blocking during computationally intensive operations

---

Enjoy summarizing texts with AI! 🤖📝