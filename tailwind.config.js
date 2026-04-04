module.exports = {
  content: ['./templates/**/*.html'],
  theme: {
    extend: {
      colors: {
        primary:  { DEFAULT: '#1E88E5', dark: '#1565C0', light: '#42A5F5' },
        accent:   { DEFAULT: '#EF6C00', light: '#FFA726' },
        sidebar:  { DEFAULT: '#0F172A', hover: '#1E293B', active: '#1E3A5F' },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      }
    }
  },
  plugins: [],
}
