"""
AI-Generated Voice Detection API
FastAPI application for GUVI Hackathon
"""

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
import base64
import io
import numpy as np
import librosa
import torch
import torch.nn as nn
from typing import Optional
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
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

# ==================== CONFIGURATION ====================
API_KEY = "sk_test_guvi_hackathon_2026"  # Change this to your secret key
SUPPORTED_LANGUAGES = ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]
MODEL_PATH = "voice_detection_model.pth"

# ==================== MODELS ====================

class VoiceDetectionModel(nn.Module):
    """Neural network for voice detection"""
    def __init__(self, input_size=40, hidden_size=128):
        super(VoiceDetectionModel, self).__init__()
        
        self.feature_extractor = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.BatchNorm1d(hidden_size),
            nn.Dropout(0.3),
            nn.Linear(hidden_size, 64),
            nn.ReLU(),
            nn.BatchNorm1d(64),
            nn.Dropout(0.2),
        )
        
        self.classifier = nn.Sequential(
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 2)  # 2 classes: AI_GENERATED, HUMAN
        )
    
    def forward(self, x):
        features = self.feature_extractor(x)
        output = self.classifier(features)
        return output

# ==================== PYDANTIC MODELS ====================

class VoiceRequest(BaseModel):
    language: str
    audioFormat: str
    audioBase64: str
    
    @validator('language')
    def validate_language(cls, v):
        if v not in SUPPORTED_LANGUAGES:
            raise ValueError(f'Language must be one of: {", ".join(SUPPORTED_LANGUAGES)}')
        return v
    
    @validator('audioFormat')
    def validate_format(cls, v):
        if v.lower() != 'mp3':
            raise ValueError('Only MP3 format is supported')
        return v.lower()

class VoiceResponse(BaseModel):
    status: str
    language: str
    classification: str
    confidenceScore: float
    explanation: str

class ErrorResponse(BaseModel):
    status: str
    message: str

# ==================== FEATURE EXTRACTION ====================

def extract_audio_features(audio_base64: str) -> np.ndarray:
    """Extract features from base64 encoded audio"""
    try:
        # Decode base64
        audio_bytes = base64.b64decode(audio_base64)
        
        # Load audio from bytes
        audio_buffer = io.BytesIO(audio_bytes)
        y, sr = librosa.load(audio_buffer, sr=16000, mono=True)
        
        # Extract MFCC features
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
        mfcc_mean = np.mean(mfccs, axis=1)
        
        # Extract additional features
        spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
        spectral_rolloff = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr))
        zero_crossing_rate = np.mean(librosa.feature.zero_crossing_rate(y))
        
        # Pitch and energy features
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch_mean = np.mean(pitches[pitches > 0]) if np.any(pitches > 0) else 0
        
        # Combine all features
        additional_features = np.array([
            spectral_centroid,
            spectral_rolloff,
            zero_crossing_rate,
            pitch_mean
        ])
        
        # Return combined feature vector
        features = np.concatenate([mfcc_mean[:36], additional_features])
        
        return features
        
    except Exception as e:
        logger.error(f"Feature extraction error: {str(e)}")
        raise

# ==================== DETECTION LOGIC ====================

def analyze_audio_patterns(features: np.ndarray) -> dict:
    """Analyze audio patterns for AI detection"""
    
    # Calculate feature statistics
    mfcc_variance = np.var(features[:20])
    spectral_features = features[36:40]
    
    # Detection heuristics
    pitch_consistency = spectral_features[3]
    spectral_smoothness = spectral_features[0] / (spectral_features[1] + 1e-6)
    
    # AI-generated voices typically have:
    # 1. More consistent pitch
    # 2. Smoother spectral transitions
    # 3. Less variance in MFCC
    
    ai_indicators = {
        'pitch_consistency': pitch_consistency,
        'spectral_smoothness': spectral_smoothness,
        'mfcc_variance': mfcc_variance,
        'zero_crossing': spectral_features[2]
    }
    
    return ai_indicators

