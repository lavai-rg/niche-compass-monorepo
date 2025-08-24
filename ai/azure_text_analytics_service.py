#!/usr/bin/env python3
"""
Azure Text Analytics Service for Niche Compass
Provides real sentiment analysis and text processing capabilities
"""
import os
import logging
import json
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import requests

logger = logging.getLogger(__name__)

class TextAnalyticsFeature(Enum):
    SENTIMENT = "sentiment"
    KEY_PHRASES = "keyPhrases"
    ENTITIES = "entities"
    LANGUAGE = "language"
    PII = "pii"
    SUMMARIZATION = "summarization"
    OPINION_MINING = "opinionMining"

@dataclass
class TextAnalysisResult:
    request_id: str
    text: str
    analysis_timestamp: datetime = field(default_factory=datetime.now)
    features_analyzed: List[TextAnalyticsFeature] = field(default_factory=list)
    sentiment: Optional[Dict[str, Any]] = None
    key_phrases: List[str] = field(default_factory=list)
    entities: List[Dict[str, Any]] = field(default_factory=list)
    language: Optional[str] = None
    pii_entities: List[Dict[str, Any]] = field(default_factory=list)
    summary: Optional[str] = None
    opinions: List[Dict[str, Any]] = field(default_factory=list)
    error_message: Optional[str] = None
    processing_time_ms: Optional[float] = None

