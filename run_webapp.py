"""
Quick deployment script for MiniLang Compiler Web App
"""

import subprocess
import sys
import os

def check_requirements():
    """Check if required packages are installed."""
    try:
        import streamlit
        import pandas
        print("✅ All dependencies are installed!")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def install_requirements():
    """Install required packages."""
    print("📦 Installing requirements...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("✅ Requirements installed successfully!")

def run_app():
    """Run the Streamlit app."""
    print("🚀 Starting MiniLang Compiler Web App...")
    print("📱 The app will open in your browser at: http://localhost:8501")
    print("🛑 Press Ctrl+C to stop the server")
    
    subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])

def main():
    print("🔧 MiniLang Compiler Web App")
    print("=" * 50)
    
    if not check_requirements():
        install_requirements()
    
    run_app()

if __name__ == "__main__":
    main()