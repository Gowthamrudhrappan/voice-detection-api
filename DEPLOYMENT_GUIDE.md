# 🚀 AI VOICE DETECTION API - COMPLETE DEPLOYMENT GUIDE

## 📋 **OVERVIEW**
This is your complete ready-to-deploy AI Voice Detection API for the GUVI Hackathon.
**Deadline: Feb 5, 2026 - 11:59 PM**

---

## 🎯 **QUICK START - 3 DEPLOYMENT OPTIONS**

### **OPTION 1: RENDER (RECOMMENDED - FASTEST & FREE)**

#### Step 1: Create Account
1. Go to https://render.com
2. Sign up with GitHub account

#### Step 2: Create New Web Service
1. Click "New" → "Web Service"
2. Connect your GitHub repository OR use "Deploy from Git"
3. If no repo, follow these steps:

#### Step 3: Setup GitHub Repository (if needed)
```bash
# On your local machine
git init
git add .
git commit -m "Initial commit - Voice Detection API"
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

#### Step 4: Configure Render
- **Name**: voice-detection-api
- **Environment**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Plan**: Free

#### Step 5: Deploy
- Click "Create Web Service"
- Wait 5-10 minutes for deployment
- Your API will be live at: `https://voice-detection-api-xxxx.onrender.com`

#### Step 6: Test Your API
```bash
# Test health check
curl https://your-render-url.onrender.com/health

# Test with the endpoint tester provided by GUVI
```

#### Step 7: Submit
- URL: `https://your-render-url.onrender.com/api/voice-detection`
- API Key: `sk_test_guvi_hackathon_2026`

---

### **OPTION 2: HEROKU (RELIABLE)**

#### Step 1: Install Heroku CLI
```bash
# Download from https://devcenter.heroku.com/articles/heroku-cli
# Or use:
# Windows: Download installer
# Mac: brew tap heroku/brew && brew install heroku
# Linux: curl https://cli-assets.heroku.com/install.sh | sh
```

#### Step 2: Login to Heroku
```bash
heroku login
```

#### Step 3: Create Heroku App
```bash
# In your project directory
heroku create voice-detection-api-guvi
```

#### Step 4: Deploy
```bash
git init
git add .
git commit -m "Deploy voice detection API"
git push heroku main
```

#### Step 5: Verify Deployment
```bash
heroku logs --tail
heroku open
```

#### Step 6: Get Your URL
```bash
heroku info
# Your API URL will be: https://voice-detection-api-guvi.herokuapp.com
```

#### Step 7: Submit
- URL: `https://your-app-name.herokuapp.com/api/voice-detection`
- API Key: `sk_test_guvi_hackathon_2026`

---

### **OPTION 3: RAILWAY (ALTERNATIVE)**

#### Step 1: Create Account
1. Go to https://railway.app
2. Sign up with GitHub

#### Step 2: New Project
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your repository

#### Step 3: Configure
- Railway will auto-detect Python
- It will use your Procfile automatically

#### Step 4: Deploy
- Automatic deployment starts
- Get your URL from Railway dashboard

---

## 🧪 **LOCAL TESTING BEFORE DEPLOYMENT**

### Step 1: Install Dependencies
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### Step 2: Run Locally
```bash
python main.py
```

### Step 3: Test Locally
```bash
# In another terminal
python test_api.py
```

### Step 4: Test with cURL
```bash
curl -X POST http://localhost:8000/api/voice-detection \
  -H "Content-Type: application/json" \
  -H "x-api-key: sk_test_guvi_hackathon_2026" \
  -d '{
    "language": "English",
    "audioFormat": "mp3",
    "audioBase64": "YOUR_BASE64_AUDIO_HERE"
  }'
```

---

## 📝 **USING THE GUVI ENDPOINT TESTER**

### Step 1: Access Tester
- Go to the Timeline section in your GUVI dashboard
- Find "AI-Generated Voice Detection - API Endpoint Tester"

### Step 2: Fill in Details
- **Headers**: `x-api-key`
- **x-api-key value**: `sk_test_guvi_hackathon_2026`
- **Endpoint URL**: Your deployed URL + `/api/voice-detection`
- **Language**: Select from Tamil, English, Hindi, Malayalam, Telugu
- **Audio Format**: mp3
- **Audio Base64 Format**: The base64 encoded audio

### Step 3: Test
- Click "Test Endpoint"
- Verify the response matches the expected format

---

## 🎨 **CUSTOMIZATION OPTIONS**

### Change API Key
In `main.py`, line 32:
```python
API_KEY = "your_custom_secret_key_here"
```

