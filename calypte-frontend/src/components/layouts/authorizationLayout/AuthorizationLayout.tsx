import React from 'react';
import { Box } from '@mui/material';
import useStyles from './styles';

interface ThemeContainerProps {
  children: React.ReactNode;
}

const AuthorizationLayout: React.FC<ThemeContainerProps> = ({ children }) => {
  const { classes } = useStyles();

  return (
    <Box className={classes.root}>
      <img src='' alt='Logo' className={classes.logo} />
      {children}
    </Box>
  );
};

export default AuthorizationLayout;