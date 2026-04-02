/**
 * Tarjeta que muestra el resultado del procesamiento de un mensaje.
 * Muestra: classification, response, rule_matched.
 */

const CLASS_META = {
  hot:  { label: "HOT",  emoji: "🔥", colorClass: "badge-hot"  },
  warm: { label: "WARM", emoji: "🌡", colorClass: "badge-warm" },
  cold: { label: "COLD", emoji: "❄", colorClass: "badge-cold" },
};

export default function ResultCard({ result }) {
  if (!result) return null;

  const meta = CLASS_META[result.classification] ?? {
    label: result.classification.toUpperCase(),
    emoji: "🤖",
    colorClass: "badge-cold",
  };

  return (
    <div className="result-card">
      <div className="result-header">
        <h2 className="result-title">Resultado del procesamiento</h2>
        <span className={`badge ${meta.colorClass}`}>
          {meta.emoji} {meta.label}
        </span>
      </div>

      <div className="result-row">
        <span className="result-key">Clasificacion</span>
        <span className={`result-val classification-${result.classification}`}>
          {result.classification}
        </span>
      </div>

      <div className="result-row">
        <span className="result-key">Fuente</span>
        <span className={`source-pill ${result.rule_matched ? "source-rule" : "source-ai"}`}>
          {result.rule_matched ? "⚡ Regla automatica" : "🤖 Groq AI"}
        </span>
      </div>

      <div className="result-response">
        <span className="result-key">Respuesta generada</span>
        <p className="response-text">{result.response}</p>
      </div>
    </div>
  );
}