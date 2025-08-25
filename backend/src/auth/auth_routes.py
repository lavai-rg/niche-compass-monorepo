#!/usr/bin/env python3
"""
Authentication Routes for Niche Compass
Handles login, logout, and user management endpoints
"""

from flask import Blueprint, request, jsonify, session, current_app
from werkzeug.security import check_password_hash
import logging
from .auth_service import auth_service, User
from datetime import datetime

logger = logging.getLogger(__name__)

# Create authentication blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400
        
        # Authenticate user
        user = auth_service.authenticate_user(email, password)
        
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Create session
        auth_service.create_session(user)
        
        # Create access token
        user_data = {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'role': getattr(user, 'role', 'user')
        }
        access_token = auth_service.create_access_token(user_data)
        
        logger.info(f"User logged in successfully: {email}")
        
        return jsonify({
            'message': 'Login successful',
            'user': user_data,
            'access_token': access_token,
            'token_type': 'Bearer'
        }), 200
        
    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """User logout endpoint"""
    try:
        # Destroy session
        auth_service.destroy_session()
        
        logger.info("User logged out successfully")
        
        return jsonify({
            'message': 'Logout successful'
        }), 200
        
    except Exception as e:
        logger.error(f"Logout error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    """Get current authenticated user"""
    try:
        if not auth_service.is_authenticated():
            return jsonify({'error': 'Not authenticated'}), 401
        
        user = auth_service.get_current_user()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        user_data = {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'picture': user.picture,
            'email_verified': user.email_verified,
            'role': getattr(user, 'role', 'user'),
            'created_at': user.created_at.isoformat() if user.created_at else None,
            'last_login': user.last_login.isoformat() if user.last_login else None
        }
        
        return jsonify({
            'user': user_data
        }), 200
        
    except Exception as e:
        logger.error(f"Get current user error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    """User registration endpoint"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        
        if not email or not password or not name:
            return jsonify({'error': 'Email, password, and name required'}), 400
        
        # Check if user already exists
        existing_user = auth_service.get_user_by_id(email)
        if existing_user:
            return jsonify({'error': 'User already exists'}), 409
        
        # Hash password
        hashed_password = auth_service.hash_password(password)
        
        # Create new user (in production, save to database)
        new_user = User(
            id=f"user-{len(auth_service.mock_users) + 1:03d}",
            email=email,
            name=name,
            email_verified=False,
            created_at=datetime.utcnow()
        )
        
        # Add to mock users (in production, save to database)
        auth_service.mock_users[email] = {
            'id': new_user.id,
            'email': new_user.email,
            'name': new_user.name,
            'password': hashed_password,
            'email_verified': False,
            'role': 'user'
        }
        
        logger.info(f"New user registered: {email}")
        
        return jsonify({
            'message': 'Registration successful',
            'user': {
                'id': new_user.id,
                'email': new_user.email,
                'name': new_user.name
            }
        }), 201
        
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/verify-token', methods=['POST'])
def verify_token():
    """Verify JWT token"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        token = data.get('token')
        
        if not token:
            return jsonify({'error': 'Token required'}), 400
        
        # Verify token
        payload = auth_service.verify_token(token)
        
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        return jsonify({
            'valid': True,
            'user': {
                'id': payload.get('sub'),
                'email': payload.get('email'),
                'name': payload.get('name'),
                'role': payload.get('role')
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Token verification error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/refresh-token', methods=['POST'])
def refresh_token():
    """Refresh JWT token"""
    try:
        if not auth_service.is_authenticated():
            return jsonify({'error': 'Not authenticated'}), 401
        
        user = auth_service.get_current_user()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Create new access token
        user_data = {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'role': getattr(user, 'role', 'user')
        }
        new_access_token = auth_service.create_access_token(user_data)
        
        logger.info(f"Token refreshed for user: {user.email}")
        
        return jsonify({
            'access_token': new_access_token,
            'token_type': 'Bearer'
        }), 200
        
    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/health', methods=['GET'])
def auth_health():
    """Authentication service health check"""
    try:
        return jsonify({
            'status': 'healthy',
            'service': 'authentication',
            'authenticated_users': len([u for u in auth_service.mock_users.values()]),
            'session_active': auth_service.is_authenticated()
        }), 200
        
    except Exception as e:
        logger.error(f"Auth health check error: {e}")
        return jsonify({
            'status': 'unhealthy',
            'service': 'authentication',
            'error': str(e)
        }), 500
