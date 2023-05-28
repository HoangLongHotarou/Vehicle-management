
import { useEffect } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import App from './App';
import BaseWebSocketAPI from './services/base-websocket.service';
import RegionView from './views/region.view';
import TestView from './views/test.view';
import Setting from './views/setting.view';
import RegionTestView from './views/region.test.view';
import FaceRegister from './views/face-register.view';

export default function WebRouters() {
    useEffect(() => {
        return (() => {
            BaseWebSocketAPI.Instance.openSocket();
        })
    }, [])


    return (
        <BrowserRouter>
            <Routes>
                <Route path='/' element={<App />} />
                <Route path='setting' element={<Setting />} />
                <Route path='region' element={<RegionView />} />
                <Route path='region-test' element={<RegionTestView />} />
                <Route path='test' element={<TestView />} />
                <Route path='face-register' element={<FaceRegister/>}/>
            </Routes>
        </BrowserRouter>
    )
}