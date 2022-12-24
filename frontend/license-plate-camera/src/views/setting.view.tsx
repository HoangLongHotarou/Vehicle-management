import { useEffect, useState } from "react";
import { FetchRegion } from "../services/license-plate-app/region.service";
import { Region, Camera } from "../interfaces/region.interface";
import { Button, FormControl, InputLabel, MenuItem, Select, TextField } from "@mui/material";


export default function Setting() {
    const fetchRegion = new FetchRegion();

    var [regions, setRegions] = useState<Region[]>([]);
    var [cameras, setCameras] = useState<Camera[]>([]);
    var [region, setRegion] = useState<Region>();
    var [value, setValue] = useState<string>('');
    var [info, setInfo] = useState<string>('');

    useEffect(() => {
        fetchRegion.get_all().then((res) => {
            console.log(res);
            setRegions(res);
        })
    }, [info])

    const handleChange = (event: any) => {
        setValue(event.target.value)
        var object = JSON.parse(event.target.value);
        setRegion(object)

        if(object){
            setCameras(object.cameras)
        }
    }

    const handleSubmit = async(event: any) => {
        // console.log(event);
        const names = Array.from(document.getElementsByName('name'))
        const rtsp_links = Array.from(document.getElementsByName('rtsp_link'))
        const types = Array.from(document.getElementsByName('type'))
        var camera_list = []

        for(var i=0;i<names.length;i++){
            var object = {
                name: (names[i] as HTMLInputElement).value,
                rtsp_url: (rtsp_links[i] as HTMLInputElement).value,
                type: (types[i] as HTMLInputElement).value
            }
            camera_list.push(object)
        }

        if(region){
            let announce = await fetchRegion.update(region._id,{cameras:camera_list})
            // console.log(info)
            if(announce){
                alert((info as any).detail)
            }
            setInfo(announce)
        }
    } 

    return (
        <>
            <h3>Setting</h3>
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
                        <MenuItem key={i} value={JSON.stringify(value)}>
                            {value['region']}
                        </MenuItem>
                    ))}
                </Select>
            </FormControl>

            <pre className="section">{JSON.stringify(region, null, ' ')}</pre>
            {/* <pre className="section">{JSON.stringify(cameras, null, ' ')}</pre> */}
            
            {cameras.map((value,i)=>(
                <div className='list_div' key={i}>
                    <br/>
                    <TextField name="name" disabled label="Name" defaultValue={value.name}/>
                    <TextField name="rtsp_link" label="RTSP" defaultValue={value.rtsp_url} variant="filled"/>
                    <TextField name="type" disabled label="type" defaultValue={value.type}/>
                    <br/>
                </div>
            ))}
            {/* <br/> 
            <Button variant="outlined" color="success">Add</Button> */}
            <br/>
            <Button variant="contained" onClick={handleSubmit}>Update</Button>
        </>
    );
}