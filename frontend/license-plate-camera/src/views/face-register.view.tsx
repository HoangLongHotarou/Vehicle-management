import { useEffect, useRef, useState } from "react";
import { useReactMediaRecorder } from "react-media-recorder";
import { FetchFaceRegister } from "../services/face-register/face-register.service";
import { TextField, Box, Typography, Button } from '@mui/material';
import RadioButtonCheckedIcon from '@mui/icons-material/RadioButtonChecked';
import RadioButtonUncheckedIcon from '@mui/icons-material/RadioButtonUnchecked';
import LoadingButton from '@mui/lab/LoadingButton';
import SendIcon from '@mui/icons-material/Send';
import '../css/face-register.css'

const VideoPreview = ({ stream }: { stream: MediaStream | null }) => {    
    const videoRef = useRef<HTMLVideoElement>(null);

    useEffect(() => {
        if (videoRef.current && stream) {
            videoRef.current.srcObject = stream;
        }
    }, [stream]);
    if (!stream) {
        return null;
    }
    return <video className="video-preview" ref={videoRef} autoPlay controls />;
};

const FaceRegister = () => {
    const fetchFace = new FetchFaceRegister();
    const [username, setUsername] = useState('');
    const [loading, setLoading] = useState(false);

    const statusText = {
        idle: 'indle',
        recording: 'recording',
        stop: 'stopped'
    }

    const { status, startRecording, stopRecording, mediaBlobUrl, previewStream } =
        useReactMediaRecorder({ video: true, audio: false });

    const handleSubmit = async () => {
        setLoading(true);
        const formData = new FormData();
        if (mediaBlobUrl === undefined || username === null || username === '') return
        const mediaBlob = await fetch(mediaBlobUrl).then(response => response.blob());
        const myFile = new File(
            [mediaBlob],
            "demo.mp4",
            { 
                type: 'video'
            }
        );

        formData.append("file", myFile);
        // console.log(myFile)
        fetchFace.postFaceVideo(formData, username).then((res) => {
            console.log(res);
            setLoading(false);
        })
    }

    const handleInputChange = (e: any) => {
        setUsername(e.target.value);
    }

    const convertStatus = (status: string) => {
        switch (status) {
            case statusText.recording:
                return 'Đang ghi hình';
            case statusText.stop:
                return 'Đã ghi hình thành công!';
            default:
                return 'Vui lòng nhấn nút ghi hình để tạo video nhận dạng khuôn mặt.';
        }
    }

    return (
        <div>
            <Box
                sx={{ pl: 3, pr: 3 }}
            >
                <Typography variant="h3" component="h3" sx={{ textAlign: 'center', mb: 5 }}><h3>Đăng ký khuôn mặt cho tài khoản</h3></Typography>
                <Box sx={{ display: 'flex', gap: 2 }}>
                    <Box sx={{ flex: 1 }}>
                        <TextField id="input-username" label="Nhập vào tên tài khoản chủ phương tiện" variant="outlined" value={username} fullWidth onInput={handleInputChange} />
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 2, mb: 2 }}>
                            <Box>
                                <Button 
                                    variant="contained" 
                                    endIcon={<RadioButtonCheckedIcon />} 
                                    onClick={startRecording} 
                                    color="success"
                                    disabled={(status === statusText.recording)}
                                    sx={{ mr: 1 }}
                                >
                                    Ghi hình
                                </Button>

                                <Button 
                                    variant="contained" 
                                    endIcon={<RadioButtonUncheckedIcon />} 
                                    color="error"
                                    disabled={!(status === statusText.recording)}
                                    onClick={stopRecording}
                                >
                                    Dừng
                                </Button>
                            </Box>
                                
                            <Box>
                                <LoadingButton
                                    loading={loading}
                                    loadingPosition="start"
                                    variant="contained"
                                    startIcon={<SendIcon />}
                                    onClick={handleSubmit}
                                >
                                    Xác nhận
                                </LoadingButton>
                            </Box>
                        </Box>
                        <p><b>Trạng thái: </b>{convertStatus(status)}</p>
                    </Box>
                    <Box sx={{ display: 'flex', gap: 2, flexDirection: 'column', flex: 1 }}>
                        <Box sx={{ border: '1px dashed black', height: '500px', position: 'relative' }}>
                            {(status === statusText.recording) && (<VideoPreview stream={previewStream} />)}
                            {(status === statusText.stop) && (<video className='video-preview' src={mediaBlobUrl} controls autoPlay loop />)}                            
                        </Box>                                                
                    </Box>
                </Box>
            </Box>
        </div>
    );
};

export default FaceRegister;