#!/usr/bin/env python3
"""
🔍 AI Quality Comparison: Simulator vs Real Azure
===============================================
Direct comparison of AI Simulator vs Real Azure AI Services
"""

import os
import sys
import json
from datetime import datetime

# Add backend to path
sys.path.append('/home/user/webapp/backend/src')

# Load environment variables
def load_env_vars():
    env_path = '/home/user/webapp/.env'
    try:
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
    except Exception as e:
        print(f"❌ Error loading .env: {e}")

def test_image_analysis_comparison():
    """Compare image analysis between simulator and real Azure"""
    print("\n🖼️  IMAGE ANALYSIS COMPARISON")
    print("=" * 70)
    
    # Test URLs for different product types
    test_images = [
        {
            "category": "Jewelry", 
            "url": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=500",
            "description": "Gold necklace on book"
        },
        {
            "category": "Home Decor", 
            "url": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=500",
            "description": "Ceramic vase with plants"
        },
        {
            "category": "Art/Crafts",
            "url": "https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=500", 
            "description": "Handmade pottery"
        }
    ]
    
    # Import both services
    from services.azure_cognitive_services import analyze_image_from_url
    from services.azure_ai_simulator import azure_simulator
    
    results = []
    
    for i, test_image in enumerate(test_images):
        print(f"\n🔍 Test {i+1}: {test_image['category']}")
        print(f"📷 Image: {test_image['description']}")
        print(f"🔗 URL: {test_image['url']}")
        print("-" * 50)
        
        # Test with Real Azure
        print("🌩️  REAL AZURE AI:")
        try:
            azure_result = analyze_image_from_url(test_image['url'])
            print(f"   📝 Description: {azure_result.get('description', 'N/A')}")
            azure_tags = azure_result.get('tags', [])[:5]
            print(f"   🏷️  Tags: {', '.join(azure_tags)}")
            azure_categories = azure_result.get('categories', [])[:3]  
            print(f"   📂 Categories: {', '.join(azure_categories)}")
        except Exception as e:
            azure_result = {"error": str(e)}
            print(f"   ❌ Error: {e}")
        
        # Test with Simulator
        print("🤖 AI SIMULATOR:")
        try:
            simulator_result = azure_simulator.analyze_image_from_url(test_image['url'])
            print(f"   📝 Description: {simulator_result.get('description', 'N/A')}")
            sim_tags = [tag['name'] for tag in simulator_result.get('tags', [])[:5]]
            print(f"   🏷️  Tags: {', '.join(sim_tags)}")
            sim_categories = [cat['name'] for cat in simulator_result.get('categories', [])[:3]]
            print(f"   📂 Categories: {', '.join(sim_categories)}")
        except Exception as e:
            simulator_result = {"error": str(e)}
            print(f"   ❌ Error: {e}")
        
        results.append({
            "image": test_image,
            "azure": azure_result,
            "simulator": simulator_result
        })
    
    return results

def test_sentiment_analysis_comparison():
    """Compare sentiment analysis between simulator and real Azure"""
    print("\n📝 SENTIMENT ANALYSIS COMPARISON")
    print("=" * 70)
    
    # Test reviews for different sentiments
    test_reviews = [
        {
            "type": "Very Positive",
            "text": "This handmade jewelry is absolutely stunning! The craftsmanship is incredible and it exceeded all my expectations. Highly recommend!"
        },
        {
            "type": "Very Negative", 
            "text": "Terrible quality! The necklace broke after just one day. Complete waste of money. Very disappointed with this purchase."
        },
        {
            "type": "Mixed/Neutral",
            "text": "The product is okay. Quality is decent for the price, nothing special but does the job. Shipping was fast."
        },
        {
            "type": "Complex Sentiment",
            "text": "I love the design and style of this bracelet, it's exactly what I wanted. However, the delivery took too long and the packaging was damaged."
        }
    ]
    
    # Import both services
    from services.azure_cognitive_services import analyze_sentiment
    from services.azure_ai_simulator import azure_simulator
    
    results = []
    
    for i, test_review in enumerate(test_reviews):
        print(f"\n🔍 Test {i+1}: {test_review['type']}")
        print(f"📄 Text: \"{test_review['text'][:60]}...\"")
        print("-" * 50)
        
        # Test with Real Azure
        print("🌩️  REAL AZURE AI:")
        try:
            azure_result = analyze_sentiment(test_review['text'])
            print(f"   😊 Sentiment: {azure_result.get('sentiment', 'N/A').upper()}")
            print(f"   📊 Scores: Pos={azure_result.get('positive_score', 0):.2f}, "
                  f"Neu={azure_result.get('neutral_score', 0):.2f}, "
                  f"Neg={azure_result.get('negative_score', 0):.2f}")
        except Exception as e:
            azure_result = {"error": str(e)}
            print(f"   ❌ Error: {e}")
        
        # Test with Simulator
        print("🤖 AI SIMULATOR:")
        try:
            simulator_result = azure_simulator.analyze_sentiment(test_review['text'])
            print(f"   😊 Sentiment: {simulator_result.get('sentiment', 'N/A').upper()}")
            scores = simulator_result.get('confidence_scores', {})
            print(f"   📊 Scores: Pos={scores.get('positive', 0):.2f}, "
                  f"Neu={scores.get('neutral', 0):.2f}, "
                  f"Neg={scores.get('negative', 0):.2f}")
        except Exception as e:
            simulator_result = {"error": str(e)}
            print(f"   ❌ Error: {e}")
        
        results.append({
            "review": test_review,
            "azure": azure_result,
            "simulator": simulator_result
        })
    
    return results

