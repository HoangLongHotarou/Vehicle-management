import { useEffect, useState } from "react";
import { LicensePlate } from "../../interfaces/license-plate";
import { Card, CardContent, Typography } from "@mui/material";
import { ShowWarningInfo } from "../../interfaces/show-information-camera";

interface WarningInfoProps{
    data: ShowWarningInfo
}

export default function WarningInfo(props: WarningInfoProps){
    var {data} = props;

    return(
        <>
            <Card sx={{ minWidth: 275 }}>
            <CardContent>
                    <Typography sx={{ mb: 1.5, color: "#FF6314"}}  gutterBottom>
                    Username: {data.username}
                    </Typography>
                    <Typography sx={{ mb: 1.5, color: "#FF6314" }} >                    
                    Plate: {data.plate}
                    </Typography>
                    <Typography sx={{ mb: 1.5, color: "#FF6314" }} >                    
                    Roles:
                    {data.role.map((role,i)=>(
                        <>
                                <Typography key={i} sx={{ mb: 1.5, color: "#FF6314" }} >
                                - {role}                             
                                </Typography>
                        </> 
                    ))}
                    </Typography>
                    <Typography sx={{ mb: 1.5, color: "#FF6314" }} >                    
                    Warning: {data.information}
                    </Typography>
                </CardContent>
            </Card>
        </>
    );
}