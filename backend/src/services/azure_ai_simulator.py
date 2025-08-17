"""
Azure AI Services Simulator for Development
Provides realistic AI responses for development/testing when real Azure services are not available
"""

import re
import random
from datetime import datetime
from typing import Dict, List, Any
import requests
from urllib.parse import urlparse

class AzureAISimulator:
    """Simulates Azure AI services with realistic responses"""
    
    def __init__(self):
        # Pre-defined image analysis datasets for different product types
        self.image_analysis_db = {
            'jewelry': {
                'tags': ['jewelry', 'necklace', 'bracelet', 'ring', 'handmade', 'silver', 'gold', 'precious', 'elegant', 'fashion'],
                'categories': ['jewelry_accessories', 'fashion', 'handmade'],
                'descriptions': [
                    'A beautiful handmade jewelry piece with intricate details',
                    'Elegant silver jewelry with modern design',
                    'Artisan crafted jewelry with precious stones',
                    'Minimalist jewelry piece perfect for everyday wear'
                ],
                'colors': ['#FFD700', '#C0C0C0', '#E6E6FA', '#DDA0DD', '#F0E68C']
            },
            'home_decor': {
                'tags': ['decor', 'home', 'wall art', 'vintage', 'rustic', 'modern', 'handmade', 'wood', 'ceramic', 'textile'],
                'categories': ['home_garden', 'decor', 'handmade'],
                'descriptions': [
                    'Stylish home decor item that adds character to any room',
                    'Handcrafted decorative piece with rustic charm',
                    'Modern home accessory with clean lines',
                    'Vintage-inspired decor perfect for contemporary homes'
                ],
                'colors': ['#8FBC8F', '#F5F5DC', '#DEB887', '#D2B48C', '#BC8F8F']
            },
            'pet_accessories': {
                'tags': ['pet', 'dog', 'cat', 'collar', 'toy', 'accessories', 'custom', 'leather', 'fabric', 'personalized'],
                'categories': ['pet_supplies', 'accessories', 'handmade'],
                'descriptions': [
                    'High-quality pet accessory designed for comfort and style',
                    'Durable pet collar with custom design options',
                    'Handmade pet toy using safe, non-toxic materials',
                    'Personalized pet accessory with unique charm'
                ],
                'colors': ['#4169E1', '#FF69B4', '#32CD32', '#FF6347', '#9370DB']
            },
            'art': {
                'tags': ['art', 'print', 'painting', 'illustration', 'poster', 'abstract', 'modern', 'vintage', 'canvas', 'frame'],
                'categories': ['art_collectibles', 'prints', 'handmade'],
                'descriptions': [
                    'Original artwork with vibrant colors and artistic expression',
                    'Limited edition print featuring contemporary design',
                    'Hand-drawn illustration with intricate details',
                    'Abstract art piece that captures modern aesthetics'
                ],
                'colors': ['#FF7F50', '#6495ED', '#DDA0DD', '#F0E68C', '#98FB98']
            },
            'crafts': {
                'tags': ['craft', 'handmade', 'diy', 'scrapbook', 'knitting', 'sewing', 'paper', 'fabric', 'supplies', 'tools'],
                'categories': ['crafts_supplies', 'handmade', 'hobby'],
                'descriptions': [
                    'High-quality craft supplies for creative projects',
                    'Handmade craft item with attention to detail',
                    'DIY craft kit complete with instructions',
                    'Artisan craft tool designed for precision work'
                ],
                'colors': ['#FFB6C1', '#98FB98', '#F0E68C', '#DDA0DD', '#87CEEB']
            }
        }
        
        # Sentiment analysis patterns
        self.positive_indicators = [
            'love', 'amazing', 'great', 'excellent', 'perfect', 'beautiful', 'wonderful', 'fantastic', 
            'awesome', 'brilliant', 'outstanding', 'superb', 'magnificent', 'incredible', 'fabulous',
            'recommend', 'highly', 'pleased', 'satisfied', 'happy', 'delighted', 'impressed', 'thrilled'
        ]
        
        self.negative_indicators = [
            'hate', 'terrible', 'awful', 'disappointed', 'broke', 'worst', 'horrible', 'disgusting',
            'useless', 'cheap', 'flimsy', 'poor', 'bad', 'defective', 'damaged', 'waste', 'regret',
            'angry', 'frustrated', 'annoyed', 'upset', 'dissatisfied', 'unhappy'
        ]
        
        self.neutral_indicators = [
            'okay', 'fine', 'average', 'decent', 'acceptable', 'standard', 'typical', 'normal',
            'expected', 'basic', 'simple', 'plain', 'regular', 'ordinary'
        ]
    
    def analyze_image_from_url(self, image_url: str) -> Dict[str, Any]:
        """Simulate Azure Computer Vision image analysis"""
        try:
            # Try to determine product category from URL or make educated guess
            category = self._detect_product_category(image_url)
            
            # Get category-specific analysis data
            analysis_data = self.image_analysis_db.get(category, self.image_analysis_db['crafts'])
            
            # Generate realistic response
            selected_tags = random.sample(analysis_data['tags'], min(random.randint(3, 7), len(analysis_data['tags'])))
            selected_categories = random.sample(analysis_data['categories'], min(random.randint(1, 2), len(analysis_data['categories'])))
            description = random.choice(analysis_data['descriptions'])
            
            # Add confidence scores for realism
            confidence_base = random.uniform(0.75, 0.95)
            
            return {
                "description": {
                    "text": description,
                    "confidence": round(confidence_base, 3)
                },
                "tags": [
                    {"name": tag, "confidence": round(random.uniform(0.6, 0.95), 3)} 
                    for tag in selected_tags
                ],
                "categories": [
                    {"name": cat, "confidence": round(random.uniform(0.7, 0.9), 3)} 
                    for cat in selected_categories
                ],
                "color_analysis": {
                    "dominant_colors": random.sample(analysis_data['colors'], 3),
                    "accent_color": random.choice(analysis_data['colors'])
                },
                "metadata": {
                    "analyzed_at": datetime.utcnow().isoformat(),
                    "source": "azure_ai_simulator",
                    "category_detected": category
                }
            }
            
        except Exception as e:
            return {
                "error": f"Image analysis simulation failed: {str(e)}",
                "fallback": {
                    "description": "Generic product image",
                    "tags": ["product", "handmade", "item"],
                    "categories": ["general"]
                }
            }
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Simulate Azure Text Analytics sentiment analysis"""
        if not text or not text.strip():
            return {
                "sentiment": "neutral",
                "confidence_scores": {
                    "positive": 0.33,
                    "neutral": 0.34,
                    "negative": 0.33
                }
            }
        
        text_lower = text.lower()
        
        # Count sentiment indicators
        positive_count = sum(1 for word in self.positive_indicators if word in text_lower)
        negative_count = sum(1 for word in self.negative_indicators if word in text_lower)
        neutral_count = sum(1 for word in self.neutral_indicators if word in text_lower)
        
        # Advanced sentiment analysis simulation
        sentiment_score = self._calculate_sentiment_score(text_lower, positive_count, negative_count, neutral_count)
        
        # Determine sentiment based on score
        if sentiment_score > 0.1:
            sentiment = "positive"
            pos_conf = 0.6 + (sentiment_score * 0.35)
            neg_conf = max(0.05, 0.3 - sentiment_score)
            neu_conf = 1.0 - pos_conf - neg_conf
        elif sentiment_score < -0.1:
            sentiment = "negative"
            neg_conf = 0.6 + (abs(sentiment_score) * 0.35)
            pos_conf = max(0.05, 0.3 - abs(sentiment_score))
            neu_conf = 1.0 - neg_conf - pos_conf
        else:
            sentiment = "neutral"
            neu_conf = 0.5 + random.uniform(0.1, 0.3)
            remaining = 1.0 - neu_conf
            pos_conf = remaining * random.uniform(0.3, 0.7)
            neg_conf = remaining - pos_conf
        
        return {
            "sentiment": sentiment,
            "confidence_scores": {
                "positive": round(max(0.01, min(0.99, pos_conf)), 3),
                "neutral": round(max(0.01, min(0.99, neu_conf)), 3),
                "negative": round(max(0.01, min(0.99, neg_conf)), 3)
            },
            "key_phrases": self._extract_key_phrases(text),
            "metadata": {
                "analyzed_at": datetime.utcnow().isoformat(),
                "source": "azure_ai_simulator",
                "text_length": len(text),
                "sentiment_indicators": {
                    "positive": positive_count,
                    "negative": negative_count,
                    "neutral": neutral_count
                }
            }
        }
    
    def _detect_product_category(self, image_url: str) -> str:
        """Detect product category from image URL or filename"""
        url_lower = image_url.lower()
        
        # Category detection based on URL patterns (order matters - most specific first)
        category_patterns = {
            'jewelry': ['jewelry', 'necklace', 'bracelet', 'ring', 'earring', 'pendant', 'silver', 'gold'],
            'pet_accessories': ['pet', 'dog', 'cat', 'collar', 'leash', 'toy'],
            'home_decor': ['decor', 'home', 'wall', 'furniture', 'vintage', 'rustic'],
            'art': ['art', 'print', 'poster', 'painting', 'canvas', 'illustration'],
            'crafts': ['craft', 'diy', 'knit', 'fabric', 'paper', 'handmade']
        }
        
        # Check each category in order
        for category, patterns in category_patterns.items():
            if any(pattern in url_lower for pattern in patterns):
                return category
        
        # Default fallback based on common Etsy categories
        return random.choice(['jewelry', 'home_decor', 'crafts'])
    
    def _calculate_sentiment_score(self, text: str, pos_count: int, neg_count: int, neu_count: int) -> float:
        """Calculate sentiment score with advanced logic"""
        # Base score from word counts
        base_score = (pos_count - neg_count) / max(1, len(text.split()))
        
        # Adjust for intensity words
        intensity_multipliers = {
            'very': 1.3, 'extremely': 1.5, 'absolutely': 1.4, 'completely': 1.4,
            'totally': 1.3, 'really': 1.2, 'quite': 1.1, 'pretty': 1.1
        }
        
        multiplier = 1.0
        for word, mult in intensity_multipliers.items():
            if word in text:
                multiplier = max(multiplier, mult)
        
        # Adjust for negation words
        negation_words = ['not', 'never', 'no', 'none', 'neither', 'nothing', "don't", "won't", "can't"]
        if any(neg_word in text for neg_word in negation_words):
            base_score *= -0.8  # Flip and reduce intensity
        
        return base_score * multiplier
    
    def _extract_key_phrases(self, text: str) -> List[str]:
        """Extract key phrases from text"""
        # Simple key phrase extraction
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Common important words in product reviews
        key_words = []
        important_patterns = [
            'quality', 'price', 'shipping', 'delivery', 'customer service', 'material',
            'design', 'color', 'size', 'fit', 'comfort', 'durability', 'value', 'recommend'
        ]
        
        for word in words:
            if word in important_patterns and word not in key_words:
                key_words.append(word)
        
        # Add some contextual phrases
        phrases = []
        if 'good quality' in text.lower():
            phrases.append('good quality')
        if 'fast shipping' in text.lower():
            phrases.append('fast shipping')
        if 'great value' in text.lower():
            phrases.append('great value')
        
        return key_words[:5] + phrases[:3]  # Limit results

# Global simulator instance
azure_simulator = AzureAISimulator()