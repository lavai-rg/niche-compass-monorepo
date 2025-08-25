import { useState, useEffect } from 'react'
import { Search, TrendingUp, Target, DollarSign, Lightbulb, Loader2, AlertCircle } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Alert, AlertDescription } from '@/components/ui/alert.jsx'
import { apiClient } from '../utils/axiosConfig'

const KeywordExplorer = () => {
  const [searchQuery, setSearchQuery] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [keywordData, setKeywordData] = useState(null)
  const [suggestions, setSuggestions] = useState([])
  const [trendingKeywords, setTrendingKeywords] = useState([])
  const [error, setError] = useState(null)

  // Mock trending keywords for initial load
  useEffect(() => {
    setTrendingKeywords([
      { keyword: 'sustainable jewelry', search_volume: 2500, competition_level: 'low', trend_direction: 'rising' },
      { keyword: 'minimalist home decor', search_volume: 3200, competition_level: 'medium', trend_direction: 'stable' },
      { keyword: 'personalized gifts', search_volume: 4100, competition_level: 'high', trend_direction: 'rising' },
      { keyword: 'handmade ceramics', search_volume: 1800, competition_level: 'low', trend_direction: 'rising' },
      { keyword: 'vintage art prints', search_volume: 2900, competition_level: 'medium', trend_direction: 'stable' },
    ])
  }, [])

  const analyzeKeyword = async () => {
    if (!searchQuery.trim()) return

    setIsLoading(true)
    setError(null)

    try {
      const response = await apiClient.analyzeKeyword(searchQuery.trim())
      setKeywordData(response.data.keyword_analysis)

      // Get suggestions (if endpoint exists)
      try {
        const suggestionsResponse = await apiClient.searchKeywords(searchQuery.trim())
        if (suggestionsResponse.data) {
          setSuggestions(suggestionsResponse.data.results || [])
        }
      } catch (suggestionsErr) {
        // Suggestions endpoint might not exist yet
        console.log('Suggestions not available:', suggestionsErr.message)
      }

    } catch (err) {
      setError(err.response?.data?.error || err.message || 'Failed to analyze keyword')
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      analyzeKeyword()
    }
  }

  const getCompetitionColor = (level) => {
    switch (level) {
      case 'low': return 'bg-green-100 text-green-800'
      case 'medium': return 'bg-yellow-100 text-yellow-800'
      case 'high': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getTrendColor = (direction) => {
    switch (direction) {
      case 'rising': return 'text-green-600'
      case 'stable': return 'text-blue-600'
      case 'declining': return 'text-red-600'
      default: return 'text-gray-600'
    }
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Keyword Explorer</h1>
        <p className="text-gray-600">Discover trending keywords and analyze their potential for your Etsy business.</p>
      </div>

      {/* Search Section */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Search className="h-5 w-5" />
            <span>Keyword Analysis</span>
          </CardTitle>
          <CardDescription>
            Enter a keyword to get detailed analysis including search volume, competition, and trends.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex space-x-2">
            <Input
              placeholder="Enter keyword (e.g., handmade jewelry, home decor...)"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={handleKeyPress}
              className="flex-1"
            />
            <Button 
              onClick={analyzeKeyword}
              disabled={isLoading || !searchQuery.trim()}
            >
              {isLoading ? (
                <Loader2 className="h-4 w-4 animate-spin mr-2" />
              ) : (
                <Search className="h-4 w-4 mr-2" />
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

      {/* Keyword Analysis Results */}
      {keywordData && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Analysis */}
          <div className="lg:col-span-2 space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span>"{keywordData.keyword}"</span>
                  <Badge className={getCompetitionColor(keywordData.competition_level)}>
                    {keywordData.competition_level} competition
                  </Badge>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-600">{keywordData.search_volume?.toLocaleString() || 'N/A'}</div>
                    <div className="text-sm text-gray-500">Monthly Searches</div>
                  </div>
                  <div className="text-center">
                    <div className={`text-2xl font-bold ${getTrendColor(keywordData.trend_direction)}`}>
                      <TrendingUp className="h-6 w-6 mx-auto mb-1" />
                    </div>
                    <div className="text-sm text-gray-500 capitalize">{keywordData.trend_direction}</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-600">
                      ${keywordData.price_range?.avg || 'N/A'}
                    </div>
                    <div className="text-sm text-gray-500">Avg Price</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-purple-600">
                      {keywordData.price_range ? `$${keywordData.price_range.min}-$${keywordData.price_range.max}` : 'N/A'}
                    </div>
                    <div className="text-sm text-gray-500">Price Range</div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Related Keywords */}
            {keywordData.related_keywords && keywordData.related_keywords.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Target className="h-5 w-5" />
                    <span>Related Keywords</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex flex-wrap gap-2">
                    {keywordData.related_keywords.map((keyword, index) => (
                      <Badge 
                        key={index} 
                        variant="outline" 
                        className="cursor-pointer hover:bg-blue-50"
                        onClick={() => {
                          setSearchQuery(keyword)
                          analyzeKeyword()
                        }}
                      >
                        {keyword}
                      </Badge>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Keyword Suggestions */}
          <div>
            {suggestions.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Lightbulb className="h-5 w-5" />
                    <span>Suggestions</span>
                  </CardTitle>
                  <CardDescription>
                    Related keywords you might want to explore
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-3">
                  {suggestions.map((suggestion, index) => (
                    <div 
                      key={index}
                      className="p-3 border rounded-lg hover:bg-gray-50 cursor-pointer transition-colors"
                      onClick={() => {
                        setSearchQuery(suggestion.keyword)
                        analyzeKeyword()
                      }}
                    >
                      <div className="font-medium text-sm">{suggestion.keyword}</div>
                      <div className="flex items-center justify-between text-xs text-gray-500 mt-1">
                        <span>{suggestion.search_volume?.toLocaleString()} searches</span>
                        <Badge size="sm" className={getCompetitionColor(suggestion.competition_level)}>
                          {suggestion.competition_level}
                        </Badge>
                      </div>
                    </div>
                  ))}
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      )}

      {/* Trending Keywords */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <TrendingUp className="h-5 w-5" />
            <span>Trending Keywords</span>
          </CardTitle>
          <CardDescription>
            Popular keywords that are gaining traction right now
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {trendingKeywords.map((keyword, index) => (
              <div 
                key={index}
                className="p-4 border rounded-lg hover:shadow-md transition-shadow cursor-pointer"
                onClick={() => {
                  setSearchQuery(keyword.keyword)
                  analyzeKeyword()
                }}
              >
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-medium text-sm">{keyword.keyword}</h3>
                  <Badge className={getCompetitionColor(keyword.competition_level)}>
                    {keyword.competition_level}
                  </Badge>
                </div>
                <div className="flex items-center justify-between text-xs text-gray-500">
                  <span>{keyword.search_volume?.toLocaleString()} searches</span>
                  <span className={`flex items-center ${getTrendColor(keyword.trend_direction)}`}>
                    <TrendingUp className="h-3 w-3 mr-1" />
                    {keyword.trend_direction}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default KeywordExplorer

