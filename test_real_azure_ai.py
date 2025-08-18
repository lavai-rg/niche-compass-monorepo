#!/usr/bin/env python3
"""
🧪 Real Azure AI Services Integration Test
=========================================
Validates connection and functionality of real Azure Cognitive Services
"""

import os
import sys
import json
import requests
from datetime import datetime

# Add backend to path
sys.path.append('/home/user/webapp/backend/src')

def load_env_vars():
    """Load environment variables from .env file"""
    env_path = '/home/user/webapp/.env'
    env_vars = {}
    
    try:
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
                    os.environ[key.strip()] = value.strip()
    except Exception as e:
        print(f"❌ Error loading .env: {e}")
    
    return env_vars

def test_azure_computer_vision():
    """Test Azure Computer Vision API"""
    print("\n🖼️  Testing Azure Computer Vision...")
    print("=" * 60)
    
    key = os.getenv('AZURE_COGNITIVE_SERVICES_KEY')
    endpoint = os.getenv('AZURE_COGNITIVE_SERVICES_ENDPOINT')
    
    if not key or not endpoint:
        print("❌ Azure keys not configured")
        return False
    
    # Test image URL - a jewelry product
    test_image_url = "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=500"
    
    # Computer Vision API endpoint
    analyze_url = endpoint + "vision/v3.2/analyze"
    
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Content-Type': 'application/json'
    }
    
    params = {
        'visualFeatures': 'Categories,Description,Tags,Color,Objects'
    }
    
    data = {
        'url': test_image_url
    }
    
    try:
        print(f"🔗 Testing with image: {test_image_url}")
        print(f"🌐 Endpoint: {endpoint}vision/v3.2/analyze")
        
        response = requests.post(analyze_url, headers=headers, params=params, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ Computer Vision Test SUCCESSFUL!")
            print(f"📝 Description: {result.get('description', {}).get('captions', [{}])[0].get('text', 'N/A')}")
            
            # Show tags
            tags = result.get('tags', [])[:5]
            tag_names = [tag['name'] for tag in tags]
            print(f"🏷️  Top Tags: {', '.join(tag_names)}")
            
            # Show categories
            categories = result.get('categories', [])[:3]
            cat_names = [cat['name'] for cat in categories]
            print(f"📂 Categories: {', '.join(cat_names)}")
            
            # Show dominant colors
            color_info = result.get('color', {})
            dominant_colors = color_info.get('dominantColors', [])
            print(f"🎨 Dominant Colors: {', '.join(dominant_colors[:3])}")
            
            return True
            
        else:
            print(f"❌ HTTP {response.status_code}: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timeout - Azure service might be slow")
        return False
    except Exception as e:
        print(f"❌ Computer Vision Test Failed: {e}")
        return False

def test_azure_text_analytics():
    """Test Azure Text Analytics API"""
    print("\n📝 Testing Azure Text Analytics...")
    print("=" * 60)
    
    key = os.getenv('AZURE_COGNITIVE_SERVICES_KEY')
    endpoint = os.getenv('AZURE_COGNITIVE_SERVICES_ENDPOINT')
    
    if not key or not endpoint:
        print("❌ Azure keys not configured")
        return False
    
    # Text Analytics API endpoint
    sentiment_url = endpoint + "text/analytics/v3.1/sentiment"
    
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Content-Type': 'application/json'
    }
    
    # Test texts for sentiment analysis
    test_texts = [
        "This handmade jewelry is absolutely stunning! The craftsmanship is amazing and it arrived quickly.",
        "The product quality was disappointing. Not worth the price at all.",
        "Average product, nothing special but decent for the price."
    ]
    
    data = {
        'documents': [
            {'id': str(i+1), 'language': 'en', 'text': text}
            for i, text in enumerate(test_texts)
        ]
    }
    
    try:
        print(f"🌐 Endpoint: {endpoint}text/analytics/v3.1/sentiment")
        print(f"📄 Testing {len(test_texts)} text samples...")
        
        response = requests.post(sentiment_url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ Text Analytics Test SUCCESSFUL!")
            
            for i, doc_result in enumerate(result.get('documents', [])):
                sentiment = doc_result.get('sentiment', 'unknown')
                scores = doc_result.get('confidenceScores', {})
                
                print(f"\n📄 Text {i+1}: \"{test_texts[i][:50]}...\"")
                print(f"   😊 Sentiment: {sentiment.upper()}")
                print(f"   📊 Scores: Pos={scores.get('positive', 0):.2f}, "
                      f"Neu={scores.get('neutral', 0):.2f}, "
                      f"Neg={scores.get('negative', 0):.2f}")
            
            return True
            
        else:
            print(f"❌ HTTP {response.status_code}: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timeout - Azure service might be slow")
        return False
    except Exception as e:
        print(f"❌ Text Analytics Test Failed: {e}")
        return False

def test_backend_integration():
    """Test if backend can use real Azure services"""
    print("\n🔧 Testing Backend Integration...")
    print("=" * 60)
    
    try:
        # Import our Azure services
        from services.azure_cognitive_services import analyze_image, analyze_sentiment
        
        print("✅ Successfully imported Azure services from backend")
        
        # Test image analysis through our backend
        test_url = "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=500"
        print(f"🖼️  Testing backend image analysis with: {test_url}")
        
        result = analyze_image(test_url)
        
        if result and 'description' in result:
            print("✅ Backend integration SUCCESSFUL!")
            print(f"📝 Backend Result: {result.get('description', 'N/A')}")
            
            # Check if it's using real Azure (not simulator)
            if 'simulator' in str(result).lower():
                print("⚠️  Still using simulator - real Azure might not be active")
                return False
            else:
                print("🎉 Real Azure AI is ACTIVE in backend!")
                return True
        else:
            print("❌ Backend integration failed")
            return False
            
    except Exception as e:
        print(f"❌ Backend Integration Test Failed: {e}")
        return False

def main():
    """Run all Azure AI tests"""
    print("🧪 REAL AZURE AI SERVICES INTEGRATION TEST")
    print("=" * 70)
    print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load environment variables
    env_vars = load_env_vars()
    
    # Show configuration
    print(f"\n🔑 Configuration:")
    print(f"   Key: {env_vars.get('AZURE_COGNITIVE_SERVICES_KEY', 'NOT SET')[:8]}...")
    print(f"   Endpoint: {env_vars.get('AZURE_COGNITIVE_SERVICES_ENDPOINT', 'NOT SET')}")
    
    # Run tests
    results = []
    
    results.append(("Computer Vision", test_azure_computer_vision()))
    results.append(("Text Analytics", test_azure_text_analytics()))
    results.append(("Backend Integration", test_backend_integration()))
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 70)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if success:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Real Azure AI is fully integrated!")
        print("🚀 Ready for production-level AI accuracy!")
    else:
        print("⚠️  Some tests failed. Check configuration and try again.")
    
    print(f"⏰ Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()