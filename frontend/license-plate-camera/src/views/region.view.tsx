/* eslint-disable react-hooks/exhaustive-deps */
import { useEffect, useState } from 'react';
import { FetchRegion } from '../services/license-plate-app/region.service';
import { Region } from '../interfaces/region.interface'
import { FormControl, InputLabel, MenuItem, Select } from '@mui/material';
// import { FetchInAndOut } from '../services/license-plate-app/in-and-out.service';
import { FetchInAndOut } from '../services/check-vehicle-realtime/in-and-out.service';

import { RTSPCamera } from '../interfaces/rtsp-camera.interface';
import ShowCamera from '../components/show-camera/show-camera.component';
import { LicensePlate } from '../interfaces/license-plate';
import BaseWebSocketAPI from '../services/base-websocket.service';
import Board from '../components/board/board.component';


export default function RegionView() {
  const fetchRegion = new FetchRegion();
  const fetchInAndOut = new FetchInAndOut();

  var [regions, setRegions] = useState<Region[]>([]);
  var [cameras, setCameras] = useState<RTSPCamera[]>([]);
  var [value, setValue] = useState<string>('');
  var [plate, setplate] = useState<LicensePlate>();

  useEffect(()=>{
    BaseWebSocketAPI.Instance.receiveDataUseState(setplate);
    // BaseWebSocketAPI.Instance.receiveData();
  },[])

  useEffect(() => {
    fetchRegion.get_all().then((res) => {
      console.log(res);
      setRegions(res);
    })
  },[])

  const handleChange = (event: any) => {
    // window.location.reload();
    BaseWebSocketAPI.Instance.sendData({
      status: event.target.value
    })
    setValue(event.target.value)
    fetchInAndOut.get_rtsp(event.target.value).then((res) => {
      setCameras(res);
    })
  }

  return (
    <>
      <FormControl fullWidth>
        <InputLabel id="demo-simple-select-label">Region</InputLabel>
        <Select
          labelId="demo-simple-select-label"
          id="demo-simple-select"
          value={value}
          label="Region"
          onChange={handleChange}
        >
          {regions.map((value, i) => (
            <MenuItem key={i} value={value['_id']}>
              {value['region']}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      {/* <pre className="section">{JSON.stringify(cameras, null, ' ')}</pre> */}
      {!cameras?(<>not camera</>):(cameras.map((camera,i)=>(
        <div key={i}>
          <Board name={camera.name} type={camera.type}/>
          <ShowCamera face_url='' url={camera['rtsp_url']} data={plate} type={camera['type']} />
        </div>
      )))}
    </>
  );
}

