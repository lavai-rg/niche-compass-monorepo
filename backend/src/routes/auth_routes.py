"""
Auth Routes untuk Niche Compass
Endpoint API yang berhubungan dengan autentikasi pengguna
"""

from flask import Blueprint, request, jsonify
from src.auth import require_auth, get_current_user

# Blueprint untuk auth routes
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/profile', methods=['GET'])
@require_auth
def get_profile():
    """Endpoint untuk mendapatkan profil user yang sedang login"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({
                'error': 'user_not_found',
                'message': 'Informasi pengguna tidak ditemukan'
            }), 404
        
        # Format user profile response
        profile = {
            'id': user['sub'],
            'email': user.get('email'),
            'name': user.get('name'),
            'picture': user.get('picture'),
            'email_verified': user.get('email_verified', False),
            'nickname': user.get('nickname'),
            'permissions': user.get('permissions', []),
            'created_at': user.get('created_at'),
            'updated_at': user.get('updated_at')
        }
        
        return jsonify({
            'success': True,
            'data': profile,
            'message': 'Profil berhasil diambil'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'server_error',
            'message': f'Terjadi kesalahan server: {str(e)}'
        }), 500


@auth_bp.route('/verify', methods=['GET'])
@require_auth
def verify_token():
    """Endpoint untuk verifikasi apakah token masih valid"""
    try:
        user = get_current_user()
        return jsonify({
            'valid': True,
            'user_id': user['sub'],
            'email': user.get('email'),
            'message': 'Token valid'
        }), 200
        
    except Exception as e:
        return jsonify({
            'valid': False,
            'error': 'verification_failed',
            'message': f'Verifikasi gagal: {str(e)}'
        }), 500


@auth_bp.route('/permissions', methods=['GET'])
@require_auth
def get_permissions():
    """Endpoint untuk mendapatkan permissions user"""
    try:
        user = get_current_user()
        permissions = user.get('permissions', [])
        
        return jsonify({
            'success': True,
            'data': {
                'user_id': user['sub'],
                'permissions': permissions,
                'has_permissions': len(permissions) > 0
            },
            'message': 'Permissions berhasil diambil'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'server_error',
            'message': f'Terjadi kesalahan server: {str(e)}'
        }), 500


@auth_bp.route('/user-stats', methods=['GET'])
@require_auth
def get_user_stats():
    """Endpoint untuk mendapatkan statistik penggunaan user"""
    try:
        user = get_current_user()
        user_id = user['sub']
        
        # TODO: Implementasi logika untuk mendapatkan stats user dari database
        # Sementara return mock data
        stats = {
            'user_id': user_id,
            'searches_today': 5,
            'searches_this_month': 47,
            'total_searches': 156,
            'keywords_analyzed': 23,
            'niches_explored': 8,
            'products_analyzed': 12,
            'plan': 'Free',
            'plan_limit': {
                'searches_per_day': 10,
                'keywords_per_day': 5,
                'niches_per_day': 3
            },
            'usage_remaining': {
                'searches': 5,
                'keywords': 2,
                'niches': 1
            }
        }
        
        return jsonify({
            'success': True,
            'data': stats,
            'message': 'Statistik pengguna berhasil diambil'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'server_error',
            'message': f'Terjadi kesalahan server: {str(e)}'
        }), 500


# Test route untuk memastikan auth berjalan
@auth_bp.route('/test', methods=['GET'])
def test_auth():
    """Test endpoint tanpa autentikasi"""
    return jsonify({
        'message': 'Auth routes berjalan dengan baik',
        'timestamp': '2024-08-19T00:00:00Z',
        'status': 'healthy'
    }), 200


@auth_bp.route('/test-protected', methods=['GET'])
@require_auth
def test_protected():
    """Test endpoint dengan autentikasi"""
    user = get_current_user()
    return jsonify({
        'message': 'Auth protection bekerja dengan baik',
        'user_id': user['sub'],
        'email': user.get('email'),
        'timestamp': '2024-08-19T00:00:00Z'
    }), 200