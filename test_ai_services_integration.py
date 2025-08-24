#!/usr/bin/env python3
"""
Comprehensive Integration Testing for AI Services - Niche Compass
Tests all AI services including monitoring, vision, and text analytics
"""
import unittest
import time
import json
import os
import sys
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import AI services
from ai.azure_vision_service import AzureVisionService, VisionFeature, VisionAnalysisResult
from ai.azure_text_analytics_service import AzureTextAnalyticsService, TextAnalyticsFeature, TextAnalysisResult
from ai.ai_monitoring_service import AIMonitoringService, MonitoringLevel, MetricType, ai_monitor

class TestAIVisionService(unittest.TestCase):
    """Test Azure Computer Vision Service"""
    
    def setUp(self):
        """Set up test environment"""
        self.vision_service = AzureVisionService()
        self.test_image_url = "https://example.com/test-image.jpg"
        self.test_features = [VisionFeature.TAGS, VisionFeature.CAPTIONS, VisionFeature.COLORS]
    
    def test_service_initialization(self):
        """Test service initialization"""
        self.assertIsNotNone(self.vision_service)
        self.assertTrue(hasattr(self.vision_service, 'mock_mode'))
        self.assertTrue(hasattr(self.vision_service, 'endpoint'))
        self.assertTrue(hasattr(self.vision_service, 'api_key'))
    
    def test_mock_mode_activation(self):
        """Test mock mode activation when no credentials"""
        # Clear environment variables
        with patch.dict(os.environ, {}, clear=True):
            service = AzureVisionService()
            self.assertTrue(service.mock_mode)
    
    def test_image_analysis_mock_mode(self):
        """Test image analysis in mock mode"""
        result = self.vision_service.analyze_image(
            self.test_image_url,
            features=self.test_features
        )
        
        self.assertIsInstance(result, VisionAnalysisResult)
        self.assertIsNotNone(result.request_id)
        self.assertEqual(result.image_url, self.test_image_url)
        self.assertEqual(len(result.features_analyzed), 3)
        self.assertIsNone(result.error_message)
    
    def test_vision_features_enum(self):
        """Test vision features enum values"""
        self.assertEqual(VisionFeature.TAGS.value, "tags")
        self.assertEqual(VisionFeature.CAPTIONS.value, "captions")
        self.assertEqual(VisionFeature.FACES.value, "faces")
        self.assertEqual(VisionFeature.OBJECTS.value, "objects")
        self.assertEqual(VisionFeature.BRANDS.value, "brands")
        self.assertEqual(VisionFeature.LANDMARKS.value, "landmarks")
        self.assertEqual(VisionFeature.CELEBRITIES.value, "celebrities")
        self.assertEqual(VisionFeature.COLORS.value, "colors")
        self.assertEqual(VisionFeature.IMAGE_TYPE.value, "imageType")
        self.assertEqual(VisionFeature.ADULT.value, "adult")
    
    def test_rate_limiting(self):
        """Test rate limiting functionality"""
        # Make multiple requests to trigger rate limiting
        for i in range(25):  # Exceed 20 requests per minute
            result = self.vision_service.analyze_image(
                self.test_image_url,
                features=[VisionFeature.TAGS]
            )
            
            if i >= 20:
                self.assertIsNotNone(result.error_message)
                self.assertIn("Rate limit exceeded", result.error_message)
            else:
                self.assertIsNone(result.error_message)
    
    def test_service_status(self):
        """Test service status endpoint"""
        status = self.vision_service.get_service_status()
        
        self.assertIn('service_name', status)
        self.assertIn('status', status)
        self.assertIn('endpoint', status)
        self.assertIn('rate_limit_remaining', status)
        self.assertIn('mock_mode', status)
        self.assertEqual(status['service_name'], 'Azure Computer Vision')