### Adjust Detection Sensitivity
In `main.py`, `rule_based_detection` function, adjust scoring thresholds:
```python
# Make it more sensitive to AI detection
if indicators['pitch_consistency'] > 80:  # Lower threshold
    ai_score += 0.35  # Higher weight
```

### Add More Languages
In `main.py`, line 33:
```python
SUPPORTED_LANGUAGES = ["Tamil", "English", "Hindi", "Malayalam", "Telugu", "Kannada"]
```

---

## 🐛 **TROUBLESHOOTING**

### Issue: "Module not found" error
**Solution**: Install missing dependencies
```bash
pip install -r requirements.txt
```

### Issue: "Port already in use"
**Solution**: Change port in main.py
```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # Use different port
```

### Issue: Audio processing error
**Solution**: Ensure audio is properly base64 encoded
```python
import base64
with open('audio.mp3', 'rb') as f:
    base64_audio = base64.b64encode(f.read()).decode('utf-8')
```

### Issue: Deployment fails on Heroku
**Solution**: Check logs
```bash
heroku logs --tail
```
Common fix: Ensure all files are committed
```bash
git add .
git commit -m "Fix deployment"
git push heroku main
```

---

## 🏆 **SUBMISSION CHECKLIST**

- [ ] API is deployed and publicly accessible
- [ ] Health check endpoint works: `/health`
- [ ] Main endpoint works: `/api/voice-detection`
- [ ] API key authentication is working
- [ ] Tested with GUVI endpoint tester
- [ ] Response format matches specification exactly
- [ ] All 5 languages are supported
- [ ] Confidence scores are between 0.0 and 1.0
- [ ] Explanation text is meaningful and specific
- [ ] API responds within 5 seconds
- [ ] Error handling works properly

---

## 📊 **EXPECTED API RESPONSE FORMAT**

### Success Response
```json
{
  "status": "success",
  "language": "Tamil",
  "classification": "AI_GENERATED",
  "confidenceScore": 0.87,
  "explanation": "Detected unnatural pitch consistency, overly smooth spectral transitions typical of AI-generated voice synthesis. Confidence: 87%. These patterns suggest algorithmic voice generation rather than natural human speech production."
}
```

### Error Response
```json
{
  "status": "error",
  "message": "Invalid API key or malformed request"
}
```

---

## 🎯 **FINAL SUBMISSION STEPS**

### Step 1: Get Your Deployed URL
- From Render: `https://your-app.onrender.com/api/voice-detection`
- From Heroku: `https://your-app.herokuapp.com/api/voice-detection`
- From Railway: `https://your-app.railway.app/api/voice-detection`

### Step 2: Get Your API Key
- Default: `sk_test_guvi_hackathon_2026`
- Or your custom key if you changed it

### Step 3: Test One More Time
Use the GUVI endpoint tester to verify everything works

### Step 4: Submit on GUVI Platform
1. Go to submission form
2. Enter "Deployed URL": Your full API endpoint URL
3. Enter "API KEY": Your API key
4. Click "Submit for review"

### Step 5: Verify Submission
- Check that submission status shows "Submitted"
- Wait for evaluation results

---

## ⚡ **QUICK DEPLOYMENT COMMANDS (COPY-PASTE)**

### For Render (via GitHub):
```bash
# 1. Initialize git
git init
git add .
git commit -m "Voice detection API for GUVI hackathon"

# 2. Push to GitHub
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main

# 3. Connect to Render and deploy (use web interface)
```

### For Heroku:
```bash
# 1. Install Heroku CLI, then:
heroku login
heroku create voice-detection-api-$(date +%s)
git init
git add .
git commit -m "Voice detection API"
git push heroku main

# 2. Get your URL
heroku info | grep "Web URL"
```

### For Docker (Advanced):
```bash
# Build
docker build -t voice-detection-api .

# Run locally
docker run -p 8000:8000 voice-detection-api

# Deploy to cloud (AWS, GCP, etc.)
```

---

## 💡 **TIPS FOR WINNING**

1. **Test thoroughly** - Use multiple audio samples
2. **Optimize response time** - Keep it under 3 seconds
3. **Write detailed explanations** - Don't just say "AI detected"
4. **Handle errors gracefully** - Return proper error messages
5. **Support all 5 languages** - Don't skip any language
6. **Deploy early** - Don't wait until last minute
7. **Keep API stable** - Ensure it doesn't crash under load

---

## 📞 **SUPPORT**

If you face any issues:
1. Check the troubleshooting section
2. Review the GUVI documentation
3. Test locally first before deploying
4. Check deployment platform logs

---

## ✅ **YOU'RE READY TO WIN!**

Follow this guide step by step, and you'll have your API deployed and submitted before the deadline.

**Good luck! 🚀**
