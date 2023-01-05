import React from 'react';
import ReactLoading from 'react-loading';

import './Loading.scss';

function Loading(props) {
  return (
    <div className='loadingContainer'>
        <ReactLoading className='loading-icon' type='spinningBubbles' height={'64px'} width={'64px'}/>
        <div className='text'>{props.text}</div> 
    </div>
  )
}

export default Loading