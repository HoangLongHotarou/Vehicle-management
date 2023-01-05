import { Alert, Slide, Snackbar } from '@mui/material'
import React from 'react'

import './AlertCustome.scss'

function AlertCustome(props) { 

    const handleClose = (event, reason) => {
        if (reason === 'clickaway') {
            return;
        }
        props.onOpen((prevState => ({...prevState, state: false})));
    };
    

    return (    
        <Snackbar 
            anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
            open={props.open} 
            autoHideDuration={props.duration || 2000}
            TransitionComponent={Slide}
            onClose={handleClose}               
        >
            <Alert variant="filled" severity={props.severity}>
                {props.text}
            </Alert>
        </Snackbar>            
    )
}

export default AlertCustome