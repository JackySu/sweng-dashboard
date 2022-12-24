import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'


// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      "@": resolve("src"),
      comps: resolve("src/components"),
      api: resolve("src/api"),
      views: resolve("src/views"),
      utils: resolve("src/utils"),
      router: resolve("src/router"),
    },
  },
  base: "./",
  server: {
    port: 5173,
    open: true,
    cors: true,
  },
})
