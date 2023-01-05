import { Button, createTheme, Divider, TextField, ThemeProvider, Typography } from '@mui/material'
import { Container } from '@mui/system';
import React, { useState } from 'react'
import CameraAltIcon from '@mui/icons-material/CameraAlt';
import RemoveRedEyeIcon from '@mui/icons-material/RemoveRedEye';
import ReactLoading from 'react-loading';
import LoadingButton from '@mui/lab/LoadingButton';
import SaveIcon from '@mui/icons-material/Save';
import Resizer from "react-image-file-resizer";

import './Info.scss'
import NavBar from '../../Components/NavBarComponent/NavBar'
import imageSrc from '../../Assets/Images/avt-default.jpg'
import palette from '../../Styles/variables.scss';
import AuthService from '../../Services/auth';
import ImgPreview from '../../Components/ImgPreviewComponent/ImgPreview';
import CheckUtils from '../../Utils/CheckUtils';
import AlertCustome from '../../Components/AlertComponent/AlertCustome';

const auth = new AuthService();
const checkUtils = new CheckUtils();

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

function Info() {
    const [info, setInfo] = useState(auth.getInfo());
    const [openImagePreview, setOpenImagePreview] = useState(false);    
    const [checkPhoneNumber, setCheckPhoneNumber] = useState({error: false, helperText: ''});   
    const [pendingAvatar, setPendingAvatar] = useState(false); 
    const [pendingInfo, setPendingInfo] = useState(false); 
    const [openAlert, setOpenAlert] = useState({ state: false, severity: 'error', text: '' });

    const uploadImage = (imageFile) => {
        let obj = new FormData();
        obj.append('file', imageFile);     
        setPendingAvatar(true);   
        auth.updateAvatar(obj).then(res => {
            let data = res.data;
            auth.updateAvatarLocalStorage(data.avatar);
            setInfo(auth.getInfo());  
            setPendingAvatar(false);          
        }).catch(err => {
            checkUtils.catchError(err);
            setOpenAlert({state: true, severity: 'error', text: 'Kích thước ảnh quá lớn!'})            
            setPendingAvatar(false);
            // console.log(error.response.status);
        });
    }

    const handleOpenPreviewClick = () => {
        setOpenImagePreview(!openImagePreview);
    }

    const handleChangeAvatar = e => {                             
        Resizer.imageFileResizer(  
            e.target.files[0],   
            500,
            500,
            e.target.files[0].type.split('/')[1],
            100,
            0,
            (uri) => {                   
                uploadImage(uri);
            },
            "file",
            400,
            400
        );        
    }

    const handleSubmit = (event) => {
        event.preventDefault();        
        if (!checkPhoneNumber.error) {   
            setPendingInfo(true);         
            const data = new FormData(event.currentTarget);

            let obj = JSON.stringify({
                phone_number: data.get('phonenumber'),
                first_name: data.get('firstname'),
                last_name: data.get('lastname')
            })
        
            auth.updateInfo(obj).then(res => {                 
                let infoUpdate = JSON.parse(res.config.data);
                auth.updateInfoLocalStorage(infoUpdate);  
                setInfo(auth.getInfo()); 
                setPendingInfo(false);  
                setOpenAlert({state: true, severity: 'success', text: 'Cập nhật thông tin thành công!'})                   
            }).catch(err => {
                checkUtils.catchError(err);               
            });
        }         
    }

    const handleChangePhoneNumber = (e) => {
        if (isVietnamesePhoneNumberValid(e.target.value)) {
            setCheckPhoneNumber({error: false, helperText: ''});
        }
        else if (e.target.value === '') {            
            setCheckPhoneNumber({error: false, helperText: ''});
        }
        else {
            setCheckPhoneNumber({error: true, helperText: 'SĐT không hợp lệ!'});
        }
    }

    const isVietnamesePhoneNumberValid = (number) => {
        return /(((\+|)84)|0)(3|5|7|8|9)+([0-9]{8})\b/.test(number);
    }

    return (
        <NavBar title='Thông tin tài khoản' active='accounts' info={info}>
            <AlertCustome
                open={openAlert.state}
                onOpen={setOpenAlert}
                duration={3000}
                severity={openAlert.severity}
                text={openAlert.text} />   

            <ThemeProvider theme={theme}>
                <Container className='container' maxWidth='xl'>
                    <div className='right'>
                        <Typography mb={2} component="h1" variant="h5" sx={{fontWeight: 500, color: 'primary.main', textAlign:'center'}}>
                            Ảnh đại diện
                        </Typography>
                        <div className={pendingAvatar ? 'img-bx' : 'img-bx not-pending'}>
                            <img src={(info.avatar) ? info.avatar : imageSrc} alt='avatar'/>  
                            <div className='btn-view-image' onClick={handleOpenPreviewClick}>
                                <RemoveRedEyeIcon/>
                                <span>Xem ảnh</span>
                            </div>   
                            {pendingAvatar ? 
                            (<div className='loading-img'>
                                <ReactLoading className='loading-icon' type='spinningBubbles' height={'30px'} width={'30px'}/>
                                <div className='text'>Đang tải ảnh...</div> 
                            </div>) : ''
                            }                     
                        </div>
                        <div style={{textAlign: 'center', marginTop: '20px'}}>
                            <Button disabled={pendingAvatar} component="label" variant="outlined" startIcon={<CameraAltIcon/>}>
                                Cập nhật ảnh
                                <input
                                    id="avatar"
                                    name="avatar"
                                    type="file"
                                    hidden
                                    accept="image/png, image/gif, image/jpeg"
                                    onChange={handleChangeAvatar}
                                />
                            </Button>    
                        </div>         
                    </div>
                    <Divider className='devider'/>
                    <form className='left' onSubmit={handleSubmit}>
                        <Typography mb={2} component="h1" variant="h5" sx={{fontWeight: 500, color: 'primary.main', textAlign:'center'}}>
                            Thông tin
                        </Typography>
                        <div>
                            <TextField id="email" name='email' label="Email" variant="outlined" fullWidth required type='email' 
                                defaultValue={info.email}
                                inputProps={
                                    { readOnly: true, }
                                }/>
                            <TextField id="username" name='username' label="Tên đăng nhập" variant="outlined" fullWidth required sx={{ mt: 2 }} defaultValue={info.username}
                             inputProps={
                                { readOnly: true, }
                            }/>
                            <TextField id="lastname" name='lastname' label="Họ và tên lót" variant="outlined" fullWidth sx={{ mt: 2 }} defaultValue={info.last_name || ''}/>
                            <TextField id="firstname" name='firstname' label="Tên" variant="outlined" fullWidth sx={{ mt: 2 }} defaultValue={info.first_name || ''}/>
                            <TextField id="phonenumber" name='phonenumber' label="SĐT" variant="outlined" fullWidth type='tel' sx={{ mt: 2 }}
                                defaultValue={info.phone_number || ''}
                                inputProps={{ maxLength: 10 }}
                                onChange={handleChangePhoneNumber}
                                error={checkPhoneNumber.error}
                                helperText={checkPhoneNumber.helperText}
                            />                       
                        </div>
                        <div className='btn-save'>
                            <LoadingButton 
                                type='submit' 
                                variant='contained' 
                                sx={{mt: 2}}
                                loading={pendingInfo}
                                loadingPosition="start"
                                startIcon={<SaveIcon />}
                                >
                                Lưu
                            </LoadingButton>
                        </div>                
                    </form>               
                </Container>                
            </ThemeProvider>    
            {(openImagePreview) ? (<ImgPreview imgSrc={(info.avatar) ? info.avatar : imageSrc} onClose={handleOpenPreviewClick}/>) : ''}                
        </NavBar>                                   
    )
}

export default Info