import { Card, CardContent, Typography } from "@mui/material";
import { ShowRegisterInfo } from "../../interfaces/show-information-camera";

interface RegisterInfoProps{
    data: ShowRegisterInfo
}

export default function RegisterInfo(props: RegisterInfoProps){
    var {data} = props;

    return(
        <>
            <Card sx={{ minWidth: 275, display: "flex", justifyContent: "space-between" }}>
                <CardContent sx={{ textAlign: "left"}}>
                    <Typography sx={{ mb: 1.5, color: "#7d9bca"}}  gutterBottom>
                    Username: {data.username}
                    </Typography>
                    <Typography sx={{ mb: 1.5, color: "#7d9bca"}}  gutterBottom>
                    Họ và tên: {data.fullname}
                    </Typography>
                    <Typography sx={{ mb: 1.5, color: "#7d9bca" }} >                    
                    Biển số: {data.plate}
                    </Typography>
                    <Typography sx={{ mb: 1.5, color: "#7d9bca" }} >                    
                    Vai trò:
                    {data.role.map((role,i)=>(
                        <>
                                <Typography key={i} sx={{ mb: 1.5, color: "#7d9bca" }} >
                                - {role}                             
                                </Typography>
                        </> 
                    ))}
                    </Typography>
                    <Typography sx={{ mb: 1.5, color: "#7d9bca" }} >                    
                    Thông tin: {data.information.message}
                    </Typography>
                    <Typography sx={{ mb: 1.5, color: "#7d9bca" }} >                    
                    Ngày: {data.information.date}
                    </Typography>
                    <Typography sx={{ mb: 1.5, color: "#7d9bca" }} >                    
                    Thời gian: {data.information.time}
                    </Typography>
                </CardContent>
                <CardContent sx={{ display: "flex", justifyContent: "center" }}>
                    <Typography sx={{ display: "flex", justifyContent: "center", alignItems: "center", border: "1px solid blue", color: "#7d9bca"  }} >                    
                    <h1>{data.information.message}</h1> 
                    </Typography>
                </CardContent>
            </Card>
        </>
    );
}