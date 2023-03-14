import React, { useEffect, useState } from 'react';
import { Box, Grid } from '@mui/material';
import { createTheme, ThemeProvider } from '@mui/material';
import GroupIcon from '@mui/icons-material/Group';
import TimeToLeaveIcon from '@mui/icons-material/TimeToLeave';
import VideocamIcon from '@mui/icons-material/Videocam';
import { BarSeries } from '@devexpress/dx-react-chart-material-ui';
import { Stack } from '@devexpress/dx-react-chart';

import './Home.scss';
import NavBar from '../../../Components/NavBarComponent/NavBar';
import AuthService from '../../../Services/auth';
import InAndOutService from '../../../Services/InAndOut';
import CardInfo from '../../../Components/CardInfoComponent/CardInfo';
import { useNavigate } from 'react-router-dom';
import CheckUtils from '../../../Utils/CheckUtils';
import FuncUtils from '../../../Utils/FuncUtils';
import PieChart from '../../../Components/PieChartComponent/PieChart';
import StackedBarChart from '../../../Components/StackedBarChartComponent/StackedBarChart';

const theme = createTheme();
const auth = new AuthService();
const in_and_out = new InAndOutService();
const checkUtils = new CheckUtils();
const funcUtils = new FuncUtils();
const dateNow = funcUtils.getDateNow();

function Home() {
    const navigate = useNavigate();
    const [numberAccount, setNumberAccount] = useState(0);
    const [numberCar, setNumberCar] = useState(0);
    const [openAxis, setOpenAxis] = useState(false);
    const [dataChartCar, setDataChartCar] = useState([]);
    const [dataSevenDays, setDataSevenDays] = useState([]);

    useEffect(() => {
        document.title = "Dashboard";
    }, []);

    useEffect(() => {
        auth.getAllUser().then(res => {
            setNumberAccount(res.data.total)
        }).catch(error => {
            checkUtils.catchError(error);
        });
    }, []);

    useEffect(() => {
        let obj = JSON.stringify({
            "date": {
                "start_date": dateNow,
                "end_date": dateNow
            },
        })
        in_and_out.searchInAndOut(obj).then(res => {
            let data = res.data;
            setNumberCar(data.total_in_and_out);
            setDataChartCar([
                { text: 'Số lượng xe vào', value: data.total_in },
                { text: 'Số lượng xe ra', value: data.total_out }
            ]);
        })
    }, []);

    useEffect(() => {
        in_and_out.statisticInAndOut(dateNow).then(res => {
            console.log(res.data);
            setDataSevenDays(res.data.reverse());
            const timeOut = setTimeout(() => {
                setOpenAxis(true);
            }, 1300)
            return () => { clearTimeout(timeOut) }
        })
    }, [])

    return (
        <NavBar title='Trang chủ' active='home'>
            <ThemeProvider theme={theme}>
                <Box>
                    <Grid container spacing={2}>
                        <Grid item sm={6} md={4} xs={12}>
                            <CardInfo
                                title='Tổng số tài khoản:'
                                icon={<GroupIcon fontSize='large' />}
                                value={numberAccount}
                                navigate={() => { navigate('/accounts') }} />
                        </Grid>
                        <Grid item sm={6} md={4} xs={12}>
                            <CardInfo
                                title='Số lượng xe hôm nay:'
                                icon={<TimeToLeaveIcon fontSize='large' />}
                                value={numberCar} />
                        </Grid>
                        <Grid item sm={12} md={4} xs={12}>
                            <CardInfo
                                title='Tổng số camera:'
                                icon={<VideocamIcon fontSize='large' />}
                                value={0} />
                        </Grid>
                    </Grid>
                </Box>
                <Grid container spacing={2} marginTop={1}>
                    <Grid item sm={12} md={5}>
                        <PieChart
                            data={dataChartCar}
                            title={`Biểu đồ số lượng xe vào/ra ngày                             
                                ${funcUtils.formatDate(dateNow, '-', 'dd-mm-yyyy')}`}
                        />
                    </Grid>
                    <Grid item sm={12} md={7}>
                        <StackedBarChart
                            data={dataSevenDays}
                            title='Tổng số lượng xe ra/vào trong 7 ngày gần đây'
                            openAxis={openAxis}
                        >
                            <BarSeries
                                name="Số lượng xe vào"
                                valueField="total_in"
                                argumentField="date"
                            />
                            <BarSeries
                                name="Số lượng xe ra"
                                valueField="total_out"
                                argumentField="date"
                            />
                            <Stack
                                stacks={[
                                    { series: ['Số lượng xe vào', 'Số lượng xe ra'] },
                                ]}
                            />
                        </StackedBarChart>
                    </Grid>
                </Grid>
            </ThemeProvider>
        </NavBar>
    )
}

export default Home