import { useState } from 'react'
import { useAuth0 } from '@auth0/auth0-react'
import { AuthProvider } from './contexts/AuthContext.jsx'
import Header from './components/Header.jsx'
import Sidebar from './components/Sidebar.jsx'
import Dashboard from './components/Dashboard.jsx'
import KeywordExplorer from './components/KeywordExplorer.jsx'
import NicheAnalyzer from './components/NicheAnalyzer.jsx'
import ProductAnalyzer from './components/ProductAnalyzer.jsx'
import ProtectedRoute from './components/auth/ProtectedRoute.jsx'
import './App.css'

function App() {
  const [currentView, setCurrentView] = useState('dashboard')
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const { isLoading, error } = useAuth0()

  // Tampilkan loading screen saat Auth0 masih memuat
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <h2 className="text-xl font-semibold text-gray-700 mb-2">Niche Compass</h2>
          <p className="text-gray-600">Memuat aplikasi...</p>
        </div>
      </div>
    )
  }

  // Tampilkan error jika ada masalah dengan Auth0
  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="text-red-500 text-6xl mb-4">⚠️</div>
          <h2 className="text-xl font-semibold text-gray-700 mb-2">Terjadi Kesalahan</h2>
          <p className="text-gray-600 mb-4">Error: {error.message}</p>
          <button 
            onClick={() => window.location.reload()} 
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Muat Ulang
          </button>
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
      case 'dashboard':
      default:
        return <Dashboard setCurrentView={setCurrentView} />
    }
  }

  return (
    <AuthProvider>
      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <Header 
          onMenuClick={() => setSidebarOpen(true)}
          currentView={currentView}
          setCurrentView={setCurrentView}
        />

        <div className="flex">
          {/* Sidebar */}
          <Sidebar 
            isOpen={sidebarOpen}
            onClose={() => setSidebarOpen(false)}
            currentView={currentView}
            setCurrentView={setCurrentView}
          />

          {/* Main Content - Dengan Proteksi Auth */}
          <main className="flex-1 min-h-screen">
            <ProtectedRoute>
              {renderCurrentView()}
            </ProtectedRoute>
          </main>
        </div>
      </div>
    </AuthProvider>
  )
}

export default App
