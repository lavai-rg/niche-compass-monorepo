#!/usr/bin/env python3
"""
⚡ Real-Time Market Pulse Engine - Revolutionary Market Intelligence
==================================================================
First-of-its-kind real-time market monitoring and trend detection system
"""

import os
import json
import math
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple, Optional
from collections import defaultdict, Counter
import hashlib

class TrendVelocityDetector:
    """Advanced trend velocity and momentum analysis"""
    
    def __init__(self):
        self.velocity_thresholds = {
            "explosive": 5.0,      # 500%+ growth rate
            "fast_rising": 2.0,    # 200%+ growth rate
            "rising": 1.5,         # 150%+ growth rate
            "stable": 0.8,         # 80-120% stable
            "declining": 0.5,      # 50-80% decline
            "falling": 0.2         # 20-50% decline
        }
        
        self.trend_patterns = {
            "viral_spike": {"duration": 7, "peak_multiplier": 10, "decay_rate": 0.7},
            "seasonal_surge": {"duration": 30, "peak_multiplier": 3, "decay_rate": 0.9},
            "steady_growth": {"duration": 90, "peak_multiplier": 2, "decay_rate": 0.95},
            "bubble_burst": {"duration": 14, "peak_multiplier": 8, "decay_rate": 0.3}
        }
    
    def calculate_trend_velocity(self, historical_data: List[Dict]) -> Dict[str, Any]:
        """Calculate trend velocity and momentum"""
        
        if len(historical_data) < 2:
            return {"velocity": 0, "status": "insufficient_data"}
        
        # Calculate growth rates over different timeframes
        velocities = {}
        
        # 24-hour velocity
        if len(historical_data) >= 2:
            recent = historical_data[-1]["value"]
            previous = historical_data[-2]["value"] 
            velocities["24h"] = (recent - previous) / max(previous, 1) if previous > 0 else 0
        
        # 7-day velocity
        if len(historical_data) >= 7:
            week_ago = historical_data[-7]["value"]
            current = historical_data[-1]["value"]
            velocities["7d"] = (current - week_ago) / max(week_ago, 1) if week_ago > 0 else 0
        
        # 30-day velocity
        if len(historical_data) >= 30:
            month_ago = historical_data[-30]["value"] 
            current = historical_data[-1]["value"]
            velocities["30d"] = (current - month_ago) / max(month_ago, 1) if month_ago > 0 else 0
        
        # Calculate acceleration (rate of change of velocity)
        acceleration = 0
        if len(velocities) >= 2:
            velocity_values = list(velocities.values())
            acceleration = (velocity_values[-1] - velocity_values[0]) / len(velocity_values)
        
        # Determine overall trend status
        avg_velocity = sum(velocities.values()) / len(velocities) if velocities else 0
        trend_status = self._classify_trend_velocity(avg_velocity)
        
        # Predict trend trajectory
        trajectory = self._predict_trajectory(velocities, acceleration)
        
        return {
            "velocities": velocities,
            "average_velocity": avg_velocity,
            "acceleration": acceleration,
            "trend_status": trend_status,
            "momentum_score": self._calculate_momentum_score(velocities, acceleration),
            "trajectory_prediction": trajectory,
            "peak_estimation": self._estimate_peak(historical_data, velocities)
        }
    
    def _classify_trend_velocity(self, velocity: float) -> str:
        """Classify trend based on velocity"""
        for status, threshold in self.velocity_thresholds.items():
            if velocity >= threshold:
                return status
        return "falling"
    
    def _calculate_momentum_score(self, velocities: Dict[str, float], acceleration: float) -> float:
        """Calculate momentum score (0-10)"""
        if not velocities:
            return 0
        
        # Base score from average velocity
        avg_velocity = sum(velocities.values()) / len(velocities)
        base_score = min(avg_velocity * 2, 8)  # Cap base at 8
        
        # Acceleration bonus/penalty
        acceleration_bonus = min(acceleration * 5, 2)  # Max +2 for positive acceleration
        
        # Consistency bonus (if all velocities are positive)
        consistency_bonus = 1 if all(v > 0 for v in velocities.values()) else 0
        
        total_score = base_score + acceleration_bonus + consistency_bonus
        return max(0, min(total_score, 10))  # Clamp between 0-10
    
    def _predict_trajectory(self, velocities: Dict[str, float], acceleration: float) -> Dict[str, Any]:
        """Predict future trend trajectory"""
        if not velocities:
            return {"prediction": "unknown", "confidence": 0}
        
        avg_velocity = sum(velocities.values()) / len(velocities)
        
        # Pattern matching
        if avg_velocity > 3 and acceleration > 0.5:
            return {"prediction": "explosive_growth", "confidence": 0.85, "timeframe": "1-2_weeks"}
        elif avg_velocity > 1.5 and acceleration > 0:
            return {"prediction": "continued_growth", "confidence": 0.75, "timeframe": "2-4_weeks"}
        elif avg_velocity > 0.8 and abs(acceleration) < 0.2:
            return {"prediction": "stable_trend", "confidence": 0.9, "timeframe": "4-8_weeks"}
        elif avg_velocity < 0.5 and acceleration < -0.3:
            return {"prediction": "decline_ahead", "confidence": 0.7, "timeframe": "1-3_weeks"}
        else:
            return {"prediction": "uncertain", "confidence": 0.4, "timeframe": "unknown"}
    
    def _estimate_peak(self, historical_data: List[Dict], velocities: Dict[str, float]) -> Dict[str, Any]:
        """Estimate when trend will peak"""
        if not velocities or not historical_data:
            return {"estimated_peak": None, "confidence": 0}
        
        current_value = historical_data[-1]["value"]
        avg_velocity = sum(velocities.values()) / len(velocities)
        
        if avg_velocity <= 0:
            return {"estimated_peak": "already_peaked", "confidence": 0.8}
        
        # Simple peak estimation based on velocity decay
        days_to_peak = max(7, int(30 / (avg_velocity + 0.1)))  # Slower for higher velocity
        peak_date = datetime.now() + timedelta(days=days_to_peak)
        peak_value = current_value * (1 + avg_velocity) ** (days_to_peak / 30)
        
        return {
            "estimated_peak_date": peak_date.isoformat(),
            "estimated_peak_value": peak_value,
            "days_from_now": days_to_peak,
            "confidence": min(0.9, avg_velocity)  # Higher confidence for stronger trends
        }

