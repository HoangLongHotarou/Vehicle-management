import { React, useState, useEffect } from 'react';
import { Box, Grid } from '@mui/material';
import { DesktopDatePicker } from '@mui/x-date-pickers/DesktopDatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { TimePicker } from '@mui/x-date-pickers/TimePicker';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import Checkbox from '@mui/material/Checkbox';
import LoadingButton from '@mui/lab/LoadingButton';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormGroup from '@mui/material/FormGroup';
import { TextField } from '@mui/material';

import RegionServices from '../../Services/region';

const regionService = new RegionServices();

function StatisInputInOut(props) {
    const {
        stateCategoryInOut,
        setStateCategoryInOut,
        valueInOut,
        setValueInOut,
        showResult,
        handleStatisticalInOut,
        pending,
    } = props;

    const [listRegions, setListRegions] = useState([]);

    useEffect(() => {
        regionService.getAllRegions().then(res => {
            setListRegions(res.data.list);
        })
    }, [])

    const cleanInfo = (type) => {
        switch (type) {
            case 'region':
                !stateCategoryInOut.region && cleanValueRegion();
                break;
            case 'vehicle':
                !stateCategoryInOut.region && cleanValueVehicle();
                break;
            default:
                break;
        }
    }

    const cleanValueRegion = () => {
        setValueInOut({ ...valueInOut, region: { ...valueInOut.region, id: '', name: '' } });
    };

    const cleanValueVehicle = () => {
        setValueInOut({ ...valueInOut, vehicle: { ...valueInOut.vehicle, plate: '', type: '' } });
    };

    const handleChangeValue = (newValue, type, subType) => {
        setValueInOut({ ...valueInOut, [type]: { ...valueInOut[type], [subType]: newValue } });
    }

    const handleCheckStateCategory = (type, subtype) => {
        if (subtype === 'state' && stateCategoryInOut.time.state) {
            setStateCategoryInOut({ ...stateCategoryInOut, time: { state: !stateCategoryInOut.time.state, time_in: false, time_out: false } });
        }
        else {
            (type === 'time') ?
                setStateCategoryInOut({ ...stateCategoryInOut, [type]: { ...stateCategoryInOut.time, [subtype]: !stateCategoryInOut.time[subtype] } }) :
                setStateCategoryInOut({ ...stateCategoryInOut, [type]: !stateCategoryInOut[type] });
        }
        cleanInfo(type);
    }

    const handleChangeSelectRegion = (event) => {
        let arrStr = event.target.value.split('-');
        setValueInOut({ ...valueInOut, region: { ...valueInOut.region, id: arrStr[0], name: arrStr[1] } });
    };

    const handleChangeSelectVehicleType = (event) => {
        let type = event.target.value;
        setValueInOut({ ...valueInOut, vehicle: { ...valueInOut.vehicle, type: type } });
    };

    const handleInputPlate = (event) => {
        // console.log(event.target.value);
        setValueInOut({ ...valueInOut, vehicle: { ...valueInOut.vehicle, plate: event.target.value } })
    }

    return (
        <LocalizationProvider dateAdapter={AdapterDayjs}>
            <Box component={'div'} className={showResult ? 'hidđen' : ''}>
                <h2>Thống kê số lượng xe vào/ra</h2>
                <FormGroup sx={{ display: 'flex', flexDirection: 'row', alignItems: 'center', gap: '10px', mt: 2 }}>
                    <h4>Chọn loại thống kê: </h4>
                    <FormControlLabel control={<Checkbox checked={stateCategoryInOut.date} onChange={() => { handleCheckStateCategory('date') }} />} label="Ngày" />
                    <FormControlLabel control={<Checkbox onChange={() => { handleCheckStateCategory('time', 'state') }} />} label="Khoảng thời gian" />
                    <FormControlLabel control={<Checkbox onChange={() => { handleCheckStateCategory('region') }} />} label="Khu vực" />
                    <FormControlLabel control={<Checkbox onChange={() => { handleCheckStateCategory('vehicle') }} />} label="Phương tiện" />
                </FormGroup>
                {stateCategoryInOut.date && (
                    <Accordion defaultExpanded sx={{ mt: 2 }}>
                        <AccordionSummary
                            expandIcon={<ExpandMoreIcon />}
                            aria-controls="panel1a-content"
                            id="panel1a-header"
                        >
                            <h4 className='group-name'>Theo ngày</h4>
                        </AccordionSummary>
                        <AccordionDetails>
                            <Grid container spacing={5}>
                                <Grid item sm={12} md={6} sx={{ width: '100%' }}>
                                    <DesktopDatePicker
                                        label="Từ ngày"
                                        inputFormat="DD/MM/YYYY"
                                        value={valueInOut.date.start}
                                        onChange={(newValue) => { handleChangeValue(newValue, 'date', 'start') }}
                                        renderInput={(params) => <TextField {...params} sx={{ width: '100%' }} />}
                                    />
                                </Grid>
                                <Grid item sm={12} md={6} sx={{ width: '100%' }}>
                                    <DesktopDatePicker
                                        label="Đến ngày"
                                        inputFormat="DD/MM/YYYY"
                                        value={valueInOut.date.end}
                                        onChange={(newValue) => { handleChangeValue(newValue, 'date', 'end') }}
                                        renderInput={(params) => <TextField {...params} sx={{ width: '100%' }} />}
                                    />
                                </Grid>
                            </Grid>
                        </AccordionDetails>
                    </Accordion>
                )}
                {stateCategoryInOut.time.state && (
                    <Accordion defaultExpanded>
                        <AccordionSummary
                            expandIcon={<ExpandMoreIcon />}
                            aria-controls="panel2a-content"
                            id="panel2a-header"
                        >
                            <h4 className='group-name'>Theo khoảng thời gian</h4>
                        </AccordionSummary>
                        <AccordionDetails>
                            <Box component='div' sx={{ mt: 0, pl: 2 }}>
                                <h4 className='sub-group-name'><Checkbox onChange={() => { handleCheckStateCategory('time', 'time_in') }} /> Thời gian vào</h4>
                                <Grid container spacing={2} sx={{ mt: '1px' }}>
                                    <Grid item sm={12} md={6} sx={{ width: '100%' }}>
                                        <TimePicker
                                            label="Bắt đầu"
                                            value={valueInOut.time_in.start}
                                            onChange={(newValue) => { handleChangeValue(newValue, 'time_in', 'start') }}
                                            renderInput={(params) => <TextField {...params}
                                                sx={{ width: '100%' }} />}
                                        />
                                    </Grid>
                                    <Grid item sm={12} md={6} sx={{ width: '100%' }}>
                                        <TimePicker
                                            label="Kết thúc"
                                            value={valueInOut.time_in.end}
                                            onChange={(newValue) => { handleChangeValue(newValue, 'time_in', 'end') }}
                                            renderInput={(params) => <TextField {...params}
                                                sx={{ width: '100%' }} />}
                                        />
                                    </Grid>
                                </Grid>
                            </Box>
                            <Box component='div' sx={{ mt: 2, pl: 2 }}>
                                <h4 className='sub-group-name'><Checkbox onChange={() => { handleCheckStateCategory('time', 'time_out') }} /> Thời gian ra</h4>
                                <Grid container spacing={2} sx={{ mt: '1px' }}>
                                    <Grid item sm={12} md={6} sx={{ width: '100%' }}>
                                        <TimePicker
                                            label="Bắt đầu"
                                            value={valueInOut.time_out.start}
                                            onChange={(newValue) => { handleChangeValue(newValue, 'time_out', 'start') }}
                                            renderInput={(params) => <TextField {...params}
                                                sx={{ width: '100%' }} />}
                                        />
                                    </Grid>
                                    <Grid item sm={12} md={6} sx={{ width: '100%' }}>
                                        <TimePicker
                                            label="Kết thúc"
                                            value={valueInOut.time_out.end}
                                            onChange={(newValue) => { handleChangeValue(newValue, 'time_out', 'end') }}
                                            renderInput={(params) => <TextField {...params}
                                                sx={{ width: '100%' }} />}
                                        />
                                    </Grid>
                                </Grid>
                            </Box>
                        </AccordionDetails>
                    </Accordion>
                )}
                {stateCategoryInOut.region && (
                    <Accordion defaultExpanded>
                        <AccordionSummary
                            expandIcon={<ExpandMoreIcon />}
                            aria-controls="panel3a-content"
                            id="panel3a-header"
                        >
                            <h4 className='group-name'>Theo khu vực</h4>
                        </AccordionSummary>
                        <AccordionDetails>
                            <FormControl fullWidth>
                                <InputLabel id="select-region">Chọn khu vực</InputLabel>
                                <Select
                                    labelId="select-region"
                                    id="select-region-id"
                                    value={valueInOut.region.id !== '' ? `${valueInOut.region.id}-${valueInOut.region.name}` : ''}
                                    label="Chọn khu vực"
                                    onChange={handleChangeSelectRegion}
                                >
                                    {listRegions.map((item, index) => (
                                        <MenuItem key={index} value={`${item._id}-${item.region}`}>{item.region}</MenuItem>
                                    ))}
                                </Select>
                            </FormControl>
                        </AccordionDetails>
                    </Accordion>
                )}
                {stateCategoryInOut.vehicle && (
                    <Accordion defaultExpanded>
                        <AccordionSummary
                            expandIcon={<ExpandMoreIcon />}
                            aria-controls="panel3a-content"
                            id="panel3a-header"
                        >
                            <h4 className='group-name'>Theo phương tiện</h4>
                        </AccordionSummary>
                        <AccordionDetails>
                            <Grid container spacing={2}>
                                <Grid item sm={12} md={6} sx={{ width: '100%' }}>
                                    <TextField fullWidth onInput={handleInputPlate} id="plate-txt" label="Biển số xe" variant="outlined" />
                                </Grid>
                                {/* <Grid item sm={12} md={4} sx={{ width: '100%' }}>
                                    <TextField fullWidth id="outlined-basic" label="ID người dùng" variant="outlined" />
                                </Grid> */}
                                <Grid item sm={12} md={6} sx={{ width: '100%' }}>
                                    <FormControl fullWidth>
                                        <InputLabel id="select-vehicle-type">Chọn loại phương tiện</InputLabel>
                                        <Select
                                            labelId="select-vehicle-type"
                                            id="vehicle-type"
                                            value={valueInOut.vehicle.type}
                                            label="Chọn loại phương tiện"
                                            onChange={handleChangeSelectVehicleType}
                                        >
                                            <MenuItem value={'motorcycle'}>Xe máy</MenuItem>
                                            <MenuItem value={'car'}>Xe hơi</MenuItem>
                                        </Select>
                                    </FormControl>
                                </Grid>
                            </Grid>
                        </AccordionDetails>
                    </Accordion>
                )}
                <Box component={'div'} sx={{ mt: 2, display: 'flex', justifyContent: 'end' }}>
                    <LoadingButton
                        loading={pending}
                        variant="contained"
                        onClick={handleStatisticalInOut}
                    >
                        Thống kê
                    </LoadingButton>
                </Box>
            </Box>
        </LocalizationProvider>
    )
}

export default StatisInputInOut