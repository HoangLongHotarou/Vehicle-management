import { useEffect, useState } from "react";
// import { LicensePlate } from "../../interfaces/license-plate";
import './show-camera.css'
import { ShowUserInfo } from "../../interfaces/show-information-camera";
import RegisterInfo from "../vehicle-info/register.components";
import NotRegisterInfo from "../vehicle-info/not-register.component";
import { Box } from "@mui/material";

interface ShowCameraProps{
    url: string;
    data?: ShowUserInfo;
    type: string;
}

export default function ShowCamera(props: ShowCameraProps){
    var {url,data,type} = props;

    var [info, setInfo] = useState<ShowUserInfo>(); 

    useEffect(()=>{
        if(data&&type===data.turn){
            setInfo(data)
        }
    },[data])

    return(
        <>
            <div className='test'>
                <img src={url} width="40%"/>
                {/* <pre className="section section2">{JSON.stringify(info, null, ' ')}</pre> */}
                <Box className="section"
                sx={{
                    mb: 2,
                    display: "flex",
                    flexDirection: "column",
                    height: 500,
                    overflow: "hidden",
                    overflowY: "scroll",
                    // justifyContent="flex-end" # DO NOT USE THIS WITH 'scroll'
                    }}
                >
                    {info&&info.register.map((register,i)=>(
                    <>
                    <RegisterInfo data={register}/>
                    </>
                ))}
                {info&&info.not_registered.map((not_register,i)=>(
                    <>
                    <NotRegisterInfo data={not_register}/>
                    </>
                ))}
                </Box>
            </div>
        </>
    );
}