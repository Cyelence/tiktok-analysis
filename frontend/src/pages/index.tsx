import { useState, useEffect } from 'react'
import { ChartBarIcon, FireIcon, StarIcon } from '@heroicons/react/24/outline'
import axios from 'axios'

interface Trend {
  id: string
  name: string
  category: string
  momentum_score: number
  mention_count: number
  description: string
}

interface Brand {
  id: string
  name: string
  category: string[]
  price_range: string
  trending_score: number
}

interface Style {
  id: string
  name: string
  description: string
  popularity_score: number
  seasonality: string[]
}

export default function Dashboard() {
  const [trends, setTrends] = useState<Trend[]>([])
  const [brands, setBrands] = useState<Brand[]>([])
  const [styles, setStyles] = useState<Style[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [trendsRes, brandsRes, stylesRes] = await Promise.all([
          axios.get(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/trends`),
          axios.get(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/brands`),
          axios.get(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/styles`)
        ])

        setTrends(trendsRes.data.trends)
        setBrands(brandsRes.data.brands)
        setStyles(stylesRes.data.styles)
      } catch (error) {
        console.error('Error fetching data:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-pink-50 to-purple-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-pink-500 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading fashion trends...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 to-purple-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                Fashion Trend Discovery
              </h1>
              <p className="text-gray-600">Discover what's trending in fashion</p>
            </div>
            <div className="flex items-center space-x-4">
              <ChartBarIcon className="h-8 w-8 text-pink-500" />
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Trends Section */}
        <section className="mb-12">
          <div className="flex items-center mb-6">
            <FireIcon className="h-6 w-6 text-orange-500 mr-2" />
            <h2 className="text-2xl font-bold text-gray-900">Trending Now</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {trends.map((trend) => (
              <div key={trend.id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold text-gray-900">{trend.name}</h3>
                  <span className="px-2 py-1 text-xs font-medium bg-pink-100 text-pink-800 rounded-full">
                    {trend.category}
                  </span>
                </div>
                <p className="text-gray-600 mb-4">{trend.description}</p>
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div className="w-16 bg-gray-200 rounded-full h-2 mr-2">
                      <div 
                        className="bg-pink-500 h-2 rounded-full" 
                        style={{ width: `${trend.momentum_score * 100}%` }}
                      ></div>
                    </div>
                    <span className="text-sm text-gray-500">
                      {Math.round(trend.momentum_score * 100)}%
                    </span>
                  </div>
                  <span className="text-sm text-gray-500">
                    {trend.mention_count.toLocaleString()} mentions
                  </span>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Brands Section */}
        <section className="mb-12">
          <div className="flex items-center mb-6">
            <StarIcon className="h-6 w-6 text-yellow-500 mr-2" />
            <h2 className="text-2xl font-bold text-gray-900">Trending Brands</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {brands.map((brand) => (
              <div key={brand.id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">{brand.name}</h3>
                <div className="flex flex-wrap gap-1 mb-3">
                  {brand.category.map((cat) => (
                    <span key={cat} className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full">
                      {cat}
                    </span>
                  ))}
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-500 capitalize">{brand.price_range}</span>
                  <div className="flex items-center">
                    <div className="w-12 bg-gray-200 rounded-full h-2 mr-2">
                      <div 
                        className="bg-blue-500 h-2 rounded-full" 
                        style={{ width: `${brand.trending_score * 100}%` }}
                      ></div>
                    </div>
                    <span className="text-sm text-gray-500">
                      {Math.round(brand.trending_score * 100)}%
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Styles Section */}
        <section>
          <div className="flex items-center mb-6">
            <ChartBarIcon className="h-6 w-6 text-green-500 mr-2" />
            <h2 className="text-2xl font-bold text-gray-900">Popular Styles</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {styles.map((style) => (
              <div key={style.id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">{style.name}</h3>
                <p className="text-gray-600 mb-3">{style.description}</p>
                <div className="flex items-center justify-between">
                  <div className="flex flex-wrap gap-1">
                    {style.seasonality.map((season) => (
                      <span key={season} className="px-2 py-1 text-xs bg-green-100 text-green-800 rounded-full">
                        {season}
                      </span>
                    ))}
                  </div>
                  <div className="flex items-center">
                    <div className="w-12 bg-gray-200 rounded-full h-2 mr-2">
                      <div 
                        className="bg-green-500 h-2 rounded-full" 
                        style={{ width: `${style.popularity_score * 100}%` }}
                      ></div>
                    </div>
                    <span className="text-sm text-gray-500">
                      {Math.round(style.popularity_score * 100)}%
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>
      </main>
    </div>
  )
} 