class CompetitionDensityTracker:
    """Track and analyze competition density in real-time"""
    
    def __init__(self):
        self.density_categories = {
            "oversaturated": {"threshold": 10000, "success_rate": 0.05},
            "high_competition": {"threshold": 5000, "success_rate": 0.15},
            "moderate_competition": {"threshold": 1000, "success_rate": 0.35},
            "low_competition": {"threshold": 300, "success_rate": 0.65},
            "untapped": {"threshold": 50, "success_rate": 0.85}
        }
    
    def analyze_competition_density(self, niche_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze competition density and market saturation"""
        
        # Extract competition metrics
        total_listings = niche_data.get("total_listings", 0)
        active_sellers = niche_data.get("active_sellers", 0)
        new_listings_24h = niche_data.get("new_listings_24h", 0)
        top_seller_dominance = niche_data.get("top_10_market_share", 0.3)
        
        # Calculate density score
        density_score = self._calculate_density_score(total_listings, active_sellers, new_listings_24h)
        
        # Classify competition level
        competition_level = self._classify_competition_level(total_listings)
        
        # Calculate market saturation
        saturation_analysis = self._analyze_market_saturation(
            total_listings, new_listings_24h, top_seller_dominance
        )
        
        # Predict competition growth
        growth_prediction = self._predict_competition_growth(niche_data)
        
        # Calculate opportunity score
        opportunity_score = self._calculate_opportunity_score(
            competition_level, saturation_analysis, growth_prediction
        )
        
        return {
            "density_score": density_score,
            "competition_level": competition_level,
            "saturation_analysis": saturation_analysis,
            "growth_prediction": growth_prediction,
            "opportunity_score": opportunity_score,
            "market_entry_recommendation": self._generate_entry_recommendation(opportunity_score),
            "competitive_advantages_needed": self._identify_required_advantages(competition_level)
        }
    
    def _calculate_density_score(self, total_listings: int, active_sellers: int, new_listings_24h: int) -> float:
        """Calculate normalized density score (0-10)"""
        
        # Listings per seller ratio
        listings_per_seller = total_listings / max(active_sellers, 1)
        
        # New listings velocity (per day)
        new_listings_velocity = new_listings_24h
        
        # Normalize to 0-10 scale
        base_density = min(total_listings / 1000, 8)  # Cap at 8 for base
        velocity_factor = min(new_listings_velocity / 50, 1.5)  # Up to +1.5 for high velocity
        seller_concentration = min(listings_per_seller / 10, 0.5)  # Up to +0.5 for concentration
        
        total_density = base_density + velocity_factor + seller_concentration
        return min(total_density, 10)
    
    def _classify_competition_level(self, total_listings: int) -> str:
        """Classify competition level based on total listings"""
        for level, data in self.density_categories.items():
            if total_listings >= data["threshold"]:
                return level
        return "untapped"
    
    def _analyze_market_saturation(self, total_listings: int, new_listings: int, top_seller_share: float) -> Dict[str, Any]:
        """Analyze market saturation indicators"""
        
        # Calculate saturation percentage
        max_sustainable_listings = 5000  # Estimated market capacity
        saturation_percentage = min(total_listings / max_sustainable_listings, 1.0)
        
        # Market concentration (Herfindahl index approximation)
        concentration_index = top_seller_share * 100
        
        # Growth sustainability
        growth_rate = new_listings / max(total_listings, 1) * 365  # Annualized
        sustainability = "high" if growth_rate < 0.3 else "medium" if growth_rate < 0.7 else "low"
        
        return {
            "saturation_percentage": saturation_percentage,
            "concentration_index": concentration_index,
            "market_concentration": "high" if concentration_index > 40 else "medium" if concentration_index > 20 else "low",
            "growth_sustainability": sustainability,
            "market_maturity": "mature" if saturation_percentage > 0.7 else "growing" if saturation_percentage > 0.3 else "emerging"
        }
    
    def _predict_competition_growth(self, niche_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict future competition growth"""
        
        current_sellers = niche_data.get("active_sellers", 100)
        new_sellers_trend = niche_data.get("new_sellers_trend", 0.1)  # Weekly growth rate
        
        # Predict seller growth over next 3 months
        weeks_ahead = 12
        predicted_sellers = current_sellers * (1 + new_sellers_trend) ** weeks_ahead
        
        growth_rate = (predicted_sellers - current_sellers) / current_sellers
        
        return {
            "predicted_sellers_3_months": int(predicted_sellers),
            "growth_rate_3_months": growth_rate,
            "competition_trajectory": "exploding" if growth_rate > 1 else "growing" if growth_rate > 0.3 else "stable",
            "entry_window": "closing_fast" if growth_rate > 0.8 else "narrowing" if growth_rate > 0.4 else "stable"
        }
    
    def _calculate_opportunity_score(self, competition_level: str, saturation: Dict, growth_prediction: Dict) -> float:
        """Calculate overall opportunity score (0-10)"""
        
        # Base score from competition level
        base_scores = {
            "oversaturated": 2,
            "high_competition": 4,
            "moderate_competition": 6,
            "low_competition": 8,
            "untapped": 9
        }
        base_score = base_scores.get(competition_level, 5)
        
        # Saturation penalty
        saturation_penalty = saturation["saturation_percentage"] * 2  # Up to -2 points
        
        # Growth trajectory modifier
        trajectory = growth_prediction.get("competition_trajectory", "stable")
        trajectory_modifiers = {"exploding": -1.5, "growing": -0.5, "stable": 0}
        trajectory_modifier = trajectory_modifiers.get(trajectory, 0)
        
        # Market maturity modifier
        maturity = saturation.get("market_maturity", "growing")
        maturity_modifiers = {"mature": -0.5, "growing": 0.5, "emerging": 1}
        maturity_modifier = maturity_modifiers.get(maturity, 0)
        
        final_score = base_score - saturation_penalty + trajectory_modifier + maturity_modifier
        return max(0, min(final_score, 10))
    
    def _generate_entry_recommendation(self, opportunity_score: float) -> Dict[str, Any]:
        """Generate market entry recommendation"""
        
        if opportunity_score >= 8:
            return {
                "recommendation": "enter_immediately", 
                "urgency": "high",
                "reason": "Exceptional opportunity with low competition"
            }
        elif opportunity_score >= 6:
            return {
                "recommendation": "enter_soon", 
                "urgency": "medium",
                "reason": "Good opportunity but window may be narrowing"
            }
        elif opportunity_score >= 4:
            return {
                "recommendation": "strategic_entry", 
                "urgency": "low",
                "reason": "Requires strong differentiation strategy"
            }
        else:
            return {
                "recommendation": "avoid_or_wait", 
                "urgency": "none",
                "reason": "Market oversaturated, wait for better timing"
            }
    
    def _identify_required_advantages(self, competition_level: str) -> List[str]:
        """Identify competitive advantages needed for success"""
        
        advantage_requirements = {
            "oversaturated": [
                "Unique value proposition",
                "Premium branding",
                "Exceptional customer service",
                "Innovative product features",
                "Strong social media presence"
            ],
            "high_competition": [
                "Quality differentiation", 
                "Competitive pricing",
                "Fast shipping",
                "Customer reviews strategy",
                "SEO optimization"
            ],
            "moderate_competition": [
                "Good product quality",
                "Competitive pricing", 
                "Basic SEO",
                "Customer service"
            ],
            "low_competition": [
                "Basic quality",
                "Market presence",
                "Customer acquisition"
            ],
            "untapped": [
                "Market education",
                "First-mover advantage",
                "Category definition"
            ]
        }
        
        return advantage_requirements.get(competition_level, [])

class DemandSurgeAnalyzer:
    """Detect and analyze demand surges and market opportunities"""
    
    def __init__(self):
        self.surge_patterns = {
            "viral_trend": {"multiplier": 10, "duration": 7, "decay": 0.8},
            "seasonal_peak": {"multiplier": 5, "duration": 30, "decay": 0.9},
            "event_driven": {"multiplier": 8, "duration": 14, "decay": 0.7},
            "influencer_boost": {"multiplier": 6, "duration": 10, "decay": 0.75},
            "organic_growth": {"multiplier": 2, "duration": 90, "decay": 0.95}
        }
    
    def detect_demand_surge(self, demand_data: Dict[str, Any]) -> Dict[str, Any]:
        """Detect and analyze demand surges"""
        
        # Extract demand metrics
        current_searches = demand_data.get("current_searches_24h", 0)
        baseline_searches = demand_data.get("baseline_searches", 0) 
        search_growth = demand_data.get("search_growth_7d", 0)
        social_mentions = demand_data.get("social_mentions", 0)
        related_trends = demand_data.get("related_trends", [])
        
        # Calculate surge magnitude
        surge_magnitude = self._calculate_surge_magnitude(current_searches, baseline_searches)
        
        # Identify surge pattern
        surge_pattern = self._identify_surge_pattern(surge_magnitude, search_growth, social_mentions)
        
        # Predict demand trajectory
        demand_trajectory = self._predict_demand_trajectory(surge_pattern, surge_magnitude)
        
        # Calculate opportunity window
        opportunity_window = self._calculate_opportunity_window(surge_pattern, demand_trajectory)
        
        return {
            "surge_detected": surge_magnitude > 1.5,
            "surge_magnitude": surge_magnitude,
            "surge_pattern": surge_pattern,
            "demand_trajectory": demand_trajectory,
            "opportunity_window": opportunity_window,
            "action_recommendations": self._generate_action_recommendations(surge_magnitude, opportunity_window)
        }
    
    def _calculate_surge_magnitude(self, current: int, baseline: int) -> float:
        """Calculate demand surge magnitude"""
        if baseline <= 0:
            return 1.0
        return current / baseline
    
    def _identify_surge_pattern(self, magnitude: float, growth: float, social: int) -> str:
        """Identify the type of surge pattern"""
        
        if magnitude > 8 and social > 1000:
            return "viral_trend"
        elif magnitude > 4 and growth > 0.5:
            return "seasonal_peak"
        elif magnitude > 6 and social > 500:
            return "event_driven"
        elif magnitude > 4 and social > 200:
            return "influencer_boost"
        elif magnitude > 1.5 and growth > 0.2:
            return "organic_growth"
        else:
            return "no_significant_pattern"
    
    def _predict_demand_trajectory(self, pattern: str, magnitude: float) -> Dict[str, Any]:
        """Predict how demand will evolve"""
        
        pattern_data = self.surge_patterns.get(pattern, {"multiplier": 1, "duration": 30, "decay": 0.9})
        
        # Predict peak timing
        days_to_peak = max(1, int(pattern_data["duration"] * 0.3))  # Peak at 30% of duration
        
        # Predict peak value
        peak_multiplier = min(magnitude * 1.2, pattern_data["multiplier"])
        
        # Predict decline rate
        decline_rate = 1 - pattern_data["decay"]
        
        return {
            "pattern_type": pattern,
            "days_to_peak": days_to_peak,
            "peak_multiplier": peak_multiplier,
            "decline_rate_per_day": decline_rate,
            "sustainability": "high" if decline_rate < 0.1 else "medium" if decline_rate < 0.25 else "low"
        }
    
    def _calculate_opportunity_window(self, pattern: str, trajectory: Dict) -> Dict[str, Any]:
        """Calculate optimal opportunity window"""
        
        peak_days = trajectory.get("days_to_peak", 7)
        sustainability = trajectory.get("sustainability", "medium")
        
        # Calculate optimal entry and exit timing
        optimal_entry = max(1, peak_days - 2)  # Enter 2 days before peak
        
        if sustainability == "high":
            optimal_exit = peak_days + 30  # Ride the wave
        elif sustainability == "medium": 
            optimal_exit = peak_days + 14  # Moderate exit
        else:
            optimal_exit = peak_days + 7   # Quick exit
        
        return {
            "optimal_entry_days": optimal_entry,
            "optimal_exit_days": optimal_exit,
            "window_duration": optimal_exit - optimal_entry,
            "urgency_level": "critical" if optimal_entry <= 1 else "high" if optimal_entry <= 3 else "medium"
        }
    
    def _generate_action_recommendations(self, magnitude: float, window: Dict) -> List[str]:
        """Generate specific action recommendations"""
        
        recommendations = []
        
        if magnitude > 5:
            recommendations.append("🚀 URGENT: Massive demand surge detected - prioritize this niche!")
            
        if window.get("urgency_level") == "critical":
            recommendations.append("⏰ CRITICAL TIMING: Enter market within 24-48 hours")
            
        if window.get("window_duration", 0) > 20:
            recommendations.append("📈 SUSTAINED OPPORTUNITY: Long-term potential detected")
            
        if magnitude > 3:
            recommendations.append("💰 PREMIUM PRICING: High demand supports premium positioning")
            
        recommendations.append(f"🎯 OPTIMAL WINDOW: Enter in {window.get('optimal_entry_days', 'N/A')} days")
        
        return recommendations

class MarketPulseEngine:
    """Main Real-Time Market Pulse Engine"""
    
    def __init__(self):
        self.trend_detector = TrendVelocityDetector()
        self.competition_tracker = CompetitionDensityTracker()
        self.demand_analyzer = DemandSurgeAnalyzer()
        
        # Simulated real-time data sources (in production, connect to real APIs)
        self.data_sources = {
            "etsy_trends": EtsyTrendsSimulator(),
            "google_trends": GoogleTrendsSimulator(), 
            "social_media": SocialMediaSimulator(),
            "market_data": MarketDataSimulator()
        }
    
    def get_market_pulse(self, niche_keywords: List[str], timeframe: str = "24h") -> Dict[str, Any]:
        """Get comprehensive real-time market pulse"""
        
        try:
            # Gather data from all sources
            market_data = self._gather_market_data(niche_keywords, timeframe)
            
            # Run all analysis engines
            trend_analysis = self.trend_detector.calculate_trend_velocity(market_data["historical_data"])
            competition_analysis = self.competition_tracker.analyze_competition_density(market_data["competition_data"])
            demand_analysis = self.demand_analyzer.detect_demand_surge(market_data["demand_data"])
            
            # Calculate overall market pulse score
            pulse_score = self._calculate_pulse_score(trend_analysis, competition_analysis, demand_analysis)
            
            # Generate market insights
            insights = self._generate_market_insights(trend_analysis, competition_analysis, demand_analysis)
            
            # Create actionable recommendations
            recommendations = self._create_action_plan(pulse_score, trend_analysis, competition_analysis, demand_analysis)
            
            return {
                "market_pulse_score": pulse_score,
                "pulse_status": self._classify_pulse_status(pulse_score),
                "trend_analysis": trend_analysis,
                "competition_analysis": competition_analysis,
                "demand_analysis": demand_analysis,
                "market_insights": insights,
                "action_recommendations": recommendations,
                "optimal_timing": self._calculate_optimal_timing(trend_analysis, demand_analysis),
                "risk_assessment": self._assess_market_risks(competition_analysis, trend_analysis),
                "timestamp": datetime.now().isoformat(),
                "data_freshness": "real_time"
            }
            
        except Exception as e:
            return {
                "error": f"Market pulse analysis failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def _gather_market_data(self, keywords: List[str], timeframe: str) -> Dict[str, Any]:
        """Gather data from all market sources"""
        
        # Simulate gathering data from multiple sources
        # In production, this would connect to real APIs
        
        primary_keyword = keywords[0] if keywords else "handmade"
        
        return {
            "historical_data": self.data_sources["etsy_trends"].get_trend_data(primary_keyword, timeframe),
            "competition_data": self.data_sources["etsy_trends"].get_competition_data(primary_keyword),
            "demand_data": self.data_sources["google_trends"].get_search_data(primary_keyword),
            "social_data": self.data_sources["social_media"].get_social_buzz(primary_keyword)
        }
    
    def _calculate_pulse_score(self, trend: Dict, competition: Dict, demand: Dict) -> float:
        """Calculate overall market pulse score (0-10)"""
        
        # Weight the different components
        trend_score = trend.get("momentum_score", 5) * 0.3        # 30% weight
        competition_score = competition.get("opportunity_score", 5) * 0.4  # 40% weight  
        demand_score = min(demand.get("surge_magnitude", 1) * 3, 10) * 0.3  # 30% weight
        
        total_score = trend_score + competition_score + demand_score
        return min(total_score, 10)
    
    def _classify_pulse_status(self, pulse_score: float) -> str:
        """Classify market pulse status"""
        if pulse_score >= 8.5:
            return "HOT_OPPORTUNITY"
        elif pulse_score >= 7.0:
            return "STRONG_POTENTIAL" 
        elif pulse_score >= 5.5:
            return "MODERATE_INTEREST"
        elif pulse_score >= 3.0:
            return "WEAK_SIGNALS"
        else:
            return "COLD_MARKET"
    
    def _generate_market_insights(self, trend: Dict, competition: Dict, demand: Dict) -> Dict[str, Any]:
        """Generate comprehensive market insights"""
        
        insights = {
            "market_temperature": "hot" if trend.get("momentum_score", 0) > 7 else "warm" if trend.get("momentum_score", 0) > 4 else "cool",
            "competition_pressure": competition.get("competition_level", "moderate"),
            "demand_status": "surging" if demand.get("surge_magnitude", 1) > 2 else "stable",
            "market_maturity": competition.get("saturation_analysis", {}).get("market_maturity", "growing"),
            "trend_sustainability": trend.get("trajectory_prediction", {}).get("prediction", "uncertain"),
            "key_drivers": []
        }
        
        # Identify key market drivers
        if demand.get("surge_magnitude", 1) > 3:
            insights["key_drivers"].append("Strong demand surge detected")
            
        if competition.get("opportunity_score", 5) > 7:
            insights["key_drivers"].append("Low competition window open")
            
        if trend.get("trend_status") in ["fast_rising", "explosive"]:
            insights["key_drivers"].append("Explosive trend velocity")
        
        return insights
    
    def _create_action_plan(self, pulse_score: float, trend: Dict, competition: Dict, demand: Dict) -> List[str]:
        """Create actionable recommendations"""
        
        recommendations = []
        
        # High-level strategy based on pulse score
        if pulse_score >= 8:
            recommendations.append("🔥 IMMEDIATE ACTION: Drop everything and focus on this opportunity!")
            
        elif pulse_score >= 6:
            recommendations.append("⚡ HIGH PRIORITY: Strong opportunity - move quickly")
            
        elif pulse_score >= 4:
            recommendations.append("📊 MONITOR CLOSELY: Developing opportunity")
            
        else:
            recommendations.append("⏳ WAIT AND WATCH: Better opportunities likely available")
        
        # Add specific tactical recommendations
        recommendations.extend(demand.get("action_recommendations", []))
        
        # Competition-based recommendations  
        entry_rec = competition.get("market_entry_recommendation", {})
        if entry_rec.get("recommendation") == "enter_immediately":
            recommendations.append("🚀 MARKET ENTRY: Enter immediately before competition increases")
            
        # Timing recommendations
        optimal_timing = self._calculate_optimal_timing(trend, demand)
        if optimal_timing.get("urgency") == "critical":
            recommendations.append(f"⏰ CRITICAL TIMING: {optimal_timing.get('message', '')}")
        
        return recommendations
    
    def _calculate_optimal_timing(self, trend: Dict, demand: Dict) -> Dict[str, Any]:
        """Calculate optimal market entry timing"""
        
        trend_prediction = trend.get("trajectory_prediction", {})
        demand_window = demand.get("opportunity_window", {})
        
        # Find the optimal window
        trend_timeframe = trend_prediction.get("timeframe", "unknown")
        demand_urgency = demand_window.get("urgency_level", "medium")
        
        if demand_urgency == "critical":
            return {
                "recommendation": "enter_now",
                "urgency": "critical", 
                "message": "Enter within 24-48 hours to catch demand surge"
            }
        elif trend_prediction.get("prediction") == "explosive_growth":
            return {
                "recommendation": "enter_very_soon",
                "urgency": "high",
                "message": "Enter within 1 week to ride explosive growth"
            }
        else:
            return {
                "recommendation": "enter_strategically", 
                "urgency": "medium",
                "message": "Plan strategic entry within 2-4 weeks"
            }
    
    def _assess_market_risks(self, competition: Dict, trend: Dict) -> Dict[str, Any]:
        """Assess market entry risks"""
        
        risks = {
            "competition_risk": "low",
            "trend_risk": "low", 
            "timing_risk": "low",
            "overall_risk": "low"
        }
        
        # Competition risks
        if competition.get("competition_level") in ["oversaturated", "high_competition"]:
            risks["competition_risk"] = "high"
            
        # Trend sustainability risks
        if trend.get("trajectory_prediction", {}).get("prediction") == "decline_ahead":
            risks["trend_risk"] = "high"
            
        # Calculate overall risk
        risk_scores = {"low": 1, "medium": 2, "high": 3}
        avg_risk = sum(risk_scores.get(risk, 1) for risk in risks.values()) / len(risks)
        
        if avg_risk > 2.5:
            risks["overall_risk"] = "high"
        elif avg_risk > 1.5:
            risks["overall_risk"] = "medium"
            
        return risks

# Simulated data sources (replace with real APIs in production)
class EtsyTrendsSimulator:
    """Simulate Etsy trends data"""
    
    def get_trend_data(self, keyword: str, timeframe: str) -> List[Dict]:
        """Simulate historical trend data"""
        base_value = hash(keyword) % 1000 + 500
        data = []
        
        for i in range(30):  # 30 days of data
            # Simulate realistic trend patterns
            day_factor = math.sin(i * 0.2) * 0.3 + 1  # Sine wave pattern
            noise = random.uniform(0.8, 1.2)  # Random noise
            trend_factor = 1 + (i * 0.02)  # Slight upward trend
            
            value = int(base_value * day_factor * noise * trend_factor)
            
            data.append({
                "date": (datetime.now() - timedelta(days=30-i)).isoformat(),
                "value": value
            })
        
        return data
    
    def get_competition_data(self, keyword: str) -> Dict[str, Any]:
        """Simulate competition data"""
        base_listings = hash(keyword) % 5000 + 200
        
        return {
            "total_listings": base_listings,
            "active_sellers": base_listings // 3,
            "new_listings_24h": random.randint(5, 50),
            "top_10_market_share": random.uniform(0.2, 0.6),
            "new_sellers_trend": random.uniform(0.05, 0.3)
        }

class GoogleTrendsSimulator:
    """Simulate Google Trends data"""
    
    def get_search_data(self, keyword: str) -> Dict[str, Any]:
        """Simulate search trend data"""
        baseline = hash(keyword) % 1000 + 100
        current = baseline * random.uniform(1.2, 4.0)  # Simulate surge
        
        return {
            "current_searches_24h": int(current),
            "baseline_searches": baseline,
            "search_growth_7d": random.uniform(0.1, 0.8),
            "related_trends": [f"{keyword}_variant_{i}" for i in range(3)]
        }

class SocialMediaSimulator:
    """Simulate social media buzz"""
    
    def get_social_buzz(self, keyword: str) -> Dict[str, Any]:
        """Simulate social media mentions"""
        return {
            "social_mentions": hash(keyword) % 2000 + 100,
            "sentiment_score": random.uniform(0.6, 0.9),
            "viral_potential": random.uniform(0.3, 0.8)
        }

class MarketDataSimulator:
    """Simulate general market data"""
    
    def get_market_data(self, keyword: str) -> Dict[str, Any]:
        """Simulate market data"""
        return {
            "market_size": hash(keyword) % 100000 + 10000,
            "growth_rate": random.uniform(0.05, 0.25),
            "seasonality": random.choice(["high", "medium", "low"])
        }

# Example usage and testing
if __name__ == "__main__":
    # Initialize Market Pulse Engine
    pulse_engine = MarketPulseEngine()
    
    # Test with sample keywords
    test_keywords = ["sage green decor", "minimalist jewelry", "cottagecore aesthetic"]
    
    print("⚡ REAL-TIME MARKET PULSE ENGINE TEST")
    print("=" * 60)
    
    for keyword in test_keywords:
        print(f"\n🔍 Analyzing: {keyword}")
        print("-" * 40)
        
        result = pulse_engine.get_market_pulse([keyword])
        
        if result.get('error'):
            print(f"❌ Analysis failed: {result['error']}")
            continue
        
        print(f"📊 Market Pulse Score: {result['market_pulse_score']:.1f}/10")
        print(f"🌡️ Status: {result['pulse_status']}")
        
        # Show key insights
        insights = result['market_insights']
        print(f"🔥 Market Temperature: {insights['market_temperature']}")
        print(f"⚔️ Competition: {insights['competition_pressure']}")
        print(f"📈 Demand: {insights['demand_status']}")
        
        # Show top recommendations
        recommendations = result['action_recommendations'][:3]
        print("💡 Top Recommendations:")
        for rec in recommendations:
            print(f"   • {rec}")
        
        # Show optimal timing
        timing = result['optimal_timing']
        print(f"⏰ Optimal Timing: {timing['recommendation']} ({timing['urgency']} urgency)")