import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom';
import DomainHeatmap from './components/DomainHeatmap';
import ZoomInfoUpload from './components/ZoomInfoUpload';
import CrucePipeline from './components/CrucePipeline';
import { mockDomains } from './utils/mockData';
import './App.css';

/**
 * App principal - ProspectScan Unificado
 * Combina Heatmap + Ingesta ZoomInfo + Pipeline de Cruce
 */
function App() {
  const [currentSnapshot, setCurrentSnapshot] = useState(null);

  const handleUploadSuccess = (uploadResult) => {
    setCurrentSnapshot(uploadResult.snapshot_id);
  };

  return (
    <Router>
      <div className="App">
        <nav className="app-nav">
          <div className="nav-brand">
            <h1>🎯 ProspectScan</h1>
            <p className="nav-subtitle">Contextual Decision Intelligence</p>
          </div>
          <div className="nav-links">
            <Link to="/ingesta" className="nav-link">
              📤 Ingesta ZoomInfo
            </Link>
            <Link to="/cruce" className="nav-link">
              🔄 Pipeline Cruce
            </Link>
            <Link to="/heatmap" className="nav-link">
              🗺️ Heatmap
            </Link>
          </div>
        </nav>

        <main className="app-main">
          <Routes>
            <Route path="/" element={<Navigate to="/ingesta" replace />} />
            
            <Route 
              path="/ingesta" 
              element={<ZoomInfoUpload onUploadSuccess={handleUploadSuccess} />} 
            />
            
            <Route 
              path="/cruce" 
              element={<CrucePipeline snapshotId={currentSnapshot} />} 
            />
            
            <Route 
              path="/heatmap" 
              element={<DomainHeatmap initialDomains={mockDomains} />} 
            />
          </Routes>
        </main>

        <footer className="app-footer">
          <p>ProspectScan v1.0 - Enero 2026 | 
            <a href="/docs" target="_blank"> Documentación</a> | 
            <a href="https://github.com/B10sp4rt4n/ProspectScan" target="_blank"> GitHub</a>
          </p>
        </footer>
      </div>
    </Router>
  );
}

export default App;
