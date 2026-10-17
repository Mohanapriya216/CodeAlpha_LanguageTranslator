# 🌿 Language Translation Tool

A modern and interactive language translation web application built with **Python** and **Streamlit**. The application allows users to translate text between multiple languages through a clean and user-friendly interface.

This project was developed as part of the **CodeAlpha Internship — Task 1: Language Translation Tool**.

## ✨ Features

- 🌍 Multiple language options
- 🔄 Swap source and target languages
- ⚡ Multiple translation engines
- 🖥️ Modern green-themed user interface
- 📋 Copy translated text
- 🕘 Recent translation history
- 🧹 Clear input and translation
- ⏳ Loading indicator during translation
- 📝 Support for sentences and longer text
- 💻 Local translation using Argos Translate when a suitable model is available
- 🌐 Online translation fallback using MyMemory and Google Translate

## 🌐 Available Languages

The current application includes:

| Language | Code |
|---|---|
| English | `en` |
| Hindi | `hi` |
| Kannada | `kn` |
| French | `fr` |
| German | `de` |
| Spanish | `es` |
| Italian | `it` |
| Japanese | `ja` |
| Korean | `ko` |
| Chinese | `zh` |
| Arabic | `ar` |

Tamil, Telugu, and Malayalam are currently excluded from the application interface because reliable translation support has not been established for the current project configuration.

Translation availability depends on the selected language pair and the translation service being used.

## 🛠️ Technologies Used

- **Python**
- **Streamlit**
- **Argos Translate**
- **MyMemory Translation API**
- **deep-translator**
- **Google Translate**
- **Requests**

## 📁 Project Structure

```text
CodeAlpha_LanguageTranslator/
│
├── app.py                  # Main Streamlit translation application
├── install_models.py       # Downloads and installs Argos Translate models
├── test_translation.py     # Tests online translation functionality
├── README.md               # Project documentation
└── .venv/                  # Python virtual environment (not uploaded)
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone <your-github-repository-url>
```

### 2. Open the Project Folder

```bash
cd CodeAlpha_LanguageTranslator
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate the Virtual Environment

For Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install Required Packages

```powershell
python -m pip install streamlit requests deep-translator argostranslate
```

### 6. Install Argos Translate Models

Run the model installation script:

```powershell
python install_models.py
```

This script updates the Argos Translate model list and installs the configured English-to-language translation models when they are available.

### 7. Test Translation Services

Run:

```powershell
python test_translation.py
```

This script checks selected online translation requests and prints the returned translations or errors in the terminal.

### 8. Run the Application

Start the Streamlit application with:

```powershell
streamlit run app.py
```

The application will open in your browser.

## 🚀 How to Use

1. Select the language you want to translate **from**.
2. Select the language you want to translate **to**.
3. Enter or paste your text.
4. Click **Translate now**.
5. View the translated result.
6. Use **Copy result** to copy the translated text.
7. Use the **Swap** button to reverse the language direction.
8. Open **Recent translations** to view or restore previous translations.
9. Use **Clear** to clear the current translation.

## 🔧 Translation Process

The application uses a fallback-based translation system.

### 1. Argos Translate

The application first checks whether a suitable local Argos Translate model is installed for the selected language pair.

If available, the translation is performed locally.

### 2. MyMemory

If a suitable local translation model is unavailable, the application attempts to use the MyMemory online translation service.

An internet connection is required for this method.

### 3. Google Translate

Google Translate is used as an additional online fallback if the previous methods cannot complete the translation.

Online services may occasionally fail because of connectivity issues, rate limits, or service availability.

## 🧪 Testing

The project includes a separate `test_translation.py` script for testing online translation requests.

The current test script checks:

- Tamil
- Kannada
- Hindi

The application interface does not currently include Tamil because it was not retained as a reliable language option for the final application.

## ⚠️ Limitations

- Translation quality can vary depending on the language pair and translation engine.
- Some translations may require grammatical or contextual corrections.
- Online translation services require an internet connection.
- Online services may have usage limits or temporary availability issues.
- Argos Translate requires the appropriate local language model to be installed.
- Not every language pair is guaranteed to have a local Argos model.
- Translation history is stored only during the current application session.

For important or official documents, always review the translated text before using it.

## 🎯 Project Objective

The objective of this project is to develop an interactive language translation application while demonstrating:

- Python programming
- Streamlit web application development
- Translation API integration
- Local machine translation
- Fallback-based service handling
- Error handling
- User interface design
- Translation testing

## 👩‍💻 Author

**A Mohana Priya**

**CodeAlpha Internship — Task 2**

## 📜 License

This project was created for educational and internship purposes.

Third-party libraries, translation services, and translation models are subject to their respective licenses and terms of use.

---

⭐ If you find this project useful, consider giving the repository a star!