import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react-swc';
import eslint from 'vite-plugin-eslint2';
import path from 'path';
import dns from 'dns';

dns.setDefaultResultOrder('verbatim');

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    eslint({
      lintInWorker: true,
      lintOnStart: true,
      overrideConfigFile: path.resolve(__dirname, './eslint.config.mjs'),
    }),
  ],
});
