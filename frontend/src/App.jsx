import { useState, useCallback } from "react";
import MessageForm from "./components/MessageForm";
import ResultCard from "./components/ResultCard";
import HistoryPanel from "./components/HistoryPanel";
import { postMessage } from "./services/api";

export default function App() {
  const [result, setResult]   = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError]     = useState(null);

  const handleSubmit = useCallback(async (content) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await postMessage(content);
      setResult(data);
      setHistory((prev) => [...prev, data]);
    } catch (err) {
      setError(err.message || "Error inesperado al conectar con la API.");
    } finally {
      setLoading(false);
    }
  }, []);

  return (
    <div className="app-bg">
      {/* Fondo con gradiente animado */}
      <div className="bg-orb orb-1" />
      <div className="bg-orb orb-2" />

      <div className="container">
        {/* Header */}
        <header className="header">
          <div className="logo">
            <span className="logo-icon">⚡</span>
            <span className="logo-text">FlowAI</span>
          </div>
          <p className="header-sub">
            Motor de clasificacion y automatizacion con IA
          </p>
        </header>

        {/* Panel principal */}
        <main className="main-panel">
          <MessageForm onSubmit={handleSubmit} loading={loading} />

          {/* Error */}
          {error && (
            <div className="error-box">
              <span>⚠️</span> {error}
            </div>
          )}

          {/* Resultado */}
          <ResultCard result={result} />
        </main>

        {/* Historial */}
        <HistoryPanel messages={history} />

        {/* Footer */}
        <footer className="footer">
          API: <code>localhost:8000</code> · Motor: Groq llama-3.3-70b
        </footer>
      </div>
    </div>
  );
}