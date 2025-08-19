"""
Auth0 JWT Token Validator untuk Niche Compass
Sistem validasi token JWT dari Auth0 untuk proteksi API endpoint
"""

import jwt
import json
import requests
from functools import wraps
from flask import request, jsonify, current_app
from urllib.parse import urljoin
import os
from datetime import datetime, timezone


class Auth0JWTValidator:
    def __init__(self, domain, audience, algorithms=['RS256']):
        self.domain = domain
        self.audience = audience
        self.algorithms = algorithms
        self.jwks_uri = f"https://{domain}/.well-known/jwks.json"
        self.issuer = f"https://{domain}/"
        self._jwks_cache = None
        self._jwks_cache_time = None
        self.cache_timeout = 3600  # 1 jam cache untuk JWKS
        
    def get_jwks(self):
        """Ambil JSON Web Key Set (JWKS) dari Auth0 dengan caching"""
        current_time = datetime.now(timezone.utc).timestamp()
        
        # Gunakan cache jika masih valid
        if (self._jwks_cache and self._jwks_cache_time and 
            current_time - self._jwks_cache_time < self.cache_timeout):
            return self._jwks_cache
            
        try:
            response = requests.get(self.jwks_uri, timeout=10)
            response.raise_for_status()
            jwks = response.json()
            
            # Update cache
            self._jwks_cache = jwks
            self._jwks_cache_time = current_time
            
            return jwks
        except Exception as e:
            current_app.logger.error(f"Error mengambil JWKS: {str(e)}")
            # Return cache lama jika ada, atau raise error
            if self._jwks_cache:
                return self._jwks_cache
            raise
    
    def get_token_auth_header(self):
        """Ekstrak token dari Authorization header"""
        auth = request.headers.get('Authorization', None)
        if not auth:
            return None
            
        parts = auth.split()
        
        if parts[0].lower() != 'bearer':
            return None
        elif len(parts) == 1:
            return None
        elif len(parts) > 2:
            return None
            
        token = parts[1]
        return token
    
    def validate_token(self, token):
        """Validasi JWT token dari Auth0"""
        try:
            # Decode header untuk mendapatkan key ID
            unverified_header = jwt.get_unverified_header(token)
            
            # Ambil JWKS
            jwks = self.get_jwks()
            
            # Cari key yang sesuai dengan kid di header
            rsa_key = {}
            for key in jwks['keys']:
                if key['kid'] == unverified_header['kid']:
                    rsa_key = {
                        'kty': key['kty'],
                        'kid': key['kid'],
                        'use': key['use'],
                        'n': key['n'],
                        'e': key['e']
                    }
                    break
            
            if not rsa_key:
                current_app.logger.error("Key ID tidak ditemukan di JWKS")
                return None
            
            # Validasi token
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=self.algorithms,
                audience=self.audience,
                issuer=self.issuer
            )
            
            return payload
            
        except jwt.ExpiredSignatureError:
            current_app.logger.error("Token sudah expired")
            return None
        except jwt.InvalidAudienceError:
            current_app.logger.error("Invalid audience")
            return None
        except jwt.InvalidIssuerError:
            current_app.logger.error("Invalid issuer")
            return None
        except jwt.InvalidSignatureError:
            current_app.logger.error("Invalid signature")
            return None
        except jwt.InvalidTokenError as e:
            current_app.logger.error(f"Invalid token: {str(e)}")
            return None
        except Exception as e:
            current_app.logger.error(f"Error validasi token: {str(e)}")
            return None


# Instance global validator
auth0_validator = None

def init_auth0_validator(app):
    """Initialize Auth0 validator dengan konfigurasi dari Flask app"""
    global auth0_validator
    
    domain = app.config.get('AUTH0_DOMAIN')
    audience = app.config.get('AUTH0_AUDIENCE')
    
    if not domain or not audience:
        app.logger.warning("Auth0 domain atau audience tidak dikonfigurasi")
        return None
    
    auth0_validator = Auth0JWTValidator(domain, audience)
    app.logger.info(f"Auth0 validator initialized: domain={domain}, audience={audience}")
    return auth0_validator


def require_auth(f):
    """Decorator untuk endpoint yang memerlukan autentikasi"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not auth0_validator:
            return jsonify({
                'error': 'auth_not_configured',
                'message': 'Sistem autentikasi belum dikonfigurasi'
            }), 500
        
        token = auth0_validator.get_token_auth_header()
        if not token:
            return jsonify({
                'error': 'authorization_header_missing',
                'message': 'Header Authorization diperlukan'
            }), 401
        
        payload = auth0_validator.validate_token(token)
        if not payload:
            return jsonify({
                'error': 'invalid_token',
                'message': 'Token tidak valid atau sudah expired'
            }), 401
        
        # Set user info ke request context
        request.user = {
            'sub': payload.get('sub'),
            'email': payload.get('email'),
            'name': payload.get('name'),
            'picture': payload.get('picture'),
            'permissions': payload.get('permissions', []),
            'token_payload': payload
        }
        
        return f(*args, **kwargs)
    return decorated


def require_permission(permission):
    """Decorator untuk endpoint yang memerlukan permission khusus"""
    def decorator(f):
        @wraps(f)
        @require_auth
        def decorated(*args, **kwargs):
            user_permissions = request.user.get('permissions', [])
            if permission not in user_permissions:
                return jsonify({
                    'error': 'insufficient_permissions',
                    'message': f'Permission {permission} diperlukan'
                }), 403
            return f(*args, **kwargs)
        return decorated
    return decorator


def get_current_user():
    """Helper function untuk mendapatkan user info dari request context"""
    return getattr(request, 'user', None)