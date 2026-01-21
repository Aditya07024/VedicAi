import { useState } from "react";
import "./AnalysisResults.css";

function AnalysisResults({ analysis, onNewAnalysis }) {
  const [activeTab, setActiveTab] = useState("kundli");

  const renderKundli = () => {
    const h = analysis.kundli.houses || {};
    const lagna = analysis.kundli.lagna?.rashi || "N/A";

    // Helper to convert values to strings and pad them
    const getHouseDisplay = (houseValue) => {
      const str = (houseValue || "Empty").toString();
      return str.padEnd(12);
    };

    return (
      <div className="kundli-chart">
        <h3>🔮 Birth Chart (Kundli)</h3>
        <div className="chart-grid">
          <pre>{`
            ┌─────────────────────┐
            │  [12] ${getHouseDisplay(h[12])} │
    ┌───────┼─────────────────────┼───────┐
    │ [11] ${getHouseDisplay(h[11]).padEnd(8)} │             │ [1] ${getHouseDisplay(h[1]).padEnd(8)} │
    │               │   LAGNA     │               │
    │               │ (${lagna})    │               │
    ├───────────────┼─────────────────────┼───────────────┤
    │ [10] ${getHouseDisplay(h[10]).padEnd(8)} │             │ [2] ${getHouseDisplay(h[2]).padEnd(8)} │
    │               │             │               │
    └───────┼───────────────┼───────┘
            │  [7] ${getHouseDisplay(h[7])} │
    ┌───────┼─────────────────────┼───────┐
    │ [8] ${getHouseDisplay(h[8]).padEnd(8)} │             │ [6] ${getHouseDisplay(h[6]).padEnd(8)} │
    │               │             │               │
    ├───────────────┼─────────────────────┼───────────────┤
    │ [9] ${getHouseDisplay(h[9]).padEnd(8)} │             │ [5] ${getHouseDisplay(h[5]).padEnd(8)} │
    │               │             │               │
    └───────┼───────────────┼───────┘
            │  [4] ${getHouseDisplay(h[4])} │
            └─────────────────────┘
          `}</pre>
        </div>

        <div className="planetary-positions">
          <h4>🪐 Planetary Positions</h4>
          <div className="planets-grid">
            {Object.entries(analysis.kundli.planets || {}).map(
              ([planet, data]) => (
                <div key={planet} className="planet-card">
                  <strong>{planet}</strong>
                  <p>{data.rashi || "N/A"}</p>
                  <small>{data.nakshatra || "N/A"}</small>
                </div>
              ),
            )}
          </div>
        </div>
      </div>
    );
  };

  const renderDoshas = () => {
    if (!analysis.doshas || analysis.doshas.length === 0) {
      return (
        <div className="doshas">
          <h3>✅ No Major Doshas Detected</h3>
          <p>This is a favorable indication for smooth life events.</p>
        </div>
      );
    }

    return (
      <div className="doshas">
        <h3>⚠️ Dosha Analysis</h3>
        {analysis.doshas.map((dosha, idx) => (
          <div key={idx} className="dosha-card">
            <h4>{dosha.name}</h4>
            <p>
              <strong>Severity:</strong> {dosha.severity}
            </p>
            <p>
              <strong>Description:</strong> {dosha.description}
            </p>
            <p>
              <strong>Impact:</strong> {dosha.impact}
            </p>
          </div>
        ))}
      </div>
    );
  };

  const renderDasha = () => {
    const maha = analysis.dasha?.mahadasha || {};
    return (
      <div className="dasha">
        <h3>⏰ Vimshottari Dasha</h3>
        <div className="dasha-card">
          <h4>Current Mahadasha: {maha.planet}</h4>
          <p>
            <strong>Start:</strong> {maha.start_date}
          </p>
          <p>
            <strong>End:</strong> {maha.end_date}
          </p>
          <p>
            <strong>Years Remaining:</strong> {maha.years_remaining?.toFixed(1)}
          </p>
          <div className="progress-bar">
            <div
              className="progress-fill"
              style={{
                width: `${(((maha.total_years - maha.years_remaining) / maha.total_years) * 100).toFixed(0)}%`,
              }}
            />
          </div>
        </div>
      </div>
    );
  };

  const renderPanchang = () => {
    return (
      <div className="panchang">
        <h3>📅 Panchang</h3>
        <div className="panchang-grid">
          <div className="panchang-item">
            <strong>Vara (Day)</strong>
            <p>{analysis.panchang?.vara || "N/A"}</p>
          </div>
          <div className="panchang-item">
            <strong>Tithi</strong>
            <p>{analysis.panchang?.tithi?.name || "N/A"}</p>
          </div>
          <div className="panchang-item">
            <strong>Nakshatra</strong>
            <p>{analysis.panchang?.nakshatra || "N/A"}</p>
          </div>
          <div className="panchang-item">
            <strong>Yoga</strong>
            <p>{analysis.panchang?.yoga || "N/A"}</p>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="analysis-results">
      <div className="results-header">
        <h2>✅ Analysis Complete for {analysis.birth_details?.name}</h2>
        <button className="primary" onClick={onNewAnalysis}>
          ← New Analysis
        </button>
      </div>

      <div className="birth-info">
        <h3>📋 Birth Details</h3>
        <div className="info-grid">
          <div>
            <strong>Name:</strong> {analysis.birth_details?.name}
          </div>
          <div>
            <strong>Date:</strong> {analysis.birth_details?.date}
          </div>
          <div>
            <strong>Time:</strong> {analysis.birth_details?.time}
          </div>
          <div>
            <strong>Place:</strong> {analysis.birth_details?.place}
          </div>
          <div>
            <strong>Latitude:</strong> {analysis.birth_details?.latitude}
          </div>
          <div>
            <strong>Longitude:</strong> {analysis.birth_details?.longitude}
          </div>
        </div>
      </div>

      <div className="tabs">
        <button
          className={activeTab === "kundli" ? "tab active" : "tab"}
          onClick={() => setActiveTab("kundli")}
        >
          📊 Kundli
        </button>
        <button
          className={activeTab === "doshas" ? "tab active" : "tab"}
          onClick={() => setActiveTab("doshas")}
        >
          ⚠️ Doshas
        </button>
        <button
          className={activeTab === "dasha" ? "tab active" : "tab"}
          onClick={() => setActiveTab("dasha")}
        >
          ⏰ Dasha
        </button>
        <button
          className={activeTab === "panchang" ? "tab active" : "tab"}
          onClick={() => setActiveTab("panchang")}
        >
          📅 Panchang
        </button>
      </div>

      <div className="tab-content">
        {activeTab === "kundli" && renderKundli()}
        {activeTab === "doshas" && renderDoshas()}
        {activeTab === "dasha" && renderDasha()}
        {activeTab === "panchang" && renderPanchang()}
      </div>
    </div>
  );
}

export default AnalysisResults;
