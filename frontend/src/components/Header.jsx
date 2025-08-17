import { Compass, Search, TrendingUp, Package, Menu } from 'lucide-react'
import { Button } from '@/components/ui/button.jsx'

const Header = ({ onMenuClick, currentView, setCurrentView }) => {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: TrendingUp },
    { id: 'keywords', label: 'Keywords', icon: Search },
    { id: 'niches', label: 'Niches', icon: Compass },
    { id: 'products', label: 'Products', icon: Package },
  ]

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
        <div className="flex items-center space-x-2">
          <div className="hidden sm:block text-right">
            <p className="text-sm font-medium text-gray-900">Free Plan</p>
            <p className="text-xs text-gray-500">5/10 searches today</p>
          </div>
          <Button variant="outline" size="sm">
            Upgrade
          </Button>
        </div>
      </div>
    </header>
  )
}

export default Header

