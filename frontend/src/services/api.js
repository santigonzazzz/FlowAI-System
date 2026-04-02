/**
 * Capa de comunicacion con la API de FlowAI.
 * Centralizar aqui todas las llamadas evita repetir fetch en los componentes
 * y facilita cambiar la base URL en un unico lugar.
 */

const API_BASE = "http://localhost:8000";

/**
 * Envia un mensaje al motor de procesamiento.
 * @param {string} content - Texto del mensaje
 * @returns {Promise<Object>} Respuesta con classification, response, rule_matched
 */
export async function postMessage(content) {
  const res = await fetch(`${API_BASE}/messages`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ content }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err?.detail || `Error ${res.status}`);
  }

  return res.json();
}

/**
 * Obtiene todos los mensajes procesados.
 * @returns {Promise<Array>} Lista de mensajes
 */
export async function getMessages() {
  const res = await fetch(`${API_BASE}/messages`);
  if (!res.ok) throw new Error(`Error ${res.status}`);
  return res.json();
}