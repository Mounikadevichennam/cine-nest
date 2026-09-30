/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        brand: {
          dark: '#0B0D12',
          card: '#141824',
          accent: '#E50914',
          gold: '#FFB800',
          blue: '#1E40AF',
          teal: '#0D9488',
          purple: '#7C3AED',
          cyan: '#06B6D4'
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
