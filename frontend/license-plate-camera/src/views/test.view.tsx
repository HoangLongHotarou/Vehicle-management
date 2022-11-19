import { MenuItem, Select } from "@mui/material";
import { useEffect } from "react";
import BaseWebSocketAPI from "../services/base-websocket.service";
// import { w3cwebsocket as W3CWebSocket } from "websocket"

// const client = new W3CWebSocket()

export default function TestView() {
    // var clone_socket: WebSocket;

    // const websocket = () => {
    //     // const socket = new WebSocket("ws://54.238.251.141/api/v1/license-plate-app/in_and_out/test_ws");
    //     const socket = new WebSocket("ws://localhost:443/api/v1/license-plate-app/in_and_out/test_ws");
    //     clone_socket = socket;
    //     socket.addEventListener('open', function (event) {
    //         console.log(event)
    //     });
    //     socket.addEventListener('message', function (event) {
    //         console.log(event.data);
    //     });
    // }

    useEffect(() => {
        BaseWebSocketAPI.Instance.receiveData()
    }, [])

    const handleChange = (event: any)=>{
        console.log(event.target.value);
        BaseWebSocketAPI.Instance.sendData({
            status: event.target.value
        })
    }

    return (
        <>
            <Select
            labelId="demo-simple-select-label"
            id="demo-simple-select"
            // value={value}
            label="Test"
            onChange={handleChange}
            >
                <MenuItem value="1">
                    test 1
                </MenuItem>
                <MenuItem value="2">
                    test 2
                </MenuItem>
                <MenuItem value="3">
                    test 3
                </MenuItem>
            </Select>
        </>
    );
}