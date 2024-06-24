/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './**/templates/**/*.html',
  ],
  theme: {
    extend: {},
    fontFamily: {
      "sans": ["Noto Sans"],
    },
    screens: {
      tablet: '640px',
      laptop: '1064px',
      desktop: '1280px'
    }
  },
  plugins: [
    require('@tailwindcss/typography'),
    require("daisyui"),
  ],
  daisyui: {
    themes: ["light", "dark"],
  },
}

