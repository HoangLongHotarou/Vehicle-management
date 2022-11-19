import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';
import WebRouters from './routers';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <WebRouters />
  </React.StrictMode>
);
