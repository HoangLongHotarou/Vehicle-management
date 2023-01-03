import { useEffect, useState } from "react";
import { LicensePlate } from "../../interfaces/license-plate";
import { Card, CardContent, Typography } from "@mui/material";

interface BoardProps{
    name: string;
    type: string;
}

export default function Board(props: BoardProps){
    var {name,type} = props;


    return(
        <>
            <Card sx={{ minWidth: 275 }}>
                <CardContent>
                    <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
                    Camera
                    </Typography>
                    <Typography sx={{ fontSize: 14 }} component="div">
                    Name: {name}
                    </Typography>
                    <Typography sx={{ mb: 1.5 }} color="text.secondary">
                    Type: {type}
                    </Typography>
                </CardContent>
            </Card>
        </>
    );
}