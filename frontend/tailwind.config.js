/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./app/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        dark: {
          900: "#0f0f0f",
          800: "#1a1a1a",
          700: "#2d2d2d",
        },
      },
    },
  },
  plugins: [],
};
