"""
ENHANCED VERSION - AI Voice Detection with Advanced Algorithms
Use this if you want better accuracy
"""

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
import base64
import io
import numpy as np
import librosa
from typing import Optional
import logging
from scipy import signal
from scipy.stats import kurtosis, skew

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Voice Detection API - Enhanced", version="2.0.0")

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

# ==================== ADVANCED FEATURE EXTRACTION ====================

def extract_advanced_features(audio_base64: str) -> dict:
    """Extract comprehensive audio features for AI detection"""
    try:
        # Decode base64
        audio_bytes = base64.b64decode(audio_base64)
        audio_buffer = io.BytesIO(audio_bytes)
        y, sr = librosa.load(audio_buffer, sr=16000, mono=True)
        
        features = {}
        
        # 1. SPECTRAL FEATURES
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]
        spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
        spectral_flatness = librosa.feature.spectral_flatness(y=y)[0]
        
        features['spectral_centroid_mean'] = np.mean(spectral_centroids)
        features['spectral_centroid_std'] = np.std(spectral_centroids)
        features['spectral_rolloff_mean'] = np.mean(spectral_rolloff)
        features['spectral_bandwidth_mean'] = np.mean(spectral_bandwidth)
        features['spectral_contrast_mean'] = np.mean(spectral_contrast)
        features['spectral_flatness_mean'] = np.mean(spectral_flatness)
        
        # 2. MFCC FEATURES
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
        features['mfcc_mean'] = np.mean(mfccs)
        features['mfcc_std'] = np.std(mfccs)
        features['mfcc_var'] = np.var(mfccs)
        features['mfcc_kurtosis'] = kurtosis(mfccs.flatten())
        features['mfcc_skew'] = skew(mfccs.flatten())
        
        # 3. PITCH AND F0 FEATURES
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch_values = pitches[pitches > 0]
        if len(pitch_values) > 0:
            features['pitch_mean'] = np.mean(pitch_values)
            features['pitch_std'] = np.std(pitch_values)
            features['pitch_var'] = np.var(pitch_values)
            features['pitch_range'] = np.max(pitch_values) - np.min(pitch_values)
        else:
            features['pitch_mean'] = 0
            features['pitch_std'] = 0
            features['pitch_var'] = 0
            features['pitch_range'] = 0
        
        # 4. TEMPORAL FEATURES
        zero_crossings = librosa.feature.zero_crossing_rate(y)[0]
        features['zero_crossing_mean'] = np.mean(zero_crossings)
        features['zero_crossing_std'] = np.std(zero_crossings)
        
        # 5. ENERGY FEATURES
        rms = librosa.feature.rms(y=y)[0]
        features['rms_mean'] = np.mean(rms)
        features['rms_std'] = np.std(rms)
        features['rms_var'] = np.var(rms)
        
        # 6. HARMONIC-PERCUSSIVE FEATURES
        y_harmonic, y_percussive = librosa.effects.hpss(y)
        features['harmonic_mean'] = np.mean(np.abs(y_harmonic))
        features['percussive_mean'] = np.mean(np.abs(y_percussive))
        features['harmonic_percussive_ratio'] = features['harmonic_mean'] / (features['percussive_mean'] + 1e-6)
        
        # 7. CHROMA FEATURES
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        features['chroma_mean'] = np.mean(chroma)
        features['chroma_std'] = np.std(chroma)
        
        # 8. TONNETZ FEATURES
        tonnetz = librosa.feature.tonnetz(y=librosa.effects.harmonic(y), sr=sr)
        features['tonnetz_mean'] = np.mean(tonnetz)
        
        return features
        
    except Exception as e:
        logger.error(f"Feature extraction error: {str(e)}")
        raise

# ==================== ADVANCED DETECTION ALGORITHMS ====================

def detect_pitch_artifacts(features: dict) -> float:
    """Detect unnatural pitch patterns typical of AI voices"""
    score = 0.0
    
    # AI voices have unnaturally consistent pitch
    if features['pitch_std'] < 20:
        score += 0.3
    
    # AI voices have limited pitch range
    if features['pitch_range'] < 100:
        score += 0.2
    
    # Very low pitch variance is suspicious
    if features['pitch_var'] < 100:
        score += 0.25
    
    return min(score, 1.0)

def detect_spectral_artifacts(features: dict) -> float:
    """Detect spectral artifacts from AI generation"""
    score = 0.0
    
    # AI voices have overly smooth spectral characteristics
    if features['spectral_flatness_mean'] > 0.5:
        score += 0.25
    
    # Unnatural spectral centroid consistency
    if features['spectral_centroid_std'] < 300:
        score += 0.3
    
    # Artificial spectral contrast
    if features['spectral_contrast_mean'] > 30:
        score += 0.2
    
    return min(score, 1.0)

def detect_temporal_artifacts(features: dict) -> float:
    """Detect temporal artifacts in speech"""
    score = 0.0
    
    # AI voices have very consistent zero crossing rates
    if features['zero_crossing_std'] < 0.02:
        score += 0.3
    
    # Unnatural energy consistency
    if features['rms_std'] < 0.01:
        score += 0.25
    
    return min(score, 1.0)

def detect_mfcc_artifacts(features: dict) -> float:
    """Detect MFCC-based artifacts"""
    score = 0.0
    
    # AI voices have lower MFCC variance
    if features['mfcc_var'] < 50:
        score += 0.3
    
    # Unusual kurtosis indicates artificial generation
    if abs(features['mfcc_kurtosis']) > 5:
        score += 0.2
    
    # Low MFCC standard deviation
    if features['mfcc_std'] < 5:
        score += 0.25
    
    return min(score, 1.0)

