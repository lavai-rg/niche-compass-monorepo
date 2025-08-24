import os
import logging
from flask import Blueprint, request, jsonify

# Import AI services
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from ai.azure_text_analytics_service import AzureTextAnalyticsService, TextAnalyticsFeature
from ai.ai_monitoring_service import ai_monitor, MetricType

# Configure logging
logger = logging.getLogger(__name__)

# Create blueprint
ai_text_bp = Blueprint('ai_text', __name__, url_prefix='/api/ai/text')

# Initialize text analytics service
text_service = AzureTextAnalyticsService()

@ai_text_bp.route('/analyze', methods=['POST'])
def analyze_text():
    """Analyze text with multiple features"""
    try:
        # Record metric
        ai_monitor.record_metric('text_analysis', 'request_count', MetricType.COUNTER)
        
        # Get request data
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Text content is required'}), 400
        
        text = data['text']
        if not text or len(text.strip()) == 0:
            return jsonify({'error': 'Text content cannot be empty'}), 400
        
        # Get analysis parameters
        features = data.get('features', ['sentiment', 'key_phrases', 'entities'])
        language = data.get('language', 'en')
        
        # Convert feature names to TextAnalyticsFeature enum
        text_features = []
        for feature in features:
            try:
                text_features.append(TextAnalyticsFeature(feature))
            except ValueError:
                logger.warning(f"Unknown feature: {feature}")
        
        if not text_features:
            text_features = [TextAnalyticsFeature.SENTIMENT, TextAnalyticsFeature.KEY_PHRASES, TextAnalyticsFeature.ENTITIES]
        
        # Perform analysis
        start_time = ai_monitor.record_metric('text_analysis', 'processing_time', MetricType.HISTOGRAM)
        
        result = text_service.analyze_text(
            text=text,
            features=text_features,
            language=language
        )
        
        # Record processing time
        ai_monitor.record_metric('text_analysis', 'processing_time', MetricType.HISTOGRAM, 
                               value=ai_monitor._get_current_time() - start_time)
        
        # Record success metric
        ai_monitor.record_metric('text_analysis', 'success_count', MetricType.COUNTER)
        
        logger.info("Text analysis completed successfully")
        
        return jsonify({
            'success': True,
            'result': result.to_dict(),
            'features_analyzed': [f.value for f in text_features],
            'language': language,
            'text_length': len(text)
        })
        
    except Exception as e:
        logger.error(f"Error in text analysis: {str(e)}")
        
        # Record error metric
        ai_monitor.record_metric('text_analysis', 'error_count', MetricType.COUNTER)
        
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@ai_text_bp.route('/sentiment', methods=['POST'])
def analyze_sentiment():
    """Analyze text sentiment specifically"""
    try:
        # Record metric
        ai_monitor.record_metric('text_sentiment', 'request_count', MetricType.COUNTER)
        
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Text content is required'}), 400
        
        text = data['text']
        language = data.get('language', 'en')
        
        start_time = ai_monitor.record_metric('text_sentiment', 'processing_time', MetricType.HISTOGRAM)
        
        result = text_service.analyze_sentiment(text, language)
        
        # Record processing time
        ai_monitor.record_metric('text_sentiment', 'processing_time', MetricType.HISTOGRAM, 
                               value=ai_monitor._get_current_time() - start_time)
        
        # Record success metric
        ai_monitor.record_metric('text_sentiment', 'success_count', MetricType.COUNTER)
        
        return jsonify({
            'success': True,
            'result': result.to_dict(),
            'language': language
        })
        
    except Exception as e:
        logger.error(f"Error in sentiment analysis: {str(e)}")
        ai_monitor.record_metric('text_sentiment', 'error_count', MetricType.COUNTER)
        
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@ai_text_bp.route('/key-phrases', methods=['POST'])
def extract_key_phrases():
    """Extract key phrases from text"""
    try:
        # Record metric
        ai_monitor.record_metric('text_key_phrases', 'request_count', MetricType.COUNTER)
        
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Text content is required'}), 400
        
        text = data['text']
        language = data.get('language', 'en')
        
        start_time = ai_monitor.record_metric('text_key_phrases', 'processing_time', MetricType.HISTOGRAM)
        
        result = text_service.extract_key_phrases(text, language)
        
        # Record processing time
        ai_monitor.record_metric('text_key_phrases', 'processing_time', MetricType.HISTOGRAM, 
                               value=ai_monitor._get_current_time() - start_time)
        
        # Record success metric
        ai_monitor.record_metric('text_key_phrases', 'success_count', MetricType.COUNTER)
        
        return jsonify({
            'success': True,
            'result': result.to_dict(),
            'language': language
        })
        
    except Exception as e:
        logger.error(f"Error in key phrase extraction: {str(e)}")
        ai_monitor.record_metric('text_key_phrases', 'error_count', MetricType.COUNTER)
        
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@ai_text_bp.route('/entities', methods=['POST'])
def extract_entities():
    """Extract entities from text"""
    try:
        # Record metric
        ai_monitor.record_metric('text_entities', 'request_count', MetricType.COUNTER)
        
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Text content is required'}), 400
        
        text = data['text']
        language = data.get('language', 'en')
        
        start_time = ai_monitor.record_metric('text_entities', 'processing_time', MetricType.HISTOGRAM)
        
        result = text_service.extract_entities(text, language)
        
        # Record processing time
        ai_monitor.record_metric('text_entities', 'processing_time', MetricType.HISTOGRAM, 
                               value=ai_monitor._get_current_time() - start_time)
        
        # Record success metric
        ai_monitor.record_metric('text_entities', 'success_count', MetricType.COUNTER)
        
        return jsonify({
            'success': True,
            'result': result.to_dict(),
            'language': language
        })
        
    except Exception as e:
        logger.error(f"Error in entity extraction: {str(e)}")
        ai_monitor.record_metric('text_entities', 'error_count', MetricType.COUNTER)
        
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@ai_text_bp.route('/language', methods=['POST'])
def detect_language():
    """Detect language of text"""
    try:
        # Record metric
        ai_monitor.record_metric('text_language', 'request_count', MetricType.COUNTER)
        
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Text content is required'}), 400
        
        text = data['text']
        
        start_time = ai_monitor.record_metric('text_language', 'processing_time', MetricType.HISTOGRAM)
        
        result = text_service.detect_language(text)
        
        # Record processing time
        ai_monitor.record_metric('text_language', 'processing_time', MetricType.HISTOGRAM, 
                               value=ai_monitor._get_current_time() - start_time)
        
        # Record success metric
        ai_monitor.record_metric('text_language', 'success_count', MetricType.COUNTER)
        
        return jsonify({
            'success': True,
            'result': result.to_dict()
        })
        
    except Exception as e:
        logger.error(f"Error in language detection: {str(e)}")
        ai_monitor.record_metric('text_language', 'error_count', MetricType.COUNTER)
        
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@ai_text_bp.route('/features', methods=['GET'])
def get_available_features():
    """Get list of available text analysis features"""
    try:
        features = [feature.value for feature in TextAnalyticsFeature]
        return jsonify({
            'success': True,
            'features': features,
            'description': 'Available text analysis features'
        })
    except Exception as e:
        logger.error(f"Error getting features: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@ai_text_bp.route('/health', methods=['GET'])
def text_service_health():
    """Check text analytics service health"""
    try:
        # Test with a simple text analysis
        test_result = text_service.analyze_text(
            "Hello world! This is a test.",
            features=[TextAnalyticsFeature.SENTIMENT],
            language='en'
        )
        
        return jsonify({
            'success': True,
            'status': 'healthy',
            'service': 'Azure Text Analytics',
            'mock_mode': text_service.mock_mode,
            'test_result': test_result.to_dict() if test_result else None
        })
    except Exception as e:
        logger.error(f"Text analytics service health check failed: {str(e)}")
        return jsonify({
            'success': False,
            'status': 'unhealthy',
            'error': str(e)
        }), 500
