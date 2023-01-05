import React from 'react'
import { Typography } from '@mui/material'
import Link from '@mui/material/Link';

function Footer(props) {
  return (
    <Typography variant="body2" color="text.secondary" align="center" {...props}>
    {'Copyright © '}
    <Link color="inherit" href="#/">
      MRL
    </Link>{' '}
    {new Date().getFullYear()}
    {'. Ứng Dụng Nhận Diện Biển Số Xe.'}
  </Typography>
  )
}

export default Footer