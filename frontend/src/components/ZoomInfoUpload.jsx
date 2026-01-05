import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import './ZoomInfoUpload.css';

/**
 * Componente para subir archivos Excel de ZoomInfo
 * Capa 1+2: Ingesta → Contexto Empresarial
 */
const ZoomInfoUpload = ({ onUploadSuccess }) => {
  const [isUploading, setIsUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState(null);
  const [error, setError] = useState(null);

  const onDrop = useCallback(async (acceptedFiles) => {
    const file = acceptedFiles[0];
    if (!file) return;

    // Validar que sea Excel
    if (!file.name.match(/\.(xlsx|xls)$/)) {
      setError('Solo se aceptan archivos Excel (.xlsx, .xls)');
      return;
    }

    setIsUploading(true);
    setError(null);
    setUploadResult(null);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('http://localhost:8000/api/ingesta/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      setUploadResult(data);
      
      // Notificar al componente padre
      if (onUploadSuccess) {
        onUploadSuccess(data);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setIsUploading(false);
    }
  }, [onUploadSuccess]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'application/vnd.ms-excel': ['.xls']
    },
    maxFiles: 1
  });

  return (
    <div className="zoominfo-upload">
      <div className="upload-header">
        <h2>📤 Ingesta ZoomInfo</h2>
        <p>Sube un reporte Excel de ZoomInfo para iniciar el análisis</p>
      </div>

      <div 
        {...getRootProps()} 
        className={`dropzone ${isDragActive ? 'active' : ''} ${isUploading ? 'uploading' : ''}`}
      >
        <input {...getInputProps()} />
        
        {isUploading ? (
          <div className="upload-loading">
            <div className="spinner"></div>
            <p>Procesando archivo...</p>
            <small>Esto puede tomar unos segundos</small>
          </div>
        ) : (
          <>
            <div className="upload-icon">📊</div>
            <p className="upload-text">
              {isDragActive 
                ? 'Suelta el archivo aquí...' 
                : 'Arrastra un archivo Excel o haz clic para seleccionar'}
            </p>
            <small className="upload-hint">Formatos: .xlsx, .xls | Máximo: 1000 empresas</small>
          </>
        )}
      </div>

      {error && (
        <div className="upload-error">
          <span className="error-icon">⚠️</span>
          <span>{error}</span>
        </div>
      )}

      {uploadResult && (
        <div className="upload-success">
          <div className="success-header">
            <span className="success-icon">✅</span>
            <h3>Snapshot Creado</h3>
          </div>
          
          <div className="success-details">
            <div className="detail-row">
              <span className="label">Snapshot ID:</span>
              <code>{uploadResult.snapshot_id}</code>
            </div>
            <div className="detail-row">
              <span className="label">Empresas procesadas:</span>
              <strong>{uploadResult.empresas_count}</strong>
            </div>
            <div className="detail-row">
              <span className="label">Timestamp:</span>
              <span>{new Date(uploadResult.timestamp).toLocaleString('es-MX')}</span>
            </div>
          </div>

          <div className="dominios-list">
            <h4>🌐 Dominios extraídos ({uploadResult.dominios.length})</h4>
            <div className="dominios-grid">
              {uploadResult.dominios.map((dominio, idx) => (
                <div key={idx} className="dominio-chip">{dominio}</div>
              ))}
            </div>
          </div>

          <div className="next-step">
            <p>✨ Ahora puedes ejecutar el cruce semántico</p>
          </div>
        </div>
      )}

      {uploadResult && (
        <div className="upload-info">
          <h4>📋 Columnas soportadas del Excel ZoomInfo:</h4>
          <ul className="columns-list">
            <li><code>Company Name</code> / <code>company_name</code></li>
            <li><code>Website</code> / <code>website</code></li>
            <li><code>Industry</code> / <code>industry</code></li>
            <li><code>Employees</code> / <code>employee_range</code></li>
            <li><code>Revenue</code> / <code>revenue_range</code></li>
            <li><code>Employee Growth (YoY)</code></li>
            <li><code>Technologies</code></li>
          </ul>
        </div>
      )}
    </div>
  );
};

export default ZoomInfoUpload;
