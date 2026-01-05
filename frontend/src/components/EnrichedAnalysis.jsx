import React, { useState } from 'react';
import './EnrichedAnalysis.css';

/**
 * EnrichedAnalysis - Componente para mostrar análisis enriquecido con insights comerciales
 * 
 * Muestra:
 * - Executive summary
 * - Insights categorizados (críticos, warnings, ok)
 * - Inteligencia comercial (budget signals, tech stack)
 * - Sales talking points
 * - Estimación de deal size
 */
const EnrichedAnalysis = ({ analysis, onClose }) => {
  const [activeTab, setActiveTab] = useState('summary');

  if (!analysis) return null;

  const getStatusColor = (status) => {
    const colors = {
      critical: '#ef4444',
      warning: '#f59e0b',
      ok: '#10b981'
    };
    return colors[status] || '#6b7280';
  };

  const getUrgencyBadge = (urgency) => {
    const badges = {
      immediate: { label: '🔴 INMEDIATO', color: '#dc2626' },
      high: { label: '🟠 ALTA', color: '#ea580c' },
      medium: { label: '🟡 MEDIA', color: '#f59e0b' },
      low: { label: '🟢 BAJA', color: '#10b981' }
    };
    return badges[urgency] || badges.medium;
  };

  return (
    <div className="enriched-analysis-overlay" onClick={onClose}>
      <div className="enriched-analysis-modal" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="ea-header">
          <div className="ea-header-content">
            <h2>📊 Análisis Enriquecido - {analysis.domain}</h2>
            <div className="ea-meta">
              <span className="ea-industry">{analysis.industry}</span>
              <span className="ea-score" style={{ 
                color: analysis.score >= 70 ? '#10b981' : analysis.score >= 40 ? '#f59e0b' : '#ef4444' 
              }}>
                {analysis.score}/100
              </span>
              <span 
                className="ea-urgency"
                style={{ 
                  backgroundColor: getUrgencyBadge(analysis.urgency_level).color,
                  color: 'white',
                  padding: '4px 12px',
                  borderRadius: '12px',
                  fontSize: '0.85rem',
                  fontWeight: '600'
                }}
              >
                {getUrgencyBadge(analysis.urgency_level).label}
              </span>
            </div>
          </div>
          <button className="ea-close" onClick={onClose}>×</button>
        </div>

        {/* Tabs */}
        <div className="ea-tabs">
          <button 
            className={`ea-tab ${activeTab === 'summary' ? 'active' : ''}`}
            onClick={() => setActiveTab('summary')}
          >
            📋 Resumen
          </button>
          <button 
            className={`ea-tab ${activeTab === 'insights' ? 'active' : ''}`}
            onClick={() => setActiveTab('insights')}
          >
            🔍 Hallazgos ({analysis.insights.length})
          </button>
          <button 
            className={`ea-tab ${activeTab === 'commercial' ? 'active' : ''}`}
            onClick={() => setActiveTab('commercial')}
          >
            💼 Intel Comercial
          </button>
          <button 
            className={`ea-tab ${activeTab === 'sales' ? 'active' : ''}`}
            onClick={() => setActiveTab('sales')}
          >
            💰 Oportunidad
          </button>
        </div>

        {/* Content */}
        <div className="ea-content">
          {/* Summary Tab */}
          {activeTab === 'summary' && (
            <div className="ea-tab-content">
              <div className="ea-section">
                <h3>📊 Executive Summary</h3>
                <div className="ea-executive-summary">
                  <pre>{analysis.executive_summary}</pre>
                </div>
              </div>

              <div className="ea-section">
                <h3>🎯 Resumen Técnico</h3>
                <p className="ea-technical-summary">{analysis.technical_summary}</p>
              </div>

              <div className="ea-section">
                <h3>🔧 Tech Stack Detectado</h3>
                <div className="ea-tech-stack">
                  {analysis.commercial_intel.tech_stack.map((tech, idx) => (
                    <span key={idx} className="ea-tech-badge">{tech}</span>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Insights Tab */}
          {activeTab === 'insights' && (
            <div className="ea-tab-content">
              {analysis.insights.map((insight, idx) => (
                <div 
                  key={idx} 
                  className="ea-insight-card"
                  style={{ borderLeftColor: getStatusColor(insight.status) }}
                >
                  <div className="ea-insight-header">
                    <h4>{insight.title}</h4>
                    <span 
                      className="ea-insight-status"
                      style={{ backgroundColor: getStatusColor(insight.status) }}
                    >
                      {insight.status.toUpperCase()}
                    </span>
                  </div>

                  <div className="ea-insight-body">
                    <div className="ea-insight-section">
                      <strong>🔧 Detalle Técnico:</strong>
                      <p>{insight.technical_detail}</p>
                    </div>

                    <div className="ea-insight-section">
                      <strong>💼 Impacto Comercial:</strong>
                      <p>{insight.business_impact}</p>
                    </div>

                    {insight.cost_estimate && (
                      <div className="ea-insight-section">
                        <strong>💰 Estimación de Costos:</strong>
                        <ul>
                          {Object.entries(insight.cost_estimate).map(([key, value]) => (
                            <li key={key}>
                              <strong>{key.replace('_', ' ')}:</strong> {value}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    <div className="ea-insight-section">
                      <strong>✅ Recomendación:</strong>
                      <p>{insight.recommendation}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Commercial Intel Tab */}
          {activeTab === 'commercial' && (
            <div className="ea-tab-content">
              <div className="ea-section">
                <h3>💸 Señales de Presupuesto</h3>
                {analysis.commercial_intel.budget_signals.length > 0 ? (
                  <ul className="ea-budget-signals">
                    {analysis.commercial_intel.budget_signals.map((signal, idx) => (
                      <li key={idx}>✅ {signal}</li>
                    ))}
                  </ul>
                ) : (
                  <p className="ea-no-data">No se detectaron inversiones en seguridad.</p>
                )}
                <div className="ea-budget-estimate">
                  <strong>Presupuesto Anual Estimado:</strong> 
                  {analysis.commercial_intel.estimated_budget && 
                   analysis.commercial_intel.estimated_budget.min > 0 ? (
                    <span className="ea-budget-amount">
                      ${analysis.commercial_intel.estimated_budget.min.toLocaleString()} - 
                      ${analysis.commercial_intel.estimated_budget.max.toLocaleString()} USD/año
                    </span>
                  ) : (
                    <span className="ea-no-data"> No disponible</span>
                  )}
                </div>
              </div>

              <div className="ea-section">
                <h3>👥 Decision Makers</h3>
                <div className="ea-decision-makers">
                  {analysis.commercial_intel.decision_makers.map((dm, idx) => (
                    <span key={idx} className="ea-dm-badge">{dm}</span>
                  ))}
                </div>
              </div>

              <div className="ea-section">
                <h3>🎯 Pain Points Identificados</h3>
                <ul className="ea-pain-points">
                  {analysis.commercial_intel.pain_points.map((pain, idx) => (
                    <li key={idx}>⚠️ {pain}</li>
                  ))}
                </ul>
              </div>
            </div>
          )}

          {/* Sales Tab */}
          {activeTab === 'sales' && (
            <div className="ea-tab-content">
              <div className="ea-section">
                <h3>💬 Sales Talking Points</h3>
                <div className="ea-talking-points">
                  {analysis.sales_talking_points.map((point, idx) => (
                    <div key={idx} className="ea-talking-point">
                      <span className="ea-tp-number">{idx + 1}</span>
                      <p>{point}</p>
                    </div>
                  ))}
                </div>
              </div>

              <div className="ea-section">
                <h3>💰 Estimación de Deal Size</h3>
                <div className="ea-deal-size">
                  <div className="ea-deal-item">
                    <span className="ea-deal-label">Setup:</span>
                    <span className="ea-deal-value">{analysis.estimated_deal_size.setup}</span>
                  </div>
                  <div className="ea-deal-item">
                    <span className="ea-deal-label">Mensual:</span>
                    <span className="ea-deal-value">{analysis.estimated_deal_size.monthly}</span>
                  </div>
                  <div className="ea-deal-item">
                    <span className="ea-deal-label">Anual:</span>
                    <span className="ea-deal-value">{analysis.estimated_deal_size.annual}</span>
                  </div>
                  <div className="ea-deal-item">
                    <span className="ea-deal-label">Confianza:</span>
                    <span 
                      className="ea-deal-confidence"
                      style={{ 
                        color: analysis.estimated_deal_size.confidence === 'high' ? '#10b981' : '#f59e0b' 
                      }}
                    >
                      {analysis.estimated_deal_size.confidence === 'high' ? 'ALTA' : 'MEDIA'}
                    </span>
                  </div>
                </div>
              </div>

              <div className="ea-section">
                <h3>🎯 Ventaja Competitiva de ProspectScan</h3>
                <ul className="ea-competitive-advantage">
                  {analysis.commercial_intel.competitive_advantage.map((adv, idx) => (
                    <li key={idx}>✨ {adv}</li>
                  ))}
                </ul>
              </div>

              <div className="ea-section ea-action-section">
                <h3>🚀 Próximos Pasos</h3>
                <div className="ea-actions">
                  <button className="ea-action-btn primary">
                    📧 Generar Email de Outreach
                  </button>
                  <button className="ea-action-btn secondary">
                    🔗 Buscar en LinkedIn
                  </button>
                  <button className="ea-action-btn secondary">
                    📄 Exportar Reporte PDF
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="ea-footer">
          <span className="ea-timestamp">
            Analizado: {new Date(analysis.analyzed_at).toLocaleString('es-ES')}
          </span>
        </div>
      </div>
    </div>
  );
};

export default EnrichedAnalysis;
