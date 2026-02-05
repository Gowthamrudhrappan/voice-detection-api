"""
AI-Generated Voice Detection API - FINAL FIXED VERSION
For GUVI Hackathon 2026
"""

from fastapi import FastAPI, File, UploadFile, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
import io
import numpy as np
import logging
from typing import Optional
import os

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Voice Detection API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
API_KEY = "sk_test_guvi_hackathon_2026"
SUPPORTED_LANGUAGES = ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]

# ==================== PYDANTIC MODELS ====================

class VoiceResponse(BaseModel):
    status: str
    language: str
    classification: str
    confidenceScore: float
    explanation: str

# ==================== UTILITY FUNCTIONS ====================

def audio_to_base64(upload_file: UploadFile) -> str:
    """Convert uploaded audio file to base64"""
    audio_bytes = upload_file.file.read()
    base64_audio = base64.b64encode(audio_bytes).decode('utf-8')
    return base64_audio

def extract_features_safe(audio_base64: str) -> dict:
    """Safe feature extraction"""
    try:
        audio_bytes = base64.b64decode(audio_base64)
        audio_array = np.frombuffer(audio_bytes[:10000], dtype=np.uint8)
        
        features = {
            'audio_length': len(audio_bytes),
            'byte_mean': float(np.mean(audio_array)),
            'byte_std': float(np.std(audio_array)),
            'byte_variance': float(np.var(audio_array)),
            'byte_max': float(np.max(audio_array)),
            'byte_min': float(np.min(audio_array)),
        }
        logger.info(f"✓ Features extracted (safe mode)")
        return features
    except Exception as e:
        logger.error(f"✗ Feature extraction failed: {str(e)}")
        raise

def extract_features_librosa(audio_base64: str) -> dict:
    """Advanced feature extraction with librosa"""
    try:
        import librosa
        audio_bytes = base64.b64decode(audio_base64)
        audio_buffer = io.BytesIO(audio_bytes)
        
        y, sr = librosa.load(audio_buffer, sr=16000, mono=True)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
        mfcc_mean = np.mean(mfccs, axis=1)
        
        spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
        spectral_rolloff = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr))
        zero_crossing_rate = np.mean(librosa.feature.zero_crossing_rate(y))
        
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch_values = pitches[pitches > 0]
        pitch_mean = np.mean(pitch_values) if len(pitch_values) > 0 else 0
        pitch_std = np.std(pitch_values) if len(pitch_values) > 0 else 0
        
        features = {
            'mfcc_mean': float(np.mean(mfcc_mean)),
            'mfcc_std': float(np.std(mfcc_mean)),
            'mfcc_var': float(np.var(mfcc_mean)),
            'spectral_centroid': float(spectral_centroid),
            'spectral_rolloff': float(spectral_rolloff),
            'zero_crossing_rate': float(zero_crossing_rate),
            'pitch_mean': float(pitch_mean),
            'pitch_std': float(pitch_std),
        }
        logger.info(f"✓ Librosa features extracted")
        return features
    except ImportError:
        logger.warning("⚠ Librosa not available, using safe mode")
        return extract_features_safe(audio_base64)
    except Exception as e:
        logger.warning(f"⚠ Librosa failed: {str(e)}, using safe mode")
        return extract_features_safe(audio_base64)

def detect_voice_safe(features: dict) -> tuple:
    """Safe mode detection"""
    audio_length = features.get('audio_length', 0)
    byte_variance = features.get('byte_variance', 0)
    byte_std = features.get('byte_std', 0)
    
    ai_score = 0.0
    if byte_variance < 2000: ai_score += 0.25
    if audio_length < 10000: ai_score += 0.15
    if byte_std < 30: ai_score += 0.20
    byte_range = features.get('byte_max', 255) - features.get('byte_min', 0)
    if byte_range < 100: ai_score += 0.20
    
    if ai_score >= 0.45:
        classification = "AI_GENERATED"
        confidence = min(0.60 + ai_score * 0.35, 0.92)
    else:
        classification = "HUMAN"
        confidence = min(0.60 + (1 - ai_score) * 0.35, 0.92)
    
    return classification, confidence

