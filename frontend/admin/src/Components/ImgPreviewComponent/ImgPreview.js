import React from 'react'
import CloseIcon from '@mui/icons-material/Close';

import './ImgPreview.scss';
import imgDefault from '../../Assets/Images/avt-default.jpg'

function ImgPreview(props) {
    return (
        <div className='img-preview'>
            <div className='btn-close' onClick={props.onClose}>
                <CloseIcon sx={{ fontSize: 30 }}/>
            </div>
            <div className='img-bx mobile'>
                <img src={props.imgSrc || imgDefault} alt='img-preview'/>
            </div>
            <img className='desktop' src={props.imgSrc || imgDefault} alt='img-preview'/>
        </div>
    )
}

export default ImgPreview