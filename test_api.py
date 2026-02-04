"""
Test script for Voice Detection API
Run this to test your API locally before deployment
"""

import requests
import json
import base64

# Configuration
API_URL = "http://localhost:8000/api/voice-detection"  # Change to your deployed URL
API_KEY = "sk_test_guvi_hackathon_2026"  # Your API key

def encode_audio_file(file_path):
    """Encode audio file to base64"""
    with open(file_path, 'rb') as audio_file:
        audio_bytes = audio_file.read()
        base64_audio = base64.b64encode(audio_bytes).decode('utf-8')
    return base64_audio

def test_api(audio_file_path, language="English"):
    """Test the API with an audio file"""
    
    print(f"\n{'='*60}")
    print(f"Testing API with: {audio_file_path}")
    print(f"Language: {language}")
    print(f"{'='*60}\n")
    
    try:
        # Encode audio
        print("📁 Encoding audio file...")
        audio_base64 = encode_audio_file(audio_file_path)
        print(f"✓ Audio encoded successfully ({len(audio_base64)} characters)")
        
        # Prepare request
        headers = {
            "Content-Type": "application/json",
            "x-api-key": API_KEY
        }
        
        payload = {
            "language": language,
            "audioFormat": "mp3",
            "audioBase64": audio_base64
        }
        
        # Send request
        print("\n🚀 Sending request to API...")
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        
        # Print response
        print(f"\n📊 Response Status: {response.status_code}")
        print(f"{'='*60}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!")
            print(f"\nResults:")
            print(f"  Status: {result['status']}")
            print(f"  Language: {result['language']}")
            print(f"  Classification: {result['classification']}")
            print(f"  Confidence: {result['confidenceScore']}")
            print(f"  Explanation: {result['explanation']}")
        else:
            print(f"❌ ERROR!")
            print(f"Response: {response.text}")
        
        print(f"\n{'='*60}\n")
        
        return response.json()
        
    except FileNotFoundError:
        print(f"❌ Error: Audio file not found at {audio_file_path}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Request Error: {str(e)}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_with_url_audio(audio_url, language="English"):
    """Test API with audio from URL"""
    
    print(f"\n{'='*60}")
    print(f"Testing API with URL: {audio_url}")
    print(f"Language: {language}")
    print(f"{'='*60}\n")
    
    try:
        # Download audio
        print("📥 Downloading audio from URL...")
        response = requests.get(audio_url, timeout=30)
        audio_bytes = response.content
        base64_audio = base64.b64encode(audio_bytes).decode('utf-8')
        print(f"✓ Audio downloaded and encoded ({len(audio_bytes)} bytes)")
        
        # Prepare request
        headers = {
            "Content-Type": "application/json",
            "x-api-key": API_KEY
        }
        
        payload = {
            "language": language,
            "audioFormat": "mp3",
            "audioBase64": base64_audio
        }
        
        # Send request
        print("\n🚀 Sending request to API...")
        api_response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        
        # Print response
        print(f"\n📊 Response Status: {api_response.status_code}")
        print(f"{'='*60}")
        
        if api_response.status_code == 200:
            result = api_response.json()
            print("✅ SUCCESS!")
            print(f"\nResults:")
            print(f"  Status: {result['status']}")
            print(f"  Language: {result['language']}")
            print(f"  Classification: {result['classification']}")
            print(f"  Confidence: {result['confidenceScore']}")
            print(f"  Explanation: {result['explanation']}")
        else:
            print(f"❌ ERROR!")
            print(f"Response: {api_response.text}")
        
        print(f"\n{'='*60}\n")
        
        return api_response.json()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_health_check():
    """Test health check endpoint"""
    print("\n🏥 Testing health check endpoint...")
    try:
        response = requests.get("http://localhost:8000/health", timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("AI VOICE DETECTION API - TEST SUITE")
    print("="*60)
    
    # Test health check
    test_health_check()
    
    # Instructions
    print("\n" + "="*60)
    print("USAGE INSTRUCTIONS:")
    print("="*60)
    print("\n1. Test with local audio file:")
    print('   test_api("path/to/your/audio.mp3", "English")')
    print("\n2. Test with audio URL:")
    print('   test_with_url_audio("https://example.com/audio.mp3", "Tamil")')
    print("\n3. Example:")
    print('   # Uncomment below to test')
    print('   # test_with_url_audio("YOUR_SAMPLE_AUDIO_URL", "Tamil")')
    print("\n" + "="*60 + "\n")
    
    # Example test - uncomment and add your audio file path or URL
    # test_api("sample_audio.mp3", "English")
    # test_with_url_audio("https://your-google-drive-link/sample.mp3", "Tamil")
