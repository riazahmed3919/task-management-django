/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html", // templates at project level
    "./**/templates/**/*.html", // templates inside apps
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