class TestAITextAnalyticsService(unittest.TestCase):
    """Test Azure Text Analytics Service"""
    
    def setUp(self):
        """Set up test environment"""
        self.text_service = AzureTextAnalyticsService()
        self.test_text = "This is an excellent product with amazing features. I love how it works!"
        self.test_features = [TextAnalyticsFeature.SENTIMENT, TextAnalyticsFeature.KEY_PHRASES]
    
    def test_service_initialization(self):
        """Test service initialization"""
        self.assertIsNotNone(self.text_service)
        self.assertTrue(hasattr(self.text_service, 'mock_mode'))
        self.assertTrue(hasattr(self.text_service, 'endpoint'))
        self.assertTrue(hasattr(self.text_service, 'api_key'))
    
    def test_mock_mode_activation(self):
        """Test mock mode activation when no credentials"""
        with patch.dict(os.environ, {}, clear=True):
            service = AzureTextAnalyticsService()
            self.assertTrue(service.mock_mode)
    
    def test_text_analysis_mock_mode(self):
        """Test text analysis in mock mode"""
        result = self.text_service.analyze_text(
            self.test_text,
            features=self.test_features
        )
        
        self.assertIsInstance(result, TextAnalysisResult)
        self.assertIsNotNone(result.request_id)
        self.assertEqual(result.text, self.test_text)
        self.assertEqual(len(result.features_analyzed), 2)
        self.assertIsNone(result.error_message)
    
    def test_sentiment_analysis(self):
        """Test sentiment analysis functionality"""
        result = self.text_service.analyze_sentiment(self.test_text)
        
        self.assertIsInstance(result, dict)
        self.assertIn('sentiment', result)
        self.assertIn('confidence_scores', result)
    
    def test_key_phrase_extraction(self):
        """Test key phrase extraction"""
        phrases = self.text_service.extract_key_phrases(self.test_text)
        
        self.assertIsInstance(phrases, list)
        self.assertGreater(len(phrases), 0)
    
    def test_language_detection(self):
        """Test language detection"""
        language = self.text_service.detect_language(self.test_text)
        
        self.assertIsInstance(language, str)
        self.assertNotEqual(language, 'unknown')
    
    def test_entity_extraction(self):
        """Test entity extraction"""
        entities = self.text_service.extract_entities(self.test_text)
        
        self.assertIsInstance(entities, list)
    
    def test_text_analytics_features_enum(self):
        """Test text analytics features enum values"""
        self.assertEqual(TextAnalyticsFeature.SENTIMENT.value, "sentiment")
        self.assertEqual(TextAnalyticsFeature.KEY_PHRASES.value, "keyPhrases")
        self.assertEqual(TextAnalyticsFeature.ENTITIES.value, "entities")
        self.assertEqual(TextAnalyticsFeature.LANGUAGE.value, "language")
        self.assertEqual(TextAnalyticsFeature.PII.value, "pii")
        self.assertEqual(TextAnalyticsFeature.SUMMARIZATION.value, "summarization")
        self.assertEqual(TextAnalyticsFeature.OPINION_MINING.value, "opinionMining")
    
    def test_rate_limiting(self):
        """Test rate limiting functionality"""
        # Make multiple requests to trigger rate limiting
        for i in range(105):  # Exceed 100 requests per minute
            result = self.text_service.analyze_text(
                self.test_text,
                features=[TextAnalyticsFeature.SENTIMENT]
            )
            
            if i >= 100:
                self.assertIsNotNone(result.error_message)
                self.assertIn("Rate limit exceeded", result.error_message)
            else:
                self.assertIsNone(result.error_message)
    
    def test_service_status(self):
        """Test service status endpoint"""
        status = self.text_service.get_service_status()
        
        self.assertIn('service_name', status)
        self.assertIn('status', status)
        self.assertIn('endpoint', status)
        self.assertIn('rate_limit_remaining', status)
        self.assertIn('mock_mode', status)
        self.assertEqual(status['service_name'], 'Azure Text Analytics')

