#!/usr/bin/env python3
"""
⚡ Market Pulse API Routes - Real-Time Market Intelligence
========================================================
Revolutionary real-time market monitoring and trend detection endpoints
"""

from flask import Blueprint, request, jsonify
from src.services.market_pulse_engine import MarketPulseEngine
import logging

logger = logging.getLogger(__name__)
market_pulse_bp = Blueprint("market_pulse", __name__)

# Initialize Market Pulse Engine
pulse_engine = MarketPulseEngine()

@market_pulse_bp.route("/pulse", methods=["POST"], strict_slashes=False)
def get_market_pulse():
    """Get real-time market pulse for keywords"""
    logger.info("get_market_pulse endpoint called")
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Request body required"}), 400
        
        # Extract parameters
        keywords = data.get("keywords", [])
        timeframe = data.get("timeframe", "24h")
        
        if not keywords:
            return jsonify({"error": "Keywords are required"}), 400
        
        if not isinstance(keywords, list):
            keywords = [keywords]  # Convert single keyword to list
        
        # Get market pulse analysis
        pulse_result = pulse_engine.get_market_pulse(keywords, timeframe)
        
        if pulse_result.get("error"):
            return jsonify({"error": pulse_result["error"]}), 500
        
        # Add metadata
        response_data = {
            "success": True,
            "analyzed_keywords": keywords,
            "timeframe": timeframe,
            "market_pulse": pulse_result,
            "api_version": "1.0",
            "feature": "real_time_market_intelligence"
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        logger.error(f"Market pulse analysis error: {e}")
        return jsonify({
            "error": "Market pulse analysis failed",
            "details": str(e)
        }), 500

@market_pulse_bp.route("/trending", methods=["GET"], strict_slashes=False)
def get_trending_niches():
    """Get currently trending niches with pulse analysis"""
    logger.info("get_trending_niches endpoint called")
    
    try:
        # Predefined trending keywords to analyze
        trending_keywords = [
            "sage green home decor",
            "minimalist jewelry", 
            "cottagecore aesthetic",
            "sustainable fashion",
            "personalized pet accessories",
            "vintage wall art",
            "boho wedding decor",
            "custom portrait art",
            "handmade ceramics",
            "digital artwork"
        ]
        
        trending_results = []
        
        # Analyze each trending keyword
        for keyword in trending_keywords:
            pulse_result = pulse_engine.get_market_pulse([keyword])
            
            if not pulse_result.get("error"):
                # Extract key metrics
                trending_data = {
                    "keyword": keyword,
                    "pulse_score": pulse_result.get("market_pulse_score", 0),
                    "status": pulse_result.get("pulse_status", "UNKNOWN"),
                    "trend_velocity": pulse_result.get("trend_analysis", {}).get("trend_status", "stable"),
                    "competition_level": pulse_result.get("competition_analysis", {}).get("competition_level", "moderate"),
                    "opportunity_score": pulse_result.get("competition_analysis", {}).get("opportunity_score", 5),
                    "demand_surge": pulse_result.get("demand_analysis", {}).get("surge_detected", False),
                    "top_recommendation": pulse_result.get("action_recommendations", ["No recommendations"])[0]
                }
                trending_results.append(trending_data)
        
        # Sort by pulse score (highest first)
        trending_results.sort(key=lambda x: x["pulse_score"], reverse=True)
        
        # Add ranking
        for i, result in enumerate(trending_results):
            result["rank"] = i + 1
        
        return jsonify({
            "success": True,
            "trending_niches": trending_results,
            "total_analyzed": len(trending_results),
            "api_version": "1.0",
            "last_updated": pulse_result.get("timestamp", ""),
            "feature": "trending_niches_intelligence"
        }), 200
        
    except Exception as e:
        logger.error(f"Trending niches analysis error: {e}")
        return jsonify({
            "error": "Trending analysis failed",
            "details": str(e)
        }), 500

@market_pulse_bp.route("/competition/<niche>", methods=["GET"], strict_slashes=False)
def analyze_competition(niche):
    """Analyze competition density for a specific niche"""
    logger.info(f"analyze_competition endpoint called for niche: {niche}")
    
    try:
        # Get full market pulse for competition analysis
        pulse_result = pulse_engine.get_market_pulse([niche])
        
        if pulse_result.get("error"):
            return jsonify({"error": pulse_result["error"]}), 500
        
        # Extract competition-specific data
        competition_analysis = pulse_result.get("competition_analysis", {})
        
        response_data = {
            "success": True,
            "niche": niche,
            "competition_analysis": competition_analysis,
            "market_entry_guidance": {
                "recommendation": competition_analysis.get("market_entry_recommendation", {}),
                "required_advantages": competition_analysis.get("competitive_advantages_needed", []),
                "opportunity_score": competition_analysis.get("opportunity_score", 0)
            },
            "risk_assessment": pulse_result.get("risk_assessment", {}),
            "timestamp": pulse_result.get("timestamp", ""),
            "api_version": "1.0"
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        logger.error(f"Competition analysis error: {e}")
        return jsonify({
            "error": "Competition analysis failed", 
            "details": str(e)
        }), 500

@market_pulse_bp.route("/velocity/<niche>", methods=["GET"], strict_slashes=False)
def analyze_trend_velocity(niche):
    """Analyze trend velocity for a specific niche"""
    logger.info(f"analyze_trend_velocity endpoint called for niche: {niche}")
    
    try:
        # Get full market pulse for trend analysis
        pulse_result = pulse_engine.get_market_pulse([niche])
        
        if pulse_result.get("error"):
            return jsonify({"error": pulse_result["error"]}), 500
        
        # Extract trend-specific data
        trend_analysis = pulse_result.get("trend_analysis", {})
        
        response_data = {
            "success": True,
            "niche": niche,
            "trend_velocity": trend_analysis,
            "momentum_insights": {
                "momentum_score": trend_analysis.get("momentum_score", 0),
                "trend_status": trend_analysis.get("trend_status", "unknown"),
                "trajectory_prediction": trend_analysis.get("trajectory_prediction", {}),
                "peak_estimation": trend_analysis.get("peak_estimation", {})
            },
            "timing_recommendations": pulse_result.get("optimal_timing", {}),
            "timestamp": pulse_result.get("timestamp", ""),
            "api_version": "1.0"
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        logger.error(f"Trend velocity analysis error: {e}")
        return jsonify({
            "error": "Trend velocity analysis failed",
            "details": str(e)
        }), 500

@market_pulse_bp.route("/opportunities", methods=["GET"], strict_slashes=False)
def get_market_opportunities():
    """Get top market opportunities based on pulse analysis"""
    logger.info("get_market_opportunities endpoint called")
    
    try:
        # Get query parameters
        limit = request.args.get("limit", 10, type=int)
        min_pulse_score = request.args.get("min_score", 6.0, type=float)
        
        # Comprehensive keyword list for opportunity scanning
        opportunity_keywords = [
            # Trending Categories
            "sage green decor", "cottagecore aesthetic", "dark academia",
            "minimalist jewelry", "chunky gold chains", "pearl accessories",
            "sustainable fashion", "eco-friendly products", "zero waste",
            "personalized gifts", "custom pet portraits", "family name signs",
            
            # Seasonal Opportunities  
            "autumn home decor", "cozy reading nook", "hygge lifestyle",
            "christmas ornaments", "holiday table settings", "winter wedding",
            
            # Emerging Trends
            "mushroom decor", "witchy aesthetic", "crystal collection",
            "plant mom gifts", "succulent arrangements", "hanging planters",
            "vintage cameras", "film photography", "polaroid frames",
            "bookish gifts", "library aesthetic", "vintage books"
        ]
        
        opportunities = []
        
        # Analyze each keyword for opportunities
        for keyword in opportunity_keywords[:limit*2]:  # Analyze more to filter top ones
            pulse_result = pulse_engine.get_market_pulse([keyword])
            
            if not pulse_result.get("error"):
                pulse_score = pulse_result.get("market_pulse_score", 0)
                
                # Filter by minimum pulse score
                if pulse_score >= min_pulse_score:
                    opportunity = {
                        "keyword": keyword,
                        "pulse_score": pulse_score,
                        "status": pulse_result.get("pulse_status", ""),
                        "opportunity_summary": {
                            "competition_level": pulse_result.get("competition_analysis", {}).get("competition_level", ""),
                            "opportunity_score": pulse_result.get("competition_analysis", {}).get("opportunity_score", 0),
                            "trend_momentum": pulse_result.get("trend_analysis", {}).get("momentum_score", 0),
                            "demand_surge": pulse_result.get("demand_analysis", {}).get("surge_detected", False)
                        },
                        "market_insights": pulse_result.get("market_insights", {}),
                        "action_plan": pulse_result.get("action_recommendations", [])[:3],  # Top 3 recommendations
                        "timing": pulse_result.get("optimal_timing", {}),
                        "risk_level": pulse_result.get("risk_assessment", {}).get("overall_risk", "unknown")
                    }
                    opportunities.append(opportunity)
        
        # Sort by pulse score and limit results
        opportunities.sort(key=lambda x: x["pulse_score"], reverse=True)
        opportunities = opportunities[:limit]
        
        # Add rankings
        for i, opp in enumerate(opportunities):
            opp["rank"] = i + 1
        
        return jsonify({
            "success": True,
            "market_opportunities": opportunities,
            "total_found": len(opportunities),
            "search_criteria": {
                "min_pulse_score": min_pulse_score,
                "limit": limit
            },
            "api_version": "1.0",
            "feature": "opportunity_scanner"
        }), 200
        
    except Exception as e:
        logger.error(f"Market opportunities analysis error: {e}")
        return jsonify({
            "error": "Opportunities analysis failed",
            "details": str(e)
        }), 500

@market_pulse_bp.route("/alerts", methods=["GET"], strict_slashes=False)
def get_market_alerts():
    """Get urgent market alerts and opportunities"""
    logger.info("get_market_alerts endpoint called")
    
    try:
        # Keywords for alert monitoring
        alert_keywords = [
            "trending home decor", "viral jewelry trend", "seasonal opportunity",
            "low competition niche", "demand surge detected", "emerging market"
        ]
        
        alerts = []
        
        for keyword in alert_keywords:
            pulse_result = pulse_engine.get_market_pulse([keyword])
            
            if not pulse_result.get("error"):
                pulse_score = pulse_result.get("market_pulse_score", 0)
                
                # Create alerts based on different criteria
                alert_conditions = []
                
                # High pulse score alert
                if pulse_score >= 8.5:
                    alert_conditions.append({
                        "type": "HOT_OPPORTUNITY",
                        "urgency": "CRITICAL",
                        "message": f"Exceptional opportunity detected in '{keyword}'"
                    })
                
                # Demand surge alert
                if pulse_result.get("demand_analysis", {}).get("surge_detected"):
                    alert_conditions.append({
                        "type": "DEMAND_SURGE", 
                        "urgency": "HIGH",
                        "message": f"Demand surge detected for '{keyword}'"
                    })
                
                # Low competition alert
                competition_level = pulse_result.get("competition_analysis", {}).get("competition_level", "")
                if competition_level in ["low_competition", "untapped"]:
                    alert_conditions.append({
                        "type": "LOW_COMPETITION",
                        "urgency": "MEDIUM", 
                        "message": f"Low competition window open for '{keyword}'"
                    })
                
                # Fast rising trend alert
                trend_status = pulse_result.get("trend_analysis", {}).get("trend_status", "")
                if trend_status in ["fast_rising", "explosive"]:
                    alert_conditions.append({
                        "type": "FAST_TREND",
                        "urgency": "HIGH",
                        "message": f"Fast rising trend detected in '{keyword}'"
                    })
                
                # Add alerts
                for condition in alert_conditions:
                    alert = {
                        **condition,
                        "keyword": keyword,
                        "pulse_score": pulse_score,
                        "timestamp": pulse_result.get("timestamp", ""),
                        "action_required": pulse_result.get("action_recommendations", [])[0] if pulse_result.get("action_recommendations") else "Monitor closely"
                    }
                    alerts.append(alert)
        
        # Sort by urgency and pulse score
        urgency_order = {"CRITICAL": 3, "HIGH": 2, "MEDIUM": 1, "LOW": 0}
        alerts.sort(key=lambda x: (urgency_order.get(x["urgency"], 0), x["pulse_score"]), reverse=True)
        
        return jsonify({
            "success": True,
            "market_alerts": alerts,
            "total_alerts": len(alerts),
            "critical_alerts": len([a for a in alerts if a["urgency"] == "CRITICAL"]),
            "high_priority_alerts": len([a for a in alerts if a["urgency"] == "HIGH"]),
            "api_version": "1.0",
            "feature": "market_alerts"
        }), 200
        
    except Exception as e:
        logger.error(f"Market alerts error: {e}")
        return jsonify({
            "error": "Market alerts failed",
            "details": str(e)
        }), 500