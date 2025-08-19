import { useAuth } from '../../contexts/AuthContext';
import { Button } from '../ui/button';
import { LogOut } from 'lucide-react';

const LogoutButton = ({ className = "" }) => {
  const { logout } = useAuth();

  return (
    <Button 
      onClick={logout}
      className={`flex items-center gap-2 ${className}`}
      variant="outline"
    >
      <LogOut size={16} />
      Keluar
    </Button>
  );
};

export default LogoutButton;