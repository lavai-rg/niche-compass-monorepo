#!/usr/bin/env python3
"""
Azure Computer Vision Service for Niche Compass
Provides real image analysis capabilities using Azure Cognitive Services
"""
import os
import logging
import json
import base64
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import requests
from PIL import Image
import io

logger = logging.getLogger(__name__)

class VisionFeature(Enum):
    TAGS = "tags"
    CAPTIONS = "captions"
    FACES = "faces"
    OBJECTS = "objects"
    BRANDS = "brands"
    LANDMARKS = "landmarks"
    CELEBRITIES = "celebrities"
    COLORS = "colors"
    IMAGE_TYPE = "imageType"
    ADULT = "adult"

@dataclass
class VisionAnalysisResult:
    request_id: str
    image_url: Optional[str] = None
    analysis_timestamp: datetime = field(default_factory=datetime.now)
    features_analyzed: List[VisionFeature] = field(default_factory=list)
    tags: List[Dict[str, Any]] = field(default_factory=list)
    captions: List[Dict[str, Any]] = field(default_factory=list)
    faces: List[Dict[str, Any]] = field(default_factory=list)
    objects: List[Dict[str, Any]] = field(default_factory=list)
    brands: List[Dict[str, Any]] = field(default_factory=list)
    landmarks: List[Dict[str, Any]] = field(default_factory=list)
    celebrities: List[Dict[str, Any]] = field(default_factory=list)
    colors: Dict[str, Any] = field(default_factory=dict)
    image_type: Dict[str, Any] = field(default_factory=dict)
    adult_content: Dict[str, Any] = field(default_factory=dict)
    ocr_text: Optional[str] = None
    thumbnail_url: Optional[str] = None
    error_message: Optional[str] = None
    processing_time_ms: Optional[float] = None

