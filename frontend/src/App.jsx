import { useState } from "react";
import "./App.css";
import BirthForm from "./components/BirthForm";
import AnalysisResults from "./components/AnalysisResults";
import api from "./services/api";

function App() {
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAnalysis = async (birthDetails) => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.post("/api/analysis", {
        birth_details: birthDetails,
      });
      setAnalysis(response.data);
    } catch (err) {
      setError(err.message);
      console.error("Analysis error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <div className="container">
          <h1>🔮 VedicAI</h1>
          <p>Explainable Astrology through Astronomical Computation</p>
        </div>
      </header>

      <main className="container">
        {!analysis ? (
          <BirthForm
            onSubmit={handleAnalysis}
            loading={loading}
            error={error}
          />
        ) : (
          <AnalysisResults
            analysis={analysis}
            onNewAnalysis={() => setAnalysis(null)}
          />
        )}
      </main>
    </div>
  );
}

export default App;
