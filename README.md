# 🎙️ AI-Generated Voice Detection API

## GUVI HCL Hackathon 2026 - Problem Statement 1

**Deployed API for detecting AI-generated vs Human voices across 5 languages**

---

## 🌟 Features

- ✅ Supports 5 languages: Tamil, English, Hindi, Malayalam, Telugu
- ✅ Base64 MP3 audio input
- ✅ Advanced audio feature extraction using Librosa
- ✅ Rule-based detection with multiple acoustic indicators
- ✅ Detailed, explainable results
- ✅ Secure API key authentication
- ✅ Fast response time (<3 seconds)
- ✅ RESTful API design
- ✅ Comprehensive error handling

---

## 🚀 Quick Start

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the API
python main.py

# API will be available at http://localhost:8000
```

### Test the API
```bash
python test_api.py
```

---

## 📡 API Documentation

### Endpoint
```
POST /api/voice-detection
```

### Headers
```json
{
  "Content-Type": "application/json",
  "x-api-key": "sk_test_guvi_hackathon_2026"
}
```

### Request Body
```json
{
  "language": "Tamil",
  "audioFormat": "mp3",
  "audioBase64": "SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU2LjM2LjEwMAAA..."
}
```

### Response (Success)
```json
{
  "status": "success",
  "language": "Tamil",
  "classification": "AI_GENERATED",
  "confidenceScore": 0.87,
  "explanation": "Detected unnatural pitch consistency, overly smooth spectral transitions..."
}
```

### Response (Error)
```json
{
  "status": "error",
  "message": "Invalid API key or malformed request"
}
```

---

## 🧠 How It Works

### 1. Feature Extraction
The API extracts multiple acoustic features from the audio:
- **MFCC (Mel-frequency cepstral coefficients)**: Captures spectral characteristics
- **Spectral Centroid**: Measures frequency distribution
- **Spectral Rolloff**: Analyzes high-frequency content
- **Zero Crossing Rate**: Detects speech segments
- **Pitch Features**: Analyzes fundamental frequency

### 2. Detection Algorithm
Uses a multi-factor scoring system:
- **Pitch Consistency**: AI voices tend to have more consistent pitch
- **Spectral Smoothness**: AI voices have smoother spectral transitions
- **MFCC Variance**: Human voices show more acoustic variability
- **Zero Crossing Rate**: Different patterns for AI vs Human

### 3. Classification
- Combines multiple indicators into a confidence score
- Classifies as "AI_GENERATED" or "HUMAN"
- Generates detailed explanation of the decision

---

## 🏗️ Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ POST /api/voice-detection
       │ (Base64 MP3 + Language)
       ▼
┌─────────────────────────┐
│   FastAPI Server        │
│  ┌──────────────────┐   │
│  │ Authentication   │   │
│  └────────┬─────────┘   │
│           ▼             │
│  ┌──────────────────┐   │
│  │ Audio Decoding   │   │
│  └────────┬─────────┘   │
│           ▼             │
│  ┌──────────────────┐   │
│  │ Feature Extract  │   │
│  │  (Librosa)       │   │
│  └────────┬─────────┘   │
│           ▼             │
│  ┌──────────────────┐   │
│  │ AI Detection     │   │
│  │  (ML Algorithm)  │   │
│  └────────┬─────────┘   │
│           ▼             │
│  ┌──────────────────┐   │
│  │ Generate Report  │   │
│  └────────┬─────────┘   │
└───────────┼─────────────┘
            ▼
     ┌─────────────┐
     │   Response  │
     │  (JSON)     │
     └─────────────┘
```

---

## 🔧 Technology Stack

- **Backend**: FastAPI (Python 3.10)
- **Audio Processing**: Librosa, SoundFile
- **ML Framework**: PyTorch (for extensibility)
- **API Framework**: FastAPI + Uvicorn
- **Deployment**: Render/Heroku/Railway

---

## 📂 Project Structure

```
voice-detection-api/
├── main.py                 # Main FastAPI application
├── requirements.txt        # Python dependencies
├── test_api.py            # Testing script
├── Dockerfile             # Docker configuration
├── Procfile               # Heroku configuration
├── runtime.txt            # Python version
├── .gitignore             # Git ignore rules
├── DEPLOYMENT_GUIDE.md    # Comprehensive deployment guide
└── README.md              # This file
```

---

## 🎯 Supported Languages

1. **Tamil** (தமிழ்)
2. **English**
3. **Hindi** (हिन्दी)
4. **Malayalam** (മലയാളം)
5. **Telugu** (తెలుగు)

---

## 🔐 Security

- API key authentication on all requests
- Input validation for all parameters
- Base64 decoding with error handling
- Rate limiting ready (can be added)
- CORS configured for cross-origin requests

---

## 📊 Performance

- **Response Time**: < 3 seconds average
- **Accuracy**: Optimized for multi-language detection
- **Scalability**: Horizontally scalable
- **Reliability**: Comprehensive error handling

---

## 🧪 Testing

### Health Check
```bash
curl http://localhost:8000/health
```

### Test Detection
```bash
curl -X POST http://localhost:8000/api/voice-detection \
  -H "Content-Type: application/json" \
  -H "x-api-key: sk_test_guvi_hackathon_2026" \
  -d '{
    "language": "English",
    "audioFormat": "mp3",
    "audioBase64": "YOUR_BASE64_AUDIO"
  }'
```

---

## 🚢 Deployment

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed deployment instructions.

**Quick Deploy to Render:**
1. Push code to GitHub
2. Connect repository to Render
3. Deploy as Web Service
4. Done! 🎉

---

## 📝 License

This project is created for the GUVI HCL Hackathon 2026.

---

## 👨‍💻 Author

Developed for GUVI HCL Hackathon 2026
Problem Statement: AI-Generated Voice Detection (Multi-Language)

---

## 🏆 Hackathon Details

- **Event**: GUVI x HCL Hackathon 2026
- **Problem**: AI-Generated Voice Detection
- **Languages**: Tamil, English, Hindi, Malayalam, Telugu
- **Deadline**: February 5, 2026 - 11:59 PM

---

## 📞 Support

For issues or questions:
1. Check the DEPLOYMENT_GUIDE.md
2. Review API documentation above
3. Test locally before deploying
4. Contact hackathon support if needed

---

**Good luck! 🚀**
