import { useState } from 'react'
import Header from './components/Header.jsx'
import Sidebar from './components/Sidebar.jsx'
import Dashboard from './components/Dashboard.jsx'
import KeywordExplorer from './components/KeywordExplorer.jsx'
import NicheAnalyzer from './components/NicheAnalyzer.jsx'
import ProductAnalyzer from './components/ProductAnalyzer.jsx'
import './App.css'

function App() {
  const [currentView, setCurrentView] = useState('dashboard')
  const [sidebarOpen, setSidebarOpen] = useState(false)

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

        {/* Main Content */}
        <main className="flex-1 min-h-screen">
          {renderCurrentView()}
        </main>
      </div>
    </div>
  )
}

export default App
