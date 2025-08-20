#!/usr/bin/env python3
"""
📊 Real-time Data Analysis Engine for Niche Compass
==================================================
This engine provides real-time analytics, insights, and data processing
"""

import os
import json
import time
import threading
from datetime import datetime, timedelta
from dotenv import load_dotenv
import random

class RealtimeAnalysisEngine:
    """Real-time data analysis engine"""
    
    def __init__(self):
        self.load_dotenv()
        self.running = False
        self.data_streams = {}
        self.insights = []
        self.analytics_cache = {}
        self.update_interval = 30  # seconds
        
    def load_dotenv(self):
        """Load environment variables"""
        load_dotenv()
    
    def start_engine(self):
        """Start the real-time analysis engine"""
        print("🚀 Starting Real-time Data Analysis Engine...")
        print("=" * 60)
        
        self.running = True
        
        # Initialize data streams
        self.initialize_data_streams()
        
        # Start analysis threads
        self.start_analysis_threads()
        
        print("✅ Real-time analysis engine started!")
        print("📊 Data streams active:")
        for stream_name in self.data_streams.keys():
            print(f"   - {stream_name}")
        
        print(f"\n🔄 Update interval: {self.update_interval} seconds")
        print("🛑 Press Ctrl+C to stop")
        
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop_engine()
    
    def stop_engine(self):
        """Stop the real-time analysis engine"""
        print("\n🛑 Stopping Real-time Analysis Engine...")
        self.running = False
        
        # Stop all threads
        for thread in threading.enumerate():
            if thread.name.startswith('analysis_'):
                thread.join(timeout=1)
        
        print("✅ Engine stopped")
    
    def initialize_data_streams(self):
        """Initialize data streams for real-time analysis"""
        self.data_streams = {
            'market_pulse': {
                'data': [],
                'last_update': datetime.now(),
                'trend': 'stable',
                'confidence': 0.85
            },
            'keyword_trends': {
                'data': [],
                'last_update': datetime.now(),
                'trend': 'rising',
                'confidence': 0.78
            },
            'niche_analysis': {
                'data': [],
                'last_update': datetime.now(),
                'trend': 'stable',
                'confidence': 0.92
            },
            'product_insights': {
                'data': [],
                'last_update': datetime.now(),
                'trend': 'rising',
                'confidence': 0.81
            },
            'competitor_analysis': {
                'data': [],
                'last_update': datetime.now(),
                'trend': 'stable',
                'confidence': 0.88
            }
        }
    
    def start_analysis_threads(self):
        """Start analysis threads for each data stream"""
        for stream_name in self.data_streams.keys():
            thread = threading.Thread(
                target=self.analyze_data_stream,
                args=(stream_name,),
                name=f'analysis_{stream_name}',
                daemon=True
            )
            thread.start()
    
    def analyze_data_stream(self, stream_name):
        """Analyze a specific data stream in real-time"""
        while self.running:
            try:
                # Generate simulated real-time data
                data = self.generate_stream_data(stream_name)
                
                # Update data stream
                self.data_streams[stream_name]['data'].append(data)
                self.data_streams[stream_name]['last_update'] = datetime.now()
                
                # Keep only last 100 data points
                if len(self.data_streams[stream_name]['data']) > 100:
                    self.data_streams[stream_name]['data'] = self.data_streams[stream_name]['data'][-100:]
                
                # Analyze trends
                self.analyze_trends(stream_name)
                
                # Generate insights
                self.generate_insights(stream_name, data)
                
                # Update cache
                self.update_analytics_cache(stream_name)
                
                time.sleep(self.update_interval)
                
            except Exception as e:
                print(f"❌ Error in {stream_name} analysis: {e}")
                time.sleep(5)
    
    def generate_stream_data(self, stream_name):
        """Generate simulated real-time data for a stream"""
        timestamp = datetime.now()
        
        if stream_name == 'market_pulse':
            # Market pulse: 0-100 scale
            base_value = 75
            variation = random.uniform(-5, 5)
            value = max(0, min(100, base_value + variation))
            
            return {
                'timestamp': timestamp.isoformat(),
                'value': round(value, 2),
                'metric': 'market_pulse_score',
                'category': 'market_overview'
            }
        
        elif stream_name == 'keyword_trends':
            # Keyword trends: search volume and competition
            search_volume = random.randint(1000, 10000)
            competition = random.uniform(0.3, 0.8)
            trend_score = random.uniform(0.4, 0.9)
            
            return {
                'timestamp': timestamp.isoformat(),
                'search_volume': search_volume,
                'competition': round(competition, 3),
                'trend_score': round(trend_score, 3),
                'metric': 'keyword_analysis',
                'category': 'search_trends'
            }
        
        elif stream_name == 'niche_analysis':
            # Niche analysis: profitability and growth potential
            profitability = random.uniform(0.6, 0.95)
            growth_potential = random.uniform(0.5, 0.9)
            market_size = random.randint(100000, 5000000)
            
            return {
                'timestamp': timestamp.isoformat(),
                'profitability': round(profitability, 3),
                'growth_potential': round(growth_potential, 3),
                'market_size': market_size,
                'metric': 'niche_viability',
                'category': 'market_opportunity'
            }
        
        elif stream_name == 'product_insights':
            # Product insights: performance and demand
            performance_score = random.uniform(0.5, 0.95)
            demand_level = random.uniform(0.4, 0.9)
            price_competitiveness = random.uniform(0.6, 0.95)
            
            return {
                'timestamp': timestamp.isoformat(),
                'performance_score': round(performance_score, 3),
                'demand_level': round(demand_level, 3),
                'price_competitiveness': round(price_competitiveness, 3),
                'metric': 'product_analysis',
                'category': 'product_performance'
            }
        
        elif stream_name == 'competitor_analysis':
            # Competitor analysis: market position and threats
            market_position = random.uniform(0.3, 0.9)
            threat_level = random.uniform(0.1, 0.7)
            competitive_advantage = random.uniform(0.4, 0.9)
            
            return {
                'timestamp': timestamp.isoformat(),
                'market_position': round(market_position, 3),
                'threat_level': round(threat_level, 3),
                'competitive_advantage': round(competitive_advantage, 3),
                'metric': 'competitor_analysis',
                'category': 'competitive_intelligence'
            }
        
        return {
            'timestamp': timestamp.isoformat(),
            'value': random.random(),
            'metric': 'unknown',
            'category': 'general'
        }
    
    def analyze_trends(self, stream_name):
        """Analyze trends in a data stream"""
        stream = self.data_streams[stream_name]
        data = stream['data']
        
        if len(data) < 3:
            return
        
        # Simple trend analysis
        recent_values = [d.get('value', 0) for d in data[-3:] if 'value' in d]
        if len(recent_values) >= 3:
            if recent_values[-1] > recent_values[0]:
                stream['trend'] = 'rising'
            elif recent_values[-1] < recent_values[0]:
                stream['trend'] = 'falling'
            else:
                stream['trend'] = 'stable'
            
            # Update confidence based on data consistency
            variance = sum((v - sum(recent_values)/len(recent_values))**2 for v in recent_values) / len(recent_values)
            stream['confidence'] = max(0.5, 1.0 - variance)
    
    def generate_insights(self, stream_name, data):
        """Generate insights from data"""
        timestamp = datetime.now()
        
        # Generate insights based on data patterns
        if stream_name == 'market_pulse':
            value = data.get('value', 0)
            if value > 80:
                insight = {
                    'timestamp': timestamp.isoformat(),
                    'type': 'market_opportunity',
                    'message': f"Market pulse is high ({value}%) - Great time for new product launches",
                    'priority': 'high',
                    'stream': stream_name
                }
                self.insights.append(insight)
            elif value < 40:
                insight = {
                    'timestamp': timestamp.isoformat(),
                    'type': 'market_warning',
                    'message': f"Market pulse is low ({value}%) - Consider market research",
                    'priority': 'medium',
                    'stream': stream_name
                }
                self.insights.append(insight)
        
        elif stream_name == 'keyword_trends':
            trend_score = data.get('trend_score', 0)
            if trend_score > 0.8:
                insight = {
                    'timestamp': timestamp.isoformat(),
                    'type': 'trend_opportunity',
                    'message': f"Keyword trend score is excellent ({trend_score}) - High potential keywords detected",
                    'priority': 'high',
                    'stream': stream_name
                }
                self.insights.append(insight)
        
        # Keep only last 50 insights
        if len(self.insights) > 50:
            self.insights = self.insights[-50:]
    
    def update_analytics_cache(self, stream_name):
        """Update analytics cache with latest data"""
        stream = self.data_streams[stream_name]
        
        if not stream['data']:
            return
        
        # Calculate summary statistics
        latest_data = stream['data'][-1]
        
        cache_entry = {
            'last_update': stream['last_update'].isoformat(),
            'trend': stream['trend'],
            'confidence': stream['confidence'],
            'latest_data': latest_data,
            'data_points': len(stream['data'])
        }
        
        self.analytics_cache[stream_name] = cache_entry
    
    def get_realtime_dashboard(self):
        """Get real-time dashboard data"""
        dashboard = {
            'timestamp': datetime.now().isoformat(),
            'engine_status': 'running' if self.running else 'stopped',
            'data_streams': {},
            'insights': self.insights[-10:],  # Last 10 insights
            'summary': {}
        }
        
        # Add data stream summaries
        for stream_name, stream in self.data_streams.items():
            dashboard['data_streams'][stream_name] = {
                'status': 'active',
                'last_update': stream['last_update'].isoformat(),
                'trend': stream['trend'],
                'confidence': stream['confidence'],
                'data_points': len(stream['data'])
            }
        
        # Calculate overall summary
        total_data_points = sum(len(stream['data']) for stream in self.data_streams.values())
        active_streams = sum(1 for stream in self.data_streams.values() if stream['data'])
        
        dashboard['summary'] = {
            'total_data_points': total_data_points,
            'active_streams': active_streams,
            'total_streams': len(self.data_streams),
            'engine_uptime': self.get_uptime()
        }
        
        return dashboard
    
    def get_uptime(self):
        """Get engine uptime"""
        if not hasattr(self, 'start_time'):
            return "0:00:00"
        
        uptime = datetime.now() - self.start_time
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    
    def export_analytics(self, format='json'):
        """Export analytics data"""
        if format == 'json':
            export_data = {
                'export_timestamp': datetime.now().isoformat(),
                'data_streams': self.data_streams,
                'insights': self.insights,
                'analytics_cache': self.analytics_cache
            }
            
            filename = f"analytics_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            return filename
        
        return None

def main():
    """Main function"""
    try:
        engine = RealtimeAnalysisEngine()
        engine.start_time = datetime.now()
        engine.start_engine()
    except KeyboardInterrupt:
        print("\n🛑 Engine stopped by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")

if __name__ == "__main__":
    main()
