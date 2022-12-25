import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'


// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  base: "./",
  server: {
    /* host = true allows forwarding an IP from the main namespace to another in docker container
      https://stackoverflow.com/questions/70012970/running-a-vite-dev-server-inside-a-docker-container
    */
    host: true,
    port: 4622,
    open: false,
    cors: true,
  },
})
