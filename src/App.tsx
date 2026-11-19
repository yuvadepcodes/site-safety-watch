import { useEffect, useState } from 'react';

export default function App() {
  const [isFullscreen, setIsFullscreen] = useState(false);

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape' && isFullscreen) {
        setIsFullscreen(false);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isFullscreen]);

  const [stats] = useState({
    total_workers: 24,
    active_violations: 3,
    status: 'Monitoring Live',
    site: 'Sector 7 - Construction Site',
    shift: 'Night shift · 22:14',
  });

  const [report] = useState({
    date: 'Fri, Oct 30, 2026',
    site_name: 'Sector 7 Construction Site',
    total_scans: 1420,
    ppe_compliance_rate: '94.5%',
    critical_incidents_logged: 2,
    recommendations: [
      'Ensure all personnel wear high-visibility vests near zone B.',
      'Inspect harness anchor points on level 3 scaffolding.',
      'Increase lighting coverage around the concrete batching area.',
    ],
  });

  const overview = [
    { label: 'Workers on site', value: '24', delta: '+3 vs yesterday', tone: 'emerald' },
    { label: 'Incidents flagged', value: '3', delta: '2 resolved today', tone: 'amber' },
    { label: 'Detection uptime', value: '99.8%', delta: 'Stable signal', tone: 'cyan' },
  ];

  const riskSignals = [
    { title: 'Missing PPE', detail: 'Zone B · 4 personnel', severity: 'High' },
    { title: 'Unsafe scaffolding', detail: 'Level 3 · anchor check due', severity: 'Medium' },
    { title: 'Restricted zone entry', detail: 'Warehouse gate · 1 breach', severity: 'Low' },
  ];

  const complianceBars = [
    { label: 'Hard hats', value: 96 },
    { label: 'Hi-vis vests', value: 89 },
    { label: 'Harness checks', value: 92 },
    { label: 'Gate compliance', value: 97 },
  ];

  if (isFullscreen) {
    return (
      <div className="fullscreen-video-shell">
        <button
          className="fullscreen-close"
          onClick={() => setIsFullscreen(false)}
          aria-label="Close fullscreen camera"
        >
          ×
        </button>

        <img
          src="http://127.0.0.1:8000/video_feed"
          alt="Live Site Safety Stream"
          className="fullscreen-video"
          onError={(e) => {
            e.currentTarget.style.display = 'none';
          }}
        />
      </div>
    );
  }

  return (
    <div className="app-shell">
      <div className="signal-grid" aria-hidden="true" />

      <header className="topbar glass-panel">
        <div className="brand-wrap">
          <div className="brand-mark">S</div>
          <div>
            <p className="eyebrow">Safety intelligence</p>
            <h1>Site Safety Watch</h1>
          </div>
        </div>

        <nav className="topbar-actions" aria-label="Main navigation">
          <button className="nav-pill active">Overview</button>
          <button className="nav-pill">CCTV</button>
          <button className="nav-pill">Violations</button>
          <button className="nav-pill">Reports</button>
        </nav>

        <div className="live-status">
          <span className="status-dot" />
          <span>{stats.status}</span>
        </div>
      </header>

      <main className="dashboard-grid">
        <section className="hero-panel glass-panel">
          <div className="section-header">
            <div>
              <p className="eyebrow">Live site feed</p>
              <h2>Construction sector camera</h2>
            </div>
            <div className="camera-actions">
              <span className="badge badge-primary">YOLOv8-Pose active</span>
              <button
                className="full-screen-button"
                onClick={() => setIsFullscreen((prev) => !prev)}
                aria-label={isFullscreen ? 'Exit fullscreen' : 'Enter fullscreen'}
              >
                {isFullscreen ? 'Exit Fullscreen' : 'Fullscreen'}
              </button>
            </div>
          </div>

          <div className={`camera-stage ${isFullscreen ? 'camera-stage-fullscreen' : ''}`}>
            {isFullscreen && (
              <button
                className="fullscreen-close"
                onClick={() => setIsFullscreen(false)}
                aria-label="Close fullscreen camera"
              >
                ×
              </button>
            )}

            <div className="camera-overlay">
              <span className="camera-tag">Zone B • Elevation 3</span>
              <span className="camera-tag alt">PPE: {report.ppe_compliance_rate}</span>
            </div>

            <img
              src="http://127.0.0.1:8000/video_feed"
              alt="Live Site Safety Stream"
              className="camera-image"
              onError={(e) => {
                e.currentTarget.style.display = 'none';
                const fallback = document.getElementById('feed-fallback');
                if (fallback) {
                  fallback.style.display = 'flex';
                }
              }}
            />

            <div id="feed-fallback" className="feed-fallback">
              <p className="text-sm font-medium">Backend Offline</p>
              <span className="text-xs mt-2 text-indigo-400">Start main.py to connect camera feed</span>
            </div>

            <div className="scan-lines" aria-hidden="true" />
          </div>

          <div className="kpi-row">
            {overview.map((metric) => (
              <div key={metric.label} className="metric-card">
                <div className={`metric-icon ${metric.tone}`} aria-hidden="true">
                  <span />
                </div>
                <div>
                  <p>{metric.label}</p>
                  <strong>{metric.value}</strong>
                  <small>{metric.delta}</small>
                </div>
              </div>
            ))}
          </div>
        </section>

        <aside className="report-panel glass-panel">
          <div className="section-header compact">
            <div>
              <p className="eyebrow">Daily report</p>
              <h2>Risk summary</h2>
            </div>
            <span className="report-date">{report.date}</span>
          </div>

          <div className="site-meta">
            <div>
              <p className="meta-label">Site</p>
              <h3>{stats.site}</h3>
            </div>
            <div>
              <p className="meta-label">Shift</p>
              <h3>{stats.shift}</h3>
            </div>
          </div>

          <div className="summary-grid">
            <div className="summary-box success">
              <span>PPE compliance</span>
              <strong>{report.ppe_compliance_rate}</strong>
            </div>
            <div className="summary-box danger">
              <span>Critical incidents</span>
              <strong>{report.critical_incidents_logged}</strong>
            </div>
          </div>

          <div className="recommendations">
            <p className="meta-label">Recommendations</p>
            <ul>
              {report.recommendations.map((recommendation) => (
                <li key={recommendation}>{recommendation}</li>
              ))}
            </ul>
          </div>

          <button className="export-button" onClick={() => window.print()}>
            Export daily report
          </button>
        </aside>

        <section className="analytics-panel glass-panel">
          <div className="section-header compact">
            <div>
              <p className="eyebrow">Compliance</p>
              <h2>Protection score</h2>
            </div>
            <span className="badge badge-soft">+6.2% this week</span>
          </div>

          <div className="ring-wrap">
            <div className="score-ring">
              <div className="score-ring-inner">
                <strong>94.5%</strong>
                <span>safe</span>
              </div>
            </div>
          </div>

          <div className="bar-list">
            {complianceBars.map((bar) => (
              <div key={bar.label} className="bar-row">
                <div className="bar-label-row">
                  <span>{bar.label}</span>
                  <span>{bar.value}%</span>
                </div>
                <div className="bar-track">
                  <span style={{ width: `${bar.value}%` }} />
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="alerts-panel glass-panel">
          <div className="section-header compact">
            <div>
              <p className="eyebrow">Live alerts</p>
              <h2>Risk signals</h2>
            </div>
            <button className="ghost-button">View all</button>
          </div>

          <ul className="alert-list">
            {riskSignals.map((signal) => (
              <li key={signal.title} className="alert-item">
                <div className="alert-icon" aria-hidden="true" />
                <div className="alert-copy">
                  <div className="alert-heading">
                    <strong>{signal.title}</strong>
                    <span className={`severity severity-${signal.severity.toLowerCase()}`}>
                      {signal.severity}
                    </span>
                  </div>
                  <small>{signal.detail}</small>
                </div>
              </li>
            ))}
          </ul>
        </section>
      </main>
    </div>
  );
}

