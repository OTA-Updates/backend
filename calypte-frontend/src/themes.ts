import { createTheme } from '@mui/material/styles';

// Create a custom theme
const theme = createTheme({
  typography: {
    fontFamily: '"Montserrat", sans-serif',
    allVariants: {
      color: '#FFFFFF', 
    },
    h2: {
      fontFamily: '"Montserrat", sans-serif',
      fontWeight: 600,
      fontSize: '18px'
    },
  },
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
});

export default theme;