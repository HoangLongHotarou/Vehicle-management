import { React, useState, useEffect, useRef } from 'react'
import { createTheme, Divider, TextField, ThemeProvider, Typography, InputAdornment } from '@mui/material'
import { LoadingButton } from '@mui/lab';
import { Container } from '@mui/system';

import SaveIcon from '@mui/icons-material/Save';
import RemoveRedEyeIcon from '@mui/icons-material/RemoveRedEye';
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff';

import './ChangePassword.scss'
import AuthService from '../../Services/auth';
import palette from '../../Styles/variables.scss'
import NavBar from '../../Components/NavBarComponent/NavBar'
import ImgPreview from '../../Components/ImgPreviewComponent/ImgPreview'
import AlertCustome from '../../Components/AlertComponent/AlertCustome';
import imageSrc from '../../Assets/Images/avt-default.jpg'

const auth = new AuthService();

const theme = createTheme({
    palette: {
        primary: {
            main: palette.primary,
        },
        secondary: {
            main: palette.secondary,
        },
    }
});

function ChangePassword() {

    const [info, setInfo] = useState({});
    const [pending, setPending] = useState(false);
    const [openImagePreview, setOpenImagePreview] = useState(false);
    const [openAlert, setOpenAlert] = useState({ state: false, severity: 'error', text: '' });
    const [showPassword, setShowPassword] = useState({ new: false, new1: false })
    const [checkPwdAgain, setCheckPwdAgain] = useState({helperText: '', error: false})
    const [pwd, setPwd] = useState({pwd1: ''});

    useEffect(() => {
        setInfo(auth.getInfo())
    }, [])

    const handleOpenPreviewClick = () => {
        setOpenImagePreview(!openImagePreview);
    }

    const handleSubmit = (event) => {
        event.preventDefault();
        // setPending(true);
        const data = new FormData(event.currentTarget);
        console.log(data.get('current'));

        let newPwd = data.get('new');
        let newPwdAgain = data.get('new1')
        checkPwd(newPwd, newPwdAgain);
    }

    const checkPwd = (newPwd, newPwdAgain) => {
        let kq = true;
        if (newPwd !== newPwdAgain && newPwdAgain !== '') {
            setCheckPwdAgain({helperText: 'Mật khẩu không trùng khớp', error: true});
            kq = false;
        }
        else {
            setCheckPwdAgain({helperText: '', error: false})
        }
        return kq;
    }

    const handleShowPassword = (type) => {
        setShowPassword({...showPassword, [type]: !showPassword[type]})
    }    

    const handleChangeValuePwd = (e, type) => {            
        type ==='pwd2' ? checkPwd(pwd.pwd1, e.target.value) : setPwd({...pwd, [type]: e.target.value}); ;
        console.log(pwd);
    }

    return (
        <NavBar title='Đổi mật khẩu' active='accounts'>
            <AlertCustome
                open={openAlert.state}
                onOpen={setOpenAlert}
                duration={3000}
                severity={openAlert.severity}
                text={openAlert.text} />

            <ThemeProvider theme={theme}>
                <Container className='container' maxWidth='xl'>
                    <div className='right'>
                        <Typography mb={2} component="h1" variant="h5" sx={{ fontWeight: 500, color: 'primary.main', textAlign: 'center' }}>
                            Ảnh đại diện
                        </Typography>
                        <div className={'img-bx not-pending'}>
                            <img src={(info.avatar) ? info.avatar : imageSrc} alt='avatar' />
                            <div className='btn-view-image' onClick={handleOpenPreviewClick}>
                                <RemoveRedEyeIcon />
                                <span>Xem ảnh</span>
                            </div>
                        </div>
                    </div>
                    <Divider className='devider' />
                    <form className='left' onSubmit={handleSubmit}>
                        <Typography mb={2} component="h1" variant="h5" sx={{ fontWeight: 500, color: 'primary.main', textAlign: 'center' }}>
                            Thay đổi mật khẩu
                        </Typography>
                        <div>
                            <TextField id="current-pwd" name='current' type='password' label="Mật khẩu cũ" variant="outlined" fullWidth sx={{ mt: 2 }} />
                            <TextField id="new-pwd" name='new' label="Mật khẩu mới" variant="outlined" fullWidth sx={{ mt: 2 }}
                                 onChange={(e) => handleChangeValuePwd(e, 'pwd1')}
                                type={showPassword.new ? 'text' : 'password'}
                                InputProps={{
                                    endAdornment: (
                                        <InputAdornment position="end" sx={{ cursor: 'pointer' }} onClick={() => {handleShowPassword('new')}}>
                                            {showPassword.new ? (<VisibilityOffIcon className='hv-color' />) : ((<RemoveRedEyeIcon className='hv-color' />))}
                                        </InputAdornment>
                                    ),
                                }}
                            />
                            <TextField id="new-pwd-1" name='new1' label="Nhập lại mật khẩu" variant="outlined" fullWidth sx={{ mt: 2 }}
                                type={showPassword.new1 ? 'text' : 'password'}
                                helperText={checkPwdAgain.helperText}
                                error={checkPwdAgain.error}
                                onChange={(e) => handleChangeValuePwd(e, 'pwd2')}
                                InputProps={{
                                    endAdornment: (
                                        <InputAdornment position="end" sx={{ cursor: 'pointer' }} onClick={() => {handleShowPassword('new1')}}>
                                            {showPassword.new1 ? (<VisibilityOffIcon className='hv-color' />) : ((<RemoveRedEyeIcon className='hv-color' />))}
                                        </InputAdornment>
                                    ),
                                }}
                            />
                        </div>
                        <div className='btn-save'>
                            <LoadingButton
                                type='submit'
                                variant='contained'
                                sx={{ mt: 2 }}
                                loading={pending}
                                loadingPosition="start"
                                startIcon={<SaveIcon />}
                            >
                                Lưu
                            </LoadingButton>
                        </div>
                    </form>
                </Container>
            </ThemeProvider>
            {(openImagePreview) ? (<ImgPreview imgSrc={(info.avatar) ? info.avatar : imageSrc} onClose={handleOpenPreviewClick} />) : ''}
        </NavBar>
    )
}

export default ChangePassword