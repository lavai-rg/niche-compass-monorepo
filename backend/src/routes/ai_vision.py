import os
import logging
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import base64
from PIL import Image
import io

# Import AI services
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from ai.azure_vision_service import AzureVisionService, VisionFeature
from ai.ai_monitoring_service import ai_monitor, MetricType

# Configure logging
logger = logging.getLogger(__name__)

# Create blueprint
ai_vision_bp = Blueprint('ai_vision', __name__, url_prefix='/api/ai/vision')

# Initialize vision service
vision_service = AzureVisionService()

# Configure file upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_file_size(file):
    """Check if file size is within limits"""
    file.seek(0, 2)  # Seek to end
    size = file.tell()
    file.seek(0)  # Reset to beginning
    return size <= MAX_FILE_SIZE

@ai_vision_bp.route('/analyze', methods=['POST'])
def analyze_image():
    """Analyze image from file upload or URL"""
    try:
        # Record metric
        ai_monitor.record_metric('vision_analysis', 'request_count', MetricType.COUNTER)
        
        # Check if file is uploaded
        if 'image' in request.files:
            file = request.files['image']
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            if not allowed_file(file.filename):
                return jsonify({'error': 'File type not allowed'}), 400
            
            if not validate_file_size(file):
                return jsonify({'error': 'File size too large (max 10MB)'}), 400
            
            # Read file content
            file_content = file.read()
            image_input = file_content
            
            logger.info(f"Processing uploaded file: {file.filename}")
            
        elif 'image_url' in request.json:
            image_input = request.json['image_url']
            logger.info(f"Processing image URL: {image_input}")
            
        else:
            return jsonify({'error': 'Either image file or image_url must be provided'}), 400
        
        # Get analysis parameters
        features = request.json.get('features', ['tags', 'captions', 'colors'])
        language = request.json.get('language', 'en')
        details = request.json.get('details', [])
        
        # Convert feature names to VisionFeature enum
        vision_features = []
        for feature in features:
            try:
                vision_features.append(VisionFeature(feature))
            except ValueError:
                logger.warning(f"Unknown feature: {feature}")
        
        if not vision_features:
            vision_features = [VisionFeature.TAGS, VisionFeature.CAPTIONS, VisionFeature.COLORS]
        
        # Perform analysis
        start_time = ai_monitor.record_metric('vision_analysis', 'processing_time', MetricType.HISTOGRAM)
        
        result = vision_service.analyze_image(
            image_input=image_input,
            features=vision_features,
            language=language,
            details=details
        )
        
        # Record processing time
        ai_monitor.record_metric('vision_analysis', 'processing_time', MetricType.HISTOGRAM, 
                               value=ai_monitor._get_current_time() - start_time)
        
        # Record success metric
        ai_monitor.record_metric('vision_analysis', 'success_count', MetricType.COUNTER)
        
        logger.info("Image analysis completed successfully")
        
        return jsonify({
            'success': True,
            'result': result.to_dict(),
            'features_analyzed': [f.value for f in vision_features],
            'language': language
        })
        
    except Exception as e:
        logger.error(f"Error in image analysis: {str(e)}")
        
        # Record error metric
        ai_monitor.record_metric('vision_analysis', 'error_count', MetricType.COUNTER)
        
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@ai_vision_bp.route('/features', methods=['GET'])
def get_available_features():
    """Get list of available vision analysis features"""
    try:
        features = [feature.value for feature in VisionFeature]
        return jsonify({
            'success': True,
            'features': features,
            'description': 'Available vision analysis features'
        })
    except Exception as e:
        logger.error(f"Error getting features: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@ai_vision_bp.route('/health', methods=['GET'])
def vision_service_health():
    """Check vision service health"""
    try:
        # Test with a simple image analysis
        test_result = vision_service.analyze_image(
            "https://via.placeholder.com/100x100",
            features=[VisionFeature.TAGS],
            language='en'
        )
        
        return jsonify({
            'success': True,
            'status': 'healthy',
            'service': 'Azure Computer Vision',
            'mock_mode': vision_service.mock_mode,
            'test_result': test_result.to_dict() if test_result else None
        })
    except Exception as e:
        logger.error(f"Vision service health check failed: {str(e)}")
        return jsonify({
            'success': False,
            'status': 'unhealthy',
            'error': str(e)
        }), 500

@ai_vision_bp.route('/upload-test', methods=['POST'])
def test_file_upload():
    """Test endpoint for file upload functionality"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400
        
        if not validate_file_size(file):
            return jsonify({'error': 'File size too large'}), 400
        
        # Get file info
        file.seek(0, 2)
        size = file.tell()
        file.seek(0)
        
        return jsonify({
            'success': True,
            'filename': file.filename,
            'size_bytes': size,
            'size_mb': round(size / (1024 * 1024), 2),
            'content_type': file.content_type,
            'message': 'File upload test successful'
        })
        
    except Exception as e:
        logger.error(f"Error in upload test: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
