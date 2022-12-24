import { Pagination } from "../../interfaces/pagination.interface";
import { Region } from "../../interfaces/region.interface";
import { FetchAPI } from "./fetch-api.service";

export class FetchRegion{
    fetchAPI: FetchAPI;
    pagination!: Pagination;
    region$!: Region[];

    constructor(){
        this.fetchAPI = new FetchAPI();
    }

    async get_all(){
        await this.fetchAPI.get(`/regions`).then((res)=>{
            this.pagination = res.data;
            this.region$ = this.pagination.list;
        }).catch((err)=>{
            console.log(err.message);
        })
        return this.region$;
    }

    async update(id: string, obj: object){
        var info = ''
        await this.fetchAPI.put(`/regions/${id}`,obj).then(res=>{
            info = res.data;
        }).catch((err)=>{
            console.log(err.message)
        })
        return info
    }
}