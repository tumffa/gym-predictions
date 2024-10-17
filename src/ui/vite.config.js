import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'build', // Specify the output directory
  },
  server: {
    proxy: {
      '/predict': 'http://localhost:5000',  // Proxy /predict to Flask backend
    },
    host: true,  // Necessary to run in Docker and Fly
    port: 3000   // Vite frontend will run on port 3000
  }
});