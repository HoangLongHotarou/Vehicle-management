import { React, useCallback, useEffect, useState } from 'react'
import { createTheme, ThemeProvider } from '@mui/material';
import dayjs from 'dayjs';

import './Statistical.scss';
import NavBar from '../../../Components/NavBarComponent/NavBar';
import palette from '../../../Styles/variables.scss';
import InAndOutService from '../../../Services/InAndOut';
import AlertCustome from '../../../Components/AlertComponent/AlertCustome';
import CheckUtils from '../../../Utils/CheckUtils';
import ResultInOut from '../../../Components/ResultInOutComponent/ResultInOut';
import StatisInputInOut from '../../../Components/StatisInputInOutComponent/StatisInputInOut';

const inAndOut = new InAndOutService();
const checkUtils = new CheckUtils();

const theme = createTheme({
    palette: {
        primary: {
            main: palette.primary,
        },
        secondary: {
            main: palette.secondary,
        },
    }
});

var dateNow = dayjs();

function Statistical() {
    const [pending, setPending] = useState(false);
    const [showResult, setShowResult] = useState(false);
    const [pageNumber, setPageNumber] = useState(0);

    const [valueInOut, setValueInOut] = useState({
        date: {
            start: dateNow,
            end: dateNow
        },
        time_in: {
            start: dateNow,
            end: dateNow
        },
        time_out: {
            start: dateNow,
            end: dateNow
        },
        region: {
            id: '',
            name: '',
        },
        vehicle: {
            plate: '',
            type: '',
        }
    })

    const [stateCategoryInOut, setStateCategoryInOut] = useState({
        date: true,
        time: {
            state: false,
            time_in: false,
            time_out: false
        },
        region: false,
        vehicle: false
    });
    const [showAlert, setShowAlert] = useState({ state: false, severity: 'error', text: '', duration: 2000 });

    const [dataInOut, setDataInOut] = useState();

    useEffect(() => {
        document.title = 'Thống kê';
    }, []);

    const handleStatisticalInOut = () => {
        fetchStatisticalTimeInOut();
    }

    const handleCloseResult = () => {
        setShowResult(!showResult);
        setPageNumber(0);
    }

    const checkConditionInOut = useCallback(() => {
        let message = '';
        let check = true;

        if (stateCategoryInOut.date) {
            if (valueInOut.date.end.diff(valueInOut.date.start) < 0) {
                message += 'Ngày bắt đầu phải trước ngày kết thúc. ';
            }
        }

        if (stateCategoryInOut.time.state && (stateCategoryInOut.time.time_in || stateCategoryInOut.time_out)) {
            if (valueInOut.time_in.end.diff(valueInOut.time_in.start) < 0 || valueInOut.time_out.end.diff(valueInOut.time_out.start) < 0) {
                message += 'Giờ bắt đầu phải trước giờ kết thúc. ';
            }
        }

        if (stateCategoryInOut.region) {
            if (valueInOut.region.id === '') {
                message += 'Bạn chưa chọn khu vực. ';
            }
        }

        if (stateCategoryInOut.vehicle) {
            if (valueInOut.vehicle.type === '' && valueInOut.vehicle.plate === '') {
                message += 'Chưa điền biển số hoặc chưa chọn loại phương tiện. ';
            }
        }

        if (message) {
            setShowAlert({ state: true, severity: 'error', text: message, duration: 3000 });
            check = false;
        }

        return check;
    }, [stateCategoryInOut, valueInOut])

    const createQuery = useCallback(() => {
        let query = {};
        if (checkConditionInOut()) {
            if (stateCategoryInOut.date) {
                query.date = {
                    start_date: valueInOut.date.start.format('YYYY-MM-DD'),
                    end_date: valueInOut.date.end.format('YYYY-MM-DD')
                }
            }
            if (stateCategoryInOut.time.state) {
                if (stateCategoryInOut.time.time_in) {
                    query.time_in = {
                        start_time: valueInOut.time_in.start.format('HH:mm:ss'),
                        end_time: valueInOut.time_in.end.format('HH:mm:ss'),
                    }
                }
                if (stateCategoryInOut.time.time_out) {
                    query.time_out = {
                        start_time: valueInOut.time_out.start.format('HH:mm:ss'),
                        end_time: valueInOut.time_out.end.format('HH:mm:ss'),
                    }
                }
            }
            if (stateCategoryInOut.region) {
                query.region = {
                    id_region: valueInOut.region.id,                 
                }
            }
            if (stateCategoryInOut.vehicle) {
                if (valueInOut.vehicle.plate !== '') {
                    query.vehicle = {
                        plate: valueInOut.vehicle.plate,                 
                    }
                }
                if (valueInOut.vehicle.type !== '') {
                    query.vehicle = {   
                        ...query.vehicle,                     
                        type: valueInOut.vehicle.type,                 
                    }
                }                
            }
        }

        return query;
    }, [checkConditionInOut, stateCategoryInOut, valueInOut])

    const fetchStatisticalTimeInOut = useCallback(() => {
        if (Object.keys(createQuery()).length !== 0) {
            setPending(true);
            let obj = JSON.stringify(createQuery());
            inAndOut.searchInAndOut(obj, pageNumber).then(res => {
                console.log(res.data);
                setPending(false);
                if (res.data.list.length !== 0) {
                    if (pageNumber === 0) {
                        setShowAlert({ ...showAlert, state: true, text: 'Đã thống kê thành công!', severity: 'success' });
                        setShowResult(true);
                    }
                    setDataInOut(res.data);
                    setPending(false);
                }
                else {
                    setShowAlert({ ...showAlert, state: true, text: 'Không có kết quả nào!', severity: 'info' });
                }
            }).catch(err => { checkUtils.catchError(err) })
        }
        else if (checkConditionInOut()) {
            setShowAlert({ state: true, severity: 'error', text: 'Chưa có thông tin để thống kê!', duration: 1200 });
        }
    }, [pageNumber, checkConditionInOut, createQuery, showAlert]);

    useEffect(() => {
        if (pageNumber !== 0)
            fetchStatisticalTimeInOut();
    }, [pageNumber, fetchStatisticalTimeInOut])

    return (
        <NavBar title='Thống kê' active='statistical'>
            <AlertCustome
                open={showAlert.state}
                onOpen={setShowAlert}
                duration={showAlert.duration}
                severity={showAlert.severity}
                text={showAlert.text} />

            <ThemeProvider theme={theme}>            
                <StatisInputInOut
                    stateCategoryInOut={stateCategoryInOut} 
                    setStateCategoryInOut={setStateCategoryInOut}
                    valueInOut={valueInOut}
                    setValueInOut={setValueInOut}
                    showResult={showResult}
                    handleStatisticalInOut={handleStatisticalInOut}
                    pending={pending}
                />

                {showResult && (
                    <ResultInOut
                        data={dataInOut}
                        stateInOut={stateCategoryInOut}
                        valueInOut={valueInOut}
                        theme={theme}
                        handleCloseResult={handleCloseResult}
                        setPageNumber={setPageNumber}
                        loadingDataGrid={pending} />)}
            </ThemeProvider>
        </NavBar>
    )
}

export default Statistical