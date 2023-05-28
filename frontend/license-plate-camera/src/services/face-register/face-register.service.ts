import { Pagination } from "../../interfaces/pagination.interface";
import { Region } from "../../interfaces/region.interface";
import { FetchAPI } from "./fetch-api.service";

export class FetchFaceRegister {
    fetchAPI: FetchAPI;
    pagination!: Pagination;
    region$!: Region[];

    constructor() {
        this.fetchAPI = new FetchAPI();
    }

    async postFaceVideo(obj: FormData, username: string) {
        var info = ''
        await this.fetchAPI.postFormData(`/face-recognition/train?username=${username}`, obj).then(res => {
            info = res.data;
        }).catch((err) => {
            console.log(err.message)
        })
        return info
    }
}