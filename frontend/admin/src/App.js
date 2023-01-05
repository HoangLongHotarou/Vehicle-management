import './Styles/main.scss'
import { Routes, Route, Navigate } from 'react-router-dom'

import AuthService from './Services/auth';

import Login from './Pages/LoginPage/Login';
import Dashboard from './Pages/Dashboard/Dashboard';
import NotFound from './Pages/NotFound/NotFound';
import Accounts from './Pages/Dashboard/Accounts/Accounts';
import Home from './Pages/Dashboard/Home/Home';
import Info from './Pages/Info/Info';
import Regions from './Pages/Dashboard/Regions/Regions';
import Statistical from './Pages/Dashboard/Statistical/Statistical';
import ChangePassword from './Pages/ChangePassword/ChangePassword';

const auth = new AuthService();

function App() {
  let isAuth = auth.checkLogin();

  return (
    <Routes>
      <Route path='*' element={<NotFound />}></Route>
      <Route path='/' element={isAuth ? <Dashboard /> : <Navigate to='/Login' />}>
        <Route index element={<Home />} />
        <Route path='accounts' element={<Accounts />} />
        <Route path='regions' element={<Regions />} />
        <Route path='statistical' element={<Statistical />} />
      </Route>
      <Route path='/Info' element={isAuth ? <Info /> : <Navigate to='/Login' />}></Route>
      <Route path='/Change_Pwd' element={isAuth ? <ChangePassword /> : <Navigate to='/Login' />}></Route>
      {/* <Route path='/' element={<Dashboard/>}></Route> */}
      <Route path='/Login' element={isAuth ? <Navigate to='/' /> : <Login />}></Route>
    </Routes>
  );
}

export default App;
