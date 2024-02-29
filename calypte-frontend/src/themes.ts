import { createTheme } from '@mui/material/styles';

// Create a custom theme
const theme = createTheme({
  palette: {
    primary: {
      main: '#007bff', // Blue color
    },
    secondary: {
      main: '#6c757d', // Gray color
    },
    background: {
      default: '#141419',
    },
  },
  typography: {
    fontFamily: 'Roboto, sans-serif',
  },
});

export default theme;