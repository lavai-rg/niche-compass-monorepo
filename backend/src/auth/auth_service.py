#!/usr/bin/env python3
"""
Authentication Service for Niche Compass
Handles user authentication, JWT tokens, and session management
"""

import os
import jwt
import time
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from dataclasses import dataclass
import requests
from flask import current_app, session, request
import logging

logger = logging.getLogger(__name__)

@dataclass
class User:
    """User data model"""
    id: str
    email: str
    name: str
    picture: Optional[str] = None
    email_verified: bool = False
    auth0_id: Optional[str] = None
    created_at: datetime = None
    last_login: datetime = None

class AuthService:
    """Main authentication service"""
    
    def __init__(self):
        self.secret_key = os.getenv('JWT_SECRET_KEY', 'dev-secret-key-change-in-production')
        self.algorithm = 'HS256'
        self.token_expiry = 24 * 60 * 60  # 24 hours
        self.auth0_domain = os.getenv('AUTH0_DOMAIN')
        self.auth0_client_id = os.getenv('AUTH0_CLIENT_ID')
        self.auth0_client_secret = os.getenv('AUTH0_CLIENT_SECRET')
        self.auth0_audience = os.getenv('AUTH0_AUDIENCE')
        
        # Mock users for development (remove in production)
        self.mock_users = {
            'admin@nichecompass.com': {
                'id': 'admin-001',
                'email': 'admin@nichecompass.com',
                'name': 'Admin User',
                'picture': 'https://via.placeholder.com/150',
                'email_verified': True,
                'role': 'admin'
            },
            'user@nichecompass.com': {
                'id': 'user-001',
                'email': 'user@nichecompass.com',
                'name': 'Demo User',
                'picture': 'https://via.placeholder.com/150',
                'email_verified': True,
                'role': 'user'
            }
        }
    
    def create_access_token(self, user_data: Dict[str, Any]) -> str:
        """Create JWT access token"""
        try:
            payload = {
                'sub': user_data['id'],
                'email': user_data['email'],
                'name': user_data['name'],
                'role': user_data.get('role', 'user'),
                'exp': datetime.utcnow() + timedelta(seconds=self.token_expiry),
                'iat': datetime.utcnow()
            }
            
            token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
            logger.info(f"Access token created for user: {user_data['email']}")
            return token
            
        except Exception as e:
            logger.error(f"Error creating access token: {e}")
            raise
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify JWT token and return payload"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            logger.info(f"Token verified for user: {payload.get('email')}")
            return payload
            
        except jwt.ExpiredSignatureError:
            logger.warning("Token expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {e}")
            return None
        except Exception as e:
            logger.error(f"Error verifying token: {e}")
            return None
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        salt = secrets.token_hex(16)
        hash_obj = hashlib.sha256()
        hash_obj.update((password + salt).encode('utf-8'))
        return f"{salt}:{hash_obj.hexdigest()}"
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        try:
            salt, hash_value = hashed.split(':')
            hash_obj = hashlib.sha256()
            hash_obj.update((password + salt).encode('utf-8'))
            return hash_obj.hexdigest() == hash_value
        except:
            return False
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        try:
            # For development, use mock users
            if email in self.mock_users:
                user_data = self.mock_users[email]
                # In production, verify against database
                if password == 'password123':  # Mock password
                    user = User(
                        id=user_data['id'],
                        email=user_data['email'],
                        name=user_data['name'],
                        picture=user_data['picture'],
                        email_verified=user_data['email_verified'],
                        created_at=datetime.utcnow(),
                        last_login=datetime.utcnow()
                    )
                    logger.info(f"User authenticated: {email}")
                    return user
            
            logger.warning(f"Authentication failed for: {email}")
            return None
            
        except Exception as e:
            logger.error(f"Error authenticating user: {e}")
            return None
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        try:
            for user_data in self.mock_users.values():
                if user_data['id'] == user_id:
                    return User(
                        id=user_data['id'],
                        email=user_data['email'],
                        name=user_data['name'],
                        picture=user_data['picture'],
                        email_verified=user_data['email_verified'],
                        created_at=datetime.utcnow()
                    )
            return None
            
        except Exception as e:
            logger.error(f"Error getting user by ID: {e}")
            return None
    
    def create_session(self, user: User) -> str:
        """Create user session"""
        try:
            session['user_id'] = user.id
            session['user_email'] = user.email
            session['user_name'] = user.name
            session['user_role'] = getattr(user, 'role', 'user')
            session['authenticated'] = True
            session['login_time'] = datetime.utcnow().isoformat()
            
            logger.info(f"Session created for user: {user.email}")
            return "Session created successfully"
            
        except Exception as e:
            logger.error(f"Error creating session: {e}")
            raise
    
    def destroy_session(self) -> str:
        """Destroy user session"""
        try:
            session.clear()
            logger.info("Session destroyed")
            return "Session destroyed successfully"
            
        except Exception as e:
            logger.error(f"Error destroying session: {e}")
            raise
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return session.get('authenticated', False)
    
    def get_current_user(self) -> Optional[User]:
        """Get current authenticated user"""
        if not self.is_authenticated():
            return None
        
        user_id = session.get('user_id')
        if user_id:
            return self.get_user_by_id(user_id)
        return None
    
    def require_auth(self, f):
        """Decorator to require authentication"""
        from functools import wraps
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not self.is_authenticated():
                return {'error': 'Authentication required'}, 401
            return f(*args, **kwargs)
        return decorated_function
    
    def require_role(self, required_role: str):
        """Decorator to require specific role"""
        def decorator(f):
            from functools import wraps
            @wraps(f)
            def decorated_function(*args, **kwargs):
                if not self.is_authenticated():
                    return {'error': 'Authentication required'}, 401
                
                user_role = session.get('user_role', 'user')
                if user_role != required_role and user_role != 'admin':
                    return {'error': 'Insufficient permissions'}, 403
                
                return f(*args, **kwargs)
            return decorated_function
        return decorator

# Global auth service instance
auth_service = AuthService()
