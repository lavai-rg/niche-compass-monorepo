import { useAuth } from '../../contexts/AuthContext';
import { Button } from '../ui/button';
import { LogIn } from 'lucide-react';

const LoginButton = ({ className = "" }) => {
  const { login, isLoading } = useAuth();

  return (
    <Button 
      onClick={login}
      disabled={isLoading}
      className={`flex items-center gap-2 ${className}`}
      variant="default"
    >
      <LogIn size={16} />
      {isLoading ? 'Memuat...' : 'Masuk'}
    </Button>
  );
};

export default LoginButton;