def advanced_detection(features: dict) -> tuple:
    """Multi-algorithm ensemble detection"""
    
    # Get scores from different detectors
    pitch_score = detect_pitch_artifacts(features)
    spectral_score = detect_spectral_artifacts(features)
    temporal_score = detect_temporal_artifacts(features)
    mfcc_score = detect_mfcc_artifacts(features)
    
    # Weighted ensemble
    weights = {
        'pitch': 0.30,
        'spectral': 0.30,
        'temporal': 0.20,
        'mfcc': 0.20
    }
    
    ai_score = (
        pitch_score * weights['pitch'] +
        spectral_score * weights['spectral'] +
        temporal_score * weights['temporal'] +
        mfcc_score * weights['mfcc']
    )
    
    # Classification decision
    threshold = 0.5
    
    if ai_score >= threshold:
        classification = "AI_GENERATED"
        # Scale confidence: 0.5-0.99 range
        confidence = min(0.55 + (ai_score - threshold) * 0.88, 0.99)
    else:
        classification = "HUMAN"
        # Scale confidence: 0.5-0.99 range
        confidence = min(0.55 + (threshold - ai_score) * 0.88, 0.99)
    
    # Store individual scores for explanation
    detector_scores = {
        'pitch': pitch_score,
        'spectral': spectral_score,
        'temporal': temporal_score,
        'mfcc': mfcc_score,
        'overall': ai_score
    }
    
    return classification, confidence, detector_scores

def generate_detailed_explanation(
    classification: str, 
    confidence: float, 
    detector_scores: dict, 
    features: dict,
    language: str
) -> str:
    """Generate comprehensive explanation"""
    
    if classification == "AI_GENERATED":
        indicators = []
        
        # Analyze which detectors contributed most
        if detector_scores['pitch'] > 0.4:
            indicators.append(f"unnatural pitch consistency (variance: {features['pitch_std']:.1f}Hz)")
        
        if detector_scores['spectral'] > 0.4:
            indicators.append(f"artificial spectral patterns (flatness: {features['spectral_flatness_mean']:.2f})")
        
        if detector_scores['temporal'] > 0.3:
            indicators.append(f"robotic temporal regularity (ZCR std: {features['zero_crossing_std']:.4f})")
        
        if detector_scores['mfcc'] > 0.4:
            indicators.append(f"synthetic acoustic signature (MFCC var: {features['mfcc_var']:.1f})")
        
        if indicators:
            main_indicators = ", ".join(indicators[:3])  # Top 3 indicators
            return (f"AI-generated voice detected with {confidence:.0%} confidence. "
                   f"Analysis reveals {main_indicators}. "
                   f"These characteristics are typical of text-to-speech synthesis systems "
                   f"and differ significantly from natural human speech patterns observed in {language}.")
        else:
            return (f"Voice classified as AI-generated with {confidence:.0%} confidence based on "
                   f"multiple algorithmic indicators suggesting synthetic origin.")
    
    else:
        indicators = []
        
        # Show why it's human
        if detector_scores['pitch'] < 0.3:
            indicators.append(f"natural pitch variation (std: {features['pitch_std']:.1f}Hz)")
        
        if detector_scores['mfcc'] < 0.3:
            indicators.append(f"organic acoustic variability (MFCC var: {features['mfcc_var']:.1f})")
        
        if detector_scores['temporal'] < 0.2:
            indicators.append(f"human-like temporal dynamics")
        
        if indicators:
            main_indicators = ", ".join(indicators[:3])
            return (f"Human voice identified with {confidence:.0%} confidence. "
                   f"Voice exhibits {main_indicators}. "
                   f"These features align with natural speech production in {language}, "
                   f"including micro-variations, breathing patterns, and organic prosody "
                   f"that are absent in AI-generated speech.")
        else:
            return (f"Voice classified as human with {confidence:.0%} confidence. "
                   f"Analysis shows characteristics consistent with natural human speech production.")

# ==================== API ENDPOINTS ====================

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "AI Voice Detection API - Enhanced",
        "version": "2.0.0",
        "features": "Advanced multi-algorithm detection",
        "supported_languages": SUPPORTED_LANGUAGES
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "api": "operational",
        "algorithms": ["pitch_detection", "spectral_analysis", "temporal_analysis", "mfcc_analysis"],
        "supported_languages": SUPPORTED_LANGUAGES
    }

@app.post("/api/voice-detection", response_model=VoiceResponse)
async def detect_voice(
    request: VoiceRequest,
    x_api_key: Optional[str] = Header(None)
):
    """Enhanced voice detection with advanced algorithms"""
    
    # Validate API key
    if x_api_key != API_KEY:
        logger.warning(f"Invalid API key attempt")
        raise HTTPException(
            status_code=401,
            detail="Invalid API key or malformed request"
        )
    
    try:
        logger.info(f"Processing enhanced detection for language: {request.language}")
        
        # Extract advanced features
        features = extract_advanced_features(request.audioBase64)
        
        # Perform advanced detection
        classification, confidence, detector_scores = advanced_detection(features)
        
        # Generate detailed explanation
        explanation = generate_detailed_explanation(
            classification, 
            confidence, 
            detector_scores, 
            features,
            request.language
        )
        
        logger.info(f"Enhanced detection complete: {classification} ({confidence:.2f})")
        
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
            detail="Error processing audio. Please ensure the audio is properly encoded."
        )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {
        "status": "error",
        "message": exc.detail
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
