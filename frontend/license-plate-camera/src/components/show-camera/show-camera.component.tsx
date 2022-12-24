import { useEffect, useState } from "react";
import { LicensePlate } from "../../interfaces/license-plate";
import './show-camera.css'

interface ShowCameraProps{
    url: string;
    data?: LicensePlate;
    type: string;
}

export default function ShowCamera(props: ShowCameraProps){
    var {url,data,type} = props;

    var [info, setInfo] = useState<LicensePlate>(); 

    useEffect(()=>{
        if(data&&type===data.turn){
            setInfo(data)
        }
    },[data])

    return(
        <>
            <div className='test'>
                <img src={url} width="40%"/>
                <pre className="section section2">{JSON.stringify(info, null, ' ')}</pre>
            </div>
        </>
    );
}