export interface Camera{
    name: string;
    rtsp_url: string;
    face_rtsp_url: string;
    type: string;
}

export interface Region{
    _id: string;
    region: string;
    type: string;
    cameras: Camera[]
}