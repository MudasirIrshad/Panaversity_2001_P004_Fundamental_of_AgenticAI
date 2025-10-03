# 🖼️ OCR + AI Summarizer

An AI-powered tool that **reads any image, extracts text with OCR**, and then **summarizes it instantly** using an LLM.  
The project is modular — each tool is in its own Python file for clean and structured coding practices.  

---

## 🚀 Features
- 📸 **Image to Text**: Reads and extracts text from images using [Tesseract OCR](https://github.com/tesseract-ocr/tesseract).  
- 🤖 **Summarization**: Summarizes the extracted text with Gemini LLM.  
- 🌍 **Web Search (Optional)**: Search the web when needed via Tavily API.  
- 🧩 **Modular Code**: OCR, Summarization, and Web Search are written in separate files for maintainability.  
- 💡 **Free to Use**: No images are sent to the LLM (avoiding token/image limits). Only text is passed — saving cost and keeping it efficient.  

---

## 🛠️ Tech Stack
- Python 3.10+  
- [Pytesseract](https://pypi.org/project/pytesseract/)  
- [Pillow (PIL)](https://pillow.readthedocs.io/)  
- [Google Gemini API](https://ai.google.dev/)  
- [Tavily API](https://tavily.com/) (for web search)  

---
