# 🚀 QUICK COPY-PASTE COMMANDS FOR TONIGHT

## ⚡ FASTEST PATH TO DEPLOYMENT (30 MINUTES)

### STEP 1: Create Project Folder (1 minute)
```bash
# Windows (Command Prompt)
mkdir C:\Users\%USERNAME%\Desktop\voice-api
cd C:\Users\%USERNAME%\Desktop\voice-api

# Mac/Linux (Terminal)
mkdir ~/Desktop/voice-api
cd ~/Desktop/voice-api
```

### STEP 2: Copy All Files (2 minutes)
```
Copy these files from the project to your folder:
- main.py
- requirements.txt
- Procfile
- runtime.txt
- test_api.py
- Dockerfile
- .gitignore
- README.md
- DEPLOYMENT_GUIDE.md
```

### STEP 3: Install Dependencies (3 minutes)
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### STEP 4: Test Locally (2 minutes - OPTIONAL)
```bash
# Run API
python main.py

# In another terminal, test
python test_api.py
```

### STEP 5: Deploy to Render (15 minutes)
```bash
# Initialize git
git init
git add .
git commit -m "Voice detection API"

# Create GitHub repo at https://github.com/new
# Then push:
git remote add origin https://github.com/YOUR_USERNAME/voice-api.git
git branch -M main
git push -u origin main

# Now go to https://render.com
# 1. Sign up with GitHub
# 2. New → Web Service
# 3. Connect your repo
# 4. Settings:
#    - Name: voice-detection-api
#    - Build: pip install -r requirements.txt
#    - Start: uvicorn main:app --host 0.0.0.0 --port $PORT
# 5. Create Web Service
# 6. Wait for deployment (5-10 min)
```

### STEP 6: Get Your URL (1 minute)
```
Your API will be at:
https://voice-detection-api-xxxx.onrender.com

Full endpoint:
https://voice-detection-api-xxxx.onrender.com/api/voice-detection
```

### STEP 7: Test with GUVI Tester (3 minutes)
```
1. Go to GUVI Dashboard → Timeline
2. Find "API Endpoint Tester"
3. Enter:
   - Endpoint: https://your-url.onrender.com/api/voice-detection
   - x-api-key: sk_test_guvi_hackathon_2026
   - Language: Tamil
   - Audio: Upload or paste base64
4. Click "Test Endpoint"
5. Verify response
```

### STEP 8: Submit (2 minutes)
```
1. Go to Submission Form
2. Enter:
   - Deployed URL: https://your-url.onrender.com/api/voice-detection
   - API KEY: sk_test_guvi_hackathon_2026
3. Submit for review
4. ✅ DONE!
```

---

## 🔥 EVEN FASTER - HEROKU ONE-LINER (IF YOU HAVE HEROKU CLI)

```bash
# Setup
mkdir voice-api && cd voice-api
# (Copy all files here)

# Deploy
heroku login
heroku create voice-api-$(date +%s)
git init
git add .
git commit -m "Deploy"
git push heroku main

# Get URL
heroku info
```

---

## 🆘 EMERGENCY BACKUP PLAN

If deployment fails, use PythonAnywhere (FREE):

1. Go to https://www.pythonanywhere.com
2. Sign up for free account
3. Upload your files
4. Install packages in bash console:
   ```bash
   pip install --user -r requirements.txt
   ```
5. Configure web app
6. Get URL: yourname.pythonanywhere.com

---

## 🎯 YOUR COMPLETE SUBMISSION

```
Deployed URL: https://your-app-name.onrender.com/api/voice-detection
API KEY: sk_test_guvi_hackathon_2026
```

---

## ⏰ TIME TRACKING

- Setup: 5 min
- Deploy: 15 min
- Test: 5 min
- Submit: 3 min
- **TOTAL: 28 MINUTES**

You have plenty of time! Start NOW! 🚀