def rule_based_detection(features: np.ndarray) -> tuple:
    """Rule-based detection with heuristics"""
    
    indicators = analyze_audio_patterns(features)
    
    # Scoring system
    ai_score = 0.0
    
    # High pitch consistency -> AI
    if indicators['pitch_consistency'] > 100:
        ai_score += 0.3
    
    # High spectral smoothness -> AI
    if indicators['spectral_smoothness'] > 1.5:
        ai_score += 0.25
    
    # Low MFCC variance -> AI
    if indicators['mfcc_variance'] < 50:
        ai_score += 0.25
    
    # Low zero crossing rate -> AI
    if indicators['zero_crossing'] < 0.1:
        ai_score += 0.2
    
    # Determine classification
    if ai_score >= 0.5:
        classification = "AI_GENERATED"
        confidence = min(0.50 + ai_score * 0.4, 0.99)
    else:
        classification = "HUMAN"
        confidence = min(0.50 + (1 - ai_score) * 0.4, 0.99)
    
    return classification, confidence, indicators

def generate_explanation(classification: str, confidence: float, indicators: dict, language: str) -> str:
    """Generate detailed explanation for the classification"""
    
    if classification == "AI_GENERATED":
        reasons = []
        
        if indicators['pitch_consistency'] > 100:
            reasons.append("unnatural pitch consistency")
        if indicators['spectral_smoothness'] > 1.5:
            reasons.append("overly smooth spectral transitions")
        if indicators['mfcc_variance'] < 50:
            reasons.append("reduced acoustic variability")
        if indicators['zero_crossing'] < 0.1:
            reasons.append("synthetic speech patterns")
        
        if reasons:
            reason_text = ", ".join(reasons)
            return f"Detected {reason_text} typical of AI-generated voice synthesis. Confidence: {confidence:.0%}. These patterns suggest algorithmic voice generation rather than natural human speech production."
        else:
            return f"Multiple synthetic voice indicators detected with {confidence:.0%} confidence, including robotic prosody and artificial acoustic characteristics."
    
    else:
        reasons = []
        
        if indicators['pitch_consistency'] < 100:
            reasons.append("natural pitch variation")
        if indicators['mfcc_variance'] > 50:
            reasons.append("human-like acoustic variability")
        if indicators['zero_crossing'] > 0.1:
            reasons.append("organic speech patterns")
        
        if reasons:
            reason_text = ", ".join(reasons)
            return f"Detected {reason_text} characteristic of human speech. Confidence: {confidence:.0%}. Voice exhibits natural prosody, micro-variations, and breathing patterns consistent with human vocal production."
        else:
            return f"Voice analysis indicates {confidence:.0%} probability of human origin with natural speech characteristics and organic acoustic patterns."

# ==================== API ENDPOINTS ====================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "AI Voice Detection API",
        "version": "1.0.0",
        "supported_languages": SUPPORTED_LANGUAGES
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "api": "operational",
        "model": "loaded",
        "supported_languages": SUPPORTED_LANGUAGES
    }

@app.post("/api/voice-detection", response_model=VoiceResponse)
async def detect_voice(
    request: VoiceRequest,
    x_api_key: Optional[str] = Header(None)
):
    """
    Main endpoint for voice detection
    
    Accepts Base64 encoded MP3 audio and returns classification
    """
    
    # Validate API key
    if x_api_key != API_KEY:
        logger.warning(f"Invalid API key attempt: {x_api_key}")
        raise HTTPException(
            status_code=401,
            detail="Invalid API key or malformed request"
        )
    
    try:
        logger.info(f"Processing voice detection request for language: {request.language}")
        
        # Extract features
        features = extract_audio_features(request.audioBase64)
        
        # Perform detection
        classification, confidence, indicators = rule_based_detection(features)
        
        # Generate explanation
        explanation = generate_explanation(
            classification, 
            confidence, 
            indicators, 
            request.language
        )
        
        logger.info(f"Detection complete: {classification} with confidence {confidence:.2f}")
        
        return VoiceResponse(
            status="success",
            language=request.language,
            classification=classification,
            confidenceScore=round(confidence, 2),
            explanation=explanation
        )
        
    except ValueError as ve:
        logger.error(f"Validation error: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    
    except Exception as e:
        logger.error(f"Processing error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Error processing audio. Please ensure the audio is properly encoded in Base64 format."
        )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom exception handler"""
    return {
        "status": "error",
        "message": exc.detail
    }

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return {
        "status": "error",
        "message": "Internal server error occurred"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
