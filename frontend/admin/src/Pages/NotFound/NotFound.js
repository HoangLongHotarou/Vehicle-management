import React from 'react'
import { Button } from '@mui/material'
import {createTheme, ThemeProvider} from '@mui/material'
import { useNavigate } from 'react-router-dom'

import './NotFound.scss'
import palette from '../../Styles/variables.scss';

const theme = createTheme({
  palette: {
    primary: {
      main: palette.primary,
    },
    secondary: {
      main: palette.secondary,
    },
  }
})

function NotFound() {
  const navigate = useNavigate();

  return (
    <ThemeProvider theme={theme}>
      <div className='error-container'>
        <div className='error-code'>
          <span>4</span>
          <span>0</span>
          <span>4</span>
        </div>
        <p>Trang không tồn tại</p>
        <Button onClick={() => {navigate('/')}} variant='contained' sx={{mt: 3}}>Trang chủ</Button>
      </div>
    </ThemeProvider>
    
  )
}

export default NotFound