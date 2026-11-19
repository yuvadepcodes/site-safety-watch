/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        safety: {
          emerald: "#34d399",
          amber: "#fbbf24",
          rose: "#f87171",
        },
      },
    },
  },
  plugins: [],
}
