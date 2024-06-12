/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './**/templates/**/*.html',
  ],
  theme: {
    extend: {},
    fontFamily: {
      "sans": ["Ubuntu", "Noto Sans"],
    }
  },
  plugins: [
    require("daisyui"),
    require('@tailwindcss/typography'),
  ],
  daisyui: {
    themes: ["emerald", "night"],
  },
}