class AzureTextAnalyticsService:
    def __init__(self):
        self.endpoint = os.getenv('AZURE_TEXT_ANALYTICS_ENDPOINT')
        self.api_key = os.getenv('AZURE_TEXT_ANALYTICS_API_KEY')
        self.max_retries = 3
        self.timeout = 30
        self.rate_limit_requests = 100
        self.rate_limit_window = 60  # seconds
        self.request_times = []
        
        # Enable mock mode if no credentials
        self.mock_mode = False if self.endpoint and self.api_key else True
        
        if self.mock_mode:
            logger.warning("Azure Text Analytics Service running in MOCK MODE - No real API calls will be made")
        else:
            logger.info("Azure Text Analytics Service initialized with real Azure credentials")

    def analyze_text(self, text: str, 
                    features: List[TextAnalyticsFeature] = None,
                    language: str = 'en') -> TextAnalysisResult:
        """
        Analyze text using Azure Text Analytics API
        """
        start_time = datetime.now()
        
        try:
            # Set default features if none specified
            if not features:
                features = [TextAnalyticsFeature.SENTIMENT, TextAnalyticsFeature.KEY_PHRASES]

            # Create result object
            result = TextAnalysisResult(
                request_id=f"text_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(text[:50])}",
                text=text,
                features_analyzed=features
            )

            # Check rate limiting
            if not self._check_rate_limit():
                result.error_message = "Rate limit exceeded. Please try again later."
                return result

            # Analyze text
            if self.mock_mode:
                analysis_data = self._generate_mock_results(text, features)
            else:
                analysis_data = self._analyze_with_azure(text, features, language)

            # Update result with analysis data
            self._update_result_from_analysis(result, analysis_data, features)
            
            # Calculate processing time
            result.processing_time_ms = (datetime.now() - start_time).total_seconds() * 1000
            
            logger.info(f"Text analysis completed in {result.processing_time_ms:.2f}ms")
            return result

        except Exception as e:
            logger.error(f"Error analyzing text: {str(e)}")
            result = TextAnalysisResult(
                request_id=f"error_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                text=text,
                error_message=str(e)
            )
            return result

    def analyze_sentiment(self, text: str, language: str = 'en') -> Dict[str, Any]:
        """Analyze sentiment of text"""
        result = self.analyze_text(text, [TextAnalyticsFeature.SENTIMENT], language)
        return result.sentiment or {}

    def extract_key_phrases(self, text: str, language: str = 'en') -> List[str]:
        """Extract key phrases from text"""
        result = self.analyze_text(text, [TextAnalyticsFeature.KEY_PHRASES], language)
        return result.key_phrases

    def detect_language(self, text: str) -> str:
        """Detect language of text"""
        result = self.analyze_text(text, [TextAnalyticsFeature.LANGUAGE])
        return result.language or 'unknown'

    def extract_entities(self, text: str, language: str = 'en') -> List[Dict[str, Any]]:
        """Extract named entities from text"""
        result = self.analyze_text(text, [TextAnalyticsFeature.ENTITIES], language)
        return result.entities

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

    def _analyze_with_azure(self, text: str, features: List[TextAnalyticsFeature], 
                           language: str) -> Dict[str, Any]:
        """Make actual API call to Azure"""
        headers = {
            'Ocp-Apim-Subscription-Key': self.api_key,
            'Content-Type': 'application/json'
        }
        
        # Prepare documents for analysis
        documents = [{
            'id': '1',
            'text': text,
            'language': language
        }]
        
        results = {}
        
        # Analyze each feature
        for feature in features:
            if feature == TextAnalyticsFeature.SENTIMENT:
                api_url = f"{self.endpoint}/text/analytics/v3.2-preview.1/sentiment"
                response = requests.post(api_url, headers=headers, json={'documents': documents}, timeout=self.timeout)
                response.raise_for_status()
                results['sentiment'] = response.json()
            
            elif feature == TextAnalyticsFeature.KEY_PHRASES:
                api_url = f"{self.endpoint}/text/analytics/v3.2-preview.1/keyPhrases"
                response = requests.post(api_url, headers=headers, json={'documents': documents}, timeout=self.timeout)
                response.raise_for_status()
                results['keyPhrases'] = response.json()
            
            elif feature == TextAnalyticsFeature.ENTITIES:
                api_url = f"{self.endpoint}/text/analytics/v3.2-preview.1/entities/recognition/general"
                response = requests.post(api_url, headers=headers, json={'documents': documents}, timeout=self.timeout)
                response.raise_for_status()
                results['entities'] = response.json()
            
            elif feature == TextAnalyticsFeature.LANGUAGE:
                api_url = f"{self.endpoint}/text/analytics/v3.2-preview.1/languages"
                response = requests.post(api_url, headers=headers, json={'documents': documents}, timeout=self.timeout)
                response.raise_for_status()
                results['languages'] = response.json()
        
        return results

    def _generate_mock_results(self, text: str, features: List[TextAnalyticsFeature]) -> Dict[str, Any]:
        """Generate mock results for testing"""
        mock_data = {}
        
        if TextAnalyticsFeature.SENTIMENT in features:
            mock_data['sentiment'] = {
                'documents': [{
                    'id': '1',
                    'sentiment': 'positive',
                    'confidenceScores': {
                        'positive': 0.85,
                        'neutral': 0.10,
                        'negative': 0.05
                    }
                }]
            }
        
        if TextAnalyticsFeature.KEY_PHRASES in features:
            mock_data['keyPhrases'] = {
                'documents': [{
                    'id': '1',
                    'keyPhrases': ['business strategy', 'market analysis', 'competitive advantage']
                }]
            }
        
        if TextAnalyticsFeature.ENTITIES in features:
            mock_data['entities'] = {
                'documents': [{
                    'id': '1',
                    'entities': [
                        {'text': 'Microsoft', 'type': 'Organization', 'confidenceScore': 0.95},
                        {'text': 'AI', 'type': 'Technology', 'confidenceScore': 0.90}
                    ]
                }]
            }
        
        if TextAnalyticsFeature.LANGUAGE in features:
            mock_data['languages'] = {
                'documents': [{
                    'id': '1',
                    'detectedLanguage': {
                        'name': 'English',
                        'iso6391Name': 'en',
                        'confidenceScore': 0.99
                    }
                }]
            }
        
        return mock_data

    def _update_result_from_analysis(self, result: TextAnalysisResult, 
                                   analysis_data: Dict[str, Any], 
                                   features: List[TextAnalyticsFeature]):
        """Update result object with analysis data"""
        if 'sentiment' in analysis_data and 'documents' in analysis_data['sentiment']:
            doc = analysis_data['sentiment']['documents'][0]
            result.sentiment = {
                'sentiment': doc.get('sentiment'),
                'confidence_scores': doc.get('confidenceScores', {})
            }
        
        if 'keyPhrases' in analysis_data and 'documents' in analysis_data['keyPhrases']:
            result.key_phrases = analysis_data['keyPhrases']['documents'][0].get('keyPhrases', [])
        
        if 'entities' in analysis_data and 'documents' in analysis_data['entities']:
            result.entities = analysis_data['entities']['documents'][0].get('entities', [])
        
        if 'languages' in analysis_data and 'documents' in analysis_data['languages']:
            lang_doc = analysis_data['languages']['documents'][0]
            if 'detectedLanguage' in lang_doc:
                result.language = lang_doc['detectedLanguage'].get('iso6391Name')

    def get_service_status(self) -> Dict[str, Any]:
        """Get service health and status information"""
        return {
            'service_name': 'Azure Text Analytics',
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
    text_service = AzureTextAnalyticsService()
    
    # Test service status
    print("Service Status:", text_service.get_service_status())
    
    # Test with mock text analysis
    sample_text = "This is an excellent product with amazing features. I love how it works!"
    result = text_service.analyze_text(
        sample_text,
        features=[TextAnalyticsFeature.SENTIMENT, TextAnalyticsFeature.KEY_PHRASES]
    )
    
    print(f"Analysis Result: {result}")
    print(f"Sentiment: {result.sentiment}")
    print(f"Key Phrases: {result.key_phrases}")
