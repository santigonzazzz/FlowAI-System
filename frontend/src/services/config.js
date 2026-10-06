/**
 * Configuracion de entorno del frontend.
 *
 * La URL de la API NO queda fija en el codigo:
 *
 *   local      → npm run dev        → llamadas relativas, Vite hace proxy a :8000
 *   produccion → VITE_API_URL=https://tu-backend.onrender.com npm run build
 *
 * Si no se define VITE_API_URL en un build, las llamadas quedan relativas ("/messages"),
 * de modo que un redirect de Netlify (/netlify.toml) pueda enrutarlas al backend.
 */

function normalize(url) {
  return (url || "").trim().replace(/\/+$/, "");
}

const ENV_URL = normalize(import.meta.env.VITE_API_URL);

/** Base de la API (sin slash final). "" = ruta relativa. */
export const API_BASE = ENV_URL;

/** Texto corto para el footer de la UI. */
export const API_LABEL = ENV_URL
  ? API_BASE.replace(/^https?:\/\//, "")
  : import.meta.env.DEV
    ? "localhost:8000"
    : "sin backend (define VITE_API_URL)";

/** True si hay un backend al que llamar (dev con proxy o VITE_API_URL). */
export const HAS_BACKEND = Boolean(ENV_URL) || import.meta.env.DEV;

/** Motor de IA declarado por el backend. */
export const AI_ENGINE = import.meta.env.VITE_AI_ENGINE || "Groq llama-3.3-70b";
