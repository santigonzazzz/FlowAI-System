import { useState } from "react";

/**
 * Formulario principal para ingresar y enviar mensajes.
 * Props:
 *   onSubmit(content) -> llamado con el texto del mensaje
 *   loading -> boolean para deshabilitar mientras se procesa
 */
export default function MessageForm({ onSubmit, loading }) {
  const [content, setContent] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    const trimmed = content.trim();
    if (!trimmed) return;
    onSubmit(trimmed);
  }

  return (
    <form className="message-form" onSubmit={handleSubmit}>
      <label className="form-label" htmlFor="msg-input">
        Escribe tu mensaje
      </label>
      <textarea
        id="msg-input"
        className="message-textarea"
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder="Ej: Hola, me gustaria saber el precio de sus planes..."
        rows={5}
        disabled={loading}
      />
      <button
        type="submit"
        className={`submit-btn ${loading ? "loading" : ""}`}
        disabled={loading || !content.trim()}
      >
        {loading ? (
          <>
            <span className="spinner" />
            Procesando...
          </>
        ) : (
          "Procesar mensaje"
        )}
      </button>
    </form>
  );
}