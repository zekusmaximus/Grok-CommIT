/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        void: '#050505',
        sigil: '#ff003c',
        neon: '#00f3ff',
        dim: '#4a4a4a',
      },
      fontFamily: {
        mono: ['"JetBrains Mono"', 'monospace'], // Good for code
      }
    },
  },
  plugins: [],
}