class AzureVisionService:
    def __init__(self):
        self.endpoint = os.getenv('AZURE_VISION_ENDPOINT')
        self.api_key = os.getenv('AZURE_VISION_API_KEY')
        self.max_retries = 3
        self.timeout = 30
        self.rate_limit_requests = 20
        self.rate_limit_window = 60  # seconds
        self.request_times = []
        
        # Enable mock mode if no credentials
        self.mock_mode = False if self.endpoint and self.api_key else True
        
        if self.mock_mode:
            logger.warning("Azure Vision Service running in MOCK MODE - No real API calls will be made")
        else:
            logger.info("Azure Vision Service initialized with real Azure credentials")

    def analyze_image(self, image_input: Union[str, bytes, Image.Image], 
                     features: List[VisionFeature] = None, 
                     language: str = 'en', 
                     details: List[str] = None) -> VisionAnalysisResult:
        """
        Analyze image using Azure Computer Vision API
        """
        start_time = datetime.now()
        
        try:
            # Convert input to bytes
            if isinstance(image_input, str):
                # URL input
                image_data = self._download_image(image_input)
                image_url = image_input
            elif isinstance(image_input, bytes):
                # Bytes input
                image_data = image_input
                image_url = None
            elif isinstance(image_input, Image.Image):
                # PIL Image input
                img_byte_arr = io.BytesIO()
                image_input.save(img_byte_arr, format='PNG')
                image_data = img_byte_arr.getvalue()
                image_url = None
            else:
                raise ValueError("Unsupported image input type")

            # Set default features if none specified
            if not features:
                features = [VisionFeature.TAGS, VisionFeature.CAPTIONS, VisionFeature.COLORS]

            # Create result object
            result = VisionAnalysisResult(
                request_id=f"vision_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(str(features))}",
                image_url=image_url,
                features_analyzed=features
            )

            # Check rate limiting
            if not self._check_rate_limit():
                result.error_message = "Rate limit exceeded. Please try again later."
                return result

            # Analyze image
            if self.mock_mode:
                analysis_data = self._generate_mock_results(result, features)
            else:
                analysis_data = self._analyze_with_azure(image_data, features, language, details)

            # Update result with analysis data
            self._update_result_from_analysis(result, analysis_data, features)
            
            # Calculate processing time
            result.processing_time_ms = (datetime.now() - start_time).total_seconds() * 1000
            
            logger.info(f"Image analysis completed in {result.processing_time_ms:.2f}ms")
            return result

        except Exception as e:
            logger.error(f"Error analyzing image: {str(e)}")
            result = VisionAnalysisResult(
                request_id=f"error_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                error_message=str(e)
            )
            return result

    def _download_image(self, url: str) -> bytes:
        """Download image from URL"""
        response = requests.get(url, timeout=self.timeout)
        response.raise_for_status()
        return response.content

    def _check_rate_limit(self) -> bool:
        """Check if we're within rate limits"""
        now = datetime.now()
        # Remove old requests outside the window
        self.request_times = [t for t in self.request_times 
                            if now - t < timedelta(seconds=self.rate_limit_window)]
        
        if len(self.request_times) >= self.rate_limit_requests:
            return False
        
        self.request_times.append(now)
        return True

    def _analyze_with_azure(self, image_data: bytes, features: List[VisionFeature], 
                           language: str, details: List[str]) -> Dict[str, Any]:
        """Make actual API call to Azure"""
        headers = {
            'Ocp-Apim-Subscription-Key': self.api_key,
            'Content-Type': 'application/octet-stream'
        }
        
        # Build API URL
        api_url = f"{self.endpoint}/vision/v3.2/analyze"
        
        # Build query parameters
        params = {
            'visualFeatures': ','.join([f.value for f in features]),
            'language': language
        }
        
        if details:
            params['details'] = ','.join(details)
        
        response = requests.post(api_url, headers=headers, params=params, 
                               data=image_data, timeout=self.timeout)
        response.raise_for_status()
        
        return response.json()

    def _generate_mock_results(self, result: VisionAnalysisResult, 
                              features: List[VisionFeature]) -> Dict[str, Any]:
        """Generate mock results for testing"""
        mock_data = {}
        
        if VisionFeature.TAGS in features:
            mock_data['tags'] = [
                {'name': 'business', 'confidence': 0.95},
                {'name': 'technology', 'confidence': 0.87},
                {'name': 'innovation', 'confidence': 0.82}
            ]
        
        if VisionFeature.CAPTIONS in features:
            mock_data['description'] = {
                'captions': [
                    {'text': 'A modern business technology concept', 'confidence': 0.89}
                ]
            }
        
        if VisionFeature.COLORS in features:
            mock_data['color'] = {
                'dominantColors': ['#2F4F4F', '#708090', '#C0C0C0'],
                'isBWImg': False
            }
        
        return mock_data

    def _update_result_from_analysis(self, result: VisionAnalysisResult, 
                                   analysis_data: Dict[str, Any], 
                                   features: List[VisionFeature]):
        """Update result object with analysis data"""
        if 'tags' in analysis_data:
            result.tags = analysis_data['tags']
        
        if 'description' in analysis_data and 'captions' in analysis_data['description']:
            result.captions = analysis_data['description']['captions']
        
        if 'faces' in analysis_data:
            result.faces = analysis_data['faces']
        
        if 'objects' in analysis_data:
            result.objects = analysis_data['objects']
        
        if 'brands' in analysis_data:
            result.brands = analysis_data['brands']
        
        if 'landmarks' in analysis_data:
            result.landmarks = analysis_data['landmarks']
        
        if 'celebrities' in analysis_data:
            result.celebrities = analysis_data['celebrities']
        
        if 'color' in analysis_data:
            result.colors = analysis_data['color']
        
        if 'imageType' in analysis_data:
            result.image_type = analysis_data['imageType']
        
        if 'adult' in analysis_data:
            result.adult_content = analysis_data['adult']

    def get_service_status(self) -> Dict[str, Any]:
        """Get service health and status information"""
        return {
            'service_name': 'Azure Computer Vision',
            'status': 'healthy' if not self.mock_mode else 'mock_mode',
            'endpoint': self.endpoint if not self.mock_mode else 'mock',
            'rate_limit_remaining': max(0, self.rate_limit_requests - len(self.request_times)),
            'rate_limit_window_seconds': self.rate_limit_window,
            'mock_mode': self.mock_mode,
            'last_updated': datetime.now().isoformat()
        }

# Example usage
if __name__ == "__main__":
    # Initialize service
    vision_service = AzureVisionService()
    
    # Test service status
    print("Service Status:", vision_service.get_service_status())
    
    # Test with mock image analysis
    result = vision_service.analyze_image(
        "https://example.com/test-image.jpg",
        features=[VisionFeature.TAGS, VisionFeature.CAPTIONS, VisionFeature.COLORS]
    )
    
    print(f"Analysis Result: {result}")
