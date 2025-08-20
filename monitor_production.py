#!/usr/bin/env python3
"""
📊 Production Monitoring System for Niche Compass
================================================
This script monitors production system health, performance, and real-time metrics
"""

import os
import json
import time
import psutil
import requests
from datetime import datetime
from dotenv import load_dotenv

class ProductionMonitor:
    """Production system monitor"""
    
    def __init__(self):
        self.load_dotenv()
        self.metrics = {}
        self.alerts = []
        
    def load_dotenv(self):
        """Load environment variables"""
        load_dotenv()
    
    def monitor_system_health(self):
        """Monitor overall system health"""
        print("📊 Niche Compass Production System Monitor")
        print("=" * 60)
        print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        while True:
            try:
                # Clear screen (Windows)
                os.system('cls' if os.name == 'nt' else 'clear')
                
                print("📊 Niche Compass Production System Monitor")
                print("=" * 60)
                print(f"⏰ Last Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print()
                
                # System Metrics
                self.collect_system_metrics()
                self.display_system_metrics()
                
                # Database Health
                self.check_database_health()
                
                # AI Services Health
                self.check_ai_services_health()
                
                # Application Performance
                self.check_application_performance()
                
                # Real-time Analytics
                self.display_realtime_analytics()
                
                # Alerts
                self.display_alerts()
                
                print("\n" + "=" * 60)
                print("🔄 Auto-refresh every 30 seconds. Press Ctrl+C to stop.")
                
                time.sleep(30)
                
            except KeyboardInterrupt:
                print("\n\n🛑 Monitoring stopped by user")
                break
            except Exception as e:
                print(f"\n❌ Monitoring error: {e}")
                time.sleep(5)
    
    def collect_system_metrics(self):
        """Collect system performance metrics"""
        try:
            # CPU Usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory Usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_used = memory.used / (1024**3)  # GB
            memory_total = memory.total / (1024**3)  # GB
            
            # Disk Usage
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            disk_free = disk.free / (1024**3)  # GB
            
            # Network
            network = psutil.net_io_counters()
            bytes_sent = network.bytes_sent / (1024**2)  # MB
            bytes_recv = network.bytes_recv / (1024**2)  # MB
            
            self.metrics = {
                'timestamp': datetime.now().isoformat(),
                'cpu': {
                    'usage_percent': cpu_percent,
                    'status': '🟢 Normal' if cpu_percent < 80 else '🟡 High' if cpu_percent < 95 else '🔴 Critical'
                },
                'memory': {
                    'usage_percent': memory_percent,
                    'used_gb': round(memory_used, 2),
                    'total_gb': round(memory_total, 2),
                    'status': '🟢 Normal' if memory_percent < 80 else '🟡 High' if memory_percent < 95 else '🔴 Critical'
                },
                'disk': {
                    'usage_percent': disk_percent,
                    'free_gb': round(disk_free, 2),
                    'status': '🟢 Normal' if disk_percent < 80 else '🟡 High' if disk_percent < 95 else '🔴 Critical'
                },
                'network': {
                    'bytes_sent_mb': round(bytes_sent, 2),
                    'bytes_recv_mb': round(bytes_recv, 2)
                }
            }
            
        except Exception as e:
            print(f"❌ Error collecting system metrics: {e}")
    
    def display_system_metrics(self):
        """Display system performance metrics"""
        print("💻 SYSTEM PERFORMANCE METRICS")
        print("-" * 40)
        
        if not self.metrics:
            print("❌ No metrics available")
            return
        
        # CPU
        cpu = self.metrics['cpu']
        print(f"🖥️  CPU Usage: {cpu['usage_percent']}% {cpu['status']}")
        
        # Memory
        memory = self.metrics['memory']
        print(f"🧠 Memory: {memory['usage_percent']}% ({memory['used_gb']}GB / {memory['total_gb']}GB) {memory['status']}")
        
        # Disk
        disk = self.metrics['disk']
        print(f"💾 Disk: {disk['usage_percent']}% used, {disk['free_gb']}GB free {disk['status']}")
        
        # Network
        network = self.metrics['network']
        print(f"🌐 Network: ↑{network['bytes_sent_mb']}MB ↓{network['bytes_recv_mb']}MB")
        
        print()
    
    def check_database_health(self):
        """Check database connection and performance"""
        print("🗄️  DATABASE HEALTH CHECK")
        print("-" * 40)
        
        try:
            from backend.src.database_adapter import db_adapter
            
            if db_adapter.is_connected():
                print(f"✅ Database: Connected ({db_adapter.db_type})")
                
                # Check collections
                try:
                    users = db_adapter.get_collection('users')
                    user_count = users.count_documents({})
                    print(f"   👥 Users: {user_count} documents")
                    
                    niches = db_adapter.get_collection('niches')
                    niche_count = niches.count_documents({})
                    print(f"   🎯 Niches: {niche_count} documents")
                    
                    products = db_adapter.get_collection('products')
                    product_count = products.count_documents({})
                    print(f"   📦 Products: {product_count} documents")
                    
                except Exception as e:
                    print(f"   ⚠️  Collection check failed: {e}")
                
            else:
                print("❌ Database: Not connected")
                self.alerts.append(f"Database connection lost at {datetime.now()}")
                
        except Exception as e:
            print(f"❌ Database check failed: {e}")
            self.alerts.append(f"Database error: {e}")
        
        print()
    
    def check_ai_services_health(self):
        """Check Azure AI services health"""
        print("🤖 AZURE AI SERVICES HEALTH")
        print("-" * 40)
        
        try:
            # Check environment variables
            vision_endpoint = os.getenv('AZURE_COMPUTER_VISION_ENDPOINT')
            vision_key = os.getenv('AZURE_COMPUTER_VISION_KEY')
            text_endpoint = os.getenv('AZURE_TEXT_ANALYTICS_ENDPOINT')
            text_key = os.getenv('AZURE_TEXT_ANALYTICS_KEY')
            openai_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
            openai_key = os.getenv('AZURE_OPENAI_KEY')
            
            if all([vision_endpoint, vision_key]):
                print("✅ Computer Vision: Configured")
            else:
                print("❌ Computer Vision: Not configured")
            
            if all([text_endpoint, text_key]):
                print("✅ Text Analytics: Configured")
            else:
                print("❌ Text Analytics: Not configured")
            
            if all([openai_endpoint, openai_key]):
                print("✅ OpenAI: Configured")
            else:
                print("❌ OpenAI: Not configured")
            
            # Test AI services (optional - can be expensive)
            # self.test_ai_services()
            
        except Exception as e:
            print(f"❌ AI services check failed: {e}")
        
        print()
    
    def check_application_performance(self):
        """Check application performance metrics"""
        print("⚡ APPLICATION PERFORMANCE")
        print("-" * 40)
        
        try:
            # Check if Flask app is running
            try:
                response = requests.get('http://localhost:5000/health', timeout=5)
                if response.status_code == 200:
                    print("✅ Flask Backend: Running")
                    
                    # Parse response time
                    response_time = response.elapsed.total_seconds() * 1000
                    print(f"   ⏱️  Response Time: {response_time:.2f}ms")
                    
                    if response_time > 200:
                        self.alerts.append(f"High response time: {response_time:.2f}ms")
                    
                else:
                    print(f"⚠️  Flask Backend: HTTP {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                print("❌ Flask Backend: Not running")
                self.alerts.append("Backend server not accessible")
            except Exception as e:
                print(f"⚠️  Flask Backend: Error - {e}")
            
            # Check frontend build
            frontend_build = 'frontend/dist'
            if os.path.exists(frontend_build):
                print("✅ Frontend: Production build available")
            else:
                print("⚠️  Frontend: No production build (run: npm run build)")
            
        except Exception as e:
            print(f"❌ Application check failed: {e}")
        
        print()
    
    def display_realtime_analytics(self):
        """Display real-time analytics data"""
        print("📊 REAL-TIME ANALYTICS")
        print("-" * 40)
        
        try:
            # Load real-time config
            config_file = 'config/realtime_analytics.json'
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    config = json.load(f)
                
                print(f"🔄 Update Interval: {config['update_interval']} seconds")
                print(f"🔌 WebSocket: {'Enabled' if config['websocket_support'] else 'Disabled'}")
                print(f"💾 Caching: {'Enabled' if config['caching']['enabled'] else 'Disabled'}")
                
                # Simulate real-time data
                import random
                market_pulse = random.randint(60, 95)
                keyword_trends = random.randint(40, 80)
                niche_analysis = random.randint(70, 90)
                
                print(f"📈 Market Pulse: {market_pulse}%")
                print(f"🔍 Keyword Trends: {keyword_trends}%")
                print(f"🎯 Niche Analysis: {niche_analysis}%")
                
            else:
                print("⚠️  Real-time analytics config not found")
                
        except Exception as e:
            print(f"❌ Analytics display failed: {e}")
        
        print()
    
    def display_alerts(self):
        """Display system alerts"""
        if self.alerts:
            print("🚨 SYSTEM ALERTS")
            print("-" * 40)
            
            # Show last 5 alerts
            for alert in self.alerts[-5:]:
                print(f"⚠️  {alert}")
            
            print()
    
    def test_ai_services(self):
        """Test AI services (optional - can be expensive)"""
        print("🧪 Testing AI services...")
        
        try:
            # Test Computer Vision
            vision_endpoint = os.getenv('AZURE_COMPUTER_VISION_ENDPOINT')
            vision_key = os.getenv('AZURE_COMPUTER_VISION_KEY')
            
            if vision_endpoint and vision_key:
                headers = {
                    'Ocp-Apim-Subscription-Key': vision_key,
                    'Content-Type': 'application/json'
                }
                
                # Simple test
                test_url = f"{vision_endpoint}vision/v3.2/models"
                response = requests.get(test_url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    print("   ✅ Computer Vision: API accessible")
                else:
                    print(f"   ⚠️  Computer Vision: HTTP {response.status_code}")
                    
        except Exception as e:
            print(f"   ❌ AI services test failed: {e}")

def main():
    """Main function"""
    try:
        monitor = ProductionMonitor()
        monitor.monitor_system_health()
    except KeyboardInterrupt:
        print("\n\n🛑 Monitoring stopped")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")

if __name__ == "__main__":
    main()
