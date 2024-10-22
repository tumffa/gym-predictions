import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'build', // Specify the output directory
  },
  server: {
    port: 5173, // Specify the port
  },
  define: {
    'process.env': process.env,
  },
});