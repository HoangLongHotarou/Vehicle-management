import React from 'react'
import {Typography, Button, Card, CardActions, CardContent } from '@mui/material'
import CountUp from 'react-countup';

import './CardInfo.scss';

function CardInfo(props) {
  return (
    <Card className='card' sx={props.sx}>
        <CardContent>
            <Typography gutterBottom variant="h5" component="div" sx={{fontWeight: 500}}>
                {props.title}
            </Typography>
            <Typography variant="h4" component="div" sx={{fontWeight: 800, display: 'flex', alignItems: 'center', gap: 1}}>
                {props.icon}
                <CountUp end={props.value}/>
            </Typography>
        </CardContent>
        <CardActions sx={{textAlign: 'right', width: '100%', display: 'block'}}>
            <Button size="small" onClick={props.navigate}>Chi tiết</Button>            
        </CardActions>
    </Card>
  )
}

export default CardInfo