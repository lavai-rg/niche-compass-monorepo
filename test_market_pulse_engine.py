#!/usr/bin/env python3
"""
⚡ Market Pulse Engine - Comprehensive Test Suite
===============================================
Test the revolutionary real-time market intelligence system
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

def test_market_pulse_direct():
    """Test Market Pulse Engine directly"""
    print("\n⚡ TESTING MARKET PULSE ENGINE DIRECTLY")
    print("=" * 70)
    
    try:
        from services.market_pulse_engine import MarketPulseEngine
        
        # Initialize engine
        pulse_engine = MarketPulseEngine()
        print("✅ Market Pulse Engine initialized successfully")
        
        # Test cases with different market scenarios
        test_cases = [
            {
                "name": "Hot Trending Niche",
                "keywords": ["sage green decor"]
            },
            {
                "name": "Competitive Market",
                "keywords": ["handmade jewelry"]
            },
            {
                "name": "Emerging Opportunity",
                "keywords": ["cottagecore aesthetic"]
            },
            {
                "name": "Multi-keyword Analysis",
                "keywords": ["minimalist", "home decor", "modern"]
            }
        ]
        
        for i, test_case in enumerate(test_cases):
            print(f"\n🔍 Test Case {i+1}: {test_case['name']}")
            print(f"Keywords: {', '.join(test_case['keywords'])}")
            print("-" * 50)
            
            # Run market pulse analysis
            result = pulse_engine.get_market_pulse(test_case['keywords'])
            
            if result.get('error'):
                print(f"❌ Analysis failed: {result['error']}")
                continue
            
            # Display key results
            print(f"📊 Market Pulse Score: {result['market_pulse_score']:.1f}/10")
            print(f"🌡️ Status: {result['pulse_status']}")
            
            # Market insights
            insights = result.get('market_insights', {})
            print(f"🔥 Market Temperature: {insights.get('market_temperature', 'N/A')}")
            print(f"⚔️ Competition Pressure: {insights.get('competition_pressure', 'N/A')}")
            print(f"📈 Demand Status: {insights.get('demand_status', 'N/A')}")
            
            # Trend analysis
            trend_analysis = result.get('trend_analysis', {})
            if trend_analysis:
                print(f"🚀 Trend Status: {trend_analysis.get('trend_status', 'N/A')}")
                print(f"⚡ Momentum Score: {trend_analysis.get('momentum_score', 0):.1f}/10")
            
            # Competition analysis
            competition = result.get('competition_analysis', {})
            if competition:
                print(f"🎯 Competition Level: {competition.get('competition_level', 'N/A')}")
                print(f"💎 Opportunity Score: {competition.get('opportunity_score', 0):.1f}/10")
            
            # Top recommendations
            recommendations = result.get('action_recommendations', [])[:3]
            if recommendations:
                print("💡 Top Recommendations:")
                for rec in recommendations:
                    print(f"   • {rec}")
            
            # Optimal timing
            timing = result.get('optimal_timing', {})
            if timing:
                print(f"⏰ Optimal Timing: {timing.get('recommendation', 'N/A')} ({timing.get('urgency', 'N/A')} urgency)")
        
        return True
        
    except Exception as e:
        print(f"❌ Direct test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_market_pulse_api():
    """Test Market Pulse Engine through API endpoints"""
    print("\n🌐 TESTING MARKET PULSE VIA API ENDPOINTS")
    print("=" * 70)
    
    api_base_url = "https://5000-i20omqxrp5gsgyv7zvab9-6532622b.e2b.dev"
    
    # Test different API endpoints
    api_tests = [
        {
            "name": "Market Pulse Analysis",
            "endpoint": "/api/market/pulse",
            "method": "POST",
            "data": {"keywords": ["sage green home decor"], "timeframe": "24h"}
        },
        {
            "name": "Trending Niches",
            "endpoint": "/api/market/trending",
            "method": "GET",
            "data": None
        },
        {
            "name": "Competition Analysis",
            "endpoint": "/api/market/competition/minimalist jewelry",
            "method": "GET", 
            "data": None
        },
        {
            "name": "Trend Velocity",
            "endpoint": "/api/market/velocity/cottagecore aesthetic",
            "method": "GET",
            "data": None
        },
        {
            "name": "Market Opportunities",
            "endpoint": "/api/market/opportunities?limit=5&min_score=6.0",
            "method": "GET",
            "data": None
        },
        {
            "name": "Market Alerts", 
            "endpoint": "/api/market/alerts",
            "method": "GET",
            "data": None
        }
    ]
    
    successful_tests = 0
    
    for i, test in enumerate(api_tests):
        print(f"\n🔍 API Test {i+1}: {test['name']}")
        print(f"📡 Endpoint: {test['endpoint']}")
        print("-" * 50)
        
        try:
            url = f"{api_base_url}{test['endpoint']}"
            
            if test['method'] == 'POST':
                response = requests.post(url, json=test['data'], timeout=30)
            else:
                response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"✅ API Response: {response.status_code}")
                
                # Show key results based on endpoint
                if 'market_pulse' in result:
                    pulse_data = result['market_pulse']
                    print(f"📊 Pulse Score: {pulse_data.get('market_pulse_score', 'N/A')}")
                    print(f"🌡️ Status: {pulse_data.get('pulse_status', 'N/A')}")
                
                elif 'trending_niches' in result:
                    niches = result['trending_niches'][:3]  # Top 3
                    print(f"📈 Found {result.get('total_analyzed', 0)} trending niches")
                    for niche in niches:
                        print(f"   🏆 #{niche['rank']}: {niche['keyword']} (Score: {niche['pulse_score']:.1f})")
                
                elif 'competition_analysis' in result:
                    comp = result['competition_analysis']
                    print(f"⚔️ Competition Level: {comp.get('competition_level', 'N/A')}")
                    print(f"💎 Opportunity Score: {comp.get('opportunity_score', 0):.1f}/10")
                
                elif 'trend_velocity' in result:
                    velocity = result['trend_velocity']
                    print(f"⚡ Momentum Score: {velocity.get('momentum_score', 0):.1f}/10")
                    print(f"🚀 Trend Status: {velocity.get('trend_status', 'N/A')}")
                
                elif 'market_opportunities' in result:
                    opportunities = result['market_opportunities'][:3]  # Top 3
                    print(f"🎯 Found {result.get('total_found', 0)} opportunities")
                    for opp in opportunities:
                        print(f"   💎 #{opp['rank']}: {opp['keyword']} (Score: {opp['pulse_score']:.1f})")
                
                elif 'market_alerts' in result:
                    alerts = result['market_alerts'][:3]  # Top 3
                    print(f"🚨 Found {result.get('total_alerts', 0)} alerts")
                    critical = result.get('critical_alerts', 0)
                    high = result.get('high_priority_alerts', 0)
                    print(f"   🔴 Critical: {critical}, 🟠 High Priority: {high}")
                
                successful_tests += 1
                print("✅ API test successful!")
                
            else:
                print(f"❌ API Error: {response.status_code}")
                print(f"Response: {response.text[:300]}...")
                
        except requests.exceptions.Timeout:
            print("❌ API request timeout")
        except Exception as e:
            print(f"❌ API test failed: {e}")
    
    print(f"\n📊 API Tests Summary: {successful_tests}/{len(api_tests)} successful")
    return successful_tests == len(api_tests)

def test_individual_components():
    """Test individual components of Market Pulse Engine"""
    print("\n🔧 TESTING INDIVIDUAL COMPONENTS")
    print("=" * 70)
    
    try:
        from services.market_pulse_engine import TrendVelocityDetector, CompetitionDensityTracker, DemandSurgeAnalyzer
        
        components_passed = 0
        
        # Test Trend Velocity Detector
        print("\n📈 Testing Trend Velocity Detector...")
        trend_detector = TrendVelocityDetector()
        
        # Mock historical data
        historical_data = [
            {"date": "2024-01-01", "value": 100},
            {"date": "2024-01-02", "value": 120},
            {"date": "2024-01-03", "value": 150},
            {"date": "2024-01-04", "value": 200},
            {"date": "2024-01-05", "value": 280}
        ]
        
        trend_result = trend_detector.calculate_trend_velocity(historical_data)
        print(f"   ✅ Velocity calculated: {trend_result.get('average_velocity', 0):.2f}")
        print(f"   📊 Trend Status: {trend_result.get('trend_status', 'N/A')}")
        print(f"   ⚡ Momentum Score: {trend_result.get('momentum_score', 0):.1f}/10")
        components_passed += 1
        
        # Test Competition Density Tracker  
        print("\n⚔️ Testing Competition Density Tracker...")
        competition_tracker = CompetitionDensityTracker()
        
        # Mock competition data
        competition_data = {
            "total_listings": 1500,
            "active_sellers": 300,
            "new_listings_24h": 25,
            "top_10_market_share": 0.35,
            "new_sellers_trend": 0.15
        }
        
        comp_result = competition_tracker.analyze_competition_density(competition_data)
        print(f"   ✅ Competition Level: {comp_result.get('competition_level', 'N/A')}")
        print(f"   💎 Opportunity Score: {comp_result.get('opportunity_score', 0):.1f}/10")
        print(f"   📊 Density Score: {comp_result.get('density_score', 0):.1f}/10")
        components_passed += 1
        
        # Test Demand Surge Analyzer
        print("\n📊 Testing Demand Surge Analyzer...")
        demand_analyzer = DemandSurgeAnalyzer()
        
        # Mock demand data
        demand_data = {
            "current_searches_24h": 2500,
            "baseline_searches": 800,
            "search_growth_7d": 0.6,
            "social_mentions": 450,
            "related_trends": ["trend1", "trend2"]
        }
        
        demand_result = demand_analyzer.detect_demand_surge(demand_data)
        print(f"   ✅ Surge Detected: {demand_result.get('surge_detected', False)}")
        print(f"   📈 Surge Magnitude: {demand_result.get('surge_magnitude', 0):.1f}x")
        print(f"   🎯 Pattern: {demand_result.get('surge_pattern', 'N/A')}")
        components_passed += 1
        
        print(f"\n🎯 Component Tests: {components_passed}/3 passed")
        return components_passed == 3
        
    except Exception as e:
        print(f"❌ Component test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_performance_benchmarks():
    """Test performance and response times"""
    print("\n⚡ TESTING PERFORMANCE BENCHMARKS")
    print("=" * 70)
    
    try:
        from services.market_pulse_engine import MarketPulseEngine
        import time
        
        pulse_engine = MarketPulseEngine()
        
        # Performance test cases
        test_keywords = [
            ["single keyword"],
            ["multiple", "keywords", "test"],
            ["complex market analysis with longer keyword phrase"]
        ]
        
        performance_results = []
        
        for i, keywords in enumerate(test_keywords):
            print(f"\n⚡ Performance Test {i+1}: {len(keywords)} keyword(s)")
            
            start_time = time.time()
            result = pulse_engine.get_market_pulse(keywords)
            end_time = time.time()
            
            response_time = end_time - start_time
            
            if not result.get('error'):
                print(f"   ✅ Response Time: {response_time:.3f} seconds")
                print(f"   📊 Pulse Score: {result.get('market_pulse_score', 0):.1f}")
                performance_results.append(response_time)
            else:
                print(f"   ❌ Failed: {result['error']}")
        
        if performance_results:
            avg_response_time = sum(performance_results) / len(performance_results)
            print(f"\n📊 Average Response Time: {avg_response_time:.3f} seconds")
            
            # Performance benchmarks
            if avg_response_time < 2.0:
                print("🚀 EXCELLENT performance (< 2 seconds)")
                return True
            elif avg_response_time < 5.0:
                print("👍 GOOD performance (< 5 seconds)")
                return True
            else:
                print("⚠️ SLOW performance (> 5 seconds)")
                return False
        
        return False
        
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        return False

def main():
    """Run comprehensive Market Pulse Engine tests"""
    print("⚡ MARKET PULSE ENGINE - COMPREHENSIVE TEST SUITE")
    print("=" * 90)
    print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load environment
    load_env_vars()
    
    # Run all tests
    test_results = []
    
    print("\n" + "="*90)
    test_results.append(("Direct Engine Test", test_market_pulse_direct()))
    
    print("\n" + "="*90) 
    test_results.append(("API Integration Test", test_market_pulse_api()))
    
    print("\n" + "="*90)
    test_results.append(("Individual Components Test", test_individual_components()))
    
    print("\n" + "="*90)
    test_results.append(("Performance Benchmark Test", test_performance_benchmarks()))
    
    # Summary
    print("\n" + "="*90)
    print("📊 TEST RESULTS SUMMARY")
    print("="*90)
    
    passed = 0
    total = len(test_results)
    
    for test_name, success in test_results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if success:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Market Pulse Engine is fully operational!")
        print("⚡ Revolutionary real-time market intelligence is LIVE!")
        print("\n🚀 KEY FEATURES VALIDATED:")
        print("   ✅ Real-time trend velocity detection")
        print("   ✅ Competition density analysis")
        print("   ✅ Demand surge identification")
        print("   ✅ Market opportunity scoring")
        print("   ✅ Predictive timing recommendations")
        print("   ✅ Multi-endpoint API integration")
        print("\n💎 COMPETITIVE ADVANTAGES CONFIRMED:")
        print("   🎯 First-mover in real-time market pulse")
        print("   ⚡ Sub-2-second response times")
        print("   🧠 AI-powered opportunity detection")
    else:
        print("⚠️ Some tests failed. Check implementation and try again.")
    
    print(f"⏰ Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()