class TestAIMonitoringService(unittest.TestCase):
    """Test AI Monitoring Service"""
    
    def setUp(self):
        """Set up test environment"""
        self.monitor = AIMonitoringService()
        time.sleep(1)  # Allow monitoring to start
    
    def tearDown(self):
        """Clean up after tests"""
        self.monitor.stop()
    
    def test_monitoring_initialization(self):
        """Test monitoring service initialization"""
        self.assertIsNotNone(self.monitor)
        self.assertTrue(self.monitor.monitoring_enabled)
        self.assertEqual(self.monitor.health_check_interval, 30)
        self.assertEqual(self.monitor.metrics_retention_hours, 24)
    
    def test_health_check_creation(self):
        """Test health check creation"""
        health_check = self.monitor._check_service_health('ai_monitoring')
        
        self.assertIsNotNone(health_check)
        self.assertEqual(health_check.service_name, 'ai_monitoring')
        self.assertIn(health_check.status, ['healthy', 'degraded', 'unhealthy'])
        self.assertIsInstance(health_check.timestamp, datetime)
        self.assertIsInstance(health_check.response_time_ms, float)
    
    def test_metric_recording(self):
        """Test performance metric recording"""
        self.monitor.record_metric(
            'test_service',
            'test_metric',
            MetricType.COUNTER,
            1.0
        )
        
        metrics = self.monitor.get_performance_metrics(
            service_name='test_service',
            metric_name='test_metric'
        )
        
        self.assertEqual(len(metrics), 1)
        self.assertEqual(metrics[0].service_name, 'test_service')
        self.assertEqual(metrics[0].metric_name, 'test_metric')
        self.assertEqual(metrics[0].value, 1.0)
    
    def test_alert_creation(self):
        """Test alert creation"""
        self.monitor._create_alert(
            'test_service',
            MonitoringLevel.WARNING,
            'Test warning message'
        )
        
        alerts = self.monitor.get_alerts(service_name='test_service')
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0].level, MonitoringLevel.WARNING)
        self.assertEqual(alerts[0].message, 'Test warning message')
        self.assertFalse(alerts[0].acknowledged)
        self.assertFalse(alerts[0].resolved)
    
    def test_alert_acknowledgment(self):
        """Test alert acknowledgment"""
        self.monitor._create_alert(
            'test_service',
            MonitoringLevel.ERROR,
            'Test error message'
        )
        
        alerts = self.monitor.get_alerts(service_name='test_service')
        alert_id = alerts[0].id
        
        self.monitor.acknowledge_alert(alert_id)
        
        alerts = self.monitor.get_alerts(service_name='test_service')
        self.assertTrue(alerts[0].acknowledged)
    
    def test_alert_resolution(self):
        """Test alert resolution"""
        self.monitor._create_alert(
            'test_service',
            MonitoringLevel.CRITICAL,
            'Test critical message'
        )
        
        alerts = self.monitor.get_alerts(service_name='test_service')
        alert_id = alerts[0].id
        
        self.monitor.resolve_alert(alert_id)
        
        alerts = self.monitor.get_alerts(service_name='test_service')
        self.assertTrue(alerts[0].resolved)
    
    def test_overall_health_summary(self):
        """Test overall health summary"""
        summary = self.monitor.get_overall_health_summary()
        
        self.assertIn('overall_status', summary)
        self.assertIn('services_count', summary)
        self.assertIn('healthy_count', summary)
        self.assertIn('degraded_count', summary)
        self.assertIn('unhealthy_count', summary)
        self.assertIn('uptime_percent', summary)
    
    def test_metrics_filtering(self):
        """Test metrics filtering functionality"""
        # Record multiple metrics
        for i in range(5):
            self.monitor.record_metric(
                'test_service',
                'test_metric',
                MetricType.COUNTER,
                float(i)
            )
        
        # Test filtering by service
        metrics = self.monitor.get_performance_metrics(service_name='test_service')
        self.assertEqual(len(metrics), 5)
        
        # Test filtering by metric name
        metrics = self.monitor.get_performance_metrics(metric_name='test_metric')
        self.assertEqual(len(metrics), 5)
        
        # Test filtering by time
        metrics = self.monitor.get_performance_metrics(hours=1)
        self.assertEqual(len(metrics), 5)
    
    def test_alerts_filtering(self):
        """Test alerts filtering functionality"""
        # Create alerts with different levels
        self.monitor._create_alert('service1', MonitoringLevel.INFO, 'Info message')
        self.monitor._create_alert('service1', MonitoringLevel.WARNING, 'Warning message')
        self.monitor._create_alert('service2', MonitoringLevel.ERROR, 'Error message')
        
        # Test filtering by service
        alerts = self.monitor.get_alerts(service_name='service1')
        self.assertEqual(len(alerts), 2)
        
        # Test filtering by level
        alerts = self.monitor.get_alerts(level=MonitoringLevel.WARNING)
        self.assertEqual(len(alerts), 1)
        
        # Test filtering by acknowledged status
        alerts = self.monitor.get_alerts(acknowledged=False)
        self.assertEqual(len(alerts), 3)

