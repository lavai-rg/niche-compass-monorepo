import { Compass, Search, TrendingUp, Package, X, BarChart3, Target, Lightbulb, Eye, FileText, Activity } from 'lucide-react'
import { Button } from '@/components/ui/button.jsx'

const Sidebar = ({ isOpen, onClose, currentView, setCurrentView }) => {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: TrendingUp, description: 'Overview & Analytics' },
    { id: 'keywords', label: 'Keyword Explorer', icon: Search, description: 'Research trending keywords' },
    { id: 'niches', label: 'Niche Analyzer', icon: Compass, description: 'Deep dive into niches' },
    { id: 'products', label: 'Product Analyzer', icon: Package, description: 'Analyze Etsy products' },
    { id: 'ai-vision', label: 'AI Vision Analysis', icon: Eye, description: 'Image analysis & insights' },
    { id: 'ai-text', label: 'AI Text Analytics', icon: FileText, description: 'Sentiment & entity analysis' },
    { id: 'ai-monitoring', label: 'AI Monitoring', icon: Activity, description: 'Service health & metrics' },
  ]

  const quickActions = [
    { id: 'trending', label: 'Trending Niches', icon: BarChart3, action: () => setCurrentView('niches') },
    { id: 'opportunities', label: 'AI Opportunities', icon: Target, action: () => setCurrentView('ai-vision') },
    { id: 'insights', label: 'Market Insights', icon: Lightbulb, action: () => setCurrentView('ai-text') },
  ]

  return (
    <>
      {/* Overlay for mobile */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-40 md:hidden"
          onClick={onClose}
        />
      )}
      
      {/* Sidebar */}
      <aside className={`
        fixed left-0 top-0 h-full w-64 bg-white border-r border-gray-200 z-50 transform transition-transform duration-300 ease-in-out
        ${isOpen ? 'translate-x-0' : '-translate-x-full'}
        md:relative md:translate-x-0
      `}>
        <div className="flex flex-col h-full">
          {/* Header */}
          <div className="flex items-center justify-between p-4 border-b border-gray-200">
            <div className="flex items-center space-x-2">
              <div className="bg-blue-600 p-2 rounded-lg">
                <Compass className="h-5 w-5 text-white" />
              </div>
              <div>
                <h2 className="font-semibold text-gray-900">Niche Compass</h2>
                <p className="text-xs text-gray-500">Research Platform</p>
              </div>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={onClose}
              className="md:hidden"
            >
              <X className="h-4 w-4" />
            </Button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 p-4 space-y-2">
            <div className="mb-6">
              <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
                Main Features
              </h3>
              {navItems.map((item) => {
                const Icon = item.icon
                return (
                  <Button
                    key={item.id}
                    variant={currentView === item.id ? "default" : "ghost"}
                    onClick={() => {
                      setCurrentView(item.id)
                      onClose()
                    }}
                    className="w-full justify-start h-auto p-3 flex-col items-start"
                  >
                    <div className="flex items-center space-x-3 w-full">
                      <Icon className="h-4 w-4 flex-shrink-0" />
                      <div className="text-left">
                        <div className="font-medium">{item.label}</div>
                        <div className="text-xs text-muted-foreground">{item.description}</div>
                      </div>
                    </div>
                  </Button>
                )
              })}
            </div>

            <div>
              <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
                Quick Actions
              </h3>
              {quickActions.map((item) => {
                const Icon = item.icon
                return (
                  <Button
                    key={item.id}
                    variant="ghost"
                    onClick={() => {
                      // Handle quick actions
                      item.action()
                      onClose()
                    }}
                    className="w-full justify-start"
                  >
                    <Icon className="h-4 w-4 mr-3" />
                    {item.label}
                  </Button>
                )
              })}
            </div>
          </nav>

          {/* Footer */}
          <div className="p-4 border-t border-gray-200">
            <div className="bg-blue-50 rounded-lg p-3">
              <h4 className="text-sm font-medium text-blue-900 mb-1">Free Plan</h4>
              <p className="text-xs text-blue-700 mb-2">5 of 10 searches used today</p>
              <div className="w-full bg-blue-200 rounded-full h-2 mb-2">
                <div className="bg-blue-600 h-2 rounded-full" style={{ width: '50%' }}></div>
              </div>
              <Button size="sm" className="w-full">
                Upgrade to Pro
              </Button>
            </div>
          </div>
        </div>
      </aside>
    </>
  )
}

export default Sidebar

