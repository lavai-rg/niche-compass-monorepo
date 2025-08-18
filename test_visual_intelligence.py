#!/usr/bin/env python3
"""
🎨 Visual Intelligence Engine Test Suite
======================================
Test the revolutionary visual market analysis capabilities
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
    try:
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
    except Exception as e:
        print(f"❌ Error loading .env: {e}")

def test_visual_intelligence_direct():
    """Test Visual Intelligence Engine directly"""
    print("\n🎨 TESTING VISUAL INTELLIGENCE ENGINE DIRECTLY")
    print("=" * 70)
    
    try:
        from services.visual_intelligence import VisualIntelligenceEngine
        
        # Initialize engine
        vi_engine = VisualIntelligenceEngine()
        print("✅ Visual Intelligence Engine initialized successfully")
        
        # Test cases with different product types
        test_cases = [
            {
                "name": "Jewelry Product",
                "analysis": {
                    "description": "a gold chain necklace on a book",
                    "tags": ["jewelry", "necklace", "gold", "chain", "fashion", "accessory", "bling-bling"],
                    "categories": ["accessories", "jewelry"],
                    "color": {"dominantColors": ["gold", "white", "black"]}
                }
            },
            {
                "name": "Minimalist Home Decor",
                "analysis": {
                    "description": "white ceramic vase with clean lines on minimalist table",
                    "tags": ["vase", "ceramic", "white", "minimalist", "home", "decor", "clean", "modern"],
                    "categories": ["home_decor", "minimalist"],
                    "color": {"dominantColors": ["white", "gray", "sage_green"]}
                }
            },
            {
                "name": "Bohemian Art Piece",
                "analysis": {
                    "description": "colorful woven tapestry with intricate patterns and earth tones",
                    "tags": ["tapestry", "woven", "colorful", "patterns", "bohemian", "art", "wall", "decor", "handmade"],
                    "categories": ["art", "textiles", "bohemian"],
                    "color": {"dominantColors": ["terracotta", "sage_green", "dusty_pink"]}
                }
            }
        ]
        
        for i, test_case in enumerate(test_cases):
            print(f"\n🔍 Test Case {i+1}: {test_case['name']}")
            print("-" * 50)
            
            # Run visual intelligence analysis
            result = vi_engine.analyze_visual_intelligence(test_case['analysis'])
            
            if result.get('error'):
                print(f"❌ Analysis failed: {result['error']}")
                continue
            
            # Display key results
            print(f"📊 Visual Intelligence Score: {result['visual_intelligence_score']:.3f}")
            print(f"🎯 Market Potential: {result['market_insights']['overall_market_potential']}")
            print(f"📈 Performance Boost: {result['market_insights']['estimated_performance_boost']}")
            
            # Color Psychology Results
            color_analysis = result.get('color_psychology', {})
            if color_analysis:
                print(f"🎨 Color Market Score: {color_analysis.get('market_performance_score', 0):.1f}/10")
                if color_analysis.get('pricing_impact', 1.0) > 1.1:
                    premium = (color_analysis['pricing_impact'] - 1) * 100
                    print(f"💰 Color Premium Potential: +{premium:.0f}%")
            
            # Style Classification Results
            style_analysis = result.get('style_classification', {})
            if style_analysis.get('dominant_style') != 'undefined':
                print(f"🎭 Dominant Style: {style_analysis['dominant_style']} ({style_analysis['confidence']:.1%} confidence)")
            
            # Quality Assessment
            quality_analysis = result.get('image_quality', {})
            if quality_analysis:
                print(f"📸 Image Quality: {quality_analysis['overall_score']:.1%} ({quality_analysis['market_readiness']} readiness)")
            
            # Show top recommendations
            recommendations = result.get('optimization_recommendations', [])[:3]
            if recommendations:
                print("💡 Top Recommendations:")
                for rec in recommendations:
                    print(f"   • {rec}")
            
            # Show competitive advantages
            advantages = result.get('competitive_advantages', [])
            if advantages:
                print("🏆 Competitive Advantages:")
                for adv in advantages:
                    print(f"   • {adv}")
        
        return True
        
    except Exception as e:
        print(f"❌ Direct test failed: {e}")
        return False

def test_visual_intelligence_api():
    """Test Visual Intelligence through API endpoint"""
    print("\n🌐 TESTING VISUAL INTELLIGENCE VIA API")
    print("=" * 70)
    
    # Test different product URLs
    test_urls = [
        {
            "name": "Jewelry Image",
            "url": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=500"
        },
        {
            "name": "Home Decor Image", 
            "url": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=500"
        },
        {
            "name": "Art/Craft Image",
            "url": "https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=500"
        }
    ]
    
    api_base_url = "https://5000-i20omqxrp5gsgyv7zvab9-6532622b.e2b.dev"
    
    for i, test_case in enumerate(test_urls):
        print(f"\n🔍 API Test {i+1}: {test_case['name']}")
        print(f"🔗 URL: {test_case['url']}")
        print("-" * 50)
        
        try:
            # Make API request
            response = requests.post(
                f"{api_base_url}/api/analyze",
                json={"url": test_case['url']},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                product_analysis = result.get('product_analysis', {})
                
                # Check if visual intelligence is present
                visual_intelligence = product_analysis.get('visual_intelligence', [])
                
                if visual_intelligence:
                    print("✅ Visual Intelligence data found in API response")
                    
                    # Show visual intelligence results for first image
                    vi_result = visual_intelligence[0]
                    
                    if not vi_result.get('error'):
                        print(f"📊 VI Score: {vi_result.get('visual_intelligence_score', 'N/A'):.3f}")
                        print(f"🎯 Market Potential: {vi_result.get('market_insights', {}).get('overall_market_potential', 'N/A')}")
                        
                        # Show key insights
                        market_insights = vi_result.get('market_insights', {})
                        key_strengths = market_insights.get('key_strengths', [])
                        if key_strengths:
                            print("💪 Key Strengths:")
                            for strength in key_strengths[:2]:
                                print(f"   • {strength}")
                        
                        # Show competitive advantages
                        comp_advantages = vi_result.get('competitive_advantages', [])
                        if comp_advantages:
                            print("🏆 Competitive Edges:")
                            for advantage in comp_advantages[:2]:
                                print(f"   • {advantage}")
                        
                        print("✅ API integration successful!")
                    else:
                        print(f"❌ Visual Intelligence error: {vi_result['error']}")
                else:
                    print("⚠️ No visual intelligence data in API response")
                    
                # Also check basic image analysis
                image_analysis = product_analysis.get('image_analysis', [])
                if image_analysis and image_analysis[0].get('description'):
                    print(f"🖼️ Basic Analysis: {image_analysis[0]['description']}")
                
            else:
                print(f"❌ API request failed: {response.status_code}")
                print(f"Response: {response.text[:200]}...")
                
        except requests.exceptions.Timeout:
            print("❌ API request timeout")
        except Exception as e:
            print(f"❌ API test failed: {e}")

def test_color_psychology():
    """Test color psychology analysis specifically"""
    print("\n🎨 TESTING COLOR PSYCHOLOGY ANALYZER")
    print("=" * 70)
    
    try:
        from services.visual_intelligence import ColorPsychologyAnalyzer
        
        color_analyzer = ColorPsychologyAnalyzer()
        
        # Test different color combinations
        color_tests = [
            {
                "name": "Trending Earth Tones",
                "colors": ["sage_green", "terracotta", "dusty_pink"]
            },
            {
                "name": "Premium Black & Gold",
                "colors": ["black", "gold", "white"]
            },
            {
                "name": "Fresh Spring Colors",
                "colors": ["green", "yellow", "white"]
            },
            {
                "name": "Luxury Purple Palette",
                "colors": ["purple", "white", "gray"]
            }
        ]
        
        for test in color_tests:
            print(f"\n🎨 Testing: {test['name']}")
            print(f"Colors: {', '.join(test['colors'])}")
            print("-" * 40)
            
            analysis = color_analyzer.analyze_color_palette(test['colors'])
            
            print(f"📊 Market Performance: {analysis.get('market_performance_score', 0):.1f}/10")
            print(f"💰 Pricing Impact: +{((analysis.get('pricing_impact', 1.0) - 1) * 100):.0f}%")
            print(f"📈 Trend Status: {analysis.get('trend_alignment', 'neutral')}")
            
            # Top emotions
            emotions = analysis.get('color_emotions', [])[:3]
            if emotions:
                print(f"😊 Top Emotions: {', '.join(emotions)}")
            
            # Demographics
            demographics = analysis.get('target_demographics', {})
            if demographics:
                top_demo = max(demographics.keys(), key=demographics.get)
                print(f"👥 Primary Demo: {top_demo}")
            
            # Recommendations
            recommendations = analysis.get('recommendations', [])[:2]
            if recommendations:
                print("💡 Recommendations:")
                for rec in recommendations:
                    print(f"   • {rec}")
        
        return True
        
    except Exception as e:
        print(f"❌ Color psychology test failed: {e}")
        return False

def main():
    """Run comprehensive Visual Intelligence tests"""
    print("🎨 VISUAL INTELLIGENCE ENGINE - COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load environment
    load_env_vars()
    
    # Run all tests
    test_results = []
    
    print("\n" + "="*80)
    test_results.append(("Direct Engine Test", test_visual_intelligence_direct()))
    
    print("\n" + "="*80) 
    test_results.append(("API Integration Test", test_visual_intelligence_api()))
    
    print("\n" + "="*80)
    test_results.append(("Color Psychology Test", test_color_psychology()))
    
    # Summary
    print("\n" + "="*80)
    print("📊 TEST RESULTS SUMMARY")
    print("="*80)
    
    passed = 0
    total = len(test_results)
    
    for test_name, success in test_results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if success:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Visual Intelligence Engine is fully operational!")
        print("🚀 Revolutionary visual market analysis capabilities are live!")
    else:
        print("⚠️ Some tests failed. Check implementation and try again.")
    
    print(f"⏰ Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()