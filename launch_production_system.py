#!/usr/bin/env python3
"""
🚀 Production System Launcher for Niche Compass
==============================================
This script launches the complete production system with all features:
- Real-time data analysis engine
- Production monitoring
- Production server
- AI insights engine
"""

import os
import sys
import time
import subprocess
import threading
from datetime import datetime
from dotenv import load_dotenv

class ProductionSystemLauncher:
    """Production system launcher"""
    
    def __init__(self):
        self.load_dotenv()
        self.processes = {}
        self.threads = {}
        self.running = False
        
    def load_dotenv(self):
        """Load environment variables"""
        load_dotenv()
    
    def launch_production_system(self):
        """Launch the complete production system"""
        print("🚀 Launching Niche Compass Production System...")
        print("=" * 70)
        
        # Check production readiness
        if not self.check_production_readiness():
            print("❌ Production system not ready. Please run activate_production_features.py first")
            return False
        
        print("✅ Production system ready!")
        print("\n🚀 Starting production components...")
        
        self.running = True
        
        try:
            # 1. Start Real-time Analysis Engine
            print("\n📊 1. Starting Real-time Analysis Engine...")
            self.start_realtime_engine()
            
            # 2. Start Production Monitoring
            print("\n📊 2. Starting Production Monitoring...")
            self.start_production_monitoring()
            
            # 3. Start Production Server
            print("\n⚙️  3. Starting Production Server...")
            self.start_production_server()
            
            # 4. Start AI Insights Engine
            print("\n🤖 4. Starting AI Insights Engine...")
            self.start_ai_insights_engine()
            
            print("\n🎉 All production components started successfully!")
            print("=" * 70)
            
            # Display system status
            self.display_system_status()
            
            # Keep system running
            self.keep_system_running()
            
        except KeyboardInterrupt:
            self.shutdown_production_system()
        except Exception as e:
            print(f"\n❌ Error launching production system: {e}")
            self.shutdown_production_system()
        
        return True
    
    def check_production_readiness(self):
        """Check if production system is ready"""
        print("🔍 Checking production readiness...")
        
        # Check config files
        required_configs = [
            'config/production_config.json',
            'config/realtime_analytics.json',
            'config/ai_insights.json',
            'config/production_traffic.json',
            'config/scalable_operations.json'
        ]
        
        missing_configs = [config for config in required_configs if not os.path.exists(config)]
        if missing_configs:
            print(f"❌ Missing config files: {', '.join(missing_configs)}")
            return False
        
        # Check environment variables
        required_env_vars = [
            'COSMOS_DB_CONNECTION_STRING',
            'AZURE_COMPUTER_VISION_ENDPOINT',
            'AZURE_COMPUTER_VISION_KEY',
            'AZURE_TEXT_ANALYTICS_ENDPOINT',
            'AZURE_TEXT_ANALYTICS_KEY'
        ]
        
        missing_env_vars = [var for var in required_env_vars if not os.getenv(var)]
        if missing_env_vars:
            print(f"❌ Missing environment variables: {', '.join(missing_env_vars)}")
            return False
        
        print("✅ Production system ready!")
        return True
    
    def start_realtime_engine(self):
        """Start real-time analysis engine"""
        try:
            # Start real-time engine in background
            process = subprocess.Popen([
                sys.executable, 'realtime_analysis_engine.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            self.processes['realtime_engine'] = process
            print("   ✅ Real-time analysis engine started")
            
            # Wait a moment for engine to initialize
            time.sleep(3)
            
        except Exception as e:
            print(f"   ❌ Failed to start real-time engine: {e}")
    
    def start_production_monitoring(self):
        """Start production monitoring"""
        try:
            # Start monitoring in background
            process = subprocess.Popen([
                sys.executable, 'monitor_production.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            self.processes['monitoring'] = process
            print("   ✅ Production monitoring started")
            
        except Exception as e:
            print(f"   ❌ Failed to start monitoring: {e}")
    
    def start_production_server(self):
        """Start production server"""
        try:
            # Start Flask server in background
            process = subprocess.Popen([
                sys.executable, 'backend/src/main.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            self.processes['production_server'] = process
            print("   ✅ Production server started")
            
            # Wait for server to start
            time.sleep(5)
            
        except Exception as e:
            print(f"   ❌ Failed to start production server: {e}")
    
    def start_ai_insights_engine(self):
        """Start AI insights engine"""
        try:
            # Start AI insights engine in background
            process = subprocess.Popen([
                sys.executable, 'ai_insights_engine.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            self.processes['ai_insights'] = process
            print("   ✅ AI insights engine started")
            
        except Exception as e:
            print(f"   ❌ Failed to start AI insights engine: {e}")
    
    def display_system_status(self):
        """Display current system status"""
        print("\n📊 PRODUCTION SYSTEM STATUS")
        print("=" * 50)
        
        for component, process in self.processes.items():
            if process.poll() is None:
                print(f"✅ {component.replace('_', ' ').title()}: Running (PID: {process.pid})")
            else:
                print(f"❌ {component.replace('_', ' ').title()}: Stopped")
        
        print("\n🌐 Access Points:")
        print("   Backend API: http://localhost:5000")
        print("   Health Check: http://localhost:5000/health")
        print("   Real-time Analytics: http://localhost:5000/analytics")
        print("   AI Insights: http://localhost:5000/ai-insights")
        
        print("\n📊 Monitoring:")
        print("   System Monitor: python monitor_production.py")
        print("   Real-time Engine: python realtime_analysis_engine.py")
        
        print("\n🛑 To stop: Press Ctrl+C")
    
    def keep_system_running(self):
        """Keep the production system running"""
        try:
            while self.running:
                # Check if all processes are still running
                for component, process in self.processes.items():
                    if process.poll() is not None:
                        print(f"⚠️  {component} has stopped unexpectedly")
                        # Restart component
                        self.restart_component(component)
                
                time.sleep(10)
                
        except KeyboardInterrupt:
            print("\n🛑 Shutdown requested by user")
            self.shutdown_production_system()
    
    def restart_component(self, component):
        """Restart a failed component"""
        print(f"🔄 Restarting {component}...")
        
        try:
            if component == 'realtime_engine':
                self.start_realtime_engine()
            elif component == 'monitoring':
                self.start_production_monitoring()
            elif component == 'production_server':
                self.start_production_server()
            elif component == 'ai_insights':
                self.start_ai_insights_engine()
                
        except Exception as e:
            print(f"❌ Failed to restart {component}: {e}")
    
    def shutdown_production_system(self):
        """Shutdown the production system"""
        print("\n🛑 Shutting down production system...")
        
        self.running = False
        
        # Stop all processes
        for component, process in self.processes.items():
            try:
                print(f"🛑 Stopping {component}...")
                process.terminate()
                process.wait(timeout=5)
                print(f"✅ {component} stopped")
            except subprocess.TimeoutExpired:
                print(f"⚠️  Force killing {component}...")
                process.kill()
            except Exception as e:
                print(f"❌ Error stopping {component}: {e}")
        
        # Stop all threads
        for thread_name, thread in self.threads.items():
            try:
                if thread.is_alive():
                    thread.join(timeout=1)
            except Exception as e:
                print(f"❌ Error stopping thread {thread_name}: {e}")
        
        print("✅ Production system shutdown complete")
    
    def get_system_health(self):
        """Get overall system health status"""
        health_status = {
            'timestamp': datetime.now().isoformat(),
            'overall_status': 'healthy',
            'components': {},
            'alerts': []
        }
        
        for component, process in self.processes.items():
            if process.poll() is None:
                health_status['components'][component] = {
                    'status': 'running',
                    'pid': process.pid
                }
            else:
                health_status['components'][component] = {
                    'status': 'stopped',
                    'pid': None
                }
                health_status['alerts'].append(f"{component} is not running")
                health_status['overall_status'] = 'degraded'
        
        if health_status['overall_status'] == 'degraded':
            health_status['overall_status'] = 'unhealthy'
        
        return health_status

def main():
    """Main function"""
    try:
        launcher = ProductionSystemLauncher()
        launcher.launch_production_system()
    except KeyboardInterrupt:
        print("\n🛑 Launcher stopped by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")

if __name__ == "__main__":
    main()
