import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [tailwindcss(), sveltekit()],
	optimizeDeps: {
		exclude: ['@lucide/svelte']
	},
	server: {
    proxy: {
      '/api': {
        target: process.env.BACKEND_URL || 'https://agentbeats.org/api',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/api/, '')
      },
      '/ws': {
        target: (process.env.BACKEND_URL || 'https://agentbeats.org/api').replace(/^http/, 'ws'),
        ws: true,
        changeOrigin: true,
        secure: false
      }
    }
  }
});
