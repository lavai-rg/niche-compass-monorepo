import { useAuth } from '../../contexts/AuthContext';
import LoginButton from './LoginButton';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Shield, Lock } from 'lucide-react';

const ProtectedRoute = ({ children, fallback = null }) => {
  const { isAuthenticated, isLoading } = useAuth();

  // Tampilkan loading spinner saat sedang memuat
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Memuat autentikasi...</p>
        </div>
      </div>
    );
  }

  // Jika tidak authenticated, tampilkan halaman login
  if (!isAuthenticated) {
    return fallback || (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
        <Card className="w-full max-w-md">
          <CardHeader className="text-center">
            <div className="flex justify-center mb-4">
              <div className="rounded-full bg-blue-100 p-3">
                <Lock className="w-8 h-8 text-blue-600" />
              </div>
            </div>
            <CardTitle className="text-xl font-bold">Akses Terbatas</CardTitle>
            <p className="text-gray-600 mt-2">
              Anda perlu masuk untuk mengakses fitur ini
            </p>
          </CardHeader>
          
          <CardContent className="space-y-4">
            <div className="bg-blue-50 p-4 rounded-lg">
              <div className="flex items-center gap-2 text-blue-800 mb-2">
                <Shield size={16} />
                <span className="font-medium">Keamanan Terjamin</span>
              </div>
              <p className="text-sm text-blue-700">
                Sistem autentikasi kami menggunakan Auth0 yang aman dan terpercaya
                untuk melindungi data Anda.
              </p>
            </div>
            
            <div className="space-y-2">
              <h4 className="font-medium">Dengan masuk, Anda dapat:</h4>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Mengakses analisis niche mendalam</li>
                <li>• Menyimpan hasil penelitian</li>
                <li>• Menggunakan fitur AI terbaru</li>
                <li>• Mengelola data produk Anda</li>
              </ul>
            </div>
            
            <LoginButton className="w-full py-2" />
            
            <p className="text-xs text-gray-500 text-center">
              Dengan masuk, Anda menyetujui syarat dan ketentuan kami
            </p>
          </CardContent>
        </Card>
      </div>
    );
  }

  // Jika authenticated, tampilkan konten
  return children;
};

export default ProtectedRoute;