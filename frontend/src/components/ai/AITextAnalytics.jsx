import React, { useState } from 'react';
import axios from 'axios';
import './AITextAnalytics.css';

const AITextAnalytics = () => {
  const [textInput, setTextInput] = useState('');
  const [analysisResult, setAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedFeatures, setSelectedFeatures] = useState(['sentiment', 'key_phrases', 'entities']);
  const [language, setLanguage] = useState('en');

  const features = [
    { id: 'sentiment', label: 'Sentiment Analysis', description: 'Analyze text sentiment (positive, negative, neutral)' },
    { id: 'key_phrases', label: 'Key Phrases', description: 'Extract important phrases and concepts' },
    { id: 'entities', label: 'Entity Recognition', description: 'Identify people, places, organizations' },
    { id: 'language', label: 'Language Detection', description: 'Detect text language automatically' },
    { id: 'pii', label: 'PII Detection', description: 'Detect personally identifiable information' },
    { id: 'summarization', label: 'Text Summarization', description: 'Generate text summaries' }
  ];

  const languages = [
    { code: 'en', name: 'English' },
    { code: 'es', name: 'Spanish' },
    { code: 'fr', name: 'French' },
    { code: 'de', name: 'German' },
    { code: 'it', name: 'Italian' },
    { code: 'pt', name: 'Portuguese' },
    { code: 'ja', name: 'Japanese' },
    { code: 'ko', name: 'Korean' },
    { code: 'zh', name: 'Chinese' },
    { code: 'ar', name: 'Arabic' }
  ];

  const handleFeatureToggle = (featureId) => {
    setSelectedFeatures(prev => 
      prev.includes(featureId)
        ? prev.filter(id => id !== featureId)
        : [...prev, featureId]
    );
  };

  const handleAnalyze = async () => {
    if (!textInput.trim()) {
      setError('Please enter some text to analyze');
      return;
    }

    if (selectedFeatures.length === 0) {
      setError('Please select at least one analysis feature');
      return;
    }

    setLoading(true);
    setError(null);
    setAnalysisResult(null);

    try {
      const response = await axios.post('/api/ai/text/analyze', {
        text: textInput,
        features: selectedFeatures,
        language: language
      });

      if (response.data.success) {
        setAnalysisResult(response.data.result);
      } else {
        setError(response.data.error || 'Analysis failed');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to analyze text');
    } finally {
      setLoading(false);
    }
  };

  const handleQuickAnalyze = async (feature) => {
    if (!textInput.trim()) {
      setError('Please enter some text first');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await axios.post(`/api/ai/text/${feature}`, {
        text: textInput,
        language: language
      });

      if (response.data.success) {
        setAnalysisResult(response.data.result);
        setSelectedFeatures([feature]);
      } else {
        setError(response.data.error || 'Analysis failed');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to analyze text');
    } finally {
      setLoading(false);
    }
  };

  const getSentimentColor = (sentiment) => {
    switch (sentiment?.toLowerCase()) {
      case 'positive': return 'text-green-600';
      case 'negative': return 'text-red-600';
      case 'neutral': return 'text-gray-600';
      default: return 'text-gray-600';
    }
  };

  const getSentimentIcon = (sentiment) => {
    switch (sentiment?.toLowerCase()) {
      case 'positive': return '😊';
      case 'negative': return '😞';
      case 'neutral': return '😐';
      default: return '🤔';
    }
  };

  return (
    <div className="ai-text-analytics">
      <div className="container mx-auto px-4 py-6">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">AI Text Analytics</h1>
          <p className="text-gray-600">
            Analyze text sentiment, extract key phrases, identify entities, and more using Azure AI services
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Input Section */}
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Text Input</h2>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Enter your text
                  </label>
                  <textarea
                    value={textInput}
                    onChange={(e) => setTextInput(e.target.value)}
                    placeholder="Enter text to analyze (e.g., product reviews, social media posts, articles)..."
                    className="w-full h-32 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    {textInput.length} characters
                  </p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Language
                  </label>
                  <select
                    value={language}
                    onChange={(e) => setLanguage(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    {languages.map(lang => (
                      <option key={lang.code} value={lang.code}>
                        {lang.name}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Analysis Features
                  </label>
                  <div className="grid grid-cols-2 gap-2">
                    {features.map(feature => (
                      <label key={feature.id} className="flex items-center space-x-2 cursor-pointer">
                        <input
                          type="checkbox"
                          checked={selectedFeatures.includes(feature.id)}
                          onChange={() => handleFeatureToggle(feature.id)}
                          className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                        />
                        <span className="text-sm text-gray-700">{feature.label}</span>
                      </label>
                    ))}
                  </div>
                </div>

                <div className="flex space-x-3">
                  <button
                    onClick={handleAnalyze}
                    disabled={loading || !textInput.trim() || selectedFeatures.length === 0}
                    className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {loading ? 'Analyzing...' : 'Analyze Text'}
                  </button>
                </div>

                {/* Quick Analysis Buttons */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Quick Analysis
                  </label>
                  <div className="flex flex-wrap gap-2">
                    <button
                      onClick={() => handleQuickAnalyze('sentiment')}
                      disabled={loading || !textInput.trim()}
                      className="px-3 py-1 text-sm bg-green-100 text-green-700 rounded-md hover:bg-green-200 disabled:opacity-50"
                    >
                      Sentiment
                    </button>
                    <button
                      onClick={() => handleQuickAnalyze('key-phrases')}
                      disabled={loading || !textInput.trim()}
                      className="px-3 py-1 text-sm bg-blue-100 text-blue-700 rounded-md hover:bg-blue-200 disabled:opacity-50"
                    >
                      Key Phrases
                    </button>
                    <button
                      onClick={() => handleQuickAnalyze('entities')}
                      disabled={loading || !textInput.trim()}
                      className="px-3 py-1 text-sm bg-purple-100 text-purple-700 rounded-md hover:bg-purple-200 disabled:opacity-50"
                    >
                      Entities
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Results Section */}
          <div className="space-y-6">
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <div className="flex">
                  <div className="text-red-400">⚠️</div>
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-red-800">Error</h3>
                    <p className="text-sm text-red-700 mt-1">{error}</p>
                  </div>
                </div>
              </div>
            )}

            {loading && (
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <div className="flex items-center justify-center py-8">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                  <span className="ml-3 text-gray-600">Analyzing text...</span>
                </div>
              </div>
            )}

            {analysisResult && (
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Analysis Results</h2>
                
                <div className="space-y-4">
                  {/* Sentiment */}
                  {analysisResult.sentiment && (
                    <div className="border border-gray-200 rounded-lg p-4">
                      <h3 className="text-lg font-medium text-gray-900 mb-2">Sentiment Analysis</h3>
                      <div className="flex items-center space-x-3">
                        <span className="text-2xl">{getSentimentIcon(analysisResult.sentiment.overall)}</span>
                        <div>
                          <p className={`text-lg font-semibold ${getSentimentColor(analysisResult.sentiment.overall)}`}>
                            {analysisResult.sentiment.overall}
                          </p>
                          <p className="text-sm text-gray-600">
                            Confidence: {Math.round(analysisResult.sentiment.confidence * 100)}%
                          </p>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Key Phrases */}
                  {analysisResult.key_phrases && analysisResult.key_phrases.length > 0 && (
                    <div className="border border-gray-200 rounded-lg p-4">
                      <h3 className="text-lg font-medium text-gray-900 mb-2">Key Phrases</h3>
                      <div className="flex flex-wrap gap-2">
                        {analysisResult.key_phrases.map((phrase, index) => (
                          <span
                            key={index}
                            className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm"
                          >
                            {phrase}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Entities */}
                  {analysisResult.entities && analysisResult.entities.length > 0 && (
                    <div className="border border-gray-200 rounded-lg p-4">
                      <h3 className="text-lg font-medium text-gray-900 mb-2">Entities</h3>
                      <div className="space-y-2">
                        {analysisResult.entities.map((entity, index) => (
                          <div key={index} className="flex items-center justify-between">
                            <span className="font-medium">{entity.text}</span>
                            <span className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs">
                              {entity.type}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Language */}
                  {analysisResult.language && (
                    <div className="border border-gray-200 rounded-lg p-4">
                      <h3 className="text-lg font-medium text-gray-900 mb-2">Language Detection</h3>
                      <p className="text-gray-700">
                        Detected language: <span className="font-medium">{analysisResult.language.name}</span>
                        {analysisResult.language.confidence && (
                          <span className="text-sm text-gray-500 ml-2">
                            (Confidence: {Math.round(analysisResult.language.confidence * 100)}%)
                          </span>
                        )}
                      </p>
                    </div>
                  )}

                  {/* Raw Data */}
                  <details className="border border-gray-200 rounded-lg">
                    <summary className="px-4 py-3 cursor-pointer text-sm font-medium text-gray-700 hover:bg-gray-50">
                      View Raw Data
                    </summary>
                    <div className="px-4 pb-4">
                      <pre className="text-xs text-gray-600 bg-gray-50 p-3 rounded overflow-auto">
                        {JSON.stringify(analysisResult, null, 2)}
                      </pre>
                    </div>
                  </details>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AITextAnalytics;