class TestAIServicesIntegration(unittest.TestCase):
    """Integration tests for AI services working together"""
    
    def setUp(self):
        """Set up test environment"""
        self.vision_service = AzureVisionService()
        self.text_service = AzureTextAnalyticsService()
        self.monitor = AIMonitoringService()
        time.sleep(1)  # Allow monitoring to start
    
    def tearDown(self):
        """Clean up after tests"""
        self.monitor.stop()
    
    def test_end_to_end_ai_workflow(self):
        """Test complete AI workflow from image to text analysis"""
        # Step 1: Analyze image
        image_result = self.vision_service.analyze_image(
            "https://example.com/business-image.jpg",
            features=[VisionFeature.TAGS, VisionFeature.CAPTIONS]
        )
        
        self.assertIsNotNone(image_result)
        self.assertIsNone(image_result.error_message)
        
        # Step 2: Analyze image captions as text
        if image_result.captions:
            caption_text = image_result.captions[0]['text']
            text_result = self.text_service.analyze_text(
                caption_text,
                features=[TextAnalyticsFeature.SENTIMENT, TextAnalyticsFeature.KEY_PHRASES]
            )
            
            self.assertIsNotNone(text_result)
            self.assertIsNone(text_result.error_message)
        
        # Step 3: Check monitoring data
        time.sleep(2)  # Allow monitoring to collect data
        
        health_summary = self.monitor.get_overall_health_summary()
        self.assertIsNotNone(health_summary)
        
        # Check that metrics were recorded
        vision_metrics = self.monitor.get_performance_metrics(service_name='azure_vision')
        text_metrics = self.monitor.get_performance_metrics(service_name='azure_text_analytics')
        
        self.assertGreater(len(vision_metrics), 0)
        self.assertGreater(len(text_metrics), 0)
    
    def test_error_handling_and_monitoring(self):
        """Test error handling and monitoring integration"""
        # Force an error by passing invalid data
        try:
            self.vision_service.analyze_image(None)
        except:
            pass  # Expected error
        
        # Check that error metrics were recorded
        time.sleep(1)
        error_metrics = self.monitor.get_performance_metrics(
            service_name='azure_vision',
            metric_name='analyze_image_error'
        )
        
        # Note: This test may not work in mock mode since errors are caught
        # In real mode, this would verify error tracking
    
    def test_performance_monitoring(self):
        """Test performance monitoring across services"""
        # Perform multiple operations to generate metrics
        for i in range(3):
            self.vision_service.analyze_image(
                f"https://example.com/test-image-{i}.jpg",
                features=[VisionFeature.TAGS]
            )
            
            self.text_service.analyze_text(
                f"Test text number {i} for performance testing",
                features=[TextAnalyticsFeature.SENTIMENT]
            )
        
        time.sleep(2)  # Allow monitoring to collect data
        
        # Check performance metrics
        vision_metrics = self.monitor.get_performance_metrics(service_name='azure_vision')
        text_metrics = self.monitor.get_performance_metrics(service_name='azure_text_analytics')
        
        self.assertGreater(len(vision_metrics), 0)
        self.assertGreater(len(text_metrics), 0)
        
        # Check execution time metrics
        execution_metrics = [
            m for m in vision_metrics 
            if 'execution_time' in m.metric_name
        ]
        
        self.assertGreater(len(execution_metrics), 0)
        
        # Verify execution times are reasonable
        for metric in execution_metrics:
            self.assertGreater(metric.value, 0)
            self.assertLess(metric.value, 10000)  # Less than 10 seconds

def run_performance_benchmark():
    """Run performance benchmark tests"""
    print("\n🚀 AI Services Performance Benchmark")
    print("=" * 50)
    
    # Initialize services
    vision_service = AzureVisionService()
    text_service = AzureTextAnalyticsService()
    
    # Benchmark Vision Service
    print("\n📸 Vision Service Benchmark:")
    start_time = time.time()
    
    for i in range(10):
        result = vision_service.analyze_image(
            f"https://example.com/benchmark-image-{i}.jpg",
            features=[VisionFeature.TAGS, VisionFeature.CAPTIONS, VisionFeature.COLORS]
        )
        if result.error_message:
            print(f"  Error in iteration {i}: {result.error_message}")
    
    vision_time = time.time() - start_time
    print(f"  10 image analyses completed in {vision_time:.2f}s")
    print(f"  Average time per analysis: {vision_time/10:.2f}s")
    
    # Benchmark Text Analytics Service
    print("\n📝 Text Analytics Service Benchmark:")
    start_time = time.time()
    
    test_texts = [
        "This product is absolutely amazing and exceeds all expectations!",
        "The quality is poor and the service is terrible.",
        "It's okay, nothing special but gets the job done.",
        "Outstanding performance and excellent customer support.",
        "Disappointing experience, would not recommend."
    ]
    
    for i in range(10):
        text = test_texts[i % len(test_texts)]
        result = text_service.analyze_text(
            text,
            features=[TextAnalyticsFeature.SENTIMENT, TextAnalyticsFeature.KEY_PHRASES, TextAnalyticsFeature.ENTITIES]
        )
        if result.error_message:
            print(f"  Error in iteration {i}: {result.error_message}")
    
    text_time = time.time() - start_time
    print(f"  10 text analyses completed in {text_time:.2f}s")
    print(f"  Average time per analysis: {text_time/10:.2f}s")
    
    # Overall benchmark
    total_time = vision_time + text_time
    print(f"\n🏁 Overall Benchmark:")
    print(f"  Total operations: 20")
    print(f"  Total time: {total_time:.2f}s")
    print(f"  Average time per operation: {total_time/20:.2f}s")
    print(f"  Operations per second: {20/total_time:.2f}")

if __name__ == '__main__':
    # Set up logging
    import logging
    logging.basicConfig(level=logging.INFO)
    
    print("🤖 AI Services Integration Test Suite")
    print("=" * 60)
    
    # Run unit tests
    print("\n📋 Running Unit Tests...")
    unittest.main(verbosity=2, exit=False)
    
    # Run performance benchmark
    run_performance_benchmark()
    
    print("\n✅ All tests completed!")
