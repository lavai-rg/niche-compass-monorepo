import { useState } from 'react'
import { Compass, TrendingUp, DollarSign, Users, Target, Loader2, AlertCircle, Palette, BarChart3 } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Alert, AlertDescription } from '@/components/ui/alert.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts'

const NicheAnalyzer = () => {
  const [searchQuery, setSearchQuery] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [nicheData, setNicheData] = useState(null)
  const [error, setError] = useState(null)

  const analyzeNiche = async () => {
    if (!searchQuery.trim()) return

    setIsLoading(true)
    setError(null)

    try {
      const response = await fetch('http://localhost:5000/api/niches/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ niche_name: searchQuery.trim() }),
      })

      if (!response.ok) {
        throw new Error('Failed to analyze niche')
      }

      const data = await response.json()
      setNicheData(data.niche_analysis)

    } catch (err) {
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      analyzeNiche()
    }
  }

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600'
    if (score >= 60) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getScoreBg = (score) => {
    if (score >= 80) return 'bg-green-100'
    if (score >= 60) return 'bg-yellow-100'
    return 'bg-red-100'
  }

  // Mock trending niches
  const trendingNiches = [
    { name: 'Sustainable Home Decor', growth_rate: 25.5, competition_score: 45, demand_score: 80 },
    { name: 'Minimalist Jewelry', growth_rate: 18.2, competition_score: 70, demand_score: 75 },
    { name: 'Pet Accessories', growth_rate: 22.1, competition_score: 60, demand_score: 85 },
    { name: 'Digital Art Prints', growth_rate: 31.8, competition_score: 55, demand_score: 78 },
  ]

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Niche Analyzer</h1>
        <p className="text-gray-600">Deep dive into niche opportunities and get comprehensive market analysis.</p>
      </div>

      {/* Search Section */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Compass className="h-5 w-5" />
            <span>Niche Analysis</span>
          </CardTitle>
          <CardDescription>
            Enter a niche to get detailed market analysis including trends, competition, and opportunities.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex space-x-2">
            <Input
              placeholder="Enter niche (e.g., sustainable home decor, handmade jewelry...)"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={handleKeyPress}
              className="flex-1"
            />
            <Button 
              onClick={analyzeNiche}
              disabled={isLoading || !searchQuery.trim()}
            >
              {isLoading ? (
                <Loader2 className="h-4 w-4 animate-spin mr-2" />
              ) : (
                <Compass className="h-4 w-4 mr-2" />
              )}
              Analyze
            </Button>
          </div>

          {error && (
            <Alert className="mt-4" variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}
        </CardContent>
      </Card>

      {/* Niche Analysis Results */}
      {nicheData && (
        <div className="space-y-6">
          {/* Overview Scores */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-lg flex items-center space-x-2">
                  <Target className="h-5 w-5" />
                  <span>Opportunity Score</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-center">
                  <div className={`text-4xl font-bold mb-2 ${getScoreColor((nicheData.demand_score + (100 - nicheData.competition_score)) / 2)}`}>
                    {Math.round((nicheData.demand_score + (100 - nicheData.competition_score)) / 2)}
                  </div>
                  <Progress 
                    value={(nicheData.demand_score + (100 - nicheData.competition_score)) / 2} 
                    className="mb-2"
                  />
                  <p className="text-sm text-gray-600">Overall market opportunity</p>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-lg flex items-center space-x-2">
                  <TrendingUp className="h-5 w-5" />
                  <span>Demand Score</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-center">
                  <div className={`text-4xl font-bold mb-2 ${getScoreColor(nicheData.demand_score)}`}>
                    {nicheData.demand_score}
                  </div>
                  <Progress value={nicheData.demand_score} className="mb-2" />
                  <p className="text-sm text-gray-600">Market demand level</p>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-lg flex items-center space-x-2">
                  <Users className="h-5 w-5" />
                  <span>Competition Score</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-center">
                  <div className={`text-4xl font-bold mb-2 ${getScoreColor(100 - nicheData.competition_score)}`}>
                    {nicheData.competition_score}
                  </div>
                  <Progress value={nicheData.competition_score} className="mb-2" />
                  <p className="text-sm text-gray-600">Competition intensity</p>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Detailed Analysis */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Trend Analysis */}
            {nicheData.trend_data && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <BarChart3 className="h-5 w-5" />
                    <span>Search Volume Trend</span>
                  </CardTitle>
                  <CardDescription>
                    Growth rate: {nicheData.trend_data.growth_rate}% | Seasonality: {nicheData.trend_data.seasonality}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={250}>
                    <LineChart data={nicheData.trend_data.months?.map((month, index) => ({
                      month,
                      volume: nicheData.trend_data.search_volume_trend?.[index] || 0
                    })) || []}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="month" />
                      <YAxis />
                      <Tooltip />
                      <Line 
                        type="monotone" 
                        dataKey="volume" 
                        stroke="#3B82F6" 
                        strokeWidth={2}
                        dot={{ fill: '#3B82F6' }}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            )}

            {/* Price Analysis */}
            {nicheData.price_analysis && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <DollarSign className="h-5 w-5" />
                    <span>Price Analysis</span>
                  </CardTitle>
                  <CardDescription>
                    Average price: ${nicheData.price_analysis.average_price} | Range: ${nicheData.price_analysis.price_range?.min}-${nicheData.price_analysis.price_range?.max}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {Object.entries(nicheData.price_analysis.price_distribution || {}).map(([range, percentage]) => (
                      <div key={range} className="flex items-center justify-between">
                        <span className="text-sm font-medium capitalize">
                          {range.replace('_', ' ').replace('under', 'Under $').replace('over', 'Over $').replace(/(\d+)/g, '$$$1')}
                        </span>
                        <div className="flex items-center space-x-2">
                          <Progress value={percentage} className="w-20" />
                          <span className="text-sm text-gray-600 w-8">{percentage}%</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Visual Analysis */}
          {nicheData.visual_analysis && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Palette className="h-5 w-5" />
                  <span>Visual Analysis</span>
                </CardTitle>
                <CardDescription>
                  Design trends and visual patterns in this niche
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  {/* Dominant Colors */}
                  <div>
                    <h4 className="font-medium mb-3">Dominant Colors</h4>
                    <div className="flex space-x-2">
                      {nicheData.visual_analysis.dominant_colors?.map((color, index) => (
                        <div key={index} className="flex flex-col items-center">
                          <div 
                            className="w-8 h-8 rounded-full border-2 border-gray-200"
                            style={{ backgroundColor: color }}
                          />
                          <span className="text-xs text-gray-600 mt-1">{color}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Popular Styles */}
                  <div>
                    <h4 className="font-medium mb-3">Popular Styles</h4>
                    <div className="space-y-1">
                      {nicheData.visual_analysis.popular_styles?.map((style, index) => (
                        <Badge key={index} variant="outline" className="mr-1 mb-1">
                          {style}
                        </Badge>
                      ))}
                    </div>
                  </div>

                  {/* Image Types */}
                  <div>
                    <h4 className="font-medium mb-3">Image Types</h4>
                    <div className="space-y-1">
                      {nicheData.visual_analysis.image_types?.map((type, index) => (
                        <Badge key={index} variant="outline" className="mr-1 mb-1">
                          {type.replace('_', ' ')}
                        </Badge>
                      ))}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      )}

      {/* Trending Niches */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <TrendingUp className="h-5 w-5" />
            <span>Trending Niches</span>
          </CardTitle>
          <CardDescription>
            High-opportunity niches that are gaining momentum
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {trendingNiches.map((niche, index) => (
              <div 
                key={index}
                className="p-4 border rounded-lg hover:shadow-md transition-shadow cursor-pointer"
                onClick={() => {
                  setSearchQuery(niche.name)
                  analyzeNiche()
                }}
              >
                <div className="flex items-center justify-between mb-3">
                  <h3 className="font-medium">{niche.name}</h3>
                  <Badge className="bg-green-100 text-green-800">
                    +{niche.growth_rate}%
                  </Badge>
                </div>
                
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-600">Demand</span>
                    <div className="flex items-center space-x-2">
                      <Progress value={niche.demand_score} className="w-16" />
                      <span className="w-8 text-right">{niche.demand_score}</span>
                    </div>
                  </div>
                  
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-600">Competition</span>
                    <div className="flex items-center space-x-2">
                      <Progress value={niche.competition_score} className="w-16" />
                      <span className="w-8 text-right">{niche.competition_score}</span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default NicheAnalyzer

