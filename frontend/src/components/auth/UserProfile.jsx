import { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { Button } from '../ui/button';
import { Card, CardHeader, CardContent, CardTitle } from '../ui/card';
import { Avatar, AvatarFallback, AvatarImage } from '../ui/avatar';
import { Badge } from '../ui/badge';
import { Separator } from '../ui/separator';
import { User, Mail, Calendar, Settings } from 'lucide-react';
import LogoutButton from './LogoutButton';

const UserProfile = () => {
  const { user, isAuthenticated, isLoading } = useAuth();
  const [showSettings, setShowSettings] = useState(false);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-4">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!isAuthenticated || !user) {
    return null;
  }

  const getInitials = (name) => {
    return name
      ?.split(' ')
      .map(word => word[0])
      .join('')
      .toUpperCase()
      .slice(0, 2) || 'U';
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('id-ID', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader className="text-center">
        <div className="flex justify-center mb-4">
          <Avatar className="w-20 h-20">
            <AvatarImage src={user.picture} alt={user.name} />
            <AvatarFallback className="text-lg font-semibold">
              {getInitials(user.name)}
            </AvatarFallback>
          </Avatar>
        </div>
        <CardTitle className="text-xl font-bold">{user.name}</CardTitle>
        <p className="text-sm text-gray-600">{user.email}</p>
        <div className="flex justify-center mt-2">
          <Badge variant={user.email_verified ? "default" : "secondary"}>
            {user.email_verified ? 'Email Terverifikasi' : 'Email Belum Terverifikasi'}
          </Badge>
        </div>
      </CardHeader>

      <CardContent className="space-y-4">
        <Separator />
        
        <div className="space-y-3">
          <div className="flex items-center gap-3">
            <User size={16} className="text-gray-500" />
            <div>
              <p className="text-sm font-medium">Nama Pengguna</p>
              <p className="text-sm text-gray-600">{user.nickname || user.name}</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <Mail size={16} className="text-gray-500" />
            <div>
              <p className="text-sm font-medium">Email</p>
              <p className="text-sm text-gray-600">{user.email}</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <Calendar size={16} className="text-gray-500" />
            <div>
              <p className="text-sm font-medium">Bergabung Sejak</p>
              <p className="text-sm text-gray-600">
                {user.created_at ? formatDate(user.created_at) : 'Tidak diketahui'}
              </p>
            </div>
          </div>
        </div>

        <Separator />

        <div className="flex flex-col gap-2">
          <Button
            onClick={() => setShowSettings(!showSettings)}
            variant="outline"
            className="flex items-center gap-2"
          >
            <Settings size={16} />
            Pengaturan Profil
          </Button>
          
          <LogoutButton className="w-full" />
        </div>

        {showSettings && (
          <div className="mt-4 p-4 bg-gray-50 rounded-lg">
            <h4 className="font-medium mb-2">Informasi Debug</h4>
            <div className="text-xs space-y-1 text-gray-600">
              <p><strong>Sub:</strong> {user.sub}</p>
              <p><strong>Auth0 ID:</strong> {user.user_id || user.sub}</p>
              <p><strong>Login Terakhir:</strong> {user.updated_at ? formatDate(user.updated_at) : 'Tidak diketahui'}</p>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default UserProfile;