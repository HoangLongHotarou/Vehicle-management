import { Box, Divider, IconButton } from '@mui/material'
import { React, useState, useEffect } from 'react'
import Avatar from '@mui/material/Avatar';
import TwoWheelerIcon from '@mui/icons-material/TwoWheeler';
import DirectionsCarIcon from '@mui/icons-material/DirectionsCar';
import CloseIcon from '@mui/icons-material/Close';
import Dialog from '@mui/material/Dialog';

import './DetailInfo.scss'
import { useStore, actions } from '../../store';
import AuthService from '../../Services/auth';

const auth = new AuthService();

function DetailInfo() {

    const [state, dispatch] = useStore();
    const { detailInfo } = state;

    const [open, setOpen] = useState(false);
    const [userInfo, setUserInfo] = useState({});

    useEffect(() => {
        if (detailInfo && detailInfo.vehicle.user_id) {
            auth.getUser(detailInfo.vehicle.user_id).then(res => {
                setUserInfo(res.data);
                setOpen(true);
            })
        }
        else if (detailInfo) {
            setUserInfo({username: 'Guest', last_name: 'Người', first_name: 'Lạ'})            
            setOpen(true);
        }
    }, [detailInfo])

    const handleClose = () => {
        setOpen(false);
        setTimeout(() => {
            dispatch(actions.setDetailInfo(null));
        }, 100);
    }

    const getTimeArr = (arr) => {
        let arrKQ = [];
        // let kq = {time_in: '', time_out: ''};
        let temp;
        let obj = {};
        arr.forEach((item, index) => {
            if (item.type === 'in' && temp !== 'in') {
                let timeInValue = item.time;
                obj = { time_in: timeInValue }
                temp = item.type;

                if (arr.length === 1 || arr.length - 1 === index) {
                    arrKQ.push(obj);
                }
            }
            else if (item.type === 'out' && temp !== 'out') {
                let timeOutValue = item.time;
                obj = { ...obj, time_out: timeOutValue }
                arrKQ.push(obj);
                obj = {};
                temp = item.type;
            }
            else {
                arrKQ.push(obj);
                obj = {};
                temp = null;
            }
        });
        return arrKQ;
    }

    return (
        <Dialog open={open} onClose={handleClose} fullWidth={true} maxWidth={'xs'}>
            <Box component={'div'} className='wrapper'>
                <IconButton className='button' onClick={handleClose}><CloseIcon /></IconButton>
                <h2>Thông tin chi tiết phương tiện</h2>
                <Box component={'div'} mb={1} mt={2} sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '30px' }}>
                    <Box component={'div'} sx={{ display: 'flex', justifyContent: 'start', alignItems: 'center', gap: '10px' }}>
                        <Avatar
                            alt={userInfo.username}
                            src={userInfo.avatar || '/'}
                            sx={{ width: 50, height: 50 }}
                        />
                        <Box component={'div'}>
                            <div className='full-name'>{(userInfo.last_name && userInfo.first_name && (`${userInfo.last_name} ${userInfo.first_name}`)) || userInfo.username}</div>
                            <div className='icon'>
                                {
                                    detailInfo && detailInfo.vehicle.type === 'motorcycle' ?
                                        (<TwoWheelerIcon />) : (<DirectionsCarIcon />)
                                }
                            </div>
                        </Box>
                    </Box>
                    <Box component={'div'} className='plate'>
                        {detailInfo && detailInfo.vehicle.plate}
                    </Box>
                </Box>
                <Divider />
                <Box className='sub-box' component={'div'} mt={1} p={1}>
                    {detailInfo && getTimeArr(detailInfo.in_and_out_time.times).map((item, index) => (
                        <Box key={index} component={'div'} sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '10px' }}>
                            {item.time_in && (<p>Vào lúc: <span>{item.time_in}</span></p>)} 
                            {item.time_out && (<p>Ra lúc: <span>{item.time_out}</span></p>)}
                        </Box>
                    ))}
                </Box>
            </Box>
        </Dialog>
    )
}

export default DetailInfo