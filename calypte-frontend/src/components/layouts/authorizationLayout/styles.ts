import { Theme } from '@mui/material/styles';
import { makeStyles } from 'tss-react/mui';

const useStyles = makeStyles()((theme: Theme) => ({
  root: {
    backgroundColor: theme.palette.background.default,
    height: '100%',
    display: 'flex',
    flexDirection: 'column',
  },
  header: {
    width: '100%',
    height: theme.spacing(8),
    display: 'flex',
    alignItems: 'center',
    gap: theme.spacing(1),
    padding: `${theme.spacing(2)} ${theme.spacing(10)}`,
  },
  content: {
    width: '100%',
    flexGrow: 1,
    display: 'flex',
  },
}));

export default useStyles;
