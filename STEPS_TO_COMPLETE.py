"""
STEP-BY-STEP EXECUTION SCRIPT
Run this to complete the hackathon tonight
"""

import os
import sys

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

def print_step(step_num, text):
    print(f"\n{'■'*3} STEP {step_num}: {text}")
    print("-"*70)

def main():
    print_header("🚀 GUVI HACKATHON - AI VOICE DETECTION API")
    print("Complete deployment guide for tonight!\n")
    
    print_step(1, "SETUP YOUR ENVIRONMENT")
    print("""
    Choose your operating system:
    
    WINDOWS:
    --------
    1. Open Command Prompt or PowerShell
    2. Navigate to your project folder:
       cd C:\\Users\\YourName\\Desktop\\voice-detection-api
    3. Create virtual environment:
       python -m venv venv
    4. Activate virtual environment:
       venv\\Scripts\\activate
    5. Install dependencies:
       pip install -r requirements.txt
    
    MAC/LINUX:
    ----------
    1. Open Terminal
    2. Navigate to your project folder:
       cd ~/Desktop/voice-detection-api
    3. Create virtual environment:
       python3 -m venv venv
    4. Activate virtual environment:
       source venv/bin/activate
    5. Install dependencies:
       pip install -r requirements.txt
    """)
    
    print_step(2, "TEST LOCALLY (OPTIONAL BUT RECOMMENDED)")
    print("""
    1. Run the API:
       python main.py
    
    2. Open another terminal and test:
       python test_api.py
    
    3. Or test with browser:
       Go to: http://localhost:8000
       You should see: {"status": "online", ...}
    
    4. Stop the server: Press Ctrl+C
    """)
    
    print_step(3, "CHOOSE YOUR DEPLOYMENT METHOD")
    print("""
    ┌─────────────────────────────────────────────────────────┐
    │  OPTION 1: RENDER (RECOMMENDED - EASIEST & FREE)        │
    └─────────────────────────────────────────────────────────┘
    
    A. Create GitHub Repository:
       1. Go to https://github.com
       2. Click "New Repository"
       3. Name: voice-detection-api
       4. Create repository
    
    B. Upload Your Code to GitHub:
       1. Open terminal in your project folder
       2. Run these commands:
       
          git init
          git add .
          git commit -m "Initial commit"
          git remote add origin https://github.com/YOUR_USERNAME/voice-detection-api.git
          git branch -M main
          git push -u origin main
    
    C. Deploy on Render:
       1. Go to https://render.com
       2. Sign up/Login with GitHub
       3. Click "New +" → "Web Service"
       4. Connect your GitHub repository
       5. Configure:
          - Name: voice-detection-api
          - Environment: Python 3
          - Build Command: pip install -r requirements.txt
          - Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
          - Plan: Free
       6. Click "Create Web Service"
       7. Wait 5-10 minutes for deployment
       8. Copy your URL: https://voice-detection-api-xxxx.onrender.com
    
    ┌─────────────────────────────────────────────────────────┐
    │  OPTION 2: HEROKU (RELIABLE)                            │
    └─────────────────────────────────────────────────────────┘
    
    A. Install Heroku CLI:
       Download from: https://devcenter.heroku.com/articles/heroku-cli
    
    B. Deploy:
       1. Open terminal in project folder
       2. Login to Heroku:
          heroku login
       
       3. Create app:
          heroku create voice-detection-api-YOURNAME
       
       4. Deploy:
          git init
          git add .
          git commit -m "Deploy to Heroku"
          git push heroku main
       
       5. Get your URL:
          heroku info
          Copy the "Web URL"
    
    ┌─────────────────────────────────────────────────────────┐
    │  OPTION 3: RAILWAY (ALTERNATIVE)                        │
    └─────────────────────────────────────────────────────────┘
    
    1. Go to https://railway.app
    2. Sign up with GitHub
    3. Click "New Project"
    4. Select "Deploy from GitHub repo"
    5. Choose your repository
    6. Railway auto-deploys
    7. Get URL from dashboard
    """)
    
    print_step(4, "TEST YOUR DEPLOYED API")
    print("""
    1. Replace YOUR_DEPLOYED_URL in test_api.py:
       API_URL = "https://your-deployed-url.onrender.com/api/voice-detection"
    
    2. Test health check:
       Visit: https://your-deployed-url.onrender.com/health
       Should see: {"status": "healthy", ...}
    
    3. Use GUVI Endpoint Tester:
       - Go to GUVI Dashboard → Timeline
       - Find "API Endpoint Tester"
       - Fill in:
         * Endpoint URL: https://your-url.onrender.com/api/voice-detection
         * x-api-key: sk_test_guvi_hackathon_2026
         * Language: Tamil (or any supported language)
         * Upload sample audio or use base64
       - Click "Test Endpoint"
       - Verify response format
    """)
    
    print_step(5, "SUBMIT TO GUVI")
    print("""
    1. Go to GUVI Hackathon Dashboard
    2. Navigate to Submission Form
    3. Fill in:
       ┌─────────────────────────────────────────────┐
       │ Deployed URL:                               │
       │ https://your-app-url.onrender.com/api/voice-detection │
       │                                             │
       │ API KEY:                                    │
       │ sk_test_guvi_hackathon_2026                 │
       └─────────────────────────────────────────────┘
    
    4. Click "Submit for review"
    5. Verify submission status shows "Submitted"
    
    ✅ YOU'RE DONE! 
    """)
    
    print_header("⏰ TIMELINE FOR TONIGHT")
    print("""
    NOW - 9:00 PM:   Setup environment and test locally
    9:00 - 10:00 PM: Deploy to Render/Heroku
    10:00 - 10:30 PM: Test deployed API thoroughly
    10:30 - 11:00 PM: Submit on GUVI platform
    11:00 - 11:59 PM: Final verification and backup plan
    
    DEADLINE: 11:59 PM - Don't wait till last minute!
    """)
    
    print_header("🆘 TROUBLESHOOTING")
    print("""
    Problem: "Module not found"
    Solution: pip install -r requirements.txt
    
    Problem: "Port already in use"
    Solution: Change port in main.py to 8001
    
    Problem: Deployment fails
    Solution: Check logs on your platform (Render/Heroku)
              Ensure all files are committed to git
    
    Problem: API returns error
    Solution: Check that audio is properly base64 encoded
              Verify API key matches
              Test with GUVI's sample audio first
    """)
    
    print_header("📋 FINAL CHECKLIST")
    checklist = [
        "Files created: main.py, requirements.txt, Procfile",
        "Code tested locally",
        "GitHub repository created",
        "Code pushed to GitHub",
        "Deployed to Render/Heroku/Railway",
        "Health check endpoint works",
        "API endpoint works with test audio",
        "Tested with GUVI endpoint tester",
        "Response format matches specification",
        "API key authentication working",
        "Submitted on GUVI platform",
        "Verified submission status"
    ]
    
    for i, item in enumerate(checklist, 1):
        print(f"  [ ] {i}. {item}")
    
    print("\n" + "="*70)
    print("\n🎯 YOU HAVE EVERYTHING YOU NEED!")
    print("💪 Follow these steps and you'll finish before midnight!")
    print("🏆 GOOD LUCK!\n")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
