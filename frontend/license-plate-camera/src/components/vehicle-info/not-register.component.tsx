import { useEffect, useState } from "react";
import { LicensePlate } from "../../interfaces/license-plate";
import { Card, CardContent, Typography } from "@mui/material";
import { ShowNotRegisterInfo } from "../../interfaces/show-information-camera";

interface NotRegisterInfoProps{
    data: ShowNotRegisterInfo
}

export default function NotRegisterInfo(props: NotRegisterInfoProps){
    var {data} = props;

    return(
        <>
            <Card sx={{ minWidth: 275 }}>
                <CardContent>
                    <Typography sx={{ mb: 1.5, color: "#8b2d2d" }}>                    
                    Biển số: {data.plate}
                    </Typography>
                    <Typography sx={{ mb: 1.5, color: "#8b2d2d" }}>                    
                    Thông tin: {data.information}
                    </Typography>
                </CardContent>
            </Card>
        </>
    );
}