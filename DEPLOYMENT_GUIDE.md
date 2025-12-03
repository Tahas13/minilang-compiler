# 🚀 Deploy MiniLang Compiler to Cloud

## Quick Deploy to Streamlit Cloud (Recommended)

### Step 1: Push to GitHub

```powershell
# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "MiniLang Compiler - Ready for deployment"

# Create GitHub repo and push
# Go to github.com, create new repository, then:
git remote add origin https://github.com/YOUR_USERNAME/minilang-compiler.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io
2. Click "New app"
3. Connect your GitHub repository
4. Set:
   - **Repository:** your-username/minilang-compiler
   - **Branch:** main
   - **Main file:** streamlit_app.py
5. Click "Deploy!"

### Step 3: Done! 🎉

Your app will be live at: `https://your-app-name.streamlit.app`

---

## Important Notes

### C++ Executable on Cloud
The C++ executable (`minilang_compiler.exe`) won't work on Streamlit Cloud (Linux environment). The app automatically falls back to the Python implementation, which:
- ✅ Works identically
- ✅ Produces same results
- ✅ Has same functionality

### For Local Presentation
Keep using the C++ core locally for your professor:
```powershell
streamlit run streamlit_app.py
```

### Show Both Versions
- **Local:** "Running with C++ compiler core"
- **Cloud:** "Python implementation (same functionality)"

---

## Alternative: Deploy with C++ Support

If you need the C++ version in production:

### Option 1: Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.11
RUN apt-get update && apt-get install -y g++
WORKDIR /app
COPY . .
RUN cd cpp_core && g++ -std=c++17 -O2 -o minilang_compiler main.cpp
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "streamlit_app.py"]
```

Deploy to:
- Render.com
- Railway.app
- Fly.io

### Option 2: VPS Deployment
Deploy to a VPS (DigitalOcean, Linode, AWS EC2) where you have full control.

---

## Quick Test Before Deploy

```powershell
# Test locally first
streamlit run streamlit_app.py

# Visit http://localhost:8501
# Compile some examples
# Ensure everything works
```

---

## Environment Variables (Optional)

If needed, create `.streamlit/config.toml`:
```toml
[server]
port = 8501
enableCORS = false

[browser]
gatherUsageStats = false
```

---

## Post-Deployment

After deploying:
1. ✅ Test all examples
2. ✅ Verify compilation works
3. ✅ Check AST visualization
4. ✅ Share the link!

Your deployed app URL will be:
- Streamlit Cloud: `https://[app-name].streamlit.app`
- Render: `https://[app-name].onrender.com`

---

## For Your Presentation

**Show two versions:**
1. **Local (C++ core):** Full implementation with compiled executable
2. **Cloud (Python):** Same functionality, accessible anywhere

Both versions demonstrate your compiler correctly! 🎓
