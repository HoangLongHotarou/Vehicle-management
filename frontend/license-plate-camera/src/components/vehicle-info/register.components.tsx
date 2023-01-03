import { Card, CardContent, Typography } from "@mui/material";
import { ShowRegisterInfo } from "../../interfaces/show-information-camera";

interface RegisterInfoProps{
    data: ShowRegisterInfo
}

export default function RegisterInfo(props: RegisterInfoProps){
    var {data} = props;

    return(
        <>
            <Card sx={{ minWidth: 275 }}>
                <CardContent>
                    <Typography sx={{ mb: 1.5, color: "#7d9bca"}}  gutterBottom>
                    Username: {data.username}
                    </Typography>
                    <Typography sx={{ mb: 1.5, color: "#7d9bca" }} >                    
                    Plate: {data.plate}
                    </Typography>
                    <Typography sx={{ mb: 1.5, color: "#7d9bca" }} >                    
                    Roles:
                    {data.role.map((role,i)=>(
                        <>
                                <Typography sx={{ mb: 1.5, color: "#7d9bca" }} >
                                - {role}                             
                                </Typography>
                        </> 
                    ))}
                    </Typography>
                    <Typography sx={{ mb: 1.5, color: "#7d9bca" }} >                    
                    Message: {data.information.message}
                    </Typography>
                    <Typography sx={{ mb: 1.5, color: "#7d9bca" }} >                    
                    Date: {data.information.date}
                    </Typography>
                    <Typography sx={{ mb: 1.5, color: "#7d9bca" }} >                    
                    Time: {data.information.time}
                    </Typography>
                </CardContent>
            </Card>
        </>
    );
}