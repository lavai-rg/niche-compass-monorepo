import { useState } from 'react'
import { Package, DollarSign, Star, TrendingUp, Users, Loader2, AlertCircle, ExternalLink, Tag, Calendar } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Alert, AlertDescription } from '@/components/ui/alert.jsx'
import { Progress } from '@/components/ui/progress.jsx'

const ProductAnalyzer = () => {
  const [productUrl, setProductUrl] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [productData, setProductData] = useState(null)
  const [error, setError] = useState(null)

  const analyzeProduct = async () => {
    if (!productUrl.trim()) return

    setIsLoading(true)
    setError(null)

    try {
      const response = await fetch("http://localhost:5000/api/analyze", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: productUrl.trim() }),
      })

      if (!response.ok) {
        throw new Error('Failed to analyze product')
      }

      const data = await response.json()
      setProductData(data.product_analysis)

    } catch (err) {
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      analyzeProduct()
    }
  }

  const getConfidenceColor = (level) => {
    switch (level) {
      case 'high': return 'text-green-600'
      case 'medium': return 'text-yellow-600'
      case 'low': return 'text-red-600'
      default: return 'text-gray-600'
    }
  }

  const getConfidenceBg = (level) => {
    switch (level) {
      case 'high': return 'bg-green-100 text-green-800'
      case 'medium': return 'bg-yellow-100 text-yellow-800'
      case 'low': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  // Mock trending products
  const trendingProducts = [
    { 
      title: 'Minimalist Gold Jewelry Set', 
      price: 45.99, 
      sales_estimate: 120, 
      rating: 4.8, 
      niche: 'minimalist_jewelry',
      revenue_estimate: 5519
    },
    { 
      title: 'Sustainable Bamboo Kitchen Set', 
      price: 32.50, 
      sales_estimate: 89, 
      rating: 4.6, 
      niche: 'eco_kitchen',
      revenue_estimate: 2892
    },
    { 
      title: 'Custom Pet Portrait Digital Art', 
      price: 28.00, 
      sales_estimate: 156, 
      rating: 4.9, 
      niche: 'pet_art',
      revenue_estimate: 4368
    },
  ]

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Product Analyzer</h1>
        <p className="text-gray-600">Analyze Etsy products to get sales estimates, competition insights, and optimization suggestions.</p>
      </div>

      {/* Search Section */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Package className="h-5 w-5" />
            <span>Product Analysis</span>
          </CardTitle>
          <CardDescription>
            Enter an Etsy product URL to get detailed analysis including sales estimates and market insights.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex space-x-2">
            <Input
              placeholder="Enter Etsy product URL (e.g., https://www.etsy.com/listing/123456/...)"
              value={productUrl}
              onChange={(e) => setProductUrl(e.target.value)}
              onKeyPress={handleKeyPress}
              className="flex-1"
            />
            <Button 
              onClick={analyzeProduct}
              disabled={isLoading || !productUrl.trim()}
            >
              {isLoading ? (
                <Loader2 className="h-4 w-4 animate-spin mr-2" />
              ) : (
                <Package className="h-4 w-4 mr-2" />
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

          <div className="mt-4 text-sm text-gray-500">
            <p><strong>Tip:</strong> Copy and paste any Etsy product URL to get instant analysis</p>
          </div>
        </CardContent>
      </Card>

      {/* Product Analysis Results */}
      {productData && (
        <div className="space-y-6">
          {/* Product Overview */}
          <Card>
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <CardTitle className="text-xl mb-2">{productData.title}</CardTitle>
                  <CardDescription className="flex items-center space-x-4">
                    <span>by {productData.store_name}</span>
                    <Badge variant="outline">{productData.niche?.replace('_', ' ')}</Badge>
                    <Badge variant="outline">{productData.category?.replace('_', ' ')}</Badge>
                  </CardDescription>
                </div>
                <Button variant="outline" size="sm" asChild>
                  <a href={productData.url} target="_blank" rel="noopener noreferrer">
                    <ExternalLink className="h-4 w-4 mr-2" />
                    View on Etsy
                  </a>
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600">${productData.price}</div>
                  <div className="text-sm text-gray-500">Price ({productData.currency})</div>
                </div>
                <div className="text-center">
                  <div className="flex items-center justify-center text-2xl font-bold text-yellow-600">
                    <Star className="h-6 w-6 mr-1 fill-current" />
                    {productData.rating}
                  </div>
                  <div className="text-sm text-gray-500">{productData.reviews_count} reviews</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">{productData.sales_estimate}</div>
                  <div className="text-sm text-gray-500">Est. Monthly Sales</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-600">
                    ${productData.sales_analysis?.estimated_monthly_revenue?.toLocaleString() || 'N/A'}
                  </div>
                  <div className="text-sm text-gray-500">Est. Monthly Revenue</div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Sales Analysis */}
          {productData.sales_analysis && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <TrendingUp className="h-5 w-5" />
                    <span>Sales Analysis</span>
                  </CardTitle>
                  <CardDescription>
                    Confidence: 
                    <Badge className={`ml-2 ${getConfidenceBg(productData.sales_analysis.confidence_level)}`}>
                      {productData.sales_analysis.confidence_level}
                    </Badge>
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Monthly Sales</span>
                    <span className="text-lg font-bold">{productData.sales_analysis.estimated_monthly_sales}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Monthly Revenue</span>
                    <span className="text-lg font-bold text-green-600">
                      ${productData.sales_analysis.estimated_monthly_revenue?.toLocaleString()}
                    </span>
                  </div>
                  
                  <div className="mt-4">
                    <h4 className="text-sm font-medium mb-2">Analysis Factors:</h4>
                    <div className="space-y-1">
                      {productData.sales_analysis.factors_considered?.map((factor, index) => (
                        <div key={index} className="flex items-center text-sm text-gray-600">
                          <div className="w-2 h-2 bg-blue-500 rounded-full mr-2" />
                          {factor}
                        </div>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Product Details */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Tag className="h-5 w-5" />
                    <span>Product Details</span>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {productData.listing_date && (
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium flex items-center">
                        <Calendar className="h-4 w-4 mr-2" />
                        Listed Date
                      </span>
                      <span className="text-sm">{new Date(productData.listing_date).toLocaleDateString()}</span>
                    </div>
                  )}
                  
                  <div>
                    <h4 className="text-sm font-medium mb-2">Tags:</h4>
                    <div className="flex flex-wrap gap-1">
                      {productData.tags?.slice(0, 8).map((tag, index) => (
                        <Badge key={index} variant="outline" className="text-xs">
                          {tag}
                        </Badge>
                      ))}
                      {productData.tags?.length > 8 && (
                        <Badge variant="outline" className="text-xs">
                          +{productData.tags.length - 8} more
                        </Badge>
                      )}
                    </div>
                  </div>

                  {productData.description && (
                    <div>
                      <h4 className="text-sm font-medium mb-2">Description:</h4>
                      <p className="text-sm text-gray-600 line-clamp-3">
                        {productData.description}
                      </p>
                    </div>
                  )}
                </CardContent>
              </Card>
            </div>
          )}

          {/* Images Preview */}
          {productData.images && productData.images.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle>Product Images</CardTitle>
                <CardDescription>Visual analysis of product presentation</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {productData.images.slice(0, 4).map((image, index) => (
                    <div key={index} className="aspect-square bg-gray-100 rounded-lg flex items-center justify-center">
                      <Package className="h-8 w-8 text-gray-400" />
                      <span className="text-xs text-gray-500 ml-2">Image {index + 1}</span>
                    </div>
                  ))}
                </div>
                <p className="text-sm text-gray-500 mt-2">
                  Note: Image analysis feature will be available in the next update
                </p>
              </CardContent>
            </Card>
          )}
        </div>
      )}

      {/* Trending Products */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <TrendingUp className="h-5 w-5" />
            <span>Trending Products</span>
          </CardTitle>
          <CardDescription>
            High-performing products across different niches
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {trendingProducts.map((product, index) => (
              <div 
                key={index}
                className="p-4 border rounded-lg hover:shadow-md transition-shadow cursor-pointer"
                onClick={() => {
                  setProductUrl(`https://www.etsy.com/listing/example-${index}/${product.title.toLowerCase().replace(/\s+/g, '-')}`)
                }}
              >
                <div className="flex items-start justify-between mb-2">
                  <h3 className="font-medium text-sm line-clamp-2 flex-1">{product.title}</h3>
                  <Badge variant="outline" className="ml-2 text-xs">
                    {product.niche.replace('_', ' ')}
                  </Badge>
                </div>
                
                <div className="grid grid-cols-2 gap-2 text-xs text-gray-600 mb-3">
                  <div className="flex items-center">
                    <DollarSign className="h-3 w-3 mr-1" />
                    ${product.price}
                  </div>
                  <div className="flex items-center">
                    <Star className="h-3 w-3 mr-1 fill-current text-yellow-500" />
                    {product.rating}
                  </div>
                  <div className="flex items-center">
                    <Package className="h-3 w-3 mr-1" />
                    {product.sales_estimate} sales/mo
                  </div>
                  <div className="flex items-center">
                    <TrendingUp className="h-3 w-3 mr-1" />
                    ${product.revenue_estimate}/mo
                  </div>
                </div>

                <Button size="sm" variant="outline" className="w-full">
                  Analyze Similar
                </Button>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default ProductAnalyzer

