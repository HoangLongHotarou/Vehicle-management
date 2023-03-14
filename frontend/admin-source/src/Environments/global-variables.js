import PeopleAltIcon from '@mui/icons-material/PeopleAlt';
import ApartmentIcon from '@mui/icons-material/Apartment';
import VideocamIcon from '@mui/icons-material/Videocam';
import AutoGraphIcon from '@mui/icons-material/AutoGraph';
import CottageIcon from '@mui/icons-material/Cottage';

export const global = {
  APILink: {
    Root: 'http://13.112.242.104/api/v1/',
    Auth: 'auth/user',
    InAndOut: 'license-plate-app/in_and_out/',
    Region: 'license-plate-app/regions',
  },
  menuList: [
    {
      icon: <CottageIcon />,
      text: 'Trang chủ',
      active: 'home',
      href: '/',
    },
    {
      icon: <PeopleAltIcon />,
      text: 'Tài khoản',
      active: 'accounts',
      href: '/accounts',
    },
    {
      icon: <ApartmentIcon />,
      text: 'Khu vực',
      active: 'regions',
      href: '/regions',
    },
    {
      icon: <VideocamIcon />,
      text: 'Camera',
      active: 'camera',
      href: '/camera',
    },
    {
      icon: <AutoGraphIcon />,
      text: 'Thống kê',
      active: 'statistical',
      href: '/statistical',
    },
  ],
};
