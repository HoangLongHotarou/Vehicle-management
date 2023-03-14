import React, { useEffect, useState } from 'react';
import NavBar from '../../../Components/NavBarComponent/NavBar';
import { DataGrid } from '@mui/x-data-grid';
import { Box } from '@mui/system';
import LinearProgress from '@mui/material/LinearProgress';
import Pagination from '@mui/material/Pagination';

import './Accounts.scss';

import Auth from '../../../Services/auth';
import { Typography } from '@mui/material';

const auth = new Auth();

const columns = [
  {field: '_id', headerName: 'ID', width: 100, hideable: false, description: 'Mã số'},
  {
    field: 'username', 
    headerName: 'Username', 
    width: 150, 
    sortable: false, 
    hideable: false,
    description: 'Tên tài khoản',
  },
  {field: 'email', headerName: 'Email', width: 200, sortable: false, hideable: false},
  {field: 'phone_number', headerName: 'SĐT', width: 160, sortable: false, description: 'Số điện thoại'},
  {field: 'last_name', headerName: 'Họ và tên lót', width: 270, sortable: false},
  {field: 'first_name', headerName: 'Tên', width: 100, sortable: false},
]

function Accounts() {
  const [loading, setLoading] = useState(false);
  const [pageNumber, setpageNumber] = useState(0);
  const [pageSize, setPageSize] = useState(0);
  const [listAccount, setListAccount] = useState([]);

  useEffect(() => {
    document.title = "Tài khoản";
  }, []);

  useEffect(() => {
    setLoading(true);
    auth.getAllUser(pageNumber).then(res => {
      let data = res.data;
      console.log(data);
      console.log(data.list);
      setPageSize(data.pages_size);
      setListAccount(data.list);
      setLoading(false);
    })
  }, [pageNumber]);

  const handleChangePage = (event, value) => {
    setpageNumber(value);
  };

  return (
    <div>
      <NavBar title='Tài khoản' active='accounts'>
        <Typography component='div' variant='h5' mb={2}>Danh sách các tài khoản</Typography>
        <Box sx={{width: '100%', height:450}}> 
          <DataGrid 
            className='data-grid'
            rows={listAccount}
            columns={columns}           
            getRowId={(row) => row._id}
            // checkboxSelection
            disableSelectionOnClick
            components={{
              LoadingOverlay: LinearProgress,
            }}
            loading={loading}     
            hideFooterPagination                    
          />
        </Box>
        <Box sx={{width: '100%', display:'flex', alignItems:'center', justifyContent:'center'}}> 
          <Pagination count={pageSize} sx={{my: 2}} variant="outlined" onChange={handleChangePage}/>
        </Box>
      </NavBar>
    </div>
  )
}

export default Accounts