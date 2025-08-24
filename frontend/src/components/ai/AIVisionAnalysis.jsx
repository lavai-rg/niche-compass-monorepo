import React, { useState, useRef } from 'react';
import axios from 'axios';
import './AIVisionAnalysis.css';

const AIVisionAnalysis = () => {
  const [imageInput, setImageInput] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedFeatures, setSelectedFeatures] = useState([
    'tags', 'captions', 'colors'
  ]);
  const [language, setLanguage] = useState('en');
  const fileInputRef = useRef(null);

  const availableFeatures = [
    { id: 'tags', label: 'Image Tags', description: 'Identify objects and concepts' },
    { id: 'captions', label: 'Image Captions', description: 'Generate descriptive captions' },
    { id: 'faces', label: 'Face Detection', description: 'Detect and analyze faces' },
    { id: 'objects', label: 'Object Detection', description: 'Identify specific objects' },
    { id: 'brands', label: 'Brand Detection', description: 'Recognize brand logos' },
    { id: 'landmarks', label: 'Landmark Detection', description: 'Identify famous landmarks' },
    { id: 'celebrities', label: 'Celebrity Recognition', description: 'Recognize famous people' },
    { id: 'colors', label: 'Color Analysis', description: 'Analyze dominant colors' },
    { id: 'imageType', label: 'Image Type', description: 'Determine image characteristics' },
    { id: 'adult', label: 'Content Moderation', description: 'Check for adult content' }
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
    { code: 'zh', name: 'Chinese' }
  ];

  const handleFeatureToggle = (featureId) => {
    setSelectedFeatures(prev => 
      prev.includes(featureId)
        ? prev.filter(f => f !== featureId)
        : [...prev, featureId]
    );
  };

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setImageInput('');
      setError(null);
    }
  };

  const handleUrlInput = (event) => {
    setImageInput(event.target.value);
    setSelectedFile(null);
    setError(null);
  };

  const handleAnalyze = async () => {
    if (!imageInput && !selectedFile) {
      setError('Please provide an image URL or select a file');
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
      let response;
      
      if (selectedFile) {
        // File upload
        const formData = new FormData();
        formData.append('image', selectedFile);
        formData.append('features', selectedFeatures.join(','));
        formData.append('language', language);
        
        response = await axios.post('/api/ai/vision/analyze', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
      } else {
        // URL analysis
        response = await axios.post('/api/ai/vision/analyze', {
          image_url: imageInput,
          features: selectedFeatures,
          language: language
        });
      }

      setAnalysisResult(response.data.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to analyze image');
      console.error('Error analyzing image:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setImageInput('');
    setSelectedFile(null);
    setAnalysisResult(null);
    setError(null);
    setSelectedFeatures(['tags', 'captions', 'colors']);
    setLanguage('en');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const formatConfidence = (confidence) => {
    return `${(confidence * 100).toFixed(1)}%`;
  };

  const getFeatureIcon = (featureId) => {
    const icons = {
      tags: '🏷️',
      captions: '📝',
      faces: '👤',
      objects: '📦',
      brands: '🏢',
      landmarks: '🗽',
      celebrities: '⭐',
      colors: '🎨',
      imageType: '🖼️',
      adult: '🔞'
    };
    return icons[featureId] || '🔍';
  };

  return (
    <div className="ai-vision-analysis">
      <div className="analysis-header">
        <h2>📸 AI Vision Analysis</h2>
        <p>Analyze images using Azure Computer Vision AI to extract insights, tags, and descriptions</p>
      </div>

      {/* Input Section */}
      <div className="input-section">
        <div className="input-tabs">
          <div className="input-tab">
            <input
              type="text"
              placeholder="Enter image URL..."
              value={imageInput}
              onChange={handleUrlInput}
              disabled={loading}
            />
            <span className="tab-label">Image URL</span>
          </div>
          
          <div className="input-tab">
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleFileSelect}
              disabled={loading}
            />
            <span className="tab-label">Upload File</span>
          </div>
        </div>

        {selectedFile && (
          <div className="file-preview">
            <img 
              src={URL.createObjectURL(selectedFile)} 
              alt="Preview" 
              className="file-preview-image"
            />
            <span className="file-name">{selectedFile.name}</span>
          </div>
        )}

        {imageInput && (
          <div className="url-preview">
            <img 
              src={imageInput} 
              alt="Preview" 
              className="url-preview-image"
              onError={(e) => {
                e.target.style.display = 'none';
                e.target.nextSibling.style.display = 'block';
              }}
            />
            <span className="url-text" style={{ display: 'none' }}>{imageInput}</span>
          </div>
        )}
      </div>

      {/* Configuration Section */}
      <div className="configuration-section">
        <div className="config-group">
          <h3>🔧 Analysis Features</h3>
          <div className="features-grid">
            {availableFeatures.map(feature => (
              <div 
                key={feature.id}
                className={`feature-item ${selectedFeatures.includes(feature.id) ? 'selected' : ''}`}
                onClick={() => handleFeatureToggle(feature.id)}
              >
                <div className="feature-icon">{getFeatureIcon(feature.id)}</div>
                <div className="feature-info">
                  <h4>{feature.label}</h4>
                  <p>{feature.description}</p>
                </div>
                <div className="feature-checkbox">
                  <input
                    type="checkbox"
                    checked={selectedFeatures.includes(feature.id)}
                    onChange={() => handleFeatureToggle(feature.id)}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="config-group">
          <h3>🌐 Language</h3>
          <select 
            value={language} 
            onChange={(e) => setLanguage(e.target.value)}
            disabled={loading}
            className="language-select"
          >
            {languages.map(lang => (
              <option key={lang.code} value={lang.code}>
                {lang.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="action-buttons">
        <button 
          onClick={handleAnalyze}
          disabled={loading || (!imageInput && !selectedFile)}
          className="analyze-button"
        >
          {loading ? '🔄 Analyzing...' : '🚀 Analyze Image'}
        </button>
        
        <button 
          onClick={handleReset}
          disabled={loading}
          className="reset-button"
        >
          🔄 Reset
        </button>
      </div>

      {/* Error Display */}
      {error && (
        <div className="error-message">
          <div className="error-icon">❌</div>
          <p>{error}</p>
        </div>
      )}

      {/* Results Section */}
      {analysisResult && (
        <div className="results-section">
          <h3>📊 Analysis Results</h3>
          
          <div className="result-summary">
            <div className="summary-item">
              <span className="label">Request ID:</span>
              <span className="value">{analysisResult.request_id}</span>
            </div>
            <div className="summary-item">
              <span className="label">Processing Time:</span>
              <span className="value">{analysisResult.processing_time_ms?.toFixed(2)}ms</span>
            </div>
            <div className="summary-item">
              <span className="label">Features Analyzed:</span>
              <span className="value">{analysisResult.features_analyzed?.length || 0}</span>
            </div>
          </div>

          {/* Tags */}
          {analysisResult.tags && analysisResult.tags.length > 0 && (
            <div className="result-group">
              <h4>🏷️ Image Tags</h4>
              <div className="tags-grid">
                {analysisResult.tags.map((tag, index) => (
                  <div key={index} className="tag-item">
                    <span className="tag-name">{tag.name}</span>
                    <span className="tag-confidence">
                      {formatConfidence(tag.confidence)}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Captions */}
          {analysisResult.captions && analysisResult.captions.length > 0 && (
            <div className="result-group">
              <h4>📝 Image Captions</h4>
              <div className="captions-list">
                {analysisResult.captions.map((caption, index) => (
                  <div key={index} className="caption-item">
                    <p className="caption-text">{caption.text}</p>
                    <span className="caption-confidence">
                      Confidence: {formatConfidence(caption.confidence)}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Colors */}
          {analysisResult.colors && (
            <div className="result-group">
              <h4>🎨 Color Analysis</h4>
              <div className="colors-section">
                <div className="color-info">
                  <span className="label">Dominant Colors:</span>
                  <div className="color-palette">
                    {analysisResult.colors.dominantColors?.map((color, index) => (
                      <div 
                        key={index} 
                        className="color-swatch"
                        style={{ backgroundColor: color }}
                        title={color}
                      />
                    ))}
                  </div>
                </div>
                <div className="color-info">
                  <span className="label">Black & White:</span>
                  <span className="value">
                    {analysisResult.colors.isBWImg ? 'Yes' : 'No'}
                  </span>
                </div>
              </div>
            </div>
          )}

          {/* Faces */}
          {analysisResult.faces && analysisResult.faces.length > 0 && (
            <div className="result-group">
              <h4>👤 Face Detection</h4>
              <div className="faces-info">
                <p>Detected {analysisResult.faces.length} face(s)</p>
                {analysisResult.faces.map((face, index) => (
                  <div key={index} className="face-item">
                    <span>Age: {face.age}</span>
                    <span>Gender: {face.gender}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Objects */}
          {analysisResult.objects && analysisResult.objects.length > 0 && (
            <div className="result-group">
              <h4>📦 Object Detection</h4>
              <div className="objects-grid">
                {analysisResult.objects.map((object, index) => (
                  <div key={index} className="object-item">
                    <span className="object-name">{object.object}</span>
                    <span className="object-confidence">
                      {formatConfidence(object.confidence)}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Error Message */}
          {analysisResult.error_message && (
            <div className="result-error">
              <h4>⚠️ Analysis Error</h4>
              <p>{analysisResult.error_message}</p>
            </div>
          )}
        </div>
      )}

      {/* Loading State */}
      {loading && (
        <div className="loading-overlay">
          <div className="loading-spinner">🔄</div>
          <p>Analyzing image with AI...</p>
        </div>
      )}
    </div>
  );
};

export default AIVisionAnalysis;
