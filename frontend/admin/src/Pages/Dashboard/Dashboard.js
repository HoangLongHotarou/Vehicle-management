import React, { useEffect } from 'react'

import './Dashboard.scss'

import { Outlet } from 'react-router-dom';

function Dashboard() {

  useEffect(() => {
    document.title = 'Dashboard';
  }, []);

  return (
    <Outlet/>                
  )
}

export default Dashboard