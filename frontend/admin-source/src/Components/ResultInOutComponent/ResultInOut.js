import { Box, Grid, Divider, ThemeProvider, Button, LinearProgress, Pagination, Typography } from '@mui/material';
import { React, useEffect, useState } from 'react'
import { DataGrid } from '@mui/x-data-grid';

import './ResultInOut.scss'
import PieChart from '../PieChartComponent/PieChart';
import DetailInfo from '../DetailInfoComponent/DetailInfo';
import { useStore, actions } from '../../store';
import FuncUtils from '../../Utils/FuncUtils';
import { LoadingButton } from '@mui/lab';

const funcUtils = new FuncUtils();

function getIDInAndOut(params) {
  return `${params.row.in_and_out_time._id}`;
}

function getDate(params) {
  return `${funcUtils.formatDate(params.row.in_and_out_time.date, '-', 'dd-mm-yyyy')}`;
}

function getPlate(params) {
  return `${params.row.vehicle.plate}`;
}

function getRegion(params) {
  return `${params.row.region.region}`;
}

const RenderDetailsButton = (params) => {
  const [state, dispatch] = useStore();
  const {detailInfo} = state;
  const [pending, setPending] = useState(false);

  useEffect(() => {
    (detailInfo && detailInfo.in_and_out_time._id === params.row.in_and_out_time._id) ? setPending(true) : setPending(false);
  }, [detailInfo, params.row])

  return (
    <LoadingButton
      variant='outlined'
      color="primary"
      size="small"
      onClick={() => {
        console.log(params.row);           
        dispatch(actions.setDetailInfo(params.row));       
      }}
      loading={pending}
    >
      Xem thêm
    </LoadingButton>
  )
}

const columns = [
  {
    field: 'id',
    headerName: 'ID',
    width: 100,
    hideable: false,
    description: 'Mã số',
    valueGetter: getIDInAndOut,
  },
  {
    field: 'date',
    headerName: 'Ngày',
    width: 150,
    sortable: true,
    description: 'Ngày vào ra của xe',
    valueGetter: getDate,
  },
  {
    field: 'plate',
    headerName: 'Biển số',
    width: 150,
    sortable: false,
    hideable: false,
    description: 'Biển số phương tiện',
    valueGetter: getPlate,
  },
  {
    field: 'region',
    headerName: 'Khu vực',
    width: 150,
    sortable: true,
    valueGetter: getRegion,
  },
  {
    field: 'detail',
    headerName: 'Chi tiết',
    width: 150,
    renderCell: RenderDetailsButton,
    disableClickEventBubbling: true,
  },
];

function ResultInOut(props) {

  const [dataChart, setDataChart] = useState([]);

  useEffect(() => {
    if (props.data) {
      setDataChart([
        { text: 'Số lượng xe vào', value: props.data.total_in },
        { text: 'Số lượng xe ra', value: props.data.total_out }
      ])
    }
  }, [props.data]);

  const handleChangePage = (event, value) => {
    props.setPageNumber(value);
  };

  return (
    <ThemeProvider theme={props.theme}>
      <DetailInfo/>
      <Box component={'div'}>
        <Grid container spacing={1} mb={1}>
          <Grid item sm={12} md={12}>
            <h2>Kết quả thống kê số lượng xe vào/ra</h2>
            <Box component={'div'} ml={1} mt={1}>
              {props.stateInOut.date ? (<p>Theo ngày: <span>{props.valueInOut.date.start.format('DD/MM/YYYY')}</span> - <span>{props.valueInOut.date.end.format('DD/MM/YYYY')}</span></p>) : ''}
              {props.stateInOut.time.time_in ? (<p>Giờ vào: <span>{props.valueInOut.time_in.start.format('HH:mm A')}</span> - <span>{props.valueInOut.time_in.end.format('HH:mm A')}</span></p>) : ''}
              {props.stateInOut.time.time_out ? (<p>Giờ ra: <span>{props.valueInOut.time_out.start.format('HH:mm A')}</span> - <span>{props.valueInOut.time_out.end.format('HH:mm A')}</span></p>) : ''}
              {props.stateInOut.region && (<p>Khu vực: <span>{props.valueInOut.region.name}</span></p>)}
              {props.stateInOut.vehicle && props.valueInOut.vehicle.plate!=='' && (<p>Biển số xe: <span>{props.valueInOut.vehicle.plate}</span></p>)}
              {props.stateInOut.vehicle && props.valueInOut.vehicle.type!=='' && (<p>Loại phương tiện: <span>{props.valueInOut.vehicle.type==='car' ? 'Xe hơi' : 'Xe máy'}</span></p>)}
            </Box>
            <Box component={'div'} ml={1} sx={{ display: 'flex', justifyContent: 'end' }}>
              <Button variant="outlined" onClick={props.handleCloseResult}>
                Thống kê lại
              </Button>
            </Box>
          </Grid>
          {/* <Grid item sm={12} md={7}>
            <DetailInfo />
          </Grid> */}
        </Grid>
        <Divider />
        <Grid container spacing={2} mt={1}>
          <Grid item sm={12} md={4}>
            <PieChart
              data={dataChart}
              title='Biểu đồ số lượng xe vào/ra'
            />
            {dataChart.length !== 0 ? (<p className='center bold-600'>Tổng số lượng xe vào/ra là: {props.data.total_in_and_out}</p>) : ''}
          </Grid>
          <Grid item sm={12} md={8}>
            <Typography component='div' variant='h5' mb={2}>
              Danh sách chi tiết các phương tiện
            </Typography>
            <Box sx={{ width: '100%', height: 450 }}>

              <DataGrid
                className='data-grid'
                rows={props.data.list}
                columns={columns}
                getRowId={(row) => row.in_and_out_time._id}
                // checkboxSelection
                disableSelectionOnClick
                components={{
                  LoadingOverlay: LinearProgress,
                }}
                loading={props.loadingDataGrid}
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
                count={props.data.pages_size}
                sx={{ my: 2 }}
                variant='outlined'
                onChange={handleChangePage}
              />
            </Box>
          </Grid>
        </Grid>
      </Box>
    </ThemeProvider>
  )
}

export default ResultInOut