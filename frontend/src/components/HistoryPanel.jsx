import { useState } from "react";

const CLASS_META = {
  hot:  { emoji: "🔥", colorClass: "badge-hot"  },
  warm: { emoji: "🌡", colorClass: "badge-warm" },
  cold: { emoji: "❄", colorClass: "badge-cold" },
};

export default function HistoryPanel({ messages }) {
  const [open, setOpen] = useState(false);

  if (!messages || messages.length === 0) return null;

  return (
    <div className="history-panel">
      <button className="history-toggle" onClick={() => setOpen((o) => !o)}>
        📋 Historial ({messages.length}) {open ? "▲" : "▼"}
      </button>

      {open && (
        <ul className="history-list">
          {[...messages].reverse().map((msg) => {
            const meta = CLASS_META[msg.classification] ?? { emoji: "🤖", colorClass: "badge-cold" };
            return (
              <li key={msg.id} className="history-item">
                <div className="history-top">
                  <span className={`badge-sm ${meta.colorClass}`}>
                    {meta.emoji} {msg.classification}
                  </span>
                  <span className="history-source">
                    {msg.rule_matched ? "⚡ Regla" : "🤖 AI"}
                  </span>
                </div>
                <p className="history-content">"{msg.content}"</p>
                <p className="history-response">{msg.response}</p>
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}