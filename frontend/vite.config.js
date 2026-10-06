import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Backend local (el dev server hace de proxy). En produccion se define
// VITE_API_URL en el build o se usan los redirects de netlify.toml.
const BACKEND = 'http://localhost:8000'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // 0.0.0.0 para que el dev server sea accesible desde fuera del contenedor
    host: true,
    port: 5173,
    allowedHosts: true,
    // El navegador llama a rutas relativas (/messages) y Vite las enruta al
    // backend: evita problemas de CORS y que el cliente apunte a localhost.
    proxy: {
      '/messages': { target: BACKEND, changeOrigin: true },
      '/health': { target: BACKEND, changeOrigin: true },
      '/docs': { target: BACKEND, changeOrigin: true },
      '/redoc': { target: BACKEND, changeOrigin: true },
      '/openapi.json': { target: BACKEND, changeOrigin: true },
    },
  },
  preview: {
    host: true,
    port: 4173,
    allowedHosts: true,
    proxy: {
      '/messages': { target: BACKEND, changeOrigin: true },
      '/health': { target: BACKEND, changeOrigin: true },
    },
  },
})