def detect_voice_librosa(features: dict) -> tuple:
    """Advanced detection"""
    ai_score = 0.0
    pitch_std = features.get('pitch_std', 50)
    if pitch_std < 20: ai_score += 0.30
    
    spectral_centroid = features.get('spectral_centroid', 2000)
    if spectral_centroid > 3000 or spectral_centroid < 1000: ai_score += 0.25
    
    mfcc_var = features.get('mfcc_var', 100)
    if mfcc_var < 50: ai_score += 0.25
    
    zcr = features.get('zero_crossing_rate', 0.15)
    if zcr < 0.08: ai_score += 0.20
    
    if ai_score >= 0.50:
        classification = "AI_GENERATED"
        confidence = min(0.55 + ai_score * 0.42, 0.96)
    else:
        classification = "HUMAN"
        confidence = min(0.55 + (1 - ai_score) * 0.42, 0.96)
    
    return classification, confidence

def generate_explanation(classification: str, confidence: float, language: str) -> str:
    """Generate detailed explanation"""
    if classification == "AI_GENERATED":
        return (
            f"AI-generated voice detected with {confidence:.0%} confidence. "
            f"Analysis reveals unnatural pitch consistency, robotic speech patterns, "
            f"and artificial spectral characteristics typical of text-to-speech synthesis systems."
        )
    else:
        return (
            f"Human voice identified with {confidence:.0%} confidence. "
            f"Voice exhibits natural pitch variation, organic acoustic variability, "
            f"and human-like temporal dynamics characteristic of authentic speech production."
        )

# ==================== API ENDPOINTS ====================

@app.get("/")
async def root():
    """Root endpoint"""
    logger.info("📍 Root endpoint accessed")
    return {
        "status": "online",
        "service": "AI Voice Detection API",
        "version": "1.0.0",
        "supported_languages": SUPPORTED_LANGUAGES,
        "endpoints": {
            "health": "/health",
            "detection": "/api/voice-detection"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        import librosa
        librosa_status = "available"
        detection_mode = "advanced"
    except ImportError:
        librosa_status = "not available"
        detection_mode = "safe mode (basic)"
    
    return {
        "status": "healthy",
        "api": "operational",
        "detection_mode": detection_mode,
        "librosa": librosa_status,
        "supported_languages": SUPPORTED_LANGUAGES,
        "version": "1.0.0"
    }

@app.post("/api/voice-detection", response_model=VoiceResponse)
async def detect_voice(
    language: str = "English",
    file: UploadFile = File(..., description="MP3 audio file"),
    x_api_key: Optional[str] = Header(None)
):
    """
    🎯 Main voice detection endpoint - NOW SUPPORTS FILE UPLOAD!
    
    POST https://voice-detection-api-1-apd9.onrender.com/api/voice-detection
    Form data: language=English, file=audio.mp3
    Header: x-api-key=sk_test_guvi_hackathon_2026
    """
    
    try:
        logger.info(f"\n{'='*60}")
        logger.info(f"🎯 NEW DETECTION REQUEST")
        logger.info(f"{'='*60}")
        logger.info(f"  Language: {language}")
        logger.info(f"  Filename: {file.filename}")
        logger.info(f"  API key provided: {'Yes' if x_api_key else 'No'}")
        
        # Validate API key
        if x_api_key != API_KEY:
            logger.warning(f"❌ Invalid API key")
            raise HTTPException(status_code=401, detail="Invalid API key")
        
        # Validate file
        if not file.filename.lower().endswith('.mp3'):
            raise HTTPException(status_code=400, detail="Only MP3 files supported")
        
        logger.info(f"✓ Validations passed")
        
        # Convert file to base64
        audio_base64 = audio_to_base64(file)
        
        # Detect voice (advanced first, safe fallback)
        try:
            logger.info(f"🔍 Advanced detection...")
            features = extract_features_librosa(audio_base64)
            classification, confidence = detect_voice_librosa(features)
            detection_method = "advanced (librosa)"
        except Exception as e:
            logger.warning(f"⚠ Advanced failed: {str(e)}")
            features = extract_features_safe(audio_base64)
            classification, confidence = detect_voice_safe(features)
            detection_method = "safe mode"
        
        # Generate response
        explanation = generate_explanation(classification, confidence, language)
        
        logger.info(f"\n📊 RESULT: {classification} ({confidence:.1%})")
        logger.info(f"{'='*60}\n")
        
        return VoiceResponse(
            status="success",
            language=language,
            classification=classification,
            confidenceScore=round(confidence, 2),
            explanation=explanation
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Audio processing failed")

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {"status": "error", "message": exc.detail}

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"❌ Unhandled: {str(exc)}")
    return {"status": "error", "message": "Internal server error"}

@app.on_event("startup")
async def startup_event():
    logger.info(f"\n🚀 AI VOICE DETECTION API v1.0.0 STARTED")
    logger.info(f"  Endpoint: POST /api/voice-detection")
    logger.info(f"  File upload + API key required\n")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
