/**
 * Capa de comunicacion con la API de FlowAI.
 * Centralizar aqui todas las llamadas evita repetir fetch en los componentes
 * y facilita cambiar la base URL en un unico lugar.
 */

import { API_BASE } from "./config";

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

  // Un sitio estatico sin backend puede responder index.html (SPA) con 200;
  // en ese caso no hay API detras y lo avisamos explicitamente.
  const ct = res.headers.get("content-type") || "";
  if (!ct.includes("application/json")) {
    throw new Error(
      "Backend no disponible: este sitio es una demo visual. Configura VITE_API_URL o el proxy de netlify.toml."
    );
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