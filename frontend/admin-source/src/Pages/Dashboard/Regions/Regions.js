import { LinearProgress, Pagination, Typography } from '@mui/material';
import { Box } from '@mui/system';
import { DataGrid } from '@mui/x-data-grid';
import React, { useState } from 'react';
import { useEffect } from 'react';
import NavBar from '../../../Components/NavBarComponent/NavBar';
import RegionServices from '../../../Services/region';

import './Regions.scss';

function getLongitude(params) {
  return `${params.row.coordinate.longitude}`;
}

function getLatitude(params) {
  return `${params.row.coordinate.latitude}`;
}
const region = new RegionServices();
const columns = [
  {
    field: '_id',
    headerName: 'ID',
    width: 100,
    hideable: false,
    description: 'Mã số',
  },
  {
    field: 'region',
    headerName: 'Region',
    width: 300,
    sortable: false,
    hideable: false,
    description: 'Khu vuc',
  },
  {
    field: 'type',
    headerName: 'Type',
    width: 200,
    sortable: false,
    hideable: false,
  },
  {
    field: 'longitude',
    headerName: 'Longitude',
    width: 160,
    sortable: false,
    description: 'longitude',
    valueGetter: getLongitude,
  },
  {
    field: 'latitude',
    headerName: 'Latitude',
    width: 160,
    sortable: false,
    description: 'latitude',
    valueGetter: getLatitude,
  },
];

function Regions() {
  const [loading, setLoading] = useState(false);
  const [pageNumber, setpageNumber] = useState(0);
  const [pageSize, setPageSize] = useState(0);
  const [regions, setRegions] = useState([]);

  useEffect(() => {
    document.title = 'Khu vực';
  }, []);

  const handleChangePage = (event, value) => {
    setpageNumber(value);
  };

  useEffect(() => {
    setLoading(true);
    console.log('Fetch');
    region.getAllRegions(pageNumber).then((res) => {
      console.log(res.status);
      console.log('Fetch');
      let data = res.data;
      setPageSize(data.page_size);
      setRegions(data.list);
      setLoading(false);
    });
  }, [pageNumber]);

  return (
    <div>
      <NavBar title='Khu vực' active='regions'>
        <Typography component='div' variant='h5' mb={2}>
          Danh sách các khu vực
        </Typography>
        <Box sx={{ width: '100%', height: 270 }}>
          <DataGrid
            className='data-grid'
            rows={regions}
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
        <Box
          sx={{
            width: '100%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}>
          <Pagination
            count={pageSize}
            sx={{ my: 2 }}
            variant='outlined'
            onChange={handleChangePage}
          />
        </Box>
      </NavBar>
    </div>
  );
}

export default Regions;
