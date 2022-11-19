
import { useEffect } from 'react';
import {BrowserRouter,Routes,Route} from 'react-router-dom'
import App from './App';
import BaseWebSocketAPI from './services/base-websocket.service';
import RegionView from './views/region.view';
import TestView from './views/test.view';

export default function WebRouters(){
    useEffect(()=>{
        return(()=>{
            BaseWebSocketAPI.Instance.openSocket();
        })
    },[])


    return (
        <BrowserRouter>
            <Routes>
            <Route path='/' element={<App/>}/>
            <Route path='region' element={<RegionView/>}/>
            <Route path='test' element={<TestView/>}/>
            </Routes>
        </BrowserRouter>
    )
}