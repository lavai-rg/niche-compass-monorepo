import { createContext, useContext, useEffect, useState } from 'react';
import { useAuth0 } from '@auth0/auth0-react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const {
    user,
    isAuthenticated,
    isLoading,
    loginWithRedirect,
    logout,
    getAccessTokenSilently,
  } = useAuth0();

  const [accessToken, setAccessToken] = useState(null);

  // Dapatkan access token secara otomatis ketika user sudah authenticated
  useEffect(() => {
    const getToken = async () => {
      if (isAuthenticated) {
        try {
          const token = await getAccessTokenSilently({
            authorizationParams: {
              audience: import.meta.env.VITE_AUTH0_AUDIENCE,
              scope: "read:current_user update:current_user_metadata",
            },
          });
          setAccessToken(token);
        } catch (error) {
          console.error('Error mendapatkan access token:', error);
        }
      }
    };

    if (isAuthenticated && !isLoading) {
      getToken();
    }
  }, [isAuthenticated, isLoading, getAccessTokenSilently]);

  const login = () => {
    loginWithRedirect({
      authorizationParams: {
        redirect_uri: import.meta.env.VITE_AUTH0_CALLBACK_URL,
      },
    });
  };

  const logoutUser = () => {
    logout({
      logoutParams: {
        returnTo: window.location.origin,
      },
    });
  };

  // Fungsi untuk membuat API calls dengan authorization header
  const makeAuthenticatedRequest = async (url, options = {}) => {
    if (!accessToken) {
      throw new Error('Tidak ada access token yang tersedia');
    }

    const authHeaders = {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
      ...options.headers,
    };

    const response = await fetch(url, {
      ...options,
      headers: authHeaders,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response;
  };

  const contextValue = {
    user,
    isAuthenticated,
    isLoading,
    accessToken,
    login,
    logout: logoutUser,
    makeAuthenticatedRequest,
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth harus digunakan dalam AuthProvider');
  }
  return context;
};

export default AuthContext;