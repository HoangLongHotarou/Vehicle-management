import { React, useEffect, useState } from 'react';
import Typography from '@mui/material/Typography';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Container from '@mui/material/Container';
import Footer from '../../Components/FooterComponent/Footer';
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff';
import RemoveRedEyeIcon from '@mui/icons-material/RemoveRedEye';
import { InputAdornment } from '@mui/material';

import './Login.scss';
import '../../Styles/main.scss';
import palette from '../../Styles/variables.scss';
import Auth from '../../Services/auth';
import Loading from '../../Components/LoadingComponent/Loading';
import AlertCustome from '../../Components/AlertComponent/AlertCustome';

const theme = createTheme({
  palette: {
    primary: {
      main: palette.primary,
    },
    secondary: {
      main: palette.secondary,
    },
  }
}
);

var auth = new Auth();

function Login() {

  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [openAlert, SetOpenAlert] = useState({ state: false, severity: 'error', text: 'Tên đăng nhập hoặc mật khẩu không chính xác!' });
  // const [checkEmail, setCheckEmail] = useState({helperText: '', error: false});

  useEffect(() => {
    document.title = 'Đăng Nhập';
  }, [])

  // const handleChangeEmail = (event) => {
  //   let emailVal = event.target.value;
  //   if (validateEmail(emailVal) && emailVal !== '') {
  //     setCheckEmail({helperText: '', error: false})
  //   }
  //   else {
  //     setCheckEmail({helperText: 'Định dạng Email không chính xác!', error: true})
  //   }
  // }

  const handleSubmit = (event) => {
    event.preventDefault();
    setLoading(true);
    const data = new FormData(event.currentTarget);
    let obj = {
      username: data.get('username'),
      password: data.get('password'),
    };
    auth.login(obj).then(result => {
      if (result) {
        setLoading(false);
        window.location.reload();
      }
      else {
        setLoading(false);
        SetOpenAlert((prevState) => ({
          ...prevState,
          state: true
        }))
      }
    });
  };

  const handlePassword = () => {
    setShowPassword(!showPassword);
  }

  // const validateEmail = (email) => {
  //   return String(email)
  //     .toLowerCase()
  //     .match(
  //       /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
  //     );
  // };

  return (
    <ThemeProvider theme={theme}>
      {loading ? (<Loading text='Đang đăng nhập...' />) : null}

      <AlertCustome
        open={openAlert.state}
        onOpen={SetOpenAlert}
        duration={3000}
        severity={openAlert.severity}
        text={openAlert.text} />      
      
      <Container component="main" maxWidth="xs" sx={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
      }}>
        <CssBaseline />
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Avatar sx={{ mb: 1, bgcolor: 'primary.main' }}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h1" variant="h5" sx={{ fontWeight: 600, color: 'primary.main' }}>
            Đăng Nhập
          </Typography>
          <Box component="form" onSubmit={handleSubmit} sx={{ mt: 4 }}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="email"
              label="Username"
              name="username"
              autoComplete="text"
              autoFocus
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type={showPassword ? "text" : "password"}
              id="password"
              autoComplete="current-password"
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end" sx={{ cursor: 'pointer' }} onClick={handlePassword}>
                    {showPassword ? (<VisibilityOffIcon className='hv-color' />) : ((<RemoveRedEyeIcon className='hv-color' />))}
                  </InputAdornment>
                ),
              }}
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Đăng nhập
            </Button>
          </Box>
        </Box>
        <Footer sx={{ mt: 8 }}></Footer>
      </Container>
    </ThemeProvider>
  )
}

export default Login