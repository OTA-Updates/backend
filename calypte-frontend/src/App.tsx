import React from 'react';
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import theme from './themes';
import AuthorizationLayout from './components/layouts/authorizationLayout/AuthorizationLayout';

const Registration = () => <div>Registration - Mail confirmation</div>;
const Login = () => <div>Login</div>;
const Dashboard = () => <div>Dashboard</div>;
const Deployments = () => <div>Deployments</div>;
const Deployment = () => <div>Deployment</div>;
const Groups = () => <div>Groups</div>;
const Group = () => <div>Group</div>;
const Settings = () => <div>Settings</div>;
const EmailConfirmation = () => <div>EmailConfirmation</div>;
const ChangePassword = () => <div>Change Password</div>;

const App = () => {
  return (
    <ThemeProvider theme={theme}>
      <BrowserRouter>
        <Routes>
          <Route
            path='/registration'
            element={
              <AuthorizationLayout>
                <Registration />
              </AuthorizationLayout>
            }
          />
          <Route
            path='/login'
            element={
              <AuthorizationLayout>
                <Login />
              </AuthorizationLayout>
            }
          />
          <Route
            path='/email-confirmation'
            element={
              <AuthorizationLayout>
                <EmailConfirmation />
              </AuthorizationLayout>
            }
          />
          <Route path='/' element={<Navigate to='/dashboard' replace />} />
          <Route path='/dashboard' element={<AuthorizationLayout><Dashboard /></AuthorizationLayout>} />
          <Route path='/deployments' element={<Deployments />} />
          <Route path='/deployments/new' element={<Deployment />} />
          <Route path='/deployments/:id/edit' element={<Deployment />} />
          <Route
            path='/deployments/:id/devicemanager'
            element={<Deployment />}
          />
          <Route path='/deployments/:id/console' element={<Deployment />} />
          <Route path='/groups' element={<Groups />} />
          <Route path='/groups/new' element={<Group />} />
          <Route path='/groups/:id/edit' element={<Group />} />
          <Route path='/groups/:id/console' element={<Group />} />
          <Route path='/groups/:id/device/new' element={<Group />} />
          <Route path='/groups/:id/device/:deviceId/edit' element={<Group />} />
          <Route
            path='/groups/:id/device/:deviceId/console'
            element={<Group />}
          />
          <Route path='/settings' element={<Settings />} />
          <Route path='/settings/changepassword' element={<ChangePassword />} />
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  );
};

export default App;
