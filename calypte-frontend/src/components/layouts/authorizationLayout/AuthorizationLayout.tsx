import React from 'react';
import { Box, Typography } from '@mui/material';
import useStyles from './styles';

interface ThemeContainerProps {
  children: React.ReactNode;
}

const AuthorizationLayout: React.FC<ThemeContainerProps> = ({ children }) => {
  const { classes } = useStyles();

  return (
    <Box className={classes.root}>
      <Box className={classes.header}>
        <img src={`${process.env.PUBLIC_URL}/logo.svg`} alt='Logo' />
        <Typography variant='h2'>Calypte</Typography>
      </Box>
      <Box className={classes.content}>{children}</Box>
    </Box>
  );
};

export default AuthorizationLayout;
