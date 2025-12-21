import { defineConfig } from "vite"
import react from "@vitejs/plugin-react"
import path from "path"

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    // Proxy API requests to the FastAPI backend during development
    proxy: {
      // Forward requests starting with /agent, /monitoring, /risks and /api to backend
      '/agent': {
        target: 'http://localhost:8002',
        changeOrigin: true,
        secure: false,
      },
      '/monitoring': {
        target: 'http://localhost:8002',
        changeOrigin: true,
        secure: false,
      },
      '/risks': {
        target: 'http://localhost:8002',
        changeOrigin: true,
        secure: false,
      },
      '/api': {
        target: 'http://localhost:8002',
        changeOrigin: true,
        secure: false,
      }
    }
  }
})
