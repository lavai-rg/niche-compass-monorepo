#!/usr/bin/env python3
"""
Authentication package for Niche Compass
"""

from .auth_service import auth_service, User
from .auth_routes import auth_bp

__all__ = ['auth_service', 'User', 'auth_bp']