import { useEffect, useState } from "react";
// import { LicensePlate } from "../../interfaces/license-plate";
import './show-camera.css'
import { ShowUserInfo } from "../../interfaces/show-information-camera";
import RegisterInfo from "../vehicle-info/register.components";
import NotRegisterInfo from "../vehicle-info/not-register.component";
import { Box } from "@mui/material";
import { parse } from "path";
import WarningInfo from "../vehicle-info/warning.component";

interface ShowCameraProps {
    url: string;
    face_url: string;
    data?: ShowUserInfo;
    type: string;
}

export default function ShowCamera(props: ShowCameraProps) {
    let { url, face_url, data, type } = props;

    let [info, setInfo] = useState<ShowUserInfo>();
    let [faceUrl, setFaceUrl] = useState<string>();
    let [vehicleUrl, setVehicleUrl] = useState<string>();

    useEffect(() => {
        // if (data && type === data.turn) {
        //     setInfo(data)
        // }
        setInfo(data);
        console.log(info);
    })

    const changeTurn = (url: string, turn: string): string=>{
        const parseUrl = new URL(url);
        const searchParams = parseUrl.searchParams;
        searchParams.set("turn",turn);
        const updateQueryString = searchParams.toString();
        const updateUrl = `${parseUrl.origin}${parseUrl.pathname}?${updateQueryString}`
        return updateUrl;
    }

    useEffect(()=>{
        setFaceUrl(changeTurn(face_url, type));
        setVehicleUrl(changeTurn(url,type));
    })

    return (
        <>
            <div className='test'>
                <Box className="camera-wrapper"
                    sx={{
                        mb: 2,                        
                        display: "flex",
                        gap: 3,
                    }}
                >
                    <div className="camera-container">
                        <h4>Camera nhận diện biển số xe</h4>
                        <div className='camera-bx'>
                            <img src={vehicleUrl} />
                        </div>
                    </div>
                    <div className="camera-container">
                        <h4>Camera nhận diện khuôn mặt</h4>
                        <div className='camera-bx'>
                            <img src={faceUrl} />
                        </div>
                    </div>
                </Box>
                {/* <pre className="section section2">{JSON.stringify(info, null, ' ')}</pre> */}
                <Box className="section"
                    sx={{
                        mb: 2,
                        display: "flex",
                        flexDirection: "column",
                        // height: 500,
                        // overflow: "hidden",
                        // overflowY: "scroll",
                        // justifyContent="flex-end" # DO NOT USE THIS WITH 'scroll'
                    }}
                >
                    {/* <p>Lorem</p> */}
                    {info && info.register.map((register, i) => (
                        <>
                            <RegisterInfo data={register} />
                        </>
                    ))}
                    {info && info.not_registered.map((not_register, i) => (
                        <>
                            <NotRegisterInfo data={not_register} />
                        </>
                    ))}
                    {
                        info && info.warning.map((warning,i)=>(
                            <>
                                <WarningInfo data={warning}/>
                            </>
                        ))
                    }
                </Box>
            </div>
        </>
    );
}