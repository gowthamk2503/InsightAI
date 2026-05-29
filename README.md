# 🧠 SummarAI — AI Smart Text Summarizer

<div align="center">

<img src="./assets/banner.png" alt="SummarAI Banner" width="100%"/>

# 🧠 SummarAI

### AI-Powered Text Summarization & Document Analysis Platform

Transform lengthy documents into concise, meaningful summaries using advanced Natural Language Processing techniques and multiple summarization algorithms.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-Modern_UI-blue?style=for-the-badge)
![NLP](https://img.shields.io/badge/NLP-Text_Summarization-success?style=for-the-badge)
![Matplotlib](https://img.shields.io/badge/Analytics-Charts-orange?style=for-the-badge)
![PDF](https://img.shields.io/badge/PDF-Supported-red?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

### 🚀 Summarize • Analyze • Discover

</div>

---

# 📖 Overview

SummarAI is an intelligent text summarization application built using Python and CustomTkinter that helps users quickly understand large amounts of text through automated summarization.

The application supports multiple NLP summarization algorithms, PDF document analysis, keyword extraction, frequency visualization, summary history management, and interactive analytics.

Whether you're a student, researcher, content creator, or professional, SummarAI helps reduce reading time while preserving important information.

---

# ✨ Key Features

## 📝 AI Text Summarization

Generate concise summaries using:

- LSA (Latent Semantic Analysis)
- TextRank Algorithm
- LexRank Algorithm

Choose from:

- Short Summary
- Medium Summary
- Long Summary

---

## 📄 Document Upload Support

Supported file formats:

- TXT Files
- PDF Documents

Features:

- One-click upload
- Automatic text extraction
- Instant document processing

---

## 🏷️ Keyword Extraction

Automatically identify:

- Important keywords
- Most frequent terms
- Topic-related phrases
- Content insights

---

## 📊 Interactive Analytics

Visualize text information through:

- Keyword Frequency Charts
- Summary Statistics
- Compression Analysis
- Reading Time Metrics

Powered by Matplotlib.

---

## 📚 Summary History

Store and manage:

- Previous summaries
- Used algorithms
- Compression ratios
- Generated keywords
- Processing timestamps

---

## 🌙 Theme Support

Switch instantly between:

- Dark Mode
- Light Mode

Modern UI powered by CustomTkinter.

---

## 📋 Productivity Tools

- Copy Summary to Clipboard
- Save Summary as TXT
- Word Counter
- Character Counter
- Reading Time Estimator
- Sentence Highlighting

---

# 📸 Application Screenshots

## 🏠 Main Dashboard

<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/bf3cbfbf-0329-4844-a5e0-701a0df6c1d4" />



Modern dashboard interface with sidebar navigation and quick controls.

---

## 📝 Text Summarization

<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/01c444f2-36fb-4700-bf6f-59d88ee7d5c2" />


Generate summaries using multiple algorithms.

---

## 📋 Summary Output


View generated summaries with statistics.

---

## 🏷️ Keyword Analysis

<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/108a1e78-9645-4043-964a-289d4f210f3b" />


Automatically extracted keywords.

---

## 📊 Frequency Visualization


Keyword frequency analysis chart.

---

## 🔍 Detailed Analysis


Highlighted sentences and text analytics.

---

## 📚 Summary History


Manage and reload previous summaries.

---

## 🌙 Dark Theme


---

## ☀️ Light Theme


---

# 🛠 Technology Stack

| Category | Technology |
|-----------|------------|
| Programming Language | Python |
| GUI Framework | CustomTkinter |
| NLP Library | Sumy |
| PDF Processing | PyPDF2 |
| Charts & Analytics | Matplotlib |
| Clipboard Operations | Pyperclip |
| Text Processing | NLTK |
| Image Processing | Pillow |

---

# 🏗 System Architecture

```text
User Input
    │
    ▼
Text / PDF Upload
    │
    ▼
Text Extraction
    │
    ▼
Summarization Engine
    │
    ├── LSA
    ├── TextRank
    └── LexRank
    │
    ▼
Summary Generation
    │
    ├── Keyword Extraction
    ├── Statistics
    ├── Charts
    └── Analysis
    │
    ▼
User Dashboard
```

# 📂 Project Structure

```bash
SummarAI/
│
├── main.py
├── ui.py
├── summarizer.py
├── pdf_reader.py
├── keyword_extractor.py
├── charts.py
├── history_manager.py
├── utils.py
│
├── assets/
│   ├── banner.png
│   ├── icons/
│   └── styles/
│
├── screenshots/
│   ├── dashboard.png
│   ├── summarizer.png
│   ├── summary.png
│   ├── keywords.png
│   ├── chart.png
│   ├── analysis.png
│   ├── history.png
│   ├── dark-theme.png
│   └── light-theme.png
│
├── requirements.txt
└── README.md
```

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/gowthamk2503/SummarAI.git
```

## Navigate to Project

```bash
cd SummarAI
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Install NLTK Data

```python
import nltk
nltk.download('punkt')
```

## Run Application

```bash
python main.py
```

# 📄 How To Use

### Step 1

Enter or paste text into the input area.

### Step 2

Or upload:

- TXT File
- PDF File

### Step 3

Choose:

- LSA
- TextRank
- LexRank

### Step 4

Select summary length:

- Short
- Medium
- Long

### Step 5

Click:

```text
🚀 Generate
```

### Step 6

View:

- Summary
- Keywords
- Analysis
- Statistics

---

# 📊 Algorithm Comparison

| Algorithm | Description | Best For |
|------------|------------|------------|
| LSA | Latent Semantic Analysis | General Purpose Summaries |
| TextRank | Graph-Based Ranking | Extractive Summaries |
| LexRank | Lexical Centrality | Coherent Summaries |

---

# 📈 Example Output

### Input

```text
Artificial Intelligence (AI) is intelligence demonstrated by machines...
```

### Generated Summary

```text
Artificial Intelligence is intelligence demonstrated by machines. It is commonly used to describe systems capable of learning and problem solving.
```

### Statistics

```text
Original Words : 148
Summary Words  : 42
Compression    : 71.6%
Reading Time   : 0.2 min
```

### Keywords

```text
Artificial Intelligence
Machine Learning
Agents
Cognitive Functions
Problem Solving
```

---

# 🔒 Key Highlights

✅ Multiple Summarization Algorithms

✅ PDF Document Support

✅ Modern Dashboard UI

✅ Dark & Light Themes

✅ Keyword Extraction

✅ Interactive Charts

✅ Reading Time Analysis

✅ Summary History

✅ Copy & Export Features

✅ Multi-threaded Processing

---

# 🎯 Future Enhancements

- AI Transformer Models (BART, T5)
- Multi-Language Summarization
- OCR Support
- Voice Summarization
- Cloud Sync
- User Authentication
- Team Collaboration
- AI Chat Assistant
- Web Version
- Mobile App

---

# 🎓 Learning Outcomes

This project demonstrates:

- Natural Language Processing
- Extractive Text Summarization
- Python GUI Development
- CustomTkinter Framework
- Data Visualization
- PDF Processing
- Multi-threading
- Software Architecture
- User Experience Design

---

# 👨‍💻 Author

## Gowtham K

🎓 B.Tech Information Technology  
🏫 Sri Eshwar College of Engineering

📧 gowtham.k2023it@sece.ac.in

### 🌐 Connect

- GitHub
- LinkedIn
- Portfolio Website

---

# 📜 License

Licensed under the MIT License.

---

<div align="center">

## ⭐ If you like this project, give it a star ⭐

### 🧠 Turning Long Documents into Quick Insights

Built with ❤️ using Python & NLP

</div>
