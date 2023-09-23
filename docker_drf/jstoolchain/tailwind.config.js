/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
      '../templates/**/*.{html,js}',
      '../api/templates/api/**/*.{html,js}',
      'node_modules/preline/dist/*.js',
      'node_modules/flowbite/**/*.js',
  ],
  theme: {
    extend: {},
  },
  plugins: [
      require('preline/plugin'),
      require('flowbite/plugin'),
  ],
}
