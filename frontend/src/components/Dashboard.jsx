import { TrendingUp, Search, Package, Target, ArrowUpRight, ArrowDownRight } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from 'recharts'

const Dashboard = ({ setCurrentView }) => {
  // Mock data for charts
  const searchTrendData = [
    { month: 'Jan', searches: 120 },
    { month: 'Feb', searches: 150 },
    { month: 'Mar', searches: 180 },
    { month: 'Apr', searches: 220 },
    { month: 'May', searches: 190 },
    { month: 'Jun', searches: 250 },
  ]

  const nichePerformanceData = [
    { niche: 'Handmade Jewelry', score: 85 },
    { niche: 'Home Decor', score: 72 },
    { niche: 'Pet Accessories', score: 68 },
    { niche: 'Art Prints', score: 61 },
    { niche: 'Phone Cases', score: 55 },
  ]

  const competitionData = [
    { name: 'Low Competition', value: 35, color: '#10B981' },
    { name: 'Medium Competition', value: 45, color: '#F59E0B' },
    { name: 'High Competition', value: 20, color: '#EF4444' },
  ]

  const stats = [
    {
      title: 'Keywords Analyzed',
      value: '1,247',
      change: '+12%',
      changeType: 'positive',
      icon: Search,
      description: 'This month'
    },
    {
      title: 'Niches Discovered',
      value: '89',
      change: '+8%',
      changeType: 'positive',
      icon: Target,
      description: 'Active opportunities'
    },
    {
      title: 'Products Tracked',
      value: '456',
      change: '-3%',
      changeType: 'negative',
      icon: Package,
      description: 'In watchlist'
    },
    {
      title: 'Success Rate',
      value: '73%',
      change: '+5%',
      changeType: 'positive',
      icon: TrendingUp,
      description: 'Profitable niches'
    },
  ]

  const recentInsights = [
    {
      title: 'Sustainable Home Decor Trending',
      description: 'Search volume increased 35% in the last 30 days',
      type: 'trending',
      action: 'Explore Niche'
    },
    {
      title: 'Low Competition Alert: Pet Jewelry',
      description: 'Only 12 competitors with high-quality listings',
      type: 'opportunity',
      action: 'Analyze Products'
    },
    {
      title: 'Seasonal Opportunity: Holiday Cards',
      description: 'Perfect timing to enter this niche',
      type: 'seasonal',
      action: 'View Keywords'
    },
  ]

  return (
    <div className="p-6 space-y-6">
      {/* Welcome Section */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Welcome back!</h1>
        <p className="text-gray-600">Here's what's happening with your Etsy research today.</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => {
          const Icon = stat.icon
          return (
            <Card key={index} className="hover:shadow-lg transition-shadow">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-gray-600">
                  {stat.title}
                </CardTitle>
                <Icon className="h-4 w-4 text-gray-400" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-gray-900 mb-1">{stat.value}</div>
                <div className="flex items-center text-sm">
                  {stat.changeType === 'positive' ? (
                    <ArrowUpRight className="h-4 w-4 text-green-500 mr-1" />
                  ) : (
                    <ArrowDownRight className="h-4 w-4 text-red-500 mr-1" />
                  )}
                  <span className={stat.changeType === 'positive' ? 'text-green-600' : 'text-red-600'}>
                    {stat.change}
                  </span>
                  <span className="text-gray-500 ml-1">{stat.description}</span>
                </div>
              </CardContent>
            </Card>
          )
        })}
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Search Trend Chart */}
        <Card>
          <CardHeader>
            <CardTitle>Search Trends</CardTitle>
            <CardDescription>Your research activity over time</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={searchTrendData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Line 
                  type="monotone" 
                  dataKey="searches" 
                  stroke="#3B82F6" 
                  strokeWidth={2}
                  dot={{ fill: '#3B82F6' }}
                />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Competition Distribution */}
        <Card>
          <CardHeader>
            <CardTitle>Competition Analysis</CardTitle>
            <CardDescription>Market competition distribution</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={competitionData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {competitionData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
            <div className="flex justify-center space-x-4 mt-4">
              {competitionData.map((item, index) => (
                <div key={index} className="flex items-center">
                  <div 
                    className="w-3 h-3 rounded-full mr-2"
                    style={{ backgroundColor: item.color }}
                  />
                  <span className="text-sm text-gray-600">{item.name}</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Niche Performance and Recent Insights */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Top Performing Niches */}
        <Card>
          <CardHeader>
            <CardTitle>Top Performing Niches</CardTitle>
            <CardDescription>Based on opportunity score</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={nichePerformanceData} layout="horizontal">
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" domain={[0, 100]} />
                <YAxis dataKey="niche" type="category" width={100} />
                <Tooltip />
                <Bar dataKey="score" fill="#3B82F6" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Recent Insights */}
        <Card>
          <CardHeader>
            <CardTitle>Recent Insights</CardTitle>
            <CardDescription>AI-powered recommendations</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {recentInsights.map((insight, index) => (
              <div key={index} className="flex items-start justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex-1">
                  <h4 className="font-medium text-gray-900 mb-1">{insight.title}</h4>
                  <p className="text-sm text-gray-600 mb-2">{insight.description}</p>
                  <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                    insight.type === 'trending' ? 'bg-green-100 text-green-800' :
                    insight.type === 'opportunity' ? 'bg-blue-100 text-blue-800' :
                    'bg-orange-100 text-orange-800'
                  }`}>
                    {insight.type}
                  </span>
                </div>
                <Button 
                  size="sm" 
                  variant="outline"
                  onClick={() => {
                    if (insight.action.includes('Niche')) setCurrentView('niches')
                    else if (insight.action.includes('Products')) setCurrentView('products')
                    else if (insight.action.includes('Keywords')) setCurrentView('keywords')
                  }}
                >
                  {insight.action}
                </Button>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle>Quick Actions</CardTitle>
          <CardDescription>Jump into your research</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Button 
              className="h-20 flex-col space-y-2"
              variant="outline"
              onClick={() => setCurrentView('keywords')}
            >
              <Search className="h-6 w-6" />
              <span>Explore Keywords</span>
            </Button>
            <Button 
              className="h-20 flex-col space-y-2"
              variant="outline"
              onClick={() => setCurrentView('niches')}
            >
              <Target className="h-6 w-6" />
              <span>Analyze Niche</span>
            </Button>
            <Button 
              className="h-20 flex-col space-y-2"
              variant="outline"
              onClick={() => setCurrentView('products')}
            >
              <Package className="h-6 w-6" />
              <span>Research Products</span>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default Dashboard

