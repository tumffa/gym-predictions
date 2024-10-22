import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'build', // Specify the output directory
  },
  server: {
    port: 8080, // Specify the port to run on
    host: '0.0.0.0', // Listen on all addresses
  },
});