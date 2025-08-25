#!/usr/bin/env python3
"""
Test AI services directly without Flask
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv('../env.local')

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

print("🔍 Testing AI Services Directly...")
print("=" * 50)

try:
    print("1. Testing AI Monitoring Service...")
    from ai.ai_monitoring_service import ai_monitor, MetricType
    
    # Test recording metrics
    ai_monitor.record_metric('test_service', 'test_count', MetricType.COUNTER)
    ai_monitor.record_metric('test_service', 'test_time', MetricType.HISTOGRAM, value=1.5)
    
    print("   ✅ AI Monitoring Service working")
    
    print("\n2. Testing Azure Vision Service...")
    from ai.azure_vision_service import AzureVisionService, VisionFeature
    
    vision_service = AzureVisionService()
    print(f"   ✅ Azure Vision Service initialized: {vision_service}")
    print(f"   ✅ Mock Mode: {vision_service.mock_mode}")
    
    print("\n3. Testing Azure Text Analytics Service...")
    from ai.azure_text_analytics_service import AzureTextAnalyticsService, TextAnalyticsFeature
    
    text_service = AzureTextAnalyticsService()
    print(f"   ✅ Azure Text Analytics Service initialized: {text_service}")
    print(f"   ✅ Mock Mode: {text_service.mock_mode}")
    
    print("\n4. Testing Vision Analysis...")
    try:
        # Test with a simple image URL
        result = vision_service.analyze_image(
            image_input="https://example.com/test.jpg",
            features=[VisionFeature.TAGS, VisionFeature.COLORS],
            language="en"
        )
        print(f"   ✅ Vision Analysis Result: {result}")
    except Exception as e:
        print(f"   ❌ Vision Analysis Error: {e}")
    
    print("\n5. Testing Text Analytics...")
    try:
        # Test with simple text
        result = text_service.analyze_text(
            text="Hello world, this is a test message.",
            features=[TextAnalyticsFeature.SENTIMENT, TextAnalyticsFeature.KEY_PHRASES],
            language="en"
        )
        print(f"   ✅ Text Analytics Result: {result}")
    except Exception as e:
        print(f"   ❌ Text Analytics Error: {e}")
    
    print("\n🎉 AI Services direct test completed!")
    
except Exception as e:
    print(f"\n❌ Error during testing: {e}")
    print(f"   Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
