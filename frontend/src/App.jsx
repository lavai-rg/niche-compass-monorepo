import { useState, useEffect } from 'react'
import Header from './components/Header.jsx'
import Sidebar from './components/Sidebar.jsx'
import Dashboard from './components/Dashboard.jsx'
import KeywordExplorer from './components/KeywordExplorer.jsx'
import NicheAnalyzer from './components/NicheAnalyzer.jsx'
import ProductAnalyzer from './components/ProductAnalyzer.jsx'
import AIMonitoringDashboard from './components/ai/AIMonitoringDashboard.jsx'
import AIVisionAnalysis from './components/ai/AIVisionAnalysis.jsx'
import AITextAnalytics from './components/ai/AITextAnalytics.jsx'
import LoginForm from './components/auth/LoginForm.jsx'
import './App.css'

function App() {
  const [currentView, setCurrentView] = useState('dashboard')
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [user, setUser] = useState(null)
  const [showLogin, setShowLogin] = useState(false)

  // Check authentication status on app load
  useEffect(() => {
    const token = localStorage.getItem('authToken')
    const userData = localStorage.getItem('userData')
    
    if (token && userData) {
      setIsAuthenticated(true)
      setUser(JSON.parse(userData))
    }
  }, [])

  const handleLoginSuccess = (userData) => {
    setIsAuthenticated(true)
    setUser(userData)
    setShowLogin(false)
  }

  const handleLogout = () => {
    localStorage.removeItem('authToken')
    localStorage.removeItem('userData')
    setIsAuthenticated(false)
    setUser(null)
  }

  // Show login form if not authenticated
  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center max-w-md mx-auto px-6">
          <div className="text-6xl mb-6">🧭</div>
          <h1 className="text-3xl font-bold text-gray-900 mb-4">Niche Compass</h1>
          <p className="text-gray-600 mb-8">Etsy Research Platform</p>
          
          <button 
            onClick={() => setShowLogin(true)}
            className="bg-blue-600 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-blue-700 transition-colors"
          >
            🔑 Sign In to Continue
          </button>
          
          {showLogin && (
            <LoginForm 
              onLoginSuccess={handleLoginSuccess}
              onClose={() => setShowLogin(false)}
            />
          )}
        </div>
      </div>
    )
  }

  const renderCurrentView = () => {
    switch (currentView) {
      case 'keywords':
        return <KeywordExplorer />
      case 'niches':
        return <NicheAnalyzer />
      case 'products':
        return <ProductAnalyzer />
      case 'ai-vision':
        return <AIVisionAnalysis />
      case 'ai-monitoring':
        return <AIMonitoringDashboard />
      case 'ai-text':
        return <AITextAnalytics />
      case 'dashboard':
      default:
        return <Dashboard setCurrentView={setCurrentView} />
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <Header 
        onMenuClick={() => setSidebarOpen(true)}
        currentView={currentView}
        setCurrentView={setCurrentView}
        user={user}
        onLogout={handleLogout}
      />

      <div className="flex">
        {/* Sidebar */}
        <Sidebar 
          isOpen={sidebarOpen}
          onClose={() => setSidebarOpen(false)}
          currentView={currentView}
          setCurrentView={setCurrentView}
        />

        {/* Main Content */}
        <main className="flex-1 min-h-screen">
          {renderCurrentView()}
        </main>
      </div>
    </div>
  )
}

export default App
