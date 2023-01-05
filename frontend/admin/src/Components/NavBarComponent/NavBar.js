import React, { useEffect } from 'react';
import { createTheme, Divider, ThemeProvider } from '@mui/material';
import MuiAppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import MenuItem from '@mui/material/MenuItem';
import Menu from '@mui/material/Menu';
import AccountCircle from '@mui/icons-material/AccountCircle';
import { styled } from '@mui/material/styles';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import { useNavigate } from 'react-router-dom';
import Avatar from '@mui/material/Avatar';
import PersonIcon from '@mui/icons-material/Person';
import LogoutIcon from '@mui/icons-material/Logout';
import VpnKeyIcon from '@mui/icons-material/VpnKey';

import './NavBar.scss';
import { global } from '../../Environments/global-variables';
import palette from '../../Styles/variables.scss';
import AuthService from '../../Services/auth';
import Footer from '../FooterComponent/Footer';

var width = document.body.clientWidth;

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

const auth = new AuthService();
const drawerWidth = 240;
const maxWidth = 700;

const Main = styled('main', { shouldForwardProp: (prop) => prop !== 'open' })(
    ({ theme, open }) => ({
        flexGrow: 1,
        padding: theme.spacing(3),
        transition: theme.transitions.create(['margin', 'width'], {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.leavingScreen,
        }),
        marginLeft: 0,
        position: 'absolute',
        width: '100%',
        minHeight: '100vh',
        ...(open && (width > maxWidth) && {
            transition: theme.transitions.create(['margin', 'width'], {
                easing: theme.transitions.easing.easeOut,
                duration: theme.transitions.duration.enteringScreen,
            }),
            marginLeft: `${drawerWidth}px`,
            width: `calc(100% - ${drawerWidth}px)`,
        }),
    }),
);

const AppBar = styled(MuiAppBar, {
    shouldForwardProp: (prop) => prop !== 'open',
})(({ theme, open }) => ({
    transition: theme.transitions.create(['margin', 'width'], {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.leavingScreen,
    }),
    ...(open && (width > maxWidth) && {
        width: `calc(100% - ${drawerWidth}px)`,
        marginLeft: `${drawerWidth}px`,
        transition: theme.transitions.create(['margin', 'width'], {
            easing: theme.transitions.easing.easeOut,
            duration: theme.transitions.duration.enteringScreen,
        }),
    }),
}));

const DrawerHeader = styled('div')(({ theme }) => ({
    display: 'flex',
    alignItems: 'center',
    padding: theme.spacing(0, 1),
    ...theme.mixins.toolbar,
    justifyContent: 'flex-end',
}));

const DrawerSX = {
    width: drawerWidth,
    flexShrink: 0,
    '& .MuiDrawer-paper': {
        width: drawerWidth,
        boxSizing: 'border-box',
    },
}

const listMenu = (props, navigate) => (
    <>
        <DrawerHeader />
        <List>
            {global.menuList.map((menuItem, index) => (
                <ListItem key={index}
                    disablePadding
                    className={(props.active === menuItem.active) ? 'item-list active' : 'item-list'}>
                    <ListItemButton onClick={() => { navigate(menuItem.href, { replace: true }) }}>
                        <ListItemIcon className='icon-item'>
                            {menuItem.icon}
                        </ListItemIcon>
                        <ListItemText primary={menuItem.text} />
                    </ListItemButton>
                </ListItem>
            ))}
        </List>
    </>
)

function NavBar(props) {
    const navigate = useNavigate();
    const infoUser = props.info || auth.getInfo();
    const [anchorEl, setAnchorEl] = React.useState(null);
    const [open, setOpen] = React.useState((width > maxWidth) ? true : false);

    // console.log(props.info);

    useEffect(() => {
        function updateWidth() {
            width = document.body.clientWidth;
        }
        window.addEventListener('resize', updateWidth);
        return () => window.removeEventListener('resize', updateWidth);
    }, [])

    const handleMenu = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };

    const toggleDrawerOpen = () => {
        setOpen(!open);
    };

    return (
        <Box sx={{ flexGrow: 1 }}>
            <ThemeProvider theme={theme}>
                <AppBar position="fixed" open={open}>
                    <Toolbar>
                        <IconButton
                            size="large"
                            edge="start"
                            color="inherit"
                            aria-label="menu"
                            sx={{ mr: 2 }}
                            onClick={toggleDrawerOpen}
                        >
                            <MenuIcon />
                        </IconButton>
                        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                            {props.title}
                        </Typography>
                        {auth.checkLogin() && (
                            <div>
                                <Box sx={{ alignItems: 'center', size: 'xs' }}>
                                    <span className='welcome'><i>Xin chào,</i> {infoUser.username || 'Khách'}</span>
                                    <IconButton
                                        size="large"
                                        aria-label="account of current user"
                                        aria-controls="menu-appbar"
                                        aria-haspopup="true"
                                        onClick={handleMenu}
                                        color="inherit"
                                    >
                                        {(infoUser.avatar) ? <Avatar alt="avt" src={infoUser.avatar} sx={{ width: 32, height: 32 }} /> : <AccountCircle />}
                                    </IconButton>
                                </Box>
                                <Menu
                                    sx={{ mt: '45px' }}
                                    id="menu-appbar"
                                    anchorEl={anchorEl}
                                    anchorOrigin={{
                                        vertical: 'top',
                                        horizontal: 'right',
                                    }}
                                    keepMounted
                                    transformOrigin={{
                                        vertical: 'top',
                                        horizontal: 'right',
                                    }}
                                    open={Boolean(anchorEl)}
                                    onClose={handleClose}
                                >
                                    <MenuItem className='menu-item' onClick={() => { navigate('/Info') }}>
                                        <span className='icon-option'><PersonIcon fontSize={'small'}/></span><span>Thông tin cá nhân</span>
                                    </MenuItem>
                                    <MenuItem className='menu-item' onClick={() => { navigate('/Change_Pwd') }}>
                                        <span className='icon-option'><VpnKeyIcon fontSize={'small'}/></span><span>Đổi mật khẩu</span>
                                    </MenuItem>
                                    <Divider/>
                                    <MenuItem className='menu-item' onClick={() => { auth.logout() }}>
                                        <span className='icon-option'><LogoutIcon fontSize={'small'}/></span><span>Đăng xuất</span>
                                    </MenuItem>
                                </Menu>
                            </div>
                        )}
                    </Toolbar>
                </AppBar>
                {width > maxWidth ? (
                    <Drawer
                        sx={DrawerSX}
                        variant="persistent"
                        anchor="left"
                        open={open}
                    >
                        {listMenu(props, navigate)}
                    </Drawer>
                ) : (
                    <Drawer
                        sx={DrawerSX}
                        anchor='left'
                        open={open}
                        onClose={toggleDrawerOpen}
                    >
                        {listMenu(props, navigate)}
                    </Drawer>
                )}
            </ThemeProvider>
            <Main open={open}>
                <DrawerHeader />
                {props.children}
                <Footer sx={{ mt: 3 }} />
            </Main>
        </Box>
    )
}

export default NavBar