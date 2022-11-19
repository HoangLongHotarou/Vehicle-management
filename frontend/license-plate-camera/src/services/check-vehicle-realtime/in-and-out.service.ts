import { RTSPCamera } from '../../interfaces/rtsp-camera.interface';
import { FetchAPI } from "./fetch-api.service";

export class FetchInAndOut{
    rtspCamera$!:RTSPCamera[];
    fetchAPI: FetchAPI;

    constructor(){
        this.fetchAPI = new FetchAPI();
    }

    async get_rtsp(id_region: string){
        await this.fetchAPI.get(`/get_rtsp_from_region/${id_region}`).then((res)=>{
            this.rtspCamera$ = res.data;
        }).catch((err)=>{
            console.log(err)
        })
        return this.rtspCamera$
    }
}