import React, { useState } from 'react';
import { apiClient } from '../../utils/axiosConfig';
import './LoginForm.css';

const LoginForm = ({ onLoginSuccess, onClose }) => {
    const [formData, setFormData] = useState({
        email: '',
        password: ''
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [showRegister, setShowRegister] = useState(false);

    const handleInputChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleLogin = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            const response = await apiClient.login(formData);
            
            if (response.data.access_token) {
                // Store token in localStorage
                localStorage.setItem('authToken', response.data.access_token);
                localStorage.setItem('userData', JSON.stringify(response.data.user));
                
                // Call success callback
                onLoginSuccess(response.data.user);
                
                // Show success message
                setError('');
            }
        } catch (err) {
            if (err.response?.data?.error) {
                setError(err.response.data.error);
            } else {
                setError('Login failed. Please try again.');
            }
        } finally {
            setLoading(false);
        }
    };

    const handleRegister = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            const response = await apiClient.register(formData);
            
            if (response.data.message === 'Registration successful') {
                setError('');
                setShowRegister(false);
                // Auto-login after successful registration
                handleLogin(e);
            }
        } catch (err) {
            if (err.response?.data?.error) {
                setError(err.response.data.error);
            } else {
                setError('Registration failed. Please try again.');
            }
        } finally {
            setLoading(false);
        }
    };

    const handleDemoLogin = () => {
        setFormData({
            email: 'admin@nichecompass.com',
            password: 'password123'
        });
    };

    return (
        <div className="login-overlay">
            <div className="login-modal">
                <div className="login-header">
                    <h2>🔐 Welcome to Niche Compass</h2>
                    <p>Sign in to access all features</p>
                    <button className="close-btn" onClick={onClose}>&times;</button>
                </div>

                {error && (
                    <div className="error-message">
                        ❌ {error}
                    </div>
                )}

                <form onSubmit={showRegister ? handleRegister : handleLogin}>
                    <div className="form-group">
                        <label htmlFor="email">Email Address</label>
                        <input
                            type="email"
                            id="email"
                            name="email"
                            value={formData.email}
                            onChange={handleInputChange}
                            placeholder="Enter your email"
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="password">Password</label>
                        <input
                            type="password"
                            id="password"
                            name="password"
                            value={formData.password}
                            onChange={handleInputChange}
                            placeholder="Enter your password"
                            required
                        />
                    </div>

                    <div className="form-actions">
                        <button 
                            type="submit" 
                            className="btn-primary"
                            disabled={loading}
                        >
                            {loading ? '⏳ Processing...' : (showRegister ? '📝 Register' : '🔑 Sign In')}
                        </button>
                        
                        <button 
                            type="button" 
                            className="btn-secondary"
                            onClick={handleDemoLogin}
                            disabled={loading}
                        >
                            🚀 Demo Login
                        </button>
                    </div>
                </form>

                <div className="login-footer">
                    <button 
                        type="button" 
                        className="link-btn"
                        onClick={() => setShowRegister(!showRegister)}
                    >
                        {showRegister ? 'Already have an account? Sign In' : 'Need an account? Register'}
                    </button>
                </div>

                <div className="demo-credentials">
                    <h4>🧪 Demo Credentials:</h4>
                    <p><strong>Admin:</strong> admin@nichecompass.com / password123</p>
                    <p><strong>User:</strong> user@nichecompass.com / password123</p>
                </div>
            </div>
        </div>
    );
};

export default LoginForm;