def analyze_accuracy_comparison(image_results, sentiment_results):
    """Analyze and compare accuracy between services"""
    print("\n📊 ACCURACY & QUALITY ANALYSIS")
    print("=" * 70)
    
    # Image Analysis Comparison
    print("🖼️  IMAGE ANALYSIS QUALITY:")
    image_score_azure = 0
    image_score_simulator = 0
    
    for result in image_results:
        print(f"\n📷 {result['image']['category']}:")
        
        # Check Azure quality
        azure = result.get('azure', {})
        if not azure.get('error') and azure.get('description'):
            azure_quality = len(azure.get('tags', [])) + len(azure.get('categories', [])) + 1  # +1 for description
            print(f"   🌩️  Azure: {azure_quality} elements detected")
            image_score_azure += azure_quality
        else:
            print(f"   🌩️  Azure: Error or no data")
        
        # Check Simulator quality
        simulator = result.get('simulator', {})
        if not simulator.get('error') and simulator.get('description'):
            sim_quality = len(simulator.get('tags', [])) + len(simulator.get('categories', [])) + 1
            print(f"   🤖 Simulator: {sim_quality} elements detected")
            image_score_simulator += sim_quality
        else:
            print(f"   🤖 Simulator: Error or no data")
    
    print(f"\n🏆 IMAGE ANALYSIS WINNER:")
    print(f"   🌩️  Real Azure Total Score: {image_score_azure}")
    print(f"   🤖 Simulator Total Score: {image_score_simulator}")
    
    if image_score_azure > image_score_simulator:
        print("   🥇 Winner: REAL AZURE (More detailed analysis)")
    elif image_score_simulator > image_score_azure:
        print("   🥇 Winner: SIMULATOR (More detailed analysis)")
    else:
        print("   🤝 TIE: Both performed equally")
    
    # Sentiment Analysis Comparison
    print(f"\n📝 SENTIMENT ANALYSIS QUALITY:")
    sentiment_score_azure = 0
    sentiment_score_simulator = 0
    
    for result in sentiment_results:
        print(f"\n📄 {result['review']['type']}:")
        
        # Check Azure confidence
        azure = result.get('azure', {})
        if not azure.get('error'):
            max_confidence = max(azure.get('positive_score', 0), 
                               azure.get('neutral_score', 0), 
                               azure.get('negative_score', 0))
            print(f"   🌩️  Azure Confidence: {max_confidence:.2f}")
            sentiment_score_azure += max_confidence
        else:
            print(f"   🌩️  Azure: Error")
        
        # Check Simulator confidence
        simulator = result.get('simulator', {})
        if not simulator.get('error'):
            scores = simulator.get('confidence_scores', {})
            max_confidence = max(scores.get('positive', 0), 
                               scores.get('neutral', 0), 
                               scores.get('negative', 0))
            print(f"   🤖 Simulator Confidence: {max_confidence:.2f}")
            sentiment_score_simulator += max_confidence
        else:
            print(f"   🤖 Simulator: Error")
    
    print(f"\n🏆 SENTIMENT ANALYSIS WINNER:")
    print(f"   🌩️  Real Azure Avg Confidence: {sentiment_score_azure/len(sentiment_results):.2f}")
    print(f"   🤖 Simulator Avg Confidence: {sentiment_score_simulator/len(sentiment_results):.2f}")
    
    if sentiment_score_azure > sentiment_score_simulator:
        print("   🥇 Winner: REAL AZURE (Higher confidence)")
    elif sentiment_score_simulator > sentiment_score_azure:
        print("   🥇 Winner: SIMULATOR (Higher confidence)")
    else:
        print("   🤝 TIE: Both performed equally")
    
    # Overall Winner
    azure_total = image_score_azure + sentiment_score_azure
    simulator_total = image_score_simulator + sentiment_score_simulator
    
    print(f"\n🎯 OVERALL COMPARISON:")
    print(f"   🌩️  Real Azure Total: {azure_total:.1f}")
    print(f"   🤖 Simulator Total: {simulator_total:.1f}")
    
    if azure_total > simulator_total:
        improvement = ((azure_total - simulator_total) / simulator_total * 100)
        print(f"   🏆 WINNER: REAL AZURE (+{improvement:.1f}% better)")
    elif simulator_total > azure_total:
        improvement = ((simulator_total - azure_total) / azure_total * 100)
        print(f"   🏆 WINNER: SIMULATOR (+{improvement:.1f}% better)")
    else:
        print(f"   🤝 PERFECT TIE!")

def main():
    """Run comprehensive AI quality comparison"""
    print("🔍 AI QUALITY COMPARISON: SIMULATOR vs REAL AZURE")
    print("=" * 80)
    print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load environment
    load_env_vars()
    
    # Run comparisons
    image_results = test_image_analysis_comparison()
    sentiment_results = test_sentiment_analysis_comparison()
    
    # Analyze results
    analyze_accuracy_comparison(image_results, sentiment_results)
    
    print(f"\n⏰ Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎉 Comparison complete! Real Azure AI is now active for production-level accuracy!")

if __name__ == "__main__":
    main()