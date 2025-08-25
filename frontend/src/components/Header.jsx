import { Compass, Search, TrendingUp, Package, Menu, User } from 'lucide-react'
import { Button } from '../components/ui/button.jsx'
import { Avatar, AvatarFallback, AvatarImage } from '../components/ui/avatar.jsx'

const Header = ({ onMenuClick, currentView, setCurrentView, user, onLogout }) => {
  const isAuthenticated = !!user
  
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: TrendingUp },
    { id: 'keywords', label: 'Keywords', icon: Search },
    { id: 'niches', label: 'Niches', icon: Compass },
    { id: 'products', label: 'Products', icon: Package },
  ]

  const getInitials = (name) => {
    return name
      ?.split(' ')
      .map(word => word[0])
      .join('')
      .toUpperCase()
      .slice(0, 2) || 'U'
  }

  return (
    <header className="bg-white border-b border-gray-200 px-6 py-4">
      <div className="flex items-center justify-between">
        {/* Logo and Brand */}
        <div className="flex items-center space-x-4">
          <Button
            variant="ghost"
            size="sm"
            onClick={onMenuClick}
            className="md:hidden"
          >
            <Menu className="h-5 w-5" />
          </Button>
          
          <div className="flex items-center space-x-2">
            <div className="bg-blue-600 p-2 rounded-lg">
              <Compass className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">Niche Compass</h1>
              <p className="text-sm text-gray-500">Etsy Research Platform</p>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <nav className="hidden md:flex items-center space-x-1">
          {navItems.map((item) => {
            const Icon = item.icon
            return (
              <Button
                key={item.id}
                variant={currentView === item.id ? "default" : "ghost"}
                onClick={() => setCurrentView(item.id)}
                className="flex items-center space-x-2"
              >
                <Icon className="h-4 w-4" />
                <span>{item.label}</span>
              </Button>
            )
          })}
        </nav>

        {/* User Actions */}
        <div className="flex items-center space-x-3">
          {isAuthenticated ? (
            <>
              <div className="hidden sm:block text-right">
                <p className="text-sm font-medium text-gray-900">Free Plan</p>
                <p className="text-xs text-gray-500">5/10 pencarian hari ini</p>
              </div>
              
              <Button variant="outline" size="sm">
                Upgrade
              </Button>

              <div className="flex items-center space-x-2">
                <Avatar className="w-8 h-8">
                  <AvatarImage src={user?.picture} alt={user?.name} />
                  <AvatarFallback className="text-xs">
                    {getInitials(user?.name)}
                  </AvatarFallback>
                </Avatar>
                <div className="hidden md:block">
                  <p className="text-sm font-medium text-gray-900">{user?.name}</p>
                  <p className="text-xs text-gray-500">{user?.email}</p>
                </div>
              </div>

              <Button 
                variant="outline" 
                size="sm" 
                onClick={onLogout}
                className="text-red-600 hover:text-red-700 border-red-200 hover:border-red-300"
              >
                🚪 Logout
              </Button>
            </>
          ) : (
            <div className="flex items-center space-x-2">
              <div className="hidden sm:block text-right">
                <p className="text-sm font-medium text-gray-900">Pengunjung</p>
                <p className="text-xs text-gray-500">Masuk untuk akses penuh</p>
              </div>
              <Button 
                variant="default" 
                size="sm"
                className="bg-blue-600 hover:bg-blue-700"
              >
                🔑 Sign In
              </Button>
            </div>
          )}
        </div>
      </div>
    </header>
  )
}

export default Header

