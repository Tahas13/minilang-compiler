# MiniLang Compiler Web App Deployment Guide

## 🚀 Local Development

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone/Download the project:**
   ```bash
   cd c:\Users\TAHA\Documents\cc_project
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app:**
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Open in browser:**
   - The app will automatically open in your default browser
   - If not, navigate to: `http://localhost:8501`

## 🌐 Cloud Deployment Options

### Option 1: Streamlit Cloud (Recommended - FREE)

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/minilang-compiler.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Visit: https://share.streamlit.io/
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file path: `streamlit_app.py`
   - Click "Deploy"

### Option 2: Heroku (FREE tier available)

1. **Create Heroku app:**
   ```bash
   heroku create minilang-compiler-app
   ```

2. **Create Procfile:**
   ```bash
   echo "web: streamlit run streamlit_app.py --server.port $PORT" > Procfile
   ```

3. **Deploy:**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

### Option 3: Railway (Modern deployment)

1. **Connect GitHub repo to Railway:**
   - Visit: https://railway.app/
   - Connect your GitHub account
   - Select your repository
   - Railway will auto-detect Streamlit and deploy

## 📱 Features of the Web App

### 🎯 Interactive Code Editor
- Real-time MiniLang code editing
- Pre-loaded example programs
- Syntax highlighting and formatting

### 🔍 Three-Phase Compilation
- **Lexical Analysis:** Token generation with detailed view
- **Syntax Analysis:** AST tree visualization  
- **Semantic Analysis:** Type checking and error detection

### 📊 Visual Results
- Interactive token table
- Beautiful AST tree display
- Symbol table visualization
- Comprehensive error reporting

### 🛠️ Developer Features
- Multiple example programs
- Language reference guide
- Configurable display options
- Real-time compilation feedback

## 🎨 Web App Screenshots

### Main Interface
- Split-screen layout with editor and results
- Professional styling with color-coded phases
- Interactive sidebar with examples and settings

### Compilation Results
- Phase-by-phase compilation progress
- Success/error indicators with detailed messages
- Expandable sections for detailed analysis

### AST Visualization
- Clean vertical tree structure
- Proper indentation and branching
- Easy-to-read node relationships

## 🏆 Extra Credit Features

1. **Professional Web Interface** - Modern, responsive design
2. **Real-time Compilation** - Instant feedback on code changes
3. **Interactive Examples** - Multiple pre-loaded programs
4. **Visual AST Display** - Beautiful tree representation
5. **Cloud Deployment Ready** - Easy deployment to multiple platforms
6. **Error Visualization** - Color-coded error reporting
7. **Symbol Table Display** - Interactive variable tracking
8. **Mobile Responsive** - Works on all devices

## 🚀 Demo URLs

Once deployed, you can share these URLs for demonstration:

- **Streamlit Cloud:** `https://YOUR_USERNAME-minilang-compiler-streamlit-app-xxxxx.streamlit.app/`
- **Heroku:** `https://minilang-compiler-app.herokuapp.com/`
- **Railway:** `https://minilang-compiler.up.railway.app/`

## 💡 Presentation Tips

1. **Start with Simple Example** - Show basic variable declarations
2. **Demonstrate Error Handling** - Use the error example to show semantic analysis
3. **Show AST Visualization** - Highlight the tree structure for complex expressions
4. **Interactive Features** - Let audience try different examples
5. **Deployment Showcase** - Show that it's accessible from anywhere

This web app will definitely give you extra marks for innovation and presentation! 